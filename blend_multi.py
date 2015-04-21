
from random import randint, uniform
def gen_data_content(m,n):
    # Oils down, acids accross (more oils than acids  m > n)
    R=[]
    for i in range(m):
        RR=[]
        P = 100
        for j in range(n-1):
            if P>1:
                acid = randint(1,min(70,P))*randint(0,1)
            else:
                acid = 0
            RR.append(acid)
            P -= acid
        RR.append(P)
        R.append(RR)
    return R
def gen_data_target(C):
    F=[]
    R0,R1=[],[]
    m,n=len(C),len(C[0])
    P=100
    R=[0 for j in range(n)]
    for i in range(m-1):
        if P:
            f=randint(1,min(20,P))
        else:
            f=0
        F.append(f)
        P-=f
        for j in range(n):
            acid = f*C[i][j]
            R[j] += acid
    f=P
    F.append(f)
    for j in range(n):
        acid = f*C[m-1][j]
        R[j] += acid
    for j in range(n):
        R0.append((0.95*R[j]/100.0))
        R1.append((1.05*R[j]/100.0))
    return [R0,R1]
def gen_data_cost(m,k):
    # Oils down, months accross
    R=[]
    for i in range(m):
        RR=[]
        for j in range(k):
            cost = randint(100,200)
            RR.append(cost)
        R.append(RR)
    return R
def gen_data_inventory(m):
    # Oils down
    R=[]
    for i in range(m):
        cost = [randint(0,200)]
        R.append(cost)
    return R

from linear_solver import pywraplp
from tools import SolVal, ObjVal
def solve_model(Part,Target,Cost,Inventory,D,SC,SL):
  t = 'Multi-period soap blending problem'
  s = pywraplp.Solver(t,pywraplp.Solver.CLP_LINEAR_PROGRAMMING)
  nO, nP, nA = len(Part), len(Cost[0]), len(Part[0])
  Buy = [[s.NumVar(0.0,D,'') for j in range(nP)] for i in range(nO)] 
  Blnd = [[s.NumVar(0.0,D,'') for j in range(nP)] for i in range(nO)] 
  Hold = [[s.NumVar(0.0,D,'') for j in range(nP)] for i in range(nO)] 
  Prod = [s.NumVar(0,D,'') for j in range(nP)]            
  CostP= [s.NumVar(0,D*1000,'') for j in range(nP)]  
  CostS= [s.NumVar(0,D*1000,'') for j in range(nP)] 
  Acid = [[s.NumVar(0,D*D,'') for j in range(nP)] for k in range(nA)] 
  for i in range(nO):                             
    s.Add(Hold[i][0] == Inventory[i][0])
  for j in range(nP):                                      
    s.Add(Prod[j] == sum(Blnd[i][j] for i in range(nO))) 
    s.Add(Prod[j] >= D)    
    if j < nP-1:                                       
      for i in range(nO):
        s.Add(Hold[i][j] + Buy[i][j] - Blnd[i][j] == Hold[i][j+1])
    s.Add(sum(Hold[i][j] for i in range(nO)) >= SL[0]) 
    s.Add(sum(Hold[i][j] for i in range(nO)) <= SL[1])
    for k in range(nA): 
      s.Add(Acid[k][j] == sum(Blnd[i][j]*Part[i][k] for i in range(nO)))
      s.Add(Acid[k][j] >= Target[0][k] * Prod[j])
      s.Add(Acid[k][j] <= Target[1][k] * Prod[j])
    s.Add(CostP[j] == sum(Buy[i][j] * Cost[i][j] for i in range(nO))) 
    s.Add(CostS[j] == sum(Hold[i][j] * SC for i in range(nO)))      
  Cost_product = s.Sum(CostP[j] for j in range(nP))
  Cost_storage = s.Sum(CostS[j] for j in range(nP))
  s.Minimize(Cost_product+Cost_storage)
  rc = s.Solve()
  B,L,H,A,P= SolVal(Buy),SolVal(Blnd),SolVal(Hold),SolVal(Acid),SolVal(Prod)
  CP,CS = SolVal(CostP),SolVal(CostS)
  return rc,ObjVal(s),B,L,H,P,A,CP,CS
