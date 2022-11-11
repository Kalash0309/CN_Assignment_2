#!/usr/bin/python
from numpy import loadtxt,mean,ones
import sys 

#number of files:
nrfiles=len(sys.argv[1:])

#just to get the dimensions of the files
data=loadtxt(str(sys.argv[1]))
rows=data.shape[0]
cols=data.shape[1]
#print(rows)
#print(cols)
#initialize array
all=ones((int(nrfiles),int(rows),int(10)))

#load all files:
n=0
for file in sys.argv[1:]:
      data=loadtxt(str(file))
      all[n,:,0:cols]=data
      n=n+1

#calculate mean:
mean_all=mean(all,axis=0)

sys.stdout = open("final_result.txt", "w")
#print to stdout
for i in range(rows):
      a=''
      for j in range(cols):
         a=a+str('%010.5f   ' % mean_all[i,j])
      print (str(a))

sys.stdout.close()
