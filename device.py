from dataclasses import dataclass


@dataclass
class DeviceFingerprint:
    SDK_INT: int
    width: int
    height: int
    screen_brightness: int
    network_operator_name: str
    system_os_version: str
    device_model: str
    build_model: int
    device_manufacturer: str
    device_name: str
    is_gps_available: bool
    is_gyroscope_available: bool
    is_accelerometeer_available: bool
    is_ethernet_available: bool
    is_touchscreen_available: bool
    is_nfc_available: bool
    is_wifi_available: bool
