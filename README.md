# ModbusTool

ModbusTool is a simple python3 Modbus TCP register read/write utility.

# Installation

```sh
pip3 install pymodbus
```

# Usage

```sh
# Read from available modbus TCP registers range
python3 modbus_enum3.py -i <IP ADDRESS> -p 502 -r -d <DELAY>

# Write to a modbus TCP register at a specified offset
python3 modbus_enum3.py -i <IP ADDRESS> -p 502 -w -o <REGISTER OFFSET> -v 1
```
