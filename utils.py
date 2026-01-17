import struct
import uuid

import tls_client


def gen_uuid_with_ts(ts):
    return str(uuid.UUID(int=((ts << 64) | 1)))


def get_perimeterx_client():
    client = tls_client.Session("perimeterx_android")
    client.proxies = "http://localhost:8083"
    return client


class WeirdCalculationShits:
    def __init__(self, text: str):
        components = text.split("|")
        self.a = int(components[2])
        self.b = components[3]
        self.f: int = int(components[4])
        self.g: int = int(components[5])
        self.c: int = int(components[6])
        self.d: int = int(components[7])
        self.e: int = int(components[8])
        self.h: int = int(components[9])

    def __repr__(self):
        result = "\n".join(
            f"self.{i} = {getattr(self, i)}"
            for i in ["a", "b", "f", "g", "c", "d", "e", "h"]
        )
        return result

    @staticmethod
    def weird_func_1(v: int, v1: int, v2: int, v3: int) -> int:
        v4 = v * v
        v5 = v1 * v1

        if v3 % 10 == 0:
            selector = v2 % 10
        else:
            selector = v2 % (v3 % 10)

        if selector == 0:
            return v4 + v1
        elif selector == 1:
            return v + v5
        elif selector == 2:
            return v4 * v1
        elif selector == 3:
            return v ^ v1
        elif selector == 4:
            return v - v5
        elif selector == 5:
            return (v + 0x30F) * (v + 0x30F) + v5
        elif selector == 6:
            return (v ^ v1) + v1
        elif selector == 7:
            return v4 - v5
        elif selector == 8:
            return v * v1
        elif selector == 9:
            return v1 * v - v
        else:
            return -1

    def weird_func_2(self, string1: str) -> int:
        v = self.weird_func_1(
            self.weird_func_1(self.c, self.d, self.f, self.h), self.e, self.g, self.h
        )
        arr_b = string1.encode("utf-8")
        return struct.unpack(">I", arr_b[:4])[0] ^ v if len(arr_b) >= 4 else v
