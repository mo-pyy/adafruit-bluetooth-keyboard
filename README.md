# adafruit-bluetooth-keyboard

## hardware setup
Use an USB serial adapter to connect the [Adafruit Bluefruit LE UART Friend](https://learn.adafruit.com/introducing-the-adafruit-bluefruit-le-uart-friend/introduction) to your pc:
```
Bluefruit | serial adapter
--------------------------
  VIN     |  5V
  GND     |  GND
  CTS     |  GND
  RX      |  TX
  TX      |  RX
```
I didn't use uart flow control, despite being recommend by adafruit, but I did not ran into any problems.

## software setup
Clone the repo and run:
```bash
pip3 install .
```

## usage
```bash
python3 -m adafruit_bluetooth_keyboard.main /dev/ttyUSB0
```
replace `/dev/ttyUSB0` with the path of your serial adapter.

## dev setup
```bash
pip3 install -e .
pip3 install pre-commit
pre-commit install
```
