
from linear_solver import pywraplp
from tools import SolVal
from non_convex_tricks import sosn
def minimize_piecewise_linear(Points,B,convex=True):
    t = 'Piecewise'
    s = pywraplp.Solver(t,pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    n = len(Points)
    x = s.NumVar(Points[0][0],Points[n-1][0],'x')
    l = [s.NumVar(0,1,'l[%i]' % (i,)) for i in range(n)]  
    s.Add(1 == sum(l[i] for i in range(n)))               
    d = sosn(s, 2, l)
    s.Add(x == sum(l[i]*Points[i][0] for i in range(n)))  
    s.Add(x >= B)                                                 
    Cost = s.Sum(l[i]*Points[i][1] for i in range(n))     
    s.Minimize(Cost)
    rc = s.Solve()
    return rc,SolVal(l),SolVal(d[1])
