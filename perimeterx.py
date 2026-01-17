import base64
import hashlib
import json
import os
import random
import urllib.parse
import uuid
from datetime import datetime

from device import DeviceFingerprint
from utils import WeirdCalculationShits, gen_uuid_with_ts, get_perimeterx_client


class PerimeterX:
    def __init__(self, fingerprint: DeviceFingerprint) -> None:
        self.fingerprint = fingerprint
        self.client = get_perimeterx_client()
        self.android_id = os.urandom(8).hex()
        self.uuid = str(uuid.uuid4())
        self.weird_shit = None
        self.sid = None
        self.vid = None

    def payload(self, t: str):
        ts = int(datetime.now().timestamp() * 1000)
        unique_string = gen_uuid_with_ts(ts)
        s3 = unique_string.split("-")[0].upper()
        input = self.fingerprint.device_model + unique_string + s3
        input_sha1 = hashlib.sha1(input.encode()).hexdigest()

        result_d = {
            "PX330": "new_session",
            "PX1214": self.android_id,
            "PX91": self.fingerprint.width,
            "PX92": self.fingerprint.height,
            "PX21215": self.fingerprint.screen_brightness,
            "PX316": True,  # network type
            "PX318": str(self.fingerprint.build_model),
            "PX319": self.fingerprint.system_os_version,
            "PX320": self.fingerprint.device_model,
            "PX339": self.fingerprint.device_manufacturer,
            "PX321": self.fingerprint.device_name,
            "PX323": int(datetime.now().timestamp()),
            "PX322": "Android",
            "PX337": True,  # has gps
            "PX336": True,  # has gyro
            "PX335": True,  # has accelerometeer
            "PX334": False,  # has ethernet
            "PX333": True,  # has touch screen
            "PX331": False,  # has nfc
            "PX332": True,  # has wifi
            "PX421": "false",  # is rooted
            "PX442": "false",  # contains test key
            "PX21218": "[]",  # touch datas
            "PX21217": "[]",  # motion datas
            "PX21224": "true",  # allow policy touch
            "PX21221": "true",  # stfu motion or smthn
            "PX317": "NA",  # version release
            "PX344": "EE",  # network operator name
            "PX347": '["en_US"]',  # obviously
            "PX343": "Unknown",
            "PX415": 100,  # charge
            "PX413": "good",
            "PX416": "AC",
            "PX414": "charging",
            "PX419": "Li-poly",
            "PX418": int(random.uniform(27, 28) * 10) / 10,  # temperature
            "PX420": 4.2,  # voltage
            "PX340": "v3.4.5",
            "PX342": "7.172.1",
            "PX341": '"Skyscanner"',
            "PX348": "net.skyscanner.android.main",
            "PX1159": False,
            "PX345": 0,
            "PX351": 0,
            "PX326": unique_string,
            "PX327": s3,
            "PX328": input_sha1.upper(),  # 600B0C3C0FE6C2112A923AD0711E7D99A4C8DBEA
        }
        if self.weird_shit:
            result_d["PX259"] = self.weird_shit.a
            result_d["PX256"] = self.weird_shit.b
            result_d["PX257"] = str(
                self.weird_shit.weird_func_2(self.fingerprint.device_model)
            )
        result_d["PX1208"] = "[]"
        result_d["PX21219"] = "{}"
        return [{"t": t, "d": result_d}]

    def execute_do(self, dos: list[str]):
        for do in dos:
            args = do.split("|")
            opcode = args[0]
            operand = args[1:]
            if opcode == "sid":
                self.sid = operand[0]
            elif opcode == "vid":
                self.vid = operand[0]
            elif opcode == "appc":
                if len(operand) >= 9 and operand[0] == "2":
                    self.weird_shit = WeirdCalculationShits(do)
            elif opcode == "bake":
                self.px_authorization = f"3:{operand[2]}"

    def send_payload(self, t: str):
        body_data = {
            "payload": base64.b64encode(
                json.dumps(self.payload(t), separators=(",", ":"), ensure_ascii=False)
                .replace("/", "\\/")
                .encode()
            ).decode(),
            "uuid": self.uuid,
            "appId": "PXrf8vapwA",
            "tag": "mobile",
            "ftag": "22",
        }
        if self.sid:
            body_data["sid"] = self.sid
        if self.vid:
            body_data["vid"] = self.vid
        body = urllib.parse.urlencode(body_data).replace(
            "%3D", "="
        )  # probably header order isnt even necessary. silly ahh antibot
        response = self.client.post(
            "https://collector-pxrf8vapwa.perimeterx.net/api/v1/collector/mobile",
            headers={
                "user-agent": "PerimeterX Android SDK/3.4.5",
                "accept-": "UTF-8",
                "accept": "*/*",
                "content-type": "application/x-www-form-urlencoded; charset=utf-8",
                "content-length": str(len(body)),
                "accept-encoding": "gzip",
            },
            data=body,
        )
        self.execute_do(response.json()["do"])

    def get_headers(self):
        return {
            "X-PX-VID": self.vid,
            "X-PX-SID": self.sid,
            "X-PX-OS-VERSION": "9",
            "X-PX-UUID": self.uuid,
            "X-PX-AUTHORIZATION": self.px_authorization,
            "X-PX-DEVICE-FP": self.android_id,
            "X-PX-DEVICE-MODEL": self.fingerprint.device_model,
            "X-PX-OS": "Android",
            "X-PX-MOBILE-SDK-VERSION": "3.4.5",
        }
