from enum import Enum

class TAGS(str, Enum):
    attandance_report = "Attandance Report"
    device_list = "Device List"

    def __str__(self) -> str:
        return self.value