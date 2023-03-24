import logging

import serial


class AdafruitBluetoothLE:
    def __init__(self, port: str):
        self.ser = serial.Serial(port=port, baudrate=9600, timeout=1)
        self.logger = logging.getLogger(__name__)

    def send_cmd(self, cmd: str, has_output=False) -> tuple[bool, list[str]]:
        self.ser.write(f"{cmd}\n".encode())
        self.ser.flush()
        if has_output:
            output = self.ser.readlines()
        else:
            output = [self.ser.readline()]
        output = [msg.decode().rstrip() for msg in output]
        self.logger.debug(output)
        success = output[-1] == "OK"
        return success, output[:-1]

    def set_cmd(self, cmd: str, value) -> tuple[bool, list[str]]:
        str_value = str(value)
        return self.send_cmd(f"{cmd}={str_value}")

    def set_bool_cmd(self, cmd: str, status: bool) -> tuple[bool, list[str]]:
        if status:
            value = 1
        else:
            value = 0
        return self.set_cmd(cmd, value)

    def ate(self, status: bool) -> bool:
        """
        Enables or disables echo of input characters
        """
        return self.set_bool_cmd("ATE", status)[0]

    def keyboard(self, status: bool) -> bool:
        """
        Advertise as a bluetooth keyboard
        """
        status1 = self.set_bool_cmd("AT+BLEKEYBOARDEN", status)[0]
        status2 = self.reset()
        return status1 and status2

    def keyboard_send_str(self, input: str) -> bool:
        return self.set_cmd("AT+BLEKEYBOARD", input)[0]

    def ping(self) -> bool:
        return self.send_cmd("AT")[0]

    def reset(self) -> bool:
        return self.send_cmd("ATZ")[0]

    def close(self):
        self.ser.close()

    def __enter__(self):
        self.reset()
        self.ate(False)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.ate(True)
        self.close()
