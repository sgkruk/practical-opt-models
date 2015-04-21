
from random import randint,uniform
def gen_data(m,n,k):
        # m is number of subsets, n is the size of universe, k is the size of each subset
        R=[]
        for i in range(m):
            RR=[]
            while len(RR)<k:
                    p=randint(0,n)
                    if p not in RR:
                            RR.append(randint(0,n))
            RR.sort()
            R.append(RR)
        return R

from linear_solver import pywraplp
def solve_model(D,C=None):
    t = 'Set Packing'
    s = pywraplp.Solver(t,pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING) 
    nbRosters = len(D)
    nbCrew = max([e for d in D for e in d])+1
    S = [s.IntVar(0,1,'')  for i in range(nbRosters)] 
    for j in range(nbCrew):
        s.Add(1 >= sum(S[i] for i in range(nbRosters) if j in D[i])) 
    s.Maximize(s.Sum(S[i]*(1 if C==None else C[i]) for i in range(nbRosters))) 
    rc = s.Solve()
    Rosters = [i for i in range(nbRosters) if S[i].SolutionValue()>0]
    return rc,s.Objective().Value(),Rosters
