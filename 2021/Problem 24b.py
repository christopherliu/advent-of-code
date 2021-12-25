import itertools
from dataclasses import dataclass

@dataclass
class Instruction:
    name: "str" = None
    argA: "str" = None
    argB: "str" = None
    
class Number():
    def __init__(self, value: int):
        self.value = value
        self.min = value
        self.max = value
        
    def __eq__(self, obj):
        return self.value == obj or (isinstance(obj, Number) and self.value == obj.value)
    
    def __add__(self, x):
        if isinstance(x, Number):
            return Number(self.value + x.value)
        else:
            return OpAdd(self, x)
        
    def __mul__(self, x):
        if isinstance(x, Number):
            return Number(self.value * x.value)
        else:
            return OpMul(self, x)
        
    def __floordiv__(self, x):
        if isinstance(x, Number):
            return Number(self.value // x.value)
        else:
            return OpDiv(self, x)
        
    def __mod__(self, x):
        if isinstance(x, Number):
            return Number(self.value % x.value)
        else:
            return OpMod(self, x)
        
    def __str__(self):
        return str(self.value)
    
class InputVariable():
    def __init__(self, position):
        self.position = position
        self.min = 1
        self.max = 9
        
    def __add__(self, x):
        return OpAdd(self, x)
    
    def __str__(self):
        return "X%s" % self.position
    
class OpAdd():
    def __init__(self, a1, a2):
        self.a1 = a1
        self.a2 = a2
        
        # Optimization
        if isinstance(a1, OpAdd) and isinstance(a1.a2, Number) and isinstance(a2, Number):
            self.a1 = a1.a1
            self.a2 = a1.a2 + a2
        self.min = a1.min + a2.min
        self.max = a1.max + a2.max
        
    def __str__(self):
        return "(%s+%s)" % (self.a1, self.a2)
        
class OpMul():
    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2
        #TODO simplify
        self.min = min(m1.min*m2.min, m1.min*m2.max, m1.max*m2.min, m1.max*m2.min)
        self.max = max(m1.min*m2.min, m1.min*m2.max, m1.max*m2.min, m1.max*m2.min)
    
    def __str__(self):
        return "(%s*%s)" % (self.m1, self.m2)
        
class OpDiv():
    def __init__(self, A, B):
        self.d1 = A
        self.d2 = B
        
        if A.min >= 0 and B.min >= 0:
            self.min = A.min // B.max
            self.max = A.max // B.min
        else:
            self.min = min(A.min//B.min, A.min//B.max, A.max//B.min, A.max//B.min)
            self.max = max(A.min//B.min, A.min//B.max, A.max//B.min, A.max//B.min)
    
    @classmethod
    def build(cls, A, B):
        # Optimization #1: if A is the sum of parts and one of those parts is a multiple of B and the other is < B, we can drop the one part.
        if isinstance(A, OpAdd):
            if isinstance(A.a1, OpMul) and (A.a1.m1 == B or A.a1.m2 == B) and A.a2.max < B.value:
                if A.a1.m1 == B: return A.a1.m2 
                elif A.a1.m2 == B: return A.a1.m1
            elif isinstance(A.a2, OpMul) and (A.a2.m1 == B or A.a2.m2 == B) and A.a1.max < B:
                if A.a2.m1 == B: return A.a2.m2 
                elif A.a2.m2 == B: return A.a2.m1
        return OpDiv(A, B)
    
    def __str__(self):
        return "(%s/%s)" % (self.d1, self.d2)
            
class OpMod():
    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2
        
        self.min = 0
        self.max = m2.max - 1
        
    def __str__(self):
        return "(%s%%%s)" % (self.m1, self.m2)
    
    @classmethod
    def build(cls, A, B):
        if isinstance(A, Number) and isinstance(B, Number):
            return A % B

        # Optimization #1: if A is the sum of parts and one of those parts is a multiple of B, we can drop that part.
        if isinstance(A, OpAdd):
            if isinstance(A.a1, OpMul) and (A.a1.m1 == B or A.a1.m2 == B):
                print("optimization found")
                A = A.a2
            elif isinstance(A.a2, OpMul) and (A.a2.m1 == B or A.a2.m2 == B):
                print("optimization found")
                A = A.a1
        
        # Optimization #2: if B is > A.max, then don't need mod at all
        if isinstance(B, Number) and B.value > A.max:
            print("optimization found")
            return A
            
        return OpMod(A, B)
        
class OpEql():
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
        
        self.min = 0
        self.max = 1
        
    def __str__(self):
        return "(%s==%s)" % (self.e1, self.e2)
    
    @classmethod
    def build(cls, A, B):
        if isinstance(A, OpEql) and B == 0:
            return OpNeq(A.e1, A.e2)
        return OpEql(A, B)
    
class OpNeq():
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
        
        self.min = 0
        self.max = 1
        
    def __str__(self):
        return "(%s!=%s)" % (self.e1, self.e2)

class MONAD():
    def __init__(self, instructions):
        self.instructions = instructions
        self.abstract_variables = {
            "w": Number(0),
            "x": Number(0),
            "y": Number(0),
            "z": Number(0),
        }
    
    def get(self, value):
        if value in self.abstract_variables:
            return self.abstract_variables[value]
        else:
            return Number(int(value))
        
    def compile_to_ast(self):
        cursor = 0
        for instruction in self.instructions:
            if instruction.name == "inp":
                self.abstract_variables[instruction.argA] = InputVariable(cursor)
                cursor += 1
            elif instruction.name == "add":
                if self.get(instruction.argB) == 0:
                    continue
                elif self.abstract_variables[instruction.argA] == 0:
                    self.abstract_variables[instruction.argA] = self.get(instruction.argB)
                    continue
                elif isinstance(self.abstract_variables[instruction.argA], Number) and isinstance(self.get(instruction.argB), Number):
                    self.abstract_variables[instruction.argA] += self.get(instruction.argB)
                else:
                    self.abstract_variables[instruction.argA] = OpAdd(self.abstract_variables[instruction.argA], self.get(instruction.argB))
            elif instruction.name == "mul":
                if self.abstract_variables[instruction.argA] == 0 or self.get(instruction.argB) == 0:
                    self.abstract_variables[instruction.argA] = Number(0)
                    continue
                elif self.get(instruction.argB) == 1:
                    continue
                elif isinstance(self.abstract_variables[instruction.argA], Number) and isinstance(self.get(instruction.argB), Number):
                    self.abstract_variables[instruction.argA] *= self.get(instruction.argB)
                else:
                    self.abstract_variables[instruction.argA] = OpMul(self.abstract_variables[instruction.argA], self.get(instruction.argB))
            elif instruction.name == "div":
                if self.abstract_variables[instruction.argA] == 0 or self.get(instruction.argB) == 1:
                    continue
                elif isinstance(self.abstract_variables[instruction.argA], Number) and isinstance(self.get(instruction.argB), Number):
                    self.abstract_variables[instruction.argA] //= self.get(instruction.argB)
                else:
                    self.abstract_variables[instruction.argA] = OpDiv.build(self.abstract_variables[instruction.argA], self.get(instruction.argB))
            elif instruction.name == "mod":
                self.abstract_variables[instruction.argA] = OpMod.build(self.abstract_variables[instruction.argA], self.get(instruction.argB))
            elif instruction.name == "eql":
                if self.abstract_variables[instruction.argA] == self.get(instruction.argB):
                    self.abstract_variables[instruction.argA] = 1
                elif self.abstract_variables[instruction.argA].max < self.get(instruction.argB).min:
                    self.abstract_variables[instruction.argA] = Number(0)
                elif self.abstract_variables[instruction.argA].min > self.get(instruction.argB).max:
                    self.abstract_variables[instruction.argA] = Number(0)
                else:
                    self.abstract_variables[instruction.argA] = OpEql.build(self.abstract_variables[instruction.argA], self.get(instruction.argB))
        
        return self.abstract_variables
    
    def is_valid(self, model_number):
        self.reset()
        self.run(model_number)
        return self.variables["z"] == 0
    
    @classmethod
    def from_file(cls, filename):
        return MONAD([Instruction(*line.strip().split(" ")) for line in open(filename, "r").readlines()])

##### COMPILATION
class And():
    def __init__(self, A, B):
        self.A = A
        self.B = B
    def __str__(self):
        return "(%s && %s)" % (self.A, self.B)
    
class Or():
    def __init__(self, A, B):
        self.A = A
        self.B = B
    def __str__(self):
        return "(%s || %s)" % (self.A, self.B)
    
class Lt():
    def __init__(self, A, B):
        self.A = A
        self.B = B
    def __str__(self):
        return "(%s < %s)" % (self.A, self.B)
        
def compile_to_logic_tree(ast):
    if isinstance(ast, OpAdd):
        return And(compile_to_logic_tree(ast.a1), compile_to_logic_tree(ast.a2))
    elif isinstance(ast, OpMul):
        return Or(compile_to_logic_tree(ast.m1), compile_to_logic_tree(ast.m2))
    elif isinstance(ast, OpDiv):
        return Lt(compile_to_logic_tree(ast.d1), compile_to_logic_tree(ast.d2))
    elif isinstance(ast, Number):
        return ast
    else:
        return ast

my_monad = MONAD.from_file("Day 24 input.txt")

# Method 3: Compile to AST to reduce.
ast = my_monad.compile_to_ast()["z"]
open("Day 24 output.txt", "w").write(str(ast))
open("Day 24 ast.txt", "w").write(str(compile_to_logic_tree(ast)))
print(compile_to_logic_tree(ast))