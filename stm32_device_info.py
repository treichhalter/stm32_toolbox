class STM32CubeDeviceInfo:
    def __init__(self, info_str):
        self.info_str = info_str
        self.usb_speed = None
        self.manufacturer_id = None
        self.product_id = None
        self.serial_number = None
        self.dfu_protocol = None
        self.board = None
        self.device_id = None
        self.device_name = None
        self.flash_size = None
        self.device_type = None
        self.revision_id = None
        self.device_cpu = None

        self.__parse_info()

    def __parse_info(self):
        lines = self.info_str.split('\n')
        for line in lines:
            if line.startswith('USB speed'):
                self.usb_speed = line.split(':')[1].strip()
            elif line.startswith('Manuf. ID'):
                self.manufacturer_id = line.split(':')[1].strip()
            elif line.startswith('Product ID'):
                self.product_id = line.split(':')[1].strip()
            elif line.startswith('SN'):
                self.serial_number = line.split(':')[1].strip()
            elif line.startswith('DFU protocol'):
                self.dfu_protocol = line.split(':')[1].strip()
            elif line.startswith('Board'):
                self.board = line.split(':')[1].strip()
            elif line.startswith('Device ID'):
                self.device_id = line.split(':')[1].strip()
            elif line.startswith('Device name'):
                self.device_name = line.split(':')[1].strip()
            elif line.startswith('Flash size'):
                self.flash_size = line.split(':')[1].strip()
            elif line.startswith('Device type'):
                self.device_type = line.split(':')[1].strip()
            elif line.startswith('Revision ID'):
                self.revision_id = line.split(':')[1].strip()
            elif line.startswith('Device CPU'):
                self.device_cpu = line.split(':')[1].strip()

    def __str__(self):
        return f"USB speed: {self.usb_speed}\n" \
               f"Manufacturer ID: {self.manufacturer_id}\n" \
               f"Product ID: {self.product_id}\n" \
               f"Serial Number: {self.serial_number}\n" \
               f"DFU Protocol: {self.dfu_protocol}\n" \
               f"Board: {self.board}\n" \
               f"Device ID: {self.device_id}\n" \
               f"Device Name: {self.device_name}\n" \
               f"Flash Size: {self.flash_size}\n" \
               f"Device Type: {self.device_type}\n" \
               f"Revision ID: {self.revision_id}\n" \
               f"Device CPU: {self.device_cpu}"

