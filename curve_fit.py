
from random import randint, uniform
def gen_data(myfunc,n):
    R=[]
    for i in range(n):
        RR=[]
        t = i+uniform(0,1)
        RR.append(t)
        RR.append(myfunc(t)+myfunc(t)*uniform(0,0.5))
        R.append(RR)
    return R

from linear_solver import pywraplp
from my_or_tools import ObjVal, SolVal, newSolver

def solve_model(D,deg=1,objective=0):
  s,n = newSolver('Polynomial fitting'),len(D)
  b = s.infinity()
  a = [s.NumVar(-b,b,'a[%i]' % i) for i in range(1+deg)]  
  u = [s.NumVar(0,b,'u[%i]' % i) for i in range(n)]       
  v = [s.NumVar(0,b,'v[%i]' % i) for i in range(n)]       
  e = s.NumVar(0,b,'e')                                 
  for i in range(n):                              
    s.Add(D[i][1]==u[i]-v[i]+sum(a[j]*D[i][0]**j for j in range(1+deg)))
  for i in range(n):                                     
    s.Add(u[i] <= e)
    s.Add(v[i] <= e)
  if objective:
    Cost = e                                               
  else:
    Cost = sum(u[i]+v[i] for i in range(n))                
  s.Minimize(Cost)
  s.Solve()
  return SolVal(a)

def main():
    import sys
    import random
    import utils
    n=10
    degree=2
    if len(sys.argv)<=1:
        print('Usage is main [data|run] [seed]')
        return
    elif len(sys.argv)>=2:
        random.seed(int(sys.argv[2]))
    C=gen_data(lambda t:  1.8*t*t - 1.5*t + 0.3, n)
    if sys.argv[1]=='data':
        C.insert(0,['$t_i$','$f_i$'])
        utils.printmat(C,True)
    elif sys.argv[1]=='run':
        G=solve_model(C,degree,0)
        G1=solve_model(C,degree,1)
        T=[]
        error=0
        for i in range(n):
            fti = sum(G[j]*C[i][0]**j for j in range(degree+1))
            fti1 = sum(G1[j]*C[i][0]**j for j in range(degree+1))
            error += abs(fti - C[i][1])
            T.append([C[i][0], C[i][1], fti, abs(C[i][1]-fti), fti1, abs(C[i][1]-fti1)])
        T.insert(0,['$t_i$','$f_i$', '$f_{sum}(t_i)$', '$e_i^{sum}$', '$f_{max}(t_i)$', '$e_i^{max}$'])          
        utils.printmat(T,True)

main()
