import uuid

from device import DeviceFingerprint
from perimeterx import PerimeterX

test_fingerprint = DeviceFingerprint(
    SDK_INT=28,
    width=1600,
    height=900,
    screen_brightness=102,
    network_operator_name="TR Turkcell",
    system_os_version="4.19.71+",
    device_model="G011A",
    build_model=28,
    device_manufacturer="google",
    device_name="G011A",
    is_gps_available=True,
    is_gyroscope_available=True,
    is_accelerometeer_available=True,
    is_ethernet_available=True,
    is_touchscreen_available=True,
    is_nfc_available=True,
    is_wifi_available=True,
)


px = PerimeterX(test_fingerprint)
px.send_payload("PX315")
px.send_payload("PX329")

px_headers = px.get_headers()

utid = str(uuid.uuid4())
search_response = px.client.post(
    "https://www.skyscanner.net/g/radar/api/v2/unified-search",
    headers={
        "skyscanner-utid": utid,
        "x-skyscanner-traveller-context": f"{utid};1",
        "x-skyscanner-devicedetection-ismobile": "true",
        "x-skyscanner-return-inline-ads": "true",
        "x-skyscanner-viewid": "6a35877e-570d-4de3-aaef-f2271375d8c6",
        "x-skyscanner-trustedfunnelid": "b4e2cfe0-5061-4279-a567-aa77299ff820",
        "x-gateway-servedby": "gw53.skyscanner.net",
        "x-radar-combined-explore-unfocused-locations-use-real-data": "true",
        "x-radar-combined-explore-unfocused-dates-use-real-data": "true",
        "x-skyscanner-consent-adverts": "false",
        "x-skyscanner-channelid": "goandroid",
        "x-skyscanner-combined-results-hotel-polling": "true",
        "x-px-vid": px_headers["X-PX-VID"],
        "x-px-os-version": px_headers["X-PX-OS-VERSION"],
        "x-px-uuid": px_headers["X-PX-UUID"],
        "x-px-authorization": px_headers["X-PX-AUTHORIZATION"],
        "x-px-device-fp": px_headers["X-PX-DEVICE-FP"],
        "x-px-device-model": px_headers["X-PX-DEVICE-FP"],
        "x-px-os": px_headers["X-PX-OS"],
        "x-px-mobile-sdk-version": px_headers["X-PX-MOBILE-SDK-VERSION"],
        "user-agent": "Skyscanner/7.172.1 (G011A; Android 9)",
        "x-skyscanner-client": "skyscanner_android_app",
        "x-skyscanner-client-version": "7.172.1",
        "x-skyscanner-client-type": "net.skyscanner.android.main",
        "x-skyscanner-authenticated": "false",
        "x-skyscanner-device-os-type": "Android",
        "x-skyscanner-device-os-version": "9",
        "x-skyscanner-device": "Android-phone",
        "x-skyscanner-device-class": "phone",
        "x-skyscanner-device-model": "G011A",
        "x-skyscanner-client-network-type": "WIFI",
        "x-skyscanner-currency": "GBP",
        "x-skyscanner-locale": "en-US",
        "x-skyscanner-market": "UK",
        "skyscanner-jha": "CAISRAjT96nLBhIkZDVmYjdkNzQtM2Y5Yi00MGJmLWIzNjUtNDhhYWRkZDIyZTY4GPuVrssGKgJVSzIFZW4tVVM4AkIDR0JQ",
        "content-type": "application/json; charset=UTF-8",
        "accept-encoding": "gzip",
    },
    data="""{"adults":1,"childAges":[],"cabinClass":"economy","legs":[{"dates":{"@type":"date","year":2026,"month":1,"day":23},"legOrigin":{"@type":"entity","entityId":"95565050"},"legDestination":{"@type":"entity","entityId":"27540839"},"placeOfStay":"27540839"},{"dates":{"@type":"date","year":2026,"month":1,"day":30},"legOrigin":{"@type":"entity","entityId":"27540839"},"legDestination":{"@type":"entity","entityId":"95565050"},"placeOfStay":"95565050"}],"options":null}""",
)
