def wrapmat(M,left,header):
    m,n=len(M),len(M[0])
    for i in range(m):
        M[i].insert(0,left[i]);
    M.insert(0,header)
    return M
def printmat(M,zeroes=False,decimals=4):
    for row in M:
        l=''
        for i in range(len(row)):
            col=row[i]
            if type(col)==int:
                if col or zeroes:
                    l=l+'{0}'.format(col)
                else:
                    l=l+''
            elif type(col)==float:
                if col or zeroes:
                    if decimals==4:
                        l=l+'{0:.4f}'.format(col)
                    elif decimals==2:
                        l=l+'{0:.2f}'.format(col)
                    elif decimals==1:
                        l=l+'{0:.1f}'.format(col)
                else:
                    l=l+''
            else:
                l=l+str(col)
            if i < len(row)-1:
                l=l+','
        print(l)
  
