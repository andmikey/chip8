"""
Chip-8 emulator. 
"""
import logging
logging.basicConfig(level = logging.INFO)

class Chip:
    def __init__(self):
        """
        Initialise the emulator with default values.
        """ 
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
        # Index register
        self.i = 0
        
        # Outputs
        # 64x32 display
        self.display = [0] * 64 * 32

        # Inputs
        # 16-key keyboard
        self.inputs = [0] * 16

        # Sprites
        self.sprites =  \
            [0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
             0x20, 0x60, 0x20, 0x20, 0x70, # 1
             0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
             0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
             0x90, 0x90, 0xF0, 0x10, 0x10, # 4
             0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
             0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
             0xF0, 0x10, 0x20, 0x40, 0x40, # 7
             0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
             0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
             0xF0, 0x90, 0xF0, 0x90, 0x90, # A
             0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
             0xF0, 0x80, 0x80, 0x80, 0xF0, # C
             0xE0, 0x90, 0x90, 0x90, 0xE0, # D
             0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
             0xF0, 0x80, 0xF0, 0x80, 0x80  # F
            ]
        
    def read_rom(self, rom_path):
        """
        Read in the ROM binary located at rom_path.
        """
        logging.info("Reading rom at location: {}".format(rom_path))
        rom_contents = open(rom_path, "rb").read()
        logging.info("Size of rom is {} bytes".format(len(rom_contents)))

        for i in range(0, len(rom_contents)):
            self.ram[0x200 + i] = ord(rom_contents[i])

        logging.info("Wrote ROM to memory starting at 0x200")
    
    def cycle(self):
        """
        Execute one cycle of the CPU.
        """
        # Op codes are 4 bytes, so we need to read in PC and PC + 1
        curr_op = (self.ram[self.program_counter] << 8) | self.ram[self.program_counter + 1]
        logging.info("Current operation: {}".format(hex(curr_op)))
        self.program_counter += 2


    # Instructions
    def _0NNN(self, address):
        """
        Execute subroutine at NNN.
        """
        pass

    def _00E0(self):
        """
        Clear the screen.
        """
        pass

    def _00EE(self):
        """
        Return from a subroutine.
        """
        pass

    def _1NNN(self, address):
        """
        Jump to address NNN.
        """
        pass

    def _2NNN(self, address):
        """
        Execute subroutine starting at address NNN.
        """
        pass

    def _3XNN(self, vx, value):
        """
        Skip the following instruction if VX = NN. 
        """
        pass

    def _4XNN(self, vx, value):
        """
        Skip the following instruction if VX != NN.
        """
        pass

    def _5XY0(self, vx, vy):
        """
        Skip the following instruction if VX = VY. 
        """
        pass

    def _6XNN(self, vx, value):
        """
        Set VX = value. 
        """
        pass

    def _7XNN(self, vx, value):
        """
        Set VX = VX + value. 
        """
        pass

    def _8XY0(self, vx, vy):
        """
        Set VX = VY.
        """
        pass

    def _8XY1(self, vx, vy):
        """
        Set VX = VX OR VY.
        """
        pass

    def _8XY2(self, vx, vy):
        """
        Set VX = VX AND VY.
        """
        pass
    
    def _8XY3(self, vx, vy):
        """
        Set VX = VX XOR VY.
        """
        pass
    
    def _8XY4(self, vx, vy):
        """
        Set VX = VX + VY.
        Set VF to 01 if there is a carry, 01 otherwise. 
        """
        pass
    
    def _8XY5(self, vx, vy):
        """
        Set VX = VX - VY. 
        Set VF to 00 if there is a borrow, 01 otherwise. 
        """
        pass
    
    def _8XY6(self, vx, vy):
        """
        Set VX = VY >> 1 (right shift). 
        Set VF to LSB of VY prior to shift. 
        """
        pass
    
    def _8XY7(self, vx, vy):
        """
        Set VX = VY - VX.
        Set VF to 00 if there is a borrow, 01 otherwise. 
        """
        pass

    def _8XYE(self, vx, vy):
        """
        Set VX = VY << 1 (left shift).
        Set VF to MSB of VY prior to shift. 
        """
        pass

    def _9XY0(self, vx, vy):
        """
        Skip the following instruction if VX != VY.
        """
        pass

    def _ANNN(self, address):
        """
        Set I = NNN. 
        """
        pass

    def _BNNN(self, address):
        """
        Jump to NNN + V0. 
        """
        pass

    def _CXNN(self, vx, value):
        """
        Set VX = random byte AND value.
        Random byte is 0 - 255. 
        """
        pass

    def _DXYN(self, vx, vy, n):
        """
        Draw sprite at (vx, vy) of height n.
        """
        pass

    def _EX9E(self, vx):
        """
        Skip the following instruction if key of value VX is currently pressed.
        """
        pass

    def _EXA1(self, vx):
        """
        Skip the following instruction if key of value VX is not currently pressed. 
        """
        pass

    def _FX07(self, vx):
        """
        Store the current value of the delay timer in VX. 
        """
        pass

    def _FX0A(self, vx):
        """
        Wait for a keypress and store keypress in VX. 
        """
        pass

    def _FX15(self, vx):
        """
        Set delay timer = VX. 
        """
        pass

    def _FX18(self, vx):
        """
        Set sound timer = VX. 
        """
        pass
    
    def _FX1E(self, vx):
        """
        Set I = I + VX.
        """
        pass

    def _FX20(self, vx):
        """ 
        Set I = digit value of VX. 
        """
        pass

    def _FX33(self, vx):
        """
        Set addresses I, I+1, I+2 to binary-coded decimal equivalent of value in VX. 
        """
        pass

    def _FX55(self, vx):
        """
        Store register values V0 - VX (inclusive) starting at address I.
        """
        pass

    def _FX65(self, vx):
        """
        Fill registers V0 - VX (inclusive) with values starting at address I. 
        """
        pass
    
if __name__ == "__main__":
    chip = Chip()
    chip.read_rom("pong.rom")
