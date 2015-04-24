
from random import randint, choice
def compute_weeks(T,P):
  from math import ceil
  nbTeams = sum([1 for sub in T for e in sub])
  nbIntra = P[0]
  nbInter = P[1]
  nbPerWeek = P[2]
  nbGames = 0
  for i in range(len(T)):
    nb = len(T[i])
    nbGames += nb*(nb-1)/2 * nbIntra
    for j in range(i+1,len(T)):
      nbGames += nb*len(T[j]) * nbInter
  nbWeeks = ceil(ceil(2*nbGames/nbTeams)/nbPerWeek)
  return int(nbWeeks)+2
def gen_data(m,n):
  R,team=[],0
  for i in range(m):
    RR=[]
    nb = choice(n)
    for j in range(nb):
      RR.append(team)
      team = team+1
    R.append(RR)
  X=randint(1,3)
  Y=randint(1,X)
  Z=randint(1,5)
  Q=compute_weeks(R,(X,Y,Z))
  return R,(X,Y,Z,Q)

from linear_solver import pywraplp
from tools import ObjVal, SolVal, newSolver

def solve_model(T,P):
  nbTeams = sum([1 for sub in T for e in sub])
  nbIntra,nbInter,nbPerWeek,nbWeeks = P[0],P[1],P[2],P[3]
  s = newSolver('Sports schedule', True)
  x = [[[s.IntVar(0,1,'') for _ in range(nbWeeks)] 
        for _ in range(nbTeams)] for _ in range(nbTeams-1)]
  for D in T:
    for i in D:
      for j in D:
        if i<j:
          s.Add(sum(x[i][j][w] for w in range(nbWeeks)) == nbIntra)
  for d in range(len(T)-1):
    for e in range(d+1,len(T)):
      for i in T[d]:
        for j in T[e]:
          s.Add(sum(x[i][j][w] for w in range(nbWeeks)) == nbInter)

  for w in range(nbWeeks):
    for i in range(nbTeams):
      s.Add(sum(x[i][j][w] for j in range(nbTeams) if i<j) + 
            sum(x[j][i][w] for j in range(nbTeams) if j<i ) <= nbPerWeek)
  rc = s.Solve()  
  return rc,ObjVal(s),SolVal(x)
