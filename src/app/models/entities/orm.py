from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DeviceType(str, enum.Enum):
    CHECK_IN = "CheckIn"
    CHECK_OUT = "CheckOut"

class DeviceSyncStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

class AttendanceDevice(Base):
    __tablename__ = "attendance_devices"
    
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(String, unique=True, nullable=False)  # ID from API
    serial_number = Column(String, unique=True, nullable=False)  # SerialNumber from API
    name = Column(String, nullable=True)  # Alias from API
    device_type = Column(Enum(DeviceType), nullable=True)
    
    # Additional fields from API
    ip_address = Column(String, nullable=True)  # IP from API
    mac_address = Column(String, nullable=True)  # MAC from API
    model = Column(String, nullable=True)  # Model from API
    firmware = Column(String, nullable=True)  # Firmware from API
    location = Column(String, nullable=True)  # Location from API
    
    # Tracking fields
    is_active = Column(Boolean, default=True, nullable=False)
    last_sync = Column(DateTime, nullable=False, default=datetime.now)
    sync_status = Column(Enum(DeviceSyncStatus), nullable=False, default=DeviceSyncStatus.ACTIVE)
    
    # Relationship
    attendance_records = relationship("AttendanceRecord", back_populates="device")

    @classmethod
    def from_api_response(cls, api_device):
        """
        Create or update an AttendanceDevice instance from API response data
        """
        return cls(
            device_id=str(api_device["ID"]),
            serial_number=api_device["SerialNumber"],
            name=api_device.get("Alias"),
            ip_address=api_device.get("IP"),
            mac_address=api_device.get("MAC"),
            model=api_device.get("Model"),
            firmware=api_device.get("Firmware"),
            location=api_device.get("Location"),
            last_sync=datetime.now()
        )

    def update_from_api(self, api_device):
        """
        Update existing device instance from API response data
        """
        self.name = api_device.get("Alias")
        self.ip_address = api_device.get("IP")
        self.mac_address = api_device.get("MAC")
        self.model = api_device.get("Model")
        self.firmware = api_device.get("Firmware")
        self.location = api_device.get("Location")
        self.last_sync = datetime.now()
        self.sync_status = DeviceSyncStatus.ACTIVE

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_uuid = Column(UUID(as_uuid=True), ForeignKey('attendance_devices.uuid'))
    
    # Fields from API response
    att_date = Column(DateTime, nullable=False)  
    check_time = Column(DateTime, nullable=False)  
    employee_id = Column(String, nullable=False)  
    employee_name = Column(String, nullable=False)  
    machine_alias = Column(String, nullable=False)  
    machine_serial = Column(String, nullable=False)  
    
    # Additional fields for data tracking
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    sync_status = Column(String, nullable=False, default="synced")  
    
    # Relationship
    device = relationship("AttendanceDevice", back_populates="attendance_records")

    @classmethod
    def from_api_response(cls, api_record):
        """
        Create an AttendanceRecord instance from API response data
        """
        return cls(
            att_date=datetime.fromisoformat(api_record["AttDate"]),
            check_time=datetime.fromisoformat(api_record["AttTime"]),
            employee_id=api_record["EmployeeID"],
            employee_name=api_record["FullName"],
            machine_alias=api_record["MachineAlias"],
            machine_serial=api_record["sn"]
        )