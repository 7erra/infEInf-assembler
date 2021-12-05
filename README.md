# infEInf-assembler
A simple tool to run programs written for the infEInf lecture at the CAU.

## Installation
Download [assembler.py](assembler.py)
* As a [zip](https://github.com/7erra/infEInf-assembler/archive/refs/heads/master.zip),
* By cloning this repository,
* Or copying its content to a local file

## Usage
- Create a new file next to [assembler.py]()
- Write your assembler code in that file. The line count corresponds to the command counter.
- A default register can be passed to the program as a dictionary (see example)
- If you don't set this register you are prompted to enter starting values for all used registers

Example:

always0.txt
```
TST 100
JMP 4
JMP 6
DEC 100
JMP 1
HLT
```

whatever.py
```python
import assembler
p = assembler.Program("always0.txt")
p.run()
p.run({100: 0})
```

### Commands
#### TST register
Increase the command counter by two if the value in `register` is 0, increase it by 1 otherwise.
#### INC register
Increase the value stored in `register` by one.
#### DEC register
Decrease the value stored in `register` by one.
#### JMP counter
Jump to line `counter`.
#### HLT
Stop the program.

### Common mistakes
#### Infinite loops
Make sure your program has a HLT statement. In all other cases you have to rethink the logic of your program.
#### TargetError
Make sure that all right hand arguments are integers (except for HLT)
#### IndexError
You tried to execute a statement/line that does not exist. I.e that means that your program is trying to access a line after your last line.

## License
[MIT](https://choosealicense.com/licenses/mit/)
