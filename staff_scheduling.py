
from random import randint
def gen_section(n):
  R=[]
  section=0
  for c in range(n):
    for j in range(randint(1,4)):
      RR=[section,c,randint(1,20)]
      R.append(RR)
      section = section+1
  return R,section

from random import randint
def gen_instructor(m,n,p,pp):
  R=[]
  for i in range(m):
    RR=[i,[randint(1,2),randint(2,3)],[randint(0,1)*randint(-10,10) for _ in range(p)],\
        [randint(0,1)*randint(-10,10) for _ in range(n)],\
        [randint(0,1)*randint(-10,10) for _ in range(pp)]
      ]
    R.append(RR)
  return R

from random import randint
def gen_sets(n,ns):
  R=[]
  for i in range(ns):
    RR=[i,[j for j in range(n) if randint(0,1)]]
    R.append(RR)
  return R

from random import randint
def gen_pairs(pp,n):
  R=[]
  for i in range(pp):
      q=4
      c0=0
      RR=[]
      for j in range(q):
        c0 = randint(c0,int(3*n/q))
        c1 = randint(c0+1,n-1)
        if (c0,c1) not in RR:
            RR.append((c0,c1))
      RR.sort()
      R.append([i,RR])
  return R

from linear_solver import pywraplp
from tools import SolVal,ObjVal,newSolver
def solve_model(S,I,R,P):
  s = newSolver('Staff Scheduling',True)
  nbS,nbI,nbSets,nbPairs,nbC = len(S),len(I),len(R),len(P),S[-1][1]+1
  x = [[s.IntVar(0,1,'') for j in range(nbS)] for i in range(nbI)]
  z = [[[s.IntVar(0,1,'') \
         for k in range(len(P[p][1]))] \
         for p in range(nbPairs)] \
         for i in range(nbI)]
  for j in range(nbS):
    s.Add(sum(x[i][j] for i in range(nbI)) <= 1)
  for i in range(nbI):
    s.Add(sum(x[i][j] for j in range(nbS)) >= I[i][1][0])    
    s.Add(sum(x[i][j] for j in range(nbS)) <= I[i][1][1])
  WC = sum(x[i][j] * I[i][2][c] for i in range(nbI) \
           for j in range(nbS) for c in range(nbC) if S[j][1] == c)
  WR = sum(I[i][3][r] * sum(x[i][j] for j in R[r][1]) \
           for r in range(nbSets) for i in range(nbI))
  for i in range(nbI):
    for p in range(nbPairs):
      for k in range(len(P[p][1])):
        s1 = P[p][1][k][0]
        s2 = P[p][1][k][1]
        s.Add(x[i][s1] + x[i][s2] -1 <= z[i][p][k])
        s.Add(z[i][p][k] <= x[i][s1])
        s.Add(z[i][p][k] <= x[i][s2])
  WP = sum(z[i][p][k]*I[i][4][p] for i in range(nbI) \
           for p in range(nbPairs) for k in range(len(P[p][1])))
  s.Maximize(WC+WR+WP)
  rc,xs = s.Solve(),[]
  for i in range(nbI):
    xs.append([i,[[j,(I[i][2][S[j][1]],
              sum(I[i][3][r] for r in range(nbSets) if j in R[r][1]),
              sum(SolVal(z[i][p][k])*I[i][4][p]/2 
                  for p in range(nbPairs) for k in range(len(P[p][1])) 
                  if j in P[p][1][k]) 
            )] for j in range(nbS) if SolVal(x[i][j])>0]])
  
  return rc,SolVal(x),xs
