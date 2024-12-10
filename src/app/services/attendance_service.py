import httpx
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from src.app.models.entities.orm import (
    AttendanceRecord,
    AttendanceDevice,
    DeviceSyncStatus,
)
from src.app.core.config import settings


class AttendanceService:
    def __init__(self):
        self.base_url = settings.EXTERNAL_API_URL
        self.credentials = {
            "user": settings.EXTERNAL_API_USER,
            "pass": settings.EXTERNAL_API_PASSWORD,
        }

    async def _make_api_request(
        self, name: str, params: List[str] = []
    ) -> List[Dict[str, Any]]:
        """
        Make a generic API request with the given name and parameters

        Returns:
            List of dictionaries containing the API response data
        """
        payload = {**self.credentials, "name": name, "param": params}

        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, json=payload, timeout=30.0)
            response.raise_for_status()

            data = response.json()
            if data["result"] != "success":
                raise ValueError(f"API Error: {data.get('reason', 'Unknown error')}")

            return (
                data["data"][0]
                if isinstance(data["data"], list) and data["data"]
                else []
            )

    async def fetch_attendance_data(
        self, from_date: datetime, to_date: datetime, employee_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch attendance data from the external API
        """
        params = [
            "FromDate",
            from_date.strftime("%Y-%m-%d"),
            "ToDate",
            to_date.strftime("%Y-%m-%d"),
        ]

        if employee_id:
            params.extend(["EmployeeID", employee_id])

        return await self._make_api_request("API_AttendanceList", params)

    async def fetch_device_list(self) -> List[Dict[str, Any]]:
        """
        Fetch list of all devices from the external API
        """
        return await self._make_api_request("API_DeviceList")

    async def fetch_employees_by_device(
        self, serial_number: str
    ) -> List[Dict[str, Any]]:
        """
        Fetch list of employees associated with a specific device

        Args:
            serial_number: The device serial number

        Returns:
            List of employee records associated with the device
        """
        params = ["SerialNumber", serial_number]
        return await self._make_api_request("API_EmployeeListByDevices", params)

    def parse_attendance_records(
        self, api_records: List[Dict[str, Any]], session
    ) -> List[AttendanceRecord]:
        """
        Parse API response into AttendanceRecord objects
        """
        records = []
        for record in api_records:
            # Get the device for this record
            device = session.query(AttendanceDevice).filter_by(
                serial_number=record["sn"]
            ).first()
            if device:
                records.append(AttendanceRecord.from_api_response(record, device))
        return records

    async def sync_devices(self, session) -> tuple[int, int]:
        """
        Sync devices from external API to database

        Returns:
            tuple[int, int]: (new_devices_count, updated_devices_count)
        """
        # Fetch current devices from API
        api_devices = await self.fetch_device_list()

        # Track counts
        new_devices = 0
        updated_devices = 0

        # Get existing devices from database
        existing_devices = {
            device.serial_number: device
            for device in session.query(AttendanceDevice).all()
        }

        for api_device in api_devices:
            serial_number = api_device["SerialNumber"]

            if serial_number in existing_devices:
                device = existing_devices[serial_number]
                device.update_from_api(api_device)
                updated_devices += 1
            else:
                device = AttendanceDevice.from_api_response(api_device)
                session.add(device)
                new_devices += 1

        api_serial_numbers = {d["SerialNumber"] for d in api_devices}
        for device in existing_devices.values():
            if device.serial_number not in api_serial_numbers:
                device.is_active = False
                device.sync_status = DeviceSyncStatus.INACTIVE

        # Commit changes
        session.commit()

        return new_devices, updated_devices
