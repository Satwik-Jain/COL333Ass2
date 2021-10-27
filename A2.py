import json
import pandas as pd
import numpy as np
import random
import sys
import signal



sys.setrecursionlimit(10**6)

class TimeOutException(Exception):
    pass
def alarm_handler(signum, frame):
    raise TimeOutException()


signal.signal(signal.SIGALRM, alarm_handler)



def varSelection(array,N,D,j):

    if j==D:
        return 0,j

    l =0
    unassigned = []
    for l in range(0,N):
        if(array[l][j]==0):
            unassigned.append(l)
    
    if len(unassigned) == 0:
        return varSelection(array,N,D,j+1)

    for k in unassigned:
        if j>0 and (array[k][j-1] == 1 or array[k][j-1]==3): #if previous day morning or evening
            return k,j


    return random.choice(unassigned),j



def valueSelection(array,N,D,i,j,m,a,e,r,availableVal,preferedVal,nurseRest):

    if j>=1 and (array[i][j-1] == 1 or array[i][j-1]==3):   #if last day morning or even

        if nurseRest[i]==0 and availableVal[4]==1 and r!=0:
            return 4 

        elif availableVal[2]==1 and a!=0:
            return 2            #Giving Afternoon
        
        elif availableVal[3]==1 and e!=0:
            return 3            #atlast evening
    
        elif availableVal[4]==1 and r!=0:
            return 4

        
        else:
            return -1
    

    if nurseRest[i]==0 and availableVal[4]==1 and r!=0:
        return 4 

    elif availableVal[2]==1 and a!=0:
        return 2            #Giving Afternoon
    
    elif availableVal[1]==1 and m!=0:
        return 1

    elif availableVal[3]==1 and e!=0:
        return 3            #atlast evening

    elif availableVal[4]==1 and r!=0:
        return 4

    return -1


def checkValid(array,i,j,val,m,a,e,r,N):

    if val == 1 and (m ==0 or(j>=1 and  (array[i][j-1]==1 or array[i][j-1]==3))):
        return False

    if val ==2 and a==0:
        return False

    if val==3 and e ==0:
        return False
        
    if val ==4 and r==0:
        return False
    
    if i==N-1:
        if val==1 and (a!=0 or e!=0):
            return False
        elif val==2 and (m!=0 or e!=0):
            return False
        elif val==3 and (a!=0 or m!=0):
            return False

    return True



def preferVal(m,a,e):
    
    d = {1:m,2:a,3:e}

    sortedDict = sorted(d.items(),key=lambda x:x[1],reverse=True)
    most = 0
    for i in sortedDict:
        return(i[0])


def NurseSol(array,N,D,m,a,e,r,nurseRest,M,A,E,R):
    
    z=0
    for _ in range(0,m):
        array[z][0] =1
        z+=1
    for _ in range(0,a):
        array[z][0]=2
        z+=1
    for _ in range(0,e):
        array[z][0]=3
        z+=1
    for _ in range(0,r):
        array[z][0]=4
        nurseRest[z]+=1
        z+=1
    sol = nurseSolver(array,0,1,N,D,m,a,e,r,nurseRest,M,A,E,R)
    if sol:
        return array

    return np.zeros((N,D))


def validfurther(array,j,m,a,e,N):
    
    if j==0:
        return True

    count = 0
    total = 0
    for k in range(0,N):
        if array[k][j]==0:
            total+=1
            if array[k][j-1] == 1 or array[k][j-1] == 3:
                count+=1
    
    if total-count < m:
        return False
    
    return True




def nurseSolver(array,i,j,N,D,m,a,e,r,nurseRest,M,A,E,R):
    
    if(j==D):
        return True
    
    if not validfurther(array,j,m,a,e,N):
        return False

    valAvailable = [1,1,1,1,1]
    
    for x in range(0,4):

        y = preferVal(m,a,e)    #which is most remaining
        
        value = valueSelection(array,N,D,i,j,m,a,e,r,valAvailable,y,nurseRest)

        if(value==-1):      
            return False
        
        valAvailable[value]=0

        if checkValid(array,i,j,value,m,a,e,r,N):
            result = False

            array[i][j] =value

            if value ==1:
                m-=1
            elif value ==2:
                a-=1
            elif value==3:
                e-=1 
            elif value ==4:
                r-=1
                nurseRest[i]+=1
            
            if i == N-1:
                if(j%7==6):
                    nurseRest1=np.zeros(N)
                    result = nurseSolver(array,0,j+1,N,D,M,A,E,R,nurseRest1,M,A,E,R)
                else:
                    result = nurseSolver(array,0,j+1,N,D,M,A,E,R,nurseRest,M,A,E,R)
            else:
                 result = nurseSolver(array,i+1,j,N,D,m,a,e,r,nurseRest,M,A,E,R)
                 
            
            if result:
                return result
            else:
                array[i][j]=0
                if value ==1:
                    m+=1
                elif value ==2:
                    a+=1
                elif value==3:
                    e+=1
                elif value==4:
                    r+=1
                    nurseRest[i]-=1
    return False






#-------------------Part B---------------------#


def valueSelectionSenior(array,N,D,i,j,m,a,e,r,availableVal,nurseRest,S):

    if(i<S):
        if j>=1 and (array[i][j-1] == 1 or array[i][j-1]==3):

            if j%7 ==6 and nurseRest[i]==0 and availableVal[4]==1 and r!=0:
                return 4 

            elif availableVal[3]==1 and e!=0:
                return 3

            elif availableVal[4]==1 and r!=0:
                return 4
            
            elif availableVal[2]==1 and a!=0:
                return 2            #Giving Afternoon

            else:
                return -1

        else:
            if j%7 ==6 and nurseRest[i]==0 and availableVal[4]==1 and r!=0:
                return 4 

            if availableVal[1] and m!=0:
                return 1

            elif availableVal[3] and e!=0:
                return 3
            
            elif availableVal[4]==1 and r!=0:
                return 4
            
            elif availableVal[2]==1 and a!=0: 
                return 2            #Giving Afternoon

            else:
                return -1
            
            

    else:
        if j>=1 and (array[i][j-1] == 1 or array[i][j-1]==3):   #if last day morning or even

            if nurseRest[i]==0 and availableVal[4]==1 and r!=0:
                return 4 

            elif availableVal[3]==1 and e!=0:
                return 3            #atlast evening
        
            elif availableVal[2]==1 and a!=0:
                return 2            #Giving Afternoon
            
            
            elif availableVal[4]==1 and r!=0:
                return 4

            
            else:
                return -1
        

        if nurseRest[i]==0 and availableVal[4]==1 and r!=0:
            return 4 

        
        elif availableVal[3]==1 and e!=0:
            return 3            #atlast evening

        elif availableVal[2]==1 and a!=0:
            return 2            #Giving Afternoon
        
        elif availableVal[1]==1 and m!=0:
            return 1

        elif availableVal[4]==1 and r!=0:
            return 4

    return -1
    
    
def NurseSolSenior(array,N,D,m,a,e,r,nurseRest,S,T,M,A,E,R):
    
    sol = nurseSolverSenior(array,0,0,N,D,m,a,e,r,nurseRest,S,T,M,A,E,R)
    if sol:
        return array
    return np.zeros((N,D))



def nurseSolverSenior(array,i,j,N,D,m,a,e,r,nurseRest,S,T,M,A,E,R):

    if(j==D):
        return True
    
    if not validfurther(array,j,m,a,e,N):
        return False

    
    valAvailable = [1,1,1,1,1]
    
    for x in range(0,4):
        
        value = valueSelectionSenior(array,N,D,i,j,m,a,e,r,valAvailable,nurseRest,S)

        if(value==-1):      
            return False
        
        valAvailable[value]=0

        if checkValid(array,i,j,value,m,a,e,r,N):
            result = False

            array[i][j] =value

            if value ==1:
                m-=1
            elif value ==2:
                a-=1
            elif value==3:
                e-=1 
            elif value ==4:
                r-=1
                nurseRest[i]+=1
            

            if i == N-1:
                if(j%7==6):
                    nurseRest1=np.zeros(N)
                    result = nurseSolverSenior(array,0,j+1,N,D,M,A,E,R,nurseRest1,S,T,M,A,E,R)
                else:
                    result = nurseSolverSenior(array,0,j+1,N,D,M,A,E,R,nurseRest,S,T,M,A,E,R)
            else:
                 result = nurseSolverSenior(array,i+1,j,N,D,m,a,e,r,nurseRest,S,T,M,A,E,R)
                 
            
            if result:
                return result
            else:
                array[i][j]=0
                if value ==1:
                    m+=1
                elif value ==2:
                    a+=1
                elif value==3:
                    e+=1
                elif value==4:
                    r+=1
                    nurseRest[i]-=1
    return False

    
#======================  Main Function  ========================#

def main(argv):

    data = np.array(pd.read_csv(str(argv)),dtype= int)
    T,L = data.shape[0],data.shape[1]

    if(L==5):
        soln_list = []
        for i in range (0,T):
            M,A,E,R =0,0,0,0
            N,D,M,A,E = data[i]
            R = N-M-A-E
            array = np.zeros((N,D))

            dic = {}
            if(M+A+E> 6*N/7) or (N < 2*M+E ):
                soln_list.append(dic)
                continue
            
            nurseRest = np.zeros(N)

            
            solu = NurseSol(array,N,D,M,A,E,R,nurseRest,M,A,E,R)
            
            for p in range (0,D):
                for q  in range(0,N):
                    k = 'N'+str(q)+'_'+str(p)
                    if(solu[q][p]==1):
                        dic[k]='M'
                    elif(solu[q][p]==2):
                        dic[k]='A'
                    elif(solu[q][p]==3):
                        dic[k]='E'
                    else:
                        dic[k]='R'

            soln_list.append(dic)

        with open('solution.json','w') as file:
            for d in soln_list:
                json.dump(d,file)
                file.write("\n")
    

    elif L==7:
        soln_list_senior=[]
        for i in range (0,T):

            N,D,M,A,E,S,T = data[i]
            R = N-M-A-E
            array = np.zeros((N,D))

            dic={}

            if(M+A+E> 6*N/7) or (N < 2*M+E ):
                soln_list_senior.append(dic)
                continue
            
            nurseRest = np.zeros(N)

            notfound = False
            solu = None

            signal.alarm(T)
            try:
                solu = NurseSolSenior(array,N,D,M,A,E,R,nurseRest,S,T,M,A,E,R)
            except TimeOutException:
                notfound = True
                pass
            

            if notfound:
                soln_list_senior.append(dic)
                continue            


            for p in range (0,D):
                for q  in range(0,N):
                    k = 'N'+str(q)+'_'+str(p)

                    if(solu[q][p]==1):
                        dic[k]='M'
                    elif(solu[q][p]==2):
                        dic[k]='A'
                    elif(solu[q][p]==3):
                        dic[k]='E'
                    else:
                        dic[k]='R'

            soln_list_senior.append(dic)
            
        with open('solution.json','w') as file:
            for d in soln_list_senior:
                json.dump(d,file)
                file.write("\n")
    

if __name__=="__main__":
    main(sys.argv[1])