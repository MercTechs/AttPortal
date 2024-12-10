import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import DetachedInstanceError
from sqlalchemy.orm import Session
from src.app.models.entities.orm import AttendanceRecord, DeviceType, AttendanceDevice
from src.app.models.entities.schemas import (
    AttendanceSyncResponse,
    AttendanceRecordResponse,
    AttendanceListResponse,
    DeviceResponse,
    EmployeeResponse,
    AttendanceDeviceInDB,
    DeviceTypeUpdate,
    
)
from src.app.models.entities.orm import AttendanceDevice, DeviceSyncStatus
from src.app.services.attendance_service import AttendanceService
from src.app.dependencies.dependencies import get_postgres_manager, get_attendance_service
import httpx
from typing import List


router = APIRouter()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.get("/attendance/sync", response_model=AttendanceSyncResponse)
async def sync_attendance_data(
    from_date: datetime = Query(default_factory=lambda: datetime.now() - timedelta(days=7)),
    to_date: datetime = Query(default_factory=lambda: datetime.now()),
    employee_id: Optional[str] = None,
    session: Session = Depends(get_postgres_manager),
    attendance_service: AttendanceService = Depends(get_attendance_service)
):
    """
    Sync attendance data from external API and store in database
    """
    try:
        # Validate date range
        if from_date > to_date:
            raise ValueError("From date must be before or equal to to date")

        # Fetch data from external API
        api_records = await attendance_service.fetch_attendance_data(
            from_date=from_date,
            to_date=to_date,
            employee_id=employee_id
        )
        
        if not api_records:
            return AttendanceSyncResponse(
                status="success",
                message="No new records to sync",
                records_count=0
            )

        # Parse API response into AttendanceRecord objects
        try:
            orm_records = attendance_service.parse_attendance_records(
                api_records=api_records,
                session=session
            )
        except Exception as e:
            logger.error(f"Error parsing attendance records: {e}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while parsing attendance records"
            )
        
        # Track new records count
        new_records_count = 0
        
        # Store in database using bulk operations
        existing_records = {
            (record.employee_id, record.check_time, record.machine_serial)
            for record in session.query(AttendanceRecord).filter(
                AttendanceRecord.check_time.between(from_date, to_date)
            )
        }
        
        records_to_add = []
        for record in orm_records:
            record_key = (record.employee_id, record.check_time, record.machine_serial)
            if record_key not in existing_records:
                records_to_add.append(record)
                new_records_count += 1

        if records_to_add:
            session.bulk_save_objects(records_to_add)
            session.commit()
        
        return AttendanceSyncResponse(
            status="success",
            message=f"Successfully synced {new_records_count} new records",
            records_count=new_records_count
        )
        
    except ValueError as e:
        session.rollback()
        logger.error(f"Validation Error in sync_attendance_data: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except httpx.HTTPError as e:
        session.rollback()
        logger.error(f"HTTP Error in sync_attendance_data: {e}")
        raise HTTPException(
            status_code=502,
            detail=f"Error communicating with attendance API: {str(e)}"
        )
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database Error in sync_attendance_data: {e}")
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while syncing attendance records"
        )
    except Exception as e:
        session.rollback()
        logger.error(f"Unexpected error in sync_attendance_data: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while syncing attendance records"
        )
    finally:
        session.close()

@router.get("/attendance", response_model=AttendanceListResponse)
async def get_attendance_records(
    from_date: datetime = Query(default_factory=lambda: datetime.now() - timedelta(days=7)),
    to_date: datetime = Query(default_factory=lambda: datetime.now()),
    employee_id: Optional[str] = None,
    session: Session = Depends(get_postgres_manager),
):
    """
    Get attendance records from local database with pagination and filtering
    """
    try:
        if from_date > to_date:
            raise ValueError("From date must be before or equal to to date")

        query = session.query(AttendanceRecord)
        
        if employee_id:
            query = query.filter(AttendanceRecord.employee_id == employee_id)
        
        query = query.filter(
            AttendanceRecord.check_time >= from_date,
            AttendanceRecord.check_time <= to_date
        ).order_by(AttendanceRecord.check_time.desc())
        
        total = query.count()
        orm_records = query.all()
        
        if not orm_records:
            return AttendanceListResponse(
                records=[],
                total=0
            )

        pydantic_records = [
            AttendanceRecordResponse(
                uuid=str(record.uuid),
                employee_id=str(record.employee_id),
                employee_name=str(record.employee_name),
                machine_alias=str(record.machine_alias),
                machine_serial=str(record.machine_serial),
                att_date=record.att_date,  #type: ignore
                check_time=record.check_time, #type: ignore
                created_at=record.created_at, #type: ignore
                attendance_status=str(record.attendance_status),
                sync_status=str(record.sync_status)
            ) for record in orm_records
        ]
        
        return AttendanceListResponse(
            records=pydantic_records,
            total=total
        )

    except ValueError as e:
        logger.error(f"Validation Error in get_attendance_records: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        logger.error(f"Database Error in get_attendance_records: {e}")
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while fetching attendance records"
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_attendance_records: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while fetching attendance records"
        )
    finally:
        session.close()


@router.get("/devices", response_model=List[DeviceResponse])
async def get_devices(
    session: Session = Depends(get_postgres_manager),
    attendance_service: AttendanceService = Depends(get_attendance_service)
):
    """
    Get list of all attendance devices from the external API and sync with database
    """
    try:
        # Fetch from API
        api_devices = await attendance_service.fetch_device_list()
        
        # Get existing devices from database
        existing_devices = {
            device.serial_number: device 
            for device in session.query(AttendanceDevice).all()
        }
        
        # Process each device from API
        for api_device in api_devices:
            serial_number = api_device["SerialNumber"]
            
            if serial_number in existing_devices:
                # Update existing device
                device = existing_devices[serial_number]
                device.update_from_api(api_device)
            else:
                # Create new device
                device = AttendanceDevice.from_api_response(api_device)
                session.add(device)
        
        # Mark devices not in API as inactive
        api_serial_numbers = {d["SerialNumber"] for d in api_devices}
        for device in existing_devices.values():
            if device.serial_number not in api_serial_numbers:
                device.update(is_active=False, sync_status=DeviceSyncStatus.INACTIVE)
        
        # Commit changes
        session.commit()
        
        # Return API response
        return [DeviceResponse(**device) for device in api_devices]
        
    except httpx.HTTPError as e:
        session.rollback()
        logger.error(f"HTTP Error in get_devices: {e}")
        raise HTTPException(
            status_code=502,
            detail=f"Error communicating with attendance API: {str(e)}"
        )
    except Exception as e:
        session.rollback()
        logger.error(f"Unexpected error in get_devices: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while fetching devices"
        )
    finally:
        session.close()

@router.get("/devices/{serial_number}/employees", response_model=List[EmployeeResponse])
async def get_device_employees(
    serial_number: str,
    attendance_service: AttendanceService = Depends(get_attendance_service)
):
    """
    Get list of employees associated with a specific device
    """
    try:
        employees = await attendance_service.fetch_employees_by_device(serial_number)
        return [EmployeeResponse(**employee) for employee in employees]
        
    except httpx.HTTPError as e:
        logger.error(f"HTTP Error in get_device_employees: {e}")
        raise HTTPException(
            status_code=502,
            detail=f"Error communicating with attendance API: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_device_employees: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while fetching employees for device {serial_number}"
        )
    
@router.patch("/devices/{serial_number}/type", response_model=AttendanceDeviceInDB)
async def update_device_type(
    serial_number: str,
    device_type: DeviceTypeUpdate,
    session: Session = Depends(get_postgres_manager)
):
    try:
        # Find the device
        device = session.query(AttendanceDevice).filter(
            AttendanceDevice.serial_number == serial_number
        ).first()
        
        if not device:
            raise HTTPException(
                status_code=404,
                detail=f"Device with serial number {serial_number} not found"
            )
        
        # Update device type
        device.device_type = device_type.device_type #type: ignore
        device.last_sync = datetime.now()
        
        session.commit()
        session.refresh(device)
        
        return device
        
    except DetachedInstanceError:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while updating device type"
        )
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating device type: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while updating device type"
        )

@router.post("/devices/{serial_number}/update-attendance-status")
async def update_attendance_status_for_device(
    serial_number: str,
    session: Session = Depends(get_postgres_manager)
):
    """
    Update attendance status for all records of a device based on its device type
    """
    try:
        # Find the device
        device = session.query(AttendanceDevice).filter(
            AttendanceDevice.serial_number == serial_number
        ).first()
        
        if device is None:
            raise HTTPException(
                status_code=404,
                detail=f"Device with serial number {serial_number} not found"
            )
            
        attendance_status = "Check In" if device.device_type.value == DeviceType.CHECK_IN.value else "Check Out"
        
        updated = session.query(AttendanceRecord).filter(
            AttendanceRecord.machine_serial == serial_number
        ).update(
            {"attendance_status": attendance_status},
            synchronize_session=False
        )
        
        session.commit()
        
        return {
            "message": f"Successfully updated {updated} records for device {serial_number}",
            "updated_records": updated
        }
        
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error in update_attendance_status_for_device: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while updating attendance status"
        )