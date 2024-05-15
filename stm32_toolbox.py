#!/usr/bin/env python3

import argparse
from stm32_programmer import STM32Programmer as sp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Toolbox for stm32 MCU and MPU for automating processes.")
    parser.add_argument('-p', '--path', help="Path to STM32_Programmer_CLI.exe.")
    parser.add_argument('-f', '--files', nargs='+', help='List of files and start addresses', metavar='FILE_ADDR', type=str)
    parser.add_argument('-d', '--data', nargs='+', help='Pass first address follwod by data. Start address must be 32-bit alignt.', metavar='FILE_ADDR', type=str)
    args = parser.parse_args()

    programmer_path = args.path

    stp = sp()

    if programmer_path is None:        
        if stp.find_stm32_programmer() is False:
            print("Found STM32_Programmer_CLI.exe in PATH found. Add to path or install STM32CubeProgrammer or pass path by argument. (https://www.st.com/en/development-tools/stm32cubeprog.html)")
            exit(1)
    
    print(f"Found STM32_Programmer_CLI.exe version {stp.version} in {stp.path}")    

    if stp.read_device_info() is False:
        print("Failed to connect to USB. Check connection and try again.")
        exit(1)

    print(stp.device_info)

    if args.data:
        start_address = args.data[0]
        data = args.data[1:]
        if stp.download_32bit_data(start_address, data) is False:
            print("Failed to download data.")
            exit(1)
    
    exit(0)

    if args.files:
        files_and_addresses = args.files
        files = files_and_addresses[::2]
        addresses = files_and_addresses[1::2]
        for file, address in zip(files, addresses):
            if stp.download(file, int(address, 16)) is False:
                print(f"Failed to download {file} to {address}.")
                exit(1)
    
    
