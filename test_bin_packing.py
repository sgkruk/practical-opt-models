
import time, tableutils
from bin_packing import gen_data, solve_model, solve_model_break_symmetry
def main():
    import sys
    import random
    import tableutils
    n=6
    if len(sys.argv)<=1:
        print('Usage is main [data|run] [seed]')
        return
    elif len(sys.argv)>2:
        random.seed(int(sys.argv[2]))
    D,S=gen_data(n)
    if sys.argv[1]=='data':
        T=tableutils.wrapmat(D,[str(i) for i in range(n)],['','nb of packages','Unit weight'])
        T.insert(0,['','Truck weight limit',S])
        tableutils.printmat(T,True)
    elif sys.argv[1] in ['run', 'nrun']:
        start = time.clock()
        if sys.argv[1]=='nrun':
          rc,Val,P2T,T2P=solve_model(D,S)
        else:
          rc,Val,P2T,T2P=solve_model_break_symmetry(D,S)
        end = time.clock()
        #print 'Elapsed time ', end-start, ' optimal value ', Val
        print 'Truck, Packges (id weight)'
        for row in T2P:
          if (len(row[1])):              print '{0},"{1}"'.format(row[0],row[1])
main()
