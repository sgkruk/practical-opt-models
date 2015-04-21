
from set_packing import gen_data, solve_model
def main():
    import sys
    import random
    import tableutils
    m=15
    n=40
    k=3
    if len(sys.argv)<=1:
        print('Usage is main [data|run] [seed]')
        return
    elif len(sys.argv)>2:
        random.seed(int(sys.argv[2]))
    D=gen_data(m,n,k)
    if sys.argv[1]=='data':
        T=[]
        for i in range(m):
            T.append([tableutils.set2string(D[i])])
        T=tableutils.wrapmat(T,[str(i) for i in range(m)],['Crew #','Crew ID'])
        tableutils.printmat(T,True)
    elif sys.argv[1]=='run':
        rc,Val,S=solve_model(D,None)
        T=[]
        #for i in range(len(C)):
        #     if len(C[i]):
        #         T.append(['Crew id '+str(i),tableutils.set2string(C[i])])
        T.insert(0,['Rosters chosen',tableutils.set2string(S)])
        tableutils.printmat(T,True)
main()
