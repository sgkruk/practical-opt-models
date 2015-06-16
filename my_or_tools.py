from linear_solver import pywraplp
def SolVal(x):
  if type(x) is not list:
    return 0 if x is None else x if isinstance(x,(int,float)) else x.SolutionValue()
  elif type(x) is list:
    return [SolVal(e) if e.Integer() is False else int(SolVal(e)) for e in x ]

def ObjVal(x):
  return x.Objective().Value()

def newSolver(name,integer=False):
  return pywraplp.Solver(name,\
                         pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING \
                         if integer else \
                         pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
  
def pairs(tuple, accum=[]):
  if tuple==[]:
    return accum
  else:
    head=tuple.pop(0)
    accum.extend((head,e) for e in tuple)
    return ordered_pairs(tuple,accum)

