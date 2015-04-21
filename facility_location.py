
from random import randint
def gen_dcost(m,n):
    R=[]
    S=0
    for i in range(m):
        RR=[]
        for j in range(n):
            RR.append(randint(10,30))
        RR.append(randint(500,700))
        R.append(RR)
        S += RR[-1]            
    A = S/n                    
    RR = []
    for i in range(n):
        RR.append(randint(int(0.5*A), int(0.75*A)))
    RR.append(0)
    R.append(RR)
    return R
def gen_fcost(m):
  return [randint(100,200) for i in range(m)]

from linear_solver import pywraplp
from tools import ObjVal, SolVal
def solve_model(D,F):
  t = 'Facility location problem'
  s = pywraplp.Solver(t,pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  m,n = len(D)-1,len(D[0])-1
  x = [[s.NumVar(0,D[i][-1],'') for j in range(n)] for i in range(m)] 
  y = [s.IntVar(0,1,'') for i in range(m)]
  for i in range(m): 
    s.Add(D[i][-1]*y[i] >= sum(x[i][j] for j in range(n))) 
  for j in range(n):
    s.Add(D[-1][j] == sum(x[i][j] for i in range(m))) 
  Fcost = s.Sum(y[i]*F[i] for i in range(m))
  Dcost = s.Sum(x[i][j]*D[i][j] for i in range(m) for j in range(n))
  s.Minimize(Dcost + Fcost) 
  rc = s.Solve()
  return rc,ObjVal(s),SolVal(x),SolVal(y)
