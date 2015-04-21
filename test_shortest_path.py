
from shortest_path import gen_data, solve_model, solve_all_pairs
def main():
    import sys
    import random
    import tableutils
    n=13
    header = ['P'+str(i) for i in range(n)]
    if len(sys.argv)<=1:
        print('Usage is main [data|run|all] [seed]')
        return
    elif len(sys.argv)>2:
        random.seed(int(sys.argv[2]))
    C=gen_data(n)
    if sys.argv[1]=='data':
        for i in range(n):
            C[i].insert(0,'P'+str(i))
        C.insert(0,['']+header)
        tableutils.printmat(C)
    elif sys.argv[1]=='run':
        rc,Value,Path,Cost,Cumul=solve_model(C)
        Path.insert(0,'Points')
        Cost.insert(0,'Distance')
        Cumul.insert(0,'Cumulative')
        T=[Path,Cost,Cumul]
        tableutils.printmat(T,True)
    elif sys.argv[1]=='all':
        Paths, Costs = solve_all_pairs(C)
        tableutils.printmat(tableutils.wrapmat(Costs,header,header))
main()
