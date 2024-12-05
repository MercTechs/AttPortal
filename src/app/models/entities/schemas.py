# schemas.py
from pydantic import BaseModel, UUID4, Field
from datetime import datetime
from enum import Enum
from typing import List, Optional


# Attendance Record Schemas
class AttendanceRecordBase(BaseModel):
    att_date: datetime
    check_time: datetime
    employee_id: str
    employee_name: str
    machine_alias: str
    machine_serial: str

class AttendanceRecordCreate(AttendanceRecordBase):
    device_uuid: Optional[UUID4] = None

# API Response Schemas
class APIAttendanceRecord(BaseModel):
    AttDate: str
    AttTime: str
    EmployeeID: str
    FullName: str
    MachineAlias: str
    sn: str

class APIResponseData(BaseModel):
    result: str
    reason: str
    data: List[List[APIAttendanceRecord]]

class AttendanceSyncResponse(BaseModel):
    status: str
    message: str
    records_count: int

class AttendanceRecordResponse(BaseModel):
    uuid: str
    employee_id: str
    employee_name: str
    machine_alias: str
    machine_serial: str
    att_date: datetime
    check_time: datetime
    created_at: datetime
    sync_status: str

    class Config:
        from_attributes = True


class AttendanceListResponse(BaseModel):
    total: int
    records: List[AttendanceRecordResponse]


class DeviceType(str, Enum):
    CHECK_IN = "CheckIn"
    CHECK_OUT = "CheckOut"

class DeviceSyncStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

class DeviceResponse(BaseModel):
    id: int = Field(alias='ID')
    serial_number: str = Field(alias='SerialNumber')
    ip: str | None = Field(default=None, alias='IP')
    mac: str | None = Field(default=None, alias='MAC')
    model: str | None = Field(default=None, alias='Model')
    firmware: str | None = Field(default=None, alias='Firmware')
    platform: str | None = Field(default=None, alias='Platform')
    alias: str | None = Field(default=None, alias='Alias')
    location: str | None = Field(default=None, alias='Location')

    class Config:
        populate_by_name = True
        from_attributes = True

class EmployeeResponse(BaseModel):
    ssn: str = Field(alias='SSN')
    name: str = Field(alias='FullName')
    card: str | None = Field(default=None, alias='Card')
    department: str | None = Field(default=None, alias='Department')
    serial_number: str | None = Field(default=None, alias='SerialNumber')

    class Config:
        populate_by_name = True
        from_attributes = True

class AttendanceDeviceBase(BaseModel):
    device_id: str
    serial_number: str
    name: str | None = None
    device_type: DeviceType | None = None
    ip_address: str | None = None
    mac_address: str | None = None
    model: str | None = None
    firmware: str | None = None
    location: str | None = None

class AttendanceDeviceUpdate(AttendanceDeviceBase):
    is_active: bool | None = None
    sync_status: DeviceSyncStatus | None = None

class AttendanceDeviceInDB(AttendanceDeviceBase):
    uuid: UUID4
    is_active: bool
    last_sync: datetime
    sync_status: DeviceSyncStatus

    class Config:
        from_attributes = True

class DeviceSyncResponse(BaseModel):
    status: str
    new_devices: int
    updated_devices: int
    message: str | None = None

class AttendanceDeviceList(BaseModel):
    devices: List[AttendanceDeviceInDB]
    total: int

class DeviceTypeUpdate(BaseModel):
    device_type: DeviceType

    class Config:
        from_attributes = True