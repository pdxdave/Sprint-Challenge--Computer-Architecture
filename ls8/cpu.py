"""CPU functionality."""
# Round Two on this assignment.  Make it easier

import sys
import re

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[7] = 255
        self.SP = 0x07

    def ram_read(self, MAR):
        """ should accept the address to read and return the value stored there."""
        # MAR contains the address that is being read or written to
        return self.ram[MAR]  


    def ram_write(self, MAR, MDR):
        """should accept a value to write, and the address to write it to."""
        # remember, MDR is the data that was read or the data to write
        self.ram[MAR] = MDR  

    def load(self):

        """Load a program into memory."""

        address = 0
        if len(sys.argv) < 2: 
            print("You didn't give me a program name! I quit.")
            sys.exit()
        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ] 
        with open(sys.argv[1]) as file: # open file in the second sys argv spot
            for line in file: 
                if line[0] != '#' and line != '\n': # if not a comment or a new line 
                    self.ram[address] = int(line[0:8], 2)  
                    address += 1 
            file.closed #close file 

            
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT  = 0b00000001  
        LDI  = 0b10000010  
        PRN  = 0b01000111  
        PUSH = 0b01000101  
        POP  = 0b01000110  
        MUL  = 0b10100010
        CALL = 0b01010000
        RET  = 0b00010001  
        ADD  = 0b10100000

        running = True
        while running:
            # this comes right out of the instructions. It talks about reading the memory
            # address stored in the register 'pc' and storing it in the 'ir'
            IR = self.ram[self.pc]
            # again, from the instructions it's saying to using the ram_read() with pc+1, pc+2 and
            # operand a and b
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # if the IR is Halted, this isn't running 
            if IR == HLT:
                running = False
            elif IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            # elif print  equals IR
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif IR == PUSH:
                self.SP -= 1
                self.ram[self.SP] = self.reg[operand_a]
                self.pc += 2
            elif IR == POP:
                self.reg[operand_a] = self.ram[self.SP]
                self.SP += 1
                self.pc += 2
            elif IR == CALL: 
                return_address = self.pc + 2
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = return_address
                self.pc = self.reg[operand_a]
            elif IR == RET: 
                return_address = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1
                self.pc = return_address
            else:
                print("Halting the program")
                running = False
            

