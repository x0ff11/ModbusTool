import sys
import argparse
import time
from pymodbus.client import ModbusTcpClient


BOLD = "\033[1m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
END = "\033[0m"


def banner():
    print("")
    print("**** PyModbus Scanner **** ")
    print("")


def arg_parsing():
    parser = argparse.ArgumentParser("PyModbus Register Scan/Read/Write Tool")
    parser.add_argument('-i','--ip', dest='address', metavar='\b', help='Target IP address')
    parser.add_argument('-p','--port', dest='port', metavar='\b', help='Target Modbus port, default is TCP 502')
    parser.add_argument('-d','--delay', dest='sleepval', type=int, default=0, metavar='\b', help='Delay value between requests')

    parser.add_argument('-r','--read', dest='isread', action='store_true', help='Read all register types')

    parser.add_argument('-w','--write', dest='iswrite', action='store_true', help='Write to a register')
    parser.add_argument('-v','--value', dest='value', metavar='\b', type=int, help='Register write value [0,1]')
    parser.add_argument('-o','--offset', dest='offset', metavar='\b', type=int, default=0, help='Offset value for coil register write')

    args = parser.parse_args()
    return args


def register_read(target_ip, target_port, time_delay):

    # Connect to modbus server
    client = ModbusTcpClient(target_ip, port=target_port)
    client.connect()

    # Request counter
    count = 1

    while True:
        ''' Coil read
        0 = Start address to read from
        8 = (optional) Number of coils to read
        1 = (optional) Modbus slave ID
        '''
        coil_result = client.read_coils(0,8,1).bits
        coil_array = []
        for bit in coil_result:
            if bit == True:
                coil_array.append(LIGHT_GREEN + str(bit) + END)
            else:
                coil_array.append(LIGHT_RED + str(bit) + END)


        ''' Discrete input register read
        0 = Start address to read from
        8 = (optional) Number of coils to read
        1 = (optional) Modbus slave ID
        '''
        disc_result = client.read_discrete_inputs(0,8,1).bits
        disc_array = []
        for bit in disc_result:
            if bit == True:
                disc_array.append(LIGHT_GREEN + str(bit) + END)
            else:
                disc_array.append(LIGHT_RED + str(bit) + END)


        print("[+] Response " + str(count))
        print("[-] Coil Registers:           [" + ', '.join(coil_array) + "]")
        print("[-] Discrete Input Registers: [" + ', '.join(disc_array) + "]")
        print("[-] Holding Registers:        ", client.read_holding_registers(0,8,1).registers)
        print("[-] Input Registers:          ", client.read_input_registers(0,8,1).registers)
        print("---"*12)

        time.sleep(time_delay)
        count += 1





def register_write(target_ip, target_port, write_value, time_delay, coil_offset):

    # Connect to modbus server
    client = ModbusTcpClient(target_ip, port=target_port)
    client.connect()

    # Request counter
    count = 1

    print(LIGHT_RED + "[!] WRITING " + str(write_value) + " TO COIL AT OFFSET " + str(coil_offset) + " INFINTELY, 5S TO CANCEL IF UNINTENDED" + END)

    time.sleep(5)


    ''' Coil write
    0 = Start address to read from
    8 = (optional) Number of coils to read
    1 = (optional) Modbus slave ID
    '''
    while True:


        write_resp = client.write_coil(coil_offset,write_value,1)
        if "True" in str(write_resp):
           print('\r\033[K' + "[-] Request [" + str(count)  + "]:" + LIGHT_GREEN + " Coil write successful" + END, end=' ')
        else:
           print('\r\033[K' + LIGHT_RED + "[!] Coil write unsuccessful" + END, end='')

        if time_delay != 0:
            time.sleep(time_delay)

        count += 1


if __name__ == '__main__':

    banner()

    args = arg_parsing()

    target_ip = args.address
    target_port = args.port
    time_delay = args.sleepval
    modbus_read = args.isread
    modbus_write = args.iswrite
    write_value = args.value
    coil_offset = args.offset

    if modbus_read:
        register_read(target_ip, target_port, time_delay)
    else:
        register_write(target_ip, target_port, write_value, time_delay, coil_offset)
