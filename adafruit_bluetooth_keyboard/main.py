import signal
import sys
from threading import Event
import logging

from adafruit_bluetooth_keyboard.adafruit_bluetooth_le import AdafruitBluetoothLE
from adafruit_bluetooth_keyboard.raw_input_reader import RawInputReader

class MainRunner:
    def __init__(self):
        self.stop_event = Event()
        signal.signal(signal.SIGINT, self.exit_handler)
        signal.signal(signal.SIGTERM, self.exit_handler)
        self.setup_logging()

    def setup_logging(self):
        self.logger = logging.getLogger(__package__)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('main.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)


    def exit_handler(self, signum, frame):
        self.stop()

    def run(self):
        with AdafruitBluetoothLE(sys.argv[1]) as ble, RawInputReader() as raw_input:
            ble.ping()
            print("ready for input")
            while not self.stop_event.is_set():
                key = raw_input.read()
                if key == b'\x03':
                    break
                self.logger.debug(f"raw key: {key}")
                adafruit_key = raw_input_to_adafruit_keyboard_output(key)
                self.logger.debug(f"adafruit key: {adafruit_key.encode()}")
                ble.keyboard_send_str(adafruit_key)

    def stop(self):
        self.logger.info("got exit request")
        self.stop_event.set()

def raw_input_to_adafruit_keyboard_output(input: bytes) -> str:
    if input == b"\x7f":
        return "\\b"
    elif input == b"\r":
        return "\\r"
    elif input == b"?":
        return "\?"
    else:
        return input.decode()

if __name__ == "__main__":
    runner = MainRunner()
    runner.run()

