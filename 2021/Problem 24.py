import itertools
from dataclasses import dataclass

@dataclass
class Instruction:
    name: "str" = None
    argA: "str" = None
    argB: "str" = None

class MONAD():
    def __init__(self, instructions):
        self.instructions = instructions
    
    def reset(self):
        self.variables = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0,
        }
        
    def get(self, value):
        if value in self.variables:
            return self.variables[value]
        else:
            return int(value)
        
    def run(self, input):
        cursor = 0
        for instruction in self.instructions:
            if instruction.name == "inp":
                self.variables[instruction.argA] = input[cursor]
                cursor += 1
            elif instruction.name == "add":
                self.variables[instruction.argA] += self.get(instruction.argB)
            elif instruction.name == "mul":
                self.variables[instruction.argA] *= self.get(instruction.argB)
            elif instruction.name == "div":
                self.variables[instruction.argA] //= self.get(instruction.argB)
            elif instruction.name == "mod":
                self.variables[instruction.argA] %= self.get(instruction.argB)
            elif instruction.name == "eql":
                self.variables[instruction.argA] = 1 if self.variables[instruction.argA] == self.get(instruction.argB) else 0
        
    def get_abstraction(self, value):
        if value in self.abstract_variables:
            return self.abstract_variables[value]
        else:
            return int(value)
                
    def compile_to_algebra(self):
        # Baby's first optimizing compiler
        self.abstract_variables = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0,
        }
        
        cursor = 0
        for instruction in self.instructions:
            if instruction.name == "inp":
                self.abstract_variables[instruction.argA] = "X%s" % cursor
                cursor += 1
            elif instruction.name == "add":
                if self.get_abstraction(instruction.argB) == 0:
                    continue
                elif self.abstract_variables[instruction.argA] == 0:
                    self.abstract_variables[instruction.argA] = self.get_abstraction(instruction.argB)
                    continue
                elif isinstance(self.abstract_variables[instruction.argA], int) and isinstance(self.get_abstraction(instruction.argB), int):
                    self.abstract_variables[instruction.argA] += self.get_abstraction(instruction.argB)
                else:
                    self.abstract_variables[instruction.argA] = "(%s+%s)" % (self.abstract_variables[instruction.argA], self.get_abstraction(instruction.argB))
            elif instruction.name == "mul":
                if self.abstract_variables[instruction.argA] == 0 or self.get_abstraction(instruction.argB) == 0:
                    self.abstract_variables[instruction.argA] = 0
                    continue
                elif self.get_abstraction(instruction.argB) == 1:
                    continue
                elif isinstance(self.abstract_variables[instruction.argA], int) and isinstance(self.get_abstraction(instruction.argB), int):
                    self.abstract_variables[instruction.argA] *= self.get_abstraction(instruction.argB)
                else:
                    self.abstract_variables[instruction.argA] = "(%s*%s)" % (self.abstract_variables[instruction.argA], self.get_abstraction(instruction.argB))
            elif instruction.name == "div":
                if self.abstract_variables[instruction.argA] == 0 or isinstance(self.get_abstraction(instruction.argB), int) and self.get_abstraction(instruction.argB) == 1:
                    continue
                elif isinstance(self.abstract_variables[instruction.argA], int) and isinstance(self.get_abstraction(instruction.argB), int):
                    self.abstract_variables[instruction.argA] //= self.get_abstraction(instruction.argB)
                else:
                    self.abstract_variables[instruction.argA] = "(%s/%s)" % (self.abstract_variables[instruction.argA], self.get_abstraction(instruction.argB))
            elif instruction.name == "mod":
                if self.abstract_variables[instruction.argA] == 0:
                    continue
                elif isinstance(self.abstract_variables[instruction.argA], int) and isinstance(self.get_abstraction(instruction.argB), int):
                    self.abstract_variables[instruction.argA] %= self.get_abstraction(instruction.argB)
                else:
                    self.abstract_variables[instruction.argA] = "(%s%%%s)" % (self.abstract_variables[instruction.argA], self.get_abstraction(instruction.argB))
            elif instruction.name == "eql":
                if self.abstract_variables[instruction.argA] == self.get_abstraction(instruction.argB):
                    self.abstract_variables[instruction.argA] = 1
                elif isinstance(self.abstract_variables[instruction.argA], str) and self.abstract_variables[instruction.argA].startswith("X") and isinstance(self.get_abstraction(instruction.argB), int) and self.get_abstraction(instruction.argB) > 10:
                    self.abstract_variables[instruction.argA] = 0
                elif isinstance(self.get_abstraction(instruction.argB), str) and self.get_abstraction(instruction.argB).startswith("X") and isinstance(self.abstract_variables[instruction.argA], int) and self.abstract_variables[instruction.argA] > 10:
                    self.abstract_variables[instruction.argA] = 0
                else:
                    self.abstract_variables[instruction.argA] = "(%s==%s)" % (self.abstract_variables[instruction.argA], self.get_abstraction(instruction.argB))
        
        return self.abstract_variables
    
    def compile_to_ast(self):
        self.abstract_variables = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0,
        }
        
        cursor = 0
        for instruction in self.instructions:
            if instruction.name == "inp":
                self.abstract_variables[instruction.argA] = InputVariable(cursor)
                cursor += 1
            elif instruction.name == "add":
                if self.get_abstraction(instruction.argB) == 0:
                    continue
                elif self.abstract_variables[instruction.argA] == 0:
                    self.abstract_variables[instruction.argA] = self.get_abstraction(instruction.argB)
                    continue
                elif isinstance(self.abstract_variables[instruction.argA], int) and isinstance(self.get_abstraction(instruction.argB), int):
                    self.abstract_variables[instruction.argA] += self.get_abstraction(instruction.argB)
                else:
                    self.abstract_variables[instruction.argA] = "(%s+%s)" % (self.abstract_variables[instruction.argA], self.get_abstraction(instruction.argB))
            elif instruction.name == "mul":
                if self.abstract_variables[instruction.argA] == 0 or self.get_abstraction(instruction.argB) == 0:
                    self.abstract_variables[instruction.argA] = 0
                    continue
                elif self.get_abstraction(instruction.argB) == 1:
                    continue
                elif isinstance(self.abstract_variables[instruction.argA], int) and isinstance(self.get_abstraction(instruction.argB), int):
                    self.abstract_variables[instruction.argA] *= self.get_abstraction(instruction.argB)
                else:
                    self.abstract_variables[instruction.argA] = "(%s*%s)" % (self.abstract_variables[instruction.argA], self.get_abstraction(instruction.argB))
            elif instruction.name == "div":
                if self.abstract_variables[instruction.argA] == 0 or isinstance(self.get_abstraction(instruction.argB), int) and self.get_abstraction(instruction.argB) == 1:
                    continue
                elif isinstance(self.abstract_variables[instruction.argA], int) and isinstance(self.get_abstraction(instruction.argB), int):
                    self.abstract_variables[instruction.argA] //= self.get_abstraction(instruction.argB)
                else:
                    self.abstract_variables[instruction.argA] = "(%s/%s)" % (self.abstract_variables[instruction.argA], self.get_abstraction(instruction.argB))
            elif instruction.name == "mod":
                if self.abstract_variables[instruction.argA] == 0:
                    continue
                elif isinstance(self.abstract_variables[instruction.argA], int) and isinstance(self.get_abstraction(instruction.argB), int):
                    self.abstract_variables[instruction.argA] %= self.get_abstraction(instruction.argB)
                else:
                    self.abstract_variables[instruction.argA] = "(%s%%%s)" % (self.abstract_variables[instruction.argA], self.get_abstraction(instruction.argB))
            elif instruction.name == "eql":
                if self.abstract_variables[instruction.argA] == self.get_abstraction(instruction.argB):
                    self.abstract_variables[instruction.argA] = 1
                elif isinstance(self.abstract_variables[instruction.argA], str) and self.abstract_variables[instruction.argA].startswith("X") and isinstance(self.get_abstraction(instruction.argB), int) and self.get_abstraction(instruction.argB) > 10:
                    self.abstract_variables[instruction.argA] = 0
                elif isinstance(self.get_abstraction(instruction.argB), str) and self.get_abstraction(instruction.argB).startswith("X") and isinstance(self.abstract_variables[instruction.argA], int) and self.abstract_variables[instruction.argA] > 10:
                    self.abstract_variables[instruction.argA] = 0
                else:
                    self.abstract_variables[instruction.argA] = "(%s==%s)" % (self.abstract_variables[instruction.argA], self.get_abstraction(instruction.argB))
        
        return self.abstract_variables
    
    def is_valid(self, model_number):
        self.reset()
        self.run(model_number)
        return self.variables["z"] == 0
    
    @classmethod
    def from_file(cls, filename):
        return MONAD([Instruction(*line.strip().split(" ")) for line in open(filename, "r").readlines()])

my_monad = MONAD.from_file("Day 24 input.txt")

# Method 1: Too slow
# valid_model_numbers = [range(9,0,-1) for _ in range(0, 14)]
# cursor = 0
# for model_number in itertools.product(*valid_model_numbers):
#     cursor += 1
#     if cursor % 1000000 == 0:
#         print("Progress: Testing %s" % "".join([str(d) for d in model_number]))
#     if my_monad.is_valid(model_number):
#         print("Found a valid model number: %s" % model_number)
#         break

# Method 2: Try it myself (generates too long of a string, but gives us some idea of what it does)
# print(my_monad.compile_to_algebra()["z"])

# Biggest: 99919765949498
valid_model_numbers = [range(0,9) for _ in range(0, 14)]
cursor = 0
for model_number in itertools.product(*valid_model_numbers):
    # Apply constraints retrieved from analysis
    if model_number[2] != 8 + model_number[3]: continue
    if model_number[4] != 2 + model_number[5]: continue
    if model_number[9] + 5 != model_number[10]: continue
    
    cursor += 1
    if cursor % 1000000 == 0:
        print("Progress: Testing %s" % "".join([str(d) for d in model_number]))
    if my_monad.is_valid(model_number):
        print("Found a valid model number: %s" % "".join([str(d) for d in model_number]))
        break