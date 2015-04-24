
from sports_timetabling import gen_data, solve_model
def main():
    import sys
    import random
    import tableutils
    nbdiv=2
    nbteam=[6,7]
    if len(sys.argv)<=1:
        print('Usage is main [data|run] [seed]')
        return
    elif len(sys.argv)>=3:
        random.seed(int(sys.argv[2]))
    D,T=gen_data(nbdiv,nbteam)
    if sys.argv[1]=='data':
        R=[['(Intra Inter G/W Weeks)',tableutils.set2string(T)]]
        for i in range(len(D)):
            R.append(['Division '+str(i)+' teams',tableutils.set2string(D[i])])
        tableutils.printmat(R)
    elif sys.argv[1]=='run':
        rc,v,x=solve_model(D,T)
        if rc != 0:
            print 'Infeasible'
        else:
            nbweeks=len(x[0][0])
            nbteams=len(x[0])
            R=[]
            for w in range(nbweeks):
                RR=[]
                for i in range(nbteams):
                    for j in range(nbteams):
                        if i<j and x[i][j][w]>0:
                            RR.append(str(i)+' vs '+str(j))
                R.append(['Weeks '+str(w),RR])
            tableutils.printmat(R)
main()
