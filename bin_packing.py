
from random import randint,uniform
def gen_data(n):
  R,T=[],0
  for i in range(n):
    RR=[randint(1,30),randint(10,500)]
    T+=RR[0]*RR[1]
    R.append(RR)
  return R,1900

from linear_solver import pywraplp
def solve_model(D,W):
  t = 'Bin Packing'
  s = pywraplp.Solver(t,pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING) 
  nbP = sum([P[0] for P in D])
  w = [e for sub in [[D[i][1]]*D[i][0] for i in range(len(D))] for e in sub] 
  nbT = bound_trucks(w,W)
  x = [[s.IntVar(0,1,'')  for j in range(nbT)] for i in range(nbP)] 
  y = [s.IntVar(0,1,'')  for j in range(nbT)]
  for j in range(nbT):
    s.Add(sum(w[i]*x[i][j] for i in range(nbP)) <= W*y[j]) 
  for i in range(nbP):
    s.Add(sum([x[i][j] for j in range(nbT)]) >= 1) 
  s.Minimize(s.Sum(y[j] for j in range(nbT))) 
  rc = s.Solve()
  P2T = [(i,j) for i in range(nbP) for j in range(nbT) if x[i][j].SolutionValue()>0]
  T2P = [[j, [(i,w[i]) for i in range(nbP) if x[i][j].SolutionValue()>0]] \
         for j in range(nbT)]
  return rc,s.Objective().Value(),P2T,T2P

from linear_solver import pywraplp
def solve_model_break_symmetry(D,W):
  t = 'Bin Packing'
  s = pywraplp.Solver(t,pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING) 
  nbP = sum([P[0] for P in D])
  w = [e for sub in [[D[i][1]]*D[i][0] for i in range(len(D))] for e in sub] 
  nbT = bound_trucks(w,W)
  x = [[s.IntVar(0,1,'')  for j in range(nbT)] for i in range(nbP)] 
  y = [s.IntVar(0,1,'')  for j in range(nbT)]
  for j in range(nbT):
    s.Add(sum(w[i]*x[i][j] for i in range(nbP)) <= W*y[j]) 
  for i in range(nbP):
    s.Add(sum([x[i][j] for j in range(nbT)]) == 1) 
  s.Minimize(s.Sum(y[j] for j in range(nbT))) 
  for j in range(nbT-1):
    s.Add(y[j]>=y[j+1])
  rc = s.Solve()
  P2T = [(i,j) for i in range(nbP) for j in range(nbT) if x[i][j].SolutionValue()>0]
  T2P = [[j, [(i,w[i]) for i in range(nbP) if x[i][j].SolutionValue()>0]] \
         for j in range(nbT)]
  return rc,s.Objective().Value(),P2T,T2P

def bound_trucks(w,W):
  nb,tot = 5,0
  for i in range(len(w)):
    if tot+w[i] < W:
      tot += w[i]
    else:
      tot = w[i]
      nb = nb+1
  return nb
