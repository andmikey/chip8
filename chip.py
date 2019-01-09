"""
Chip-8 emulator. 
"""
import logging
logging.basicConfig(level = logging.INFO)

class Chip:
    def __init__(self):
        # Memory
        # Byte addressable: 4096 bytes
        self.ram = [0] * 4096
        # 16 registers, referred to as Vx 
        self.registers = [0] * 16
        # Delay and sound timers
        self.delay = 0
        self.sound = 0
        # PC register
        # Starts at 512 - this is where programs are read in
        self.program_counter = 0x200
        # SP register
        self.stack_pointer = 0
        # Stack itself - 16 16-bit values
        self.stack = [0] * 16
        
        # Outputs
        # 64x32 display
        self.display = [0] * 64 * 32

        # Inputs
        # 16-key keyboard
        self.inputs = [0] * 16

    def read_rom(self, rom_path):
        logging.info("Reading rom at location: {}".format(rom_path))
        rom_contents = open(rom_path, "rb").read()
        logging.info("Size of rom is {} bytes".format(len(rom_contents)))

        for i in range(0, len(rom_contents)):
            self.ram[0x200 + i] = ord(rom_contents[i])

        logging.info("Wrote ROM to memory starting at 0x200")
        
if __name__ == "__main__":
    chip = Chip()
    chip.read_rom("pong.rom")
    
