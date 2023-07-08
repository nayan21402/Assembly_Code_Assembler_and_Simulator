# Assembly Code Compiler and Simulator

This is a simple assembly code compiler and simulator created using Python. The tool consists of two separate programs: an assembler and a simulator. The assembler program converts assembly code from `inputA.txt` into binary instructions and performs syntax error checking. The simulator program executes the binary instructions from `inputS.txt`, allowing you to observe the behavior of the assembly code at each line as it executes.

## Features

- **Assembly Code Compilation:** The assembler program translates assembly code instructions into binary instructions.
- **Syntax Error Checking:** The assembler verifies the syntax of the assembly code and reports any errors encountered.
- **Simulation Execution:** The simulator program executes the binary instructions to simulate the behavior of the assembly code.
- **Command Line Output:** The simulator displays the output, including the state of registers and the program counter, in the command line.

## Valid Instructions and Registers

Here are the valid instructions and registers supported by the assembler and simulator:

### Instructions

- `addf`: Addition (Floating-point)
- `subf`: Subtraction (Floating-point)
- `movf`: Move (Floating-point)
- `add`: Addition
- `sub`: Subtraction
- `mov`: Move
- `ld`: Load
- `st`: Store
- `mul`: Multiplication
- `div`: Division
- `rs`: Right Shift
- `ls`: Left Shift
- `xor`: Bitwise XOR
- `or`: Bitwise OR
- `and`: Bitwise AND
- `not`: Bitwise NOT
- `cmp`: Compare
- `jmp`: Jump
- `jlt`: Jump if Less Than
- `jgt`: Jump if Greater Than
- `je`: Jump if Equal
- `hlt`: Halt

### Registers

- `R0`: Register 0
- `R1`: Register 1
- `R2`: Register 2
- `R3`: Register 3
- `R4`: Register 4
- `R5`: Register 5
- `R6`: Register 6
- `FLAGS`: Flags Register

## Usage

1. Clone the repository or download the source code.
2. Make sure you have Python installed on your machine (version X.X.X or higher).
3. Open a terminal or command prompt and navigate to the project directory.
4. Prepare your assembly code in `inputA.txt` file, following the appropriate syntax and using the valid instructions and registers listed above.
5. Run the assembler program by executing the following command:

```
python assembler.py inputA.txt
```


6. If there are no syntax errors and the instructions and registers are valid, the assembler will compile the assembly code and report any errors in the command line.
7. Prepare your binary instructions in `inputS.txt` file, following the appropriate format.
8. Run the simulator program by executing the following command:

```
python simulator.py inputS.txt
```


9. The simulator will start executing the binary instructions and display the output, including the state of registers and the program counter, in the command line.

## Example Assembly Code 

Here's an example of a simple assembly code snippet in `inputA.txt` using the valid instructions and registers mentioned above:

```
mov R0, $6   
mov R6, $1   
hlt        
```
## Example binary of the above code (generated using assembler)
```
1001000000000110
1001011000000001
0101000000000000
```
