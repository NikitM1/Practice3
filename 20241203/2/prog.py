import math
import sys

class AssemblerInterpreter:
    def __init__(self, program):
        self.program = program.splitlines()
        self.labels = {}
        self.variables = {}
        self.commands = []
        self.parse_program()
    
    def parse_program(self):
        for line_num, line in enumerate(self.program):
            line = line.strip()
            if not line:
                continue
            if ':' in line:
                label, command = line.split(':', 1)
                label = label.strip()
                self.labels[label] = len(self.commands)
                line = command.strip()
            if line:
                self.commands.append(line)

    def run(self):
        pc = 0
        while pc < len(self.commands):
            parts = self.commands[pc].split()
            command = parts[0]
            args = parts[1:]
            
            if command == "stop":
                break
            elif command == "store":
                if len(args) != 2:
                    pc += 1
                    continue
                try:
                    value = float(args[0])
                except ValueError:
                    value = 0.0
                self.variables[args[1]] = value
            elif command in ("add", "sub", "mul", "div"):
                if len(args) != 3:
                    pc += 1
                    continue
                src = self.variables.get(args[0], 0.0)
                opn = self.variables.get(args[1], 0.0)
                dest = args[2]
                if command == "add":
                    result = src + opn
                elif command == "sub":
                    result = src - opn
                elif command == "mul":
                    result = src * opn
                elif command == "div":
                    if opn == 0:
                        result = math.inf
                    else:
                        result = src / opn
                self.variables[dest] = result
            elif command in ("ifeq", "ifne", "ifgt", "ifge", "iflt", "ifle"):
                if len(args) != 3:
                    pc += 1
                    continue
                src = self.variables.get(args[0], 0.0)
                opn = self.variables.get(args[1], 0.0)
                label = args[2]
                if label not in self.labels:
                    return  # Несуществующая метка
                if command == "ifeq" and src == opn:
                    pc = self.labels[label]
                    continue
                elif command == "ifne" and src != opn:
                    pc = self.labels[label]
                    continue
                elif command == "ifgt" and src > opn:
                    pc = self.labels[label]
                    continue
                elif command == "ifge" and src >= opn:
                    pc = self.labels[label]
                    continue
                elif command == "iflt" and src < opn:
                    pc = self.labels[label]
                    continue
                elif command == "ifle" and src <= opn:
                    pc = self.labels[label]
                    continue
            elif command == "out":
                if len(args) != 1:
                    pc += 1
                    continue
                print(self.variables.get(args[0], 0.0))
            pc += 1

program = sys.stdin.read()
interpreter = AssemblerInterpreter(program)
interpreter.run()
