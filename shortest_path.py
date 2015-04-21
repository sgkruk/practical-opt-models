
from random import randint
from math import sqrt
def dist(p1,p2):
    return int(round(sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2))/10)
def gen_data(n):
    points=[(randint(1,1000), randint(1,1000)) for i in range(n)]
    points.sort()
    R=[]
    S=0
    for i in range(n):
        RR=[]
        for j in range(n):
            if i==j or abs(i-j)>0.5*n:
                d = 0
            else:
                d=dist(points[i],points[j])*randint(0,1)
            RR.append(d)
        R.append(RR)
    return R

from linear_solver import pywraplp
def solve_model(D,Start=None, End=None):
  t = 'Shortest path problem'
  s = pywraplp.Solver(t,pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
  n = len(D)
  if Start is None:
    Start,End = 0,len(D)-1
  G = [[s.NumVar(0,min(1,D[i][j]),'') for j in range(n)] for i in range(n)]
  for i in range(n): 
    if i == Start:
      s.Add(1 == sum(G[Start][j] for j in range(n))) 
      s.Add(0 == sum(G[j][Start] for j in range(n))) 
    elif i == End:
      s.Add(1 == sum(G[j][End] for j in range(n))) 
      s.Add(0 == sum(G[End][j] for j in range(n))) 
    else:
      s.Add(sum(G[i][j] for j in range(n))==sum(G[j][i] for j in range(n))) 
  Distance = s.Sum(G[i][j]*D[i][j] for i in range(n) for j in range(n)) 
  s.Minimize(Distance)
  rc = s.Solve()
  Path,Cost,Cumul,node=[Start],[0],[0],Start
  while rc == 0 and node != End and len(Path)<n:
    next = [i for i in range(n) if G[node][i].SolutionValue()==1][0]
    Path.append(next)
    Cost.append(D[node][next])
    Cumul.append(Cumul[-1]+Cost[-1])
    node = next
  return rc,s.Objective().Value(),Path,Cost,Cumul

def solve_all_pairs(D):
  n = len(D)
  Costs = [[None if i != j else 0 for i in range(n)] for j in range(n)]
  Paths = [[None for i in range(n)] for j in range(n)]
  for start in range(n):
    for end in range(n):
      if start != end and Costs[start][end] is None:
        rc, Value, Path, Cost, Cumul = solve_model(D,start,end)
        if rc==0:
          for k in range(len(Path)-1): 
            for l in range(k+1,len(Path)):
              if Costs[Path[k]][Path[l]] is None:
                Costs[Path[k]][Path[l]] = Cumul[l]-Cumul[k]
                Paths[Path[k]][Path[l]] = Path[k:l+1]
  return Paths, Costs
