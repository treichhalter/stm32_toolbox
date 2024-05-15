import os
import re
import subprocess
from typing import List
from stm32_device_info import STM32CubeDeviceInfo as sdi

class STM32Programmer:
    def __init__(self):
        self.__version = None
        self.__path = None
        self.__exe_path = None
        self.__connection_port = "usb1"
        self.__device_info = None

    def find_stm32_programmer(self) -> bool:
        paths = os.environ.get("PATH", "").split(os.pathsep)
        stm32_programmer_paths = []
        for path in paths:
            if os.path.isfile(os.path.join(path, "STM32_Programmer_CLI.exe")):
                stm32_programmer_paths.append(path)

        stm32_programmer_dict = {}
        for path in stm32_programmer_paths:                        
            version_output = os.popen(f"{os.path.join(path, 'STM32_Programmer_CLI.exe')} --version").read()
            version_line = re.search(r"version:\s*(\S+)", version_output, re.IGNORECASE)
            if version_line:
                version = version_line.group(1)            
                stm32_programmer_dict[version] = path

        if not stm32_programmer_dict:            
            return False
        
        self.__version = max(stm32_programmer_dict.keys(), key=lambda x: tuple(map(int, x.split('.'))))                
        self.__path = stm32_programmer_dict[self.__version]
        self.__exe_path = os.path.join(self.__path, "STM32_Programmer_CLI.exe")
        return True
    
    @property
    def version(self) -> str:
        return self.__version
    
    @property
    def path(self) -> str:        
        return self.__path
    
    @property
    def device_info(self) -> sdi:
        return self.__device_info

    def read_device_info(self) -> bool:
        command = f"{self.__exe_path} -c port={self.__connection_port}"        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            self.__device_info = sdi(result.stdout)
            return True
                
        return False
    
    def erase(self, sector_range: List[int] ) -> bool:
        command = None
        if len(sector_range) == 1:
            command = f"{self.__exe_path} -c port={self.__connection_port} -e {sector_range[0]}"

        if len(sector_range) == 2:
            command = f"{self.__exe_path} -c port={self.__connection_port} -e [{sector_range[0]} {sector_range[1]}]"
        
        if command is None:
            return False
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        return result.returncode == 0
    
    def download(self, file_path: str, address: int) -> bool:
        command = f"{self.__exe_path} -c port={self.__connection_port} -d {file_path} 0x{address:X}"
        result = subprocess.run(command)        
        return result.returncode == 0
    
    def download_32bit_data(self, address: int, data: int) -> bool:
        data_str = str()
        for d in data:
            data_str = f"{data_str} {d}"
        command = f"{self.__exe_path} -c port={self.__connection_port} -w32 {address} {data_str} --verify"
        result = subprocess.run(command)        
        return result.returncode == 0
