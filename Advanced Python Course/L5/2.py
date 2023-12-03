class Formula:
    def __init__(self):
        pass

    def __str__(self):
        pass

    def __add__(self, f):
        return And(self, f)
    
    def __mul__(self, f):
        return Or(self, f)

    def calc(self):
        pass

    def collect_variables(self):
        return set()

    def tautology(self):
        variables = self.collect_variables()
        for combination in self.generate_combinations(len(variables), []):
            try:
                if self.calc(zip(variables, combination)):
                    continue
                else:
                    return False
            except UnassignedVariableError:
                continue
        return True

    def generate_combinations(self, n, res=[]):
        if n == 0:
            return [res]
        else:
            combinations = []
            combinations.extend(self.generate_combinations(n - 1, res + [True]))
            combinations.extend(self.generate_combinations(n - 1, res + [False]))
            return combinations
        
    def simplify(self):
        pass


class FormulaError(Exception):
    pass


class UnassignedVariableError(FormulaError):
    def __init__(self, variable_name):
        self.variable_name = variable_name
        super().__init__(f"Variable '{variable_name}' is unassigned.")


class Var(Formula):
    def __init__(self, name=""):
        self.name = name

    def __str__(self):
        return f"{self.name}"

    def calc(self, variables):
        if self.name in variables:
            return variables[self.name]
        else:
            raise UnassignedVariableError(self.name)

        
    def collect_variables(self):
        return {self.name}
    
    def simplify(self):
        return self
        

class Const(Formula):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"
    
    def calc(self, _):
        return self.value

    def simplify(self):
        return self
    

class Not(Formula):
    def __init__(self, formula):
        self.formula = formula

    def __str__(self):
        return f"¬({self.formula})"
    
    def calc(self, vars):
        return not self.formula.calc(vars)
    
    def simplify(self):
        if isinstance(self.formula, Const):
            if self.formula.calc(None) == True:
                return Const(False)
            else:
                return Const(True)
        return self


class Or(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} ∨ {self.right})"

    def calc(self, vars):
        return self.left.calc(vars) or self.right.calc(vars)
    
    def simplify(self):
        l = self.left.simplify()
        r = self.right.simplify()
        if isinstance(l, Const):
            if l.calc(None) == True:
                return Const(True)
            else:
                return self.right
        elif isinstance(r, Const):
            if r.calc(None) == True:
                return Const(True)
            else:
                return self.left
        return Or(l, r)


class And(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} ∧ {self.right})"

    def calc(self, vars):
        return self.left.calc(vars) and self.right.calc(vars)

    def simplify(self):
        l = self.left.simplify()
        r = self.right.simplify()
        if isinstance(l, Const):
            if l.calc(None) == False:
                return Const(False)
            else:
                return self.right 
        elif isinstance(r, Const):
            if r.calc(None) == False:
                return Const(False)
            else:
                return self.left
        return And(l, r)
   

vars1 = {"x" : False, "y" : False}

f1 = And(Not(Var("x")), Or(Var("y"), Const(True)))
f2 = Or(Not(Var("x")), Var("x"))

print(f1.calc(vars1))
print(Or(Var("x"), Not(Const(True))).simplify())
print(f1.simplify())
print(f1.tautology())

f3 = f1 + f2
print(f3)
print(f3.simplify())
print((f1 + f2).tautology())
print(Const(True).tautology())
