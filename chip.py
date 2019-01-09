"""
Chip-8 emulator. 
"""
import logging
import random
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
        self.index = 0
        
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

        # Set sprites to be in first 16 * 5 locations in memory
        for i in range(0, (16 * 5) + 1):
            self.ram[i] = sprites[i]
        
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
    def _00E0(self):
        """
        Clear the screen.
        """
        logging.info("Clearing screen")
        self.display = [0] * 64 * 32

    def _00EE(self):
        """
        Return from a subroutine.
        """
        self.program_counter = self.stack.pop()
        logging.info("Returning to PC: {}".format(self.program_counter))

    def _1NNN(self, address):
        """
        Jump to address NNN.
        """
        logging.info("Jumping to address {}".format(address))
        self.program_counter = address

    def _2NNN(self, address):
        """
        Execute subroutine starting at address NNN.
        """
        logging.info("Executing subroutine at {}".format(address))
        self.stack.push(self.program_counter)
        self.program_counter = address

    def _3XNN(self, vx, value):
        """
        Skip the following instruction if VX = NN. 
        """
        if self.registers[vx] == value:
            logging.info("{} = {}, skipping next instruction".format(vx, value))
            self.program_counter += 2

    def _4XNN(self, vx, value):
        """
        Skip the following instruction if VX != NN.
        """
        if self.registers[vx] != value:
            logging.info("{} != {}, skipping next instruction".format(vx, value))
            self.program_counter += 2

    def _5XY0(self, vx, vy):
        """
        Skip the following instruction if VX = VY. 
        """
        if self.registers[vx] == self.registers[vy]:
            logging.info("{} = {}, skipping next instruction".format(vx, vy))
            self.program_counter += 2

    def _6XNN(self, vx, value):
        """
        Set VX = value. 
        """
        logging.info("Setting register {} to {}".format(vx, value))
        self.registers[vx] = value

    def _7XNN(self, vx, value):
        """
        Set VX = VX + value. 
        """
        logging.info("Adding {} to value of register {}".format(value, vx))
        self.registers[vx] = self.registers[vx] + value

    def _8XY0(self, vx, vy):
        """
        Set VX = VY.
        """
        logging.info("Setting value of register {} to value of {}".format(vx, vy))
        self.registers[vx] = self.registers[vy]

    def _8XY1(self, vx, vy):
        """
        Set VX = VX OR VY.
        """
        logging.info("Setting register {} to OR {}".format(vx, vy))
        self.registers[vx] = self.registers[vx] | self.registers[vy]

    def _8XY2(self, vx, vy):
        """
        Set VX = VX AND VY.
        """
        logging.info("Setting register {} to AND {}".format(vx, vy))
        self.registers[vx] = self.registers[vx] & self.registers[vy]
    
    def _8XY3(self, vx, vy):
        """
        Set VX = VX XOR VY.
        """
        logging.info("Setting register {} to XOR {}".format(vx, vy))
        self.registers[vx] = self.registers[vx] ^ self.registers[vy]
    
    def _8XY4(self, vx, vy):
        """
        Set VX = VX + VY.
        Set VF to 01 if there is a carry, 01 otherwise. 
        """
        logging.info("Setting register {} to + {}".format(vx, vy))
        add = self.registers[vx] + self.registers[vy]
        if add > 0xff:
            logging.info("Overflow, setting VF to 1")
            self.registers[15] = 1
        else:
            logging.info("No overflow, setting VF to 0")
            self.registers[15] = 0
            
        self.registers[vx] = add
    
    def _8XY5(self, vx, vy):
        """
        Set VX = VX - VY. 
        Set VF to 00 if there is a borrow, 01 otherwise. 
        """
        vx = self.registers[vx]
        vy = self.registers[vy]

        logging.info("Setting register {} to - {}".format(vx, vy))
        
        if (vx < vy):
            logging.info("Carry, setting VF to 0")
            self.registers[15] = 0
        else:
            logging.info("No carry, setting VF to 1")
            self.registers[15] = 1

        self.registers[vx] = vx - vy
    
    def _8XY6(self, vx, vy):
        """
        Set VX = VY >> 1 (right shift). 
        Set VF to LSB of VY prior to shift. 
        """
        logging.info("Setting register {} to {} >> 1".format(vx, vy))
        self.registers[vx] = self.registers[vy] >> 1
        self.registers[15] = this._lsb(self.registers[vy])
    
    def _8XY7(self, vx, vy):
        """
        Set VX = VY - VX.
        Set VF to 00 if there is a borrow, 01 otherwise. 
        """
        vx = self.registers[vx]
        vy = self.registers[vy]

        logging.info("Setting register {} to {} -".format(vx, vy))
        
        if (vx > vy):
            logging.info("Carry, setting VF to 0")
            self.registers[15] = 0
        else:
            logging.info("No carry, setting VF to 1")
            self.registers[15] = 1

        self.registers[vx] = vy - vx

    def _8XYE(self, vx, vy):
        """
        Set VX = VY << 1 (left shift).
        Set VF to MSB of VY prior to shift. 
        """
        logging.info("Setting register {} to {} << 1".format(vx, vy))
        self.registers[vx] = self.registers[vy] << 1
        self.registers[15] = this._msb(self.registers[vy])

    def _9XY0(self, vx, vy):
        """
        Skip the following instruction if VX != VY.
        """
        if self.registers[vx] != self.registers[vy]:
            logging.info("{} != {}, skipping next instruction".format(vx, vy))
            self.program_counter += 2

    def _ANNN(self, address):
        """
        Set I = NNN. 
        """
        self.index = address

    def _BNNN(self, address):
        """
        Jump to NNN + V0. 
        """
        self.program_counter = address + self.registers[0]

    def _CXNN(self, vx, value):
        """
        Set VX = random byte AND value.
        Random byte is 0 - 255. 
        """
        byte = random.randint(0, 255)
        self.registers[vx] = byte & value

    def _DXYN(self, vx, vy, n):
        """
        Draw sprite at (vx, vy) of height n.
        """
        pass

    def _EX9E(self, vx):
        """
        Skip the following instruction if key of value VX is currently pressed.
        """
        if self.inputs[vx]:
            self.program_counter += 2

    def _EXA1(self, vx):
        """
        Skip the following instruction if key of value VX is not currently pressed. 
        """
        if not self.inputs[vx]:
            self.program_counter += 2

    def _FX07(self, vx):
        """
        Store the current value of the delay timer in VX. 
        """
        self.registers[vx] = self.delay_timer

    def _FX0A(self, vx):
        """
        Wait for a keypress and store keypress in VX. 
        """
        pass

    def _FX15(self, vx):
        """
        Set delay timer = VX. 
        """
        self.delay_timer = self.registers[vx]

    def _FX18(self, vx):
        """
        Set sound timer = VX. 
        """
        self.sound_timer = self.registers[vx]
    
    def _FX1E(self, vx):
        """
        Set I = I + VX.
        """
        self.index = self.index + self.registers[vx]

    def _FX20(self, vx):
        """ 
        Set I = digit value of VX. 
        """
        self.index = 5 * self.registers[vx]

    def _FX33(self, vx):
        """
        Set addresses I, I+1, I+2 to binary-coded decimal equivalent of value in VX. 
        """
        dec = str(self.registers[vx])
        self.memory[self.index] = dec[0]
        self.memory[self.index + 1] = dec[1]
        self.memory[self.index + 2] = dec[2]
        self.index += 3
        
    def _FX55(self, vx):
        """
        Store register values V0 - VX (inclusive) starting at address I.
        """
        for i in range(0, vx):
            # TODO is this index + i or just i?
            self.memory[self.index + i] = self.registers[i]
            
        self.index += i + 1

    def _FX65(self, vx):
        """
        Fill registers V0 - VX (inclusive) with values starting at address I. 
        """
        for i in range(0, vx):
            # TODO is this index + i or just i?
            self.registers[i] = self.memory[self.index + i]
            
        self.index += i + 1


    # Utility functions
    def _msb(n):
        msb = n >> (n.bit_length() - 8)
        logging.info("MSB is {}".format(msb))
        return msb

    def _lsb(n):
        lsb = n & 1
        logging.info("LSB is {}".format(lsb))
        return lsb
    
if __name__ == "__main__":
    chip = Chip()
    chip.read_rom("pong.rom")
