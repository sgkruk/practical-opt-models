from linear_solver import pywraplp
def SolVal(x):
  if type(x) is not list:
    return x.SolutionValue()
  elif type(x) is list:
    return [SolVal(e) for e in x ]

def ObjVal(x):
  return x.Objective().Value()

def newSolver(name,integer=False):
  return pywraplp.Solver(name,\
                         pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING \
                         if integer else \
                         pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
  
