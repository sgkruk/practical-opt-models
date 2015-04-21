from multi_commodity_flow import solve_model
from tableutils import printmat, wrapmat
import copy
import random
import sys
import transship_dist 
# A test to see how often we get fractional solutions
def get_known():
  n = 8
  C0=[[0 for i in range(n+1)] for j in range(n+1)]
  C0[0][1] = 1
  C0[2][3] = 1
  C0[4][5] = 1
  C0[6][7] = 1
  C0[0][4] = 1
  C0[1][6] = 1
  C0[5][2] = 1
  C0[7][3] = 1
  C0[5][0] = 1
  C0[7][1] = 1
  C0[2][4] = 1
  C0[3][6] = 1
  C1=copy.deepcopy(C0)
  C0[0][-1] = 1
  C0[-1][3] = 1

  C1[2][-1] = 1
  C1[-1][1] = 1
  D = 1
  return [C0,C1],1

def fractional(v):
  return abs(v- round(v)) > 0.01
class getOutOfLoop( Exception ):
    pass
def main():
  n = 8
  K = 5
  nb = 100
  trc = 0
  tfrac = 0
  tot = 0
  for w in range(nb):
    print 'Test ',w
    if w == -1:
      C,Cap = get_known()
    else:
      C=[transship_dist.gen_data(n,False) for _ in range(K)]
      X=[[0 for _ in range(n)] for _ in range(n)]
      for k in range(K):
        rc,Val,x = transship_dist.solve_model(C[k])
        if rc==0:
          for i in range(n):
            for j in range(n):
              X[i][j] += x[i][j]
      Cap = max([e for row in X for e in row])
    rc = 0
    while rc == 0:
      Cap = Cap - 1
      rc,Val,x=solve_model(C,Cap)
      tot += 1
      try:
        if rc == 0:
          for k in range(K):
            for i in range(n):
              for j in range(n):
                if fractional(x[k][i][j]):
                  print 'Fractional example', Val, x[k][i][j]
                  tfrac += 1
                  raise getOutOfLoop
        else:
          trc += 1
      except getOutOfLoop:
        rc = 3
    print 'Fractional ',tfrac, 'Infeasible ',trc, 'Total ',tot
main()
