
from subprocess import call

testfiles =[]
registeranswers=[]
dataanswers=[]
registerfile=[]
data=[]
reg1=[]
reg2=[]
registerstatus=[]
datastatus=[]


no_of_testcases = input("Enter number of testcases :")
for i in range (int(no_of_testcases)):
   file_name = input("Enter name of testcase file(without .txt) :")+".txt"
   testfiles.append(file_name) 

for i in range (int(no_of_testcases)):
   file_name = input("Enter name of registerfile answers(without .txt) :")+".txt"
   registeranswers.append(file_name) 

for i in range (int(no_of_testcases)):
   file_name = input("Enter name of datamemory answers(without .txt) :")+".txt"
   dataanswers.append(file_name) 




for i in range (len(testfiles)) : 
    registerfile.clear()
    data.clear()
    reg1.clear()
    reg2.clear()
    with open(testfiles[i]) as f:
        with open("inputassembly.txt", "w+") as f1:
            for line in f:
                f1.write(line)
#to get the values of register files result from the running of simulation 

    call(["python", "automated.py"])

    f_reg=open("reg.txt", "r")
    
    for line in f_reg:
        registerfile.append(line)


    for z in range (len(registerfile)) :
        
        ind=registerfile[z].find(":")
        registerfile[z]=registerfile[z][ind+1:].strip()


    del registerfile[:3]    
    f_reg.close()        
#to get the values of register files that we expect
    
    with open(registeranswers[i]) as refile:
        for line in refile:
            reg1.append(line)
    for k in range (len(reg1)) :
        ind=reg1[k].find(":")
        reg1[k]=reg1[k][ind+1:].strip()


    
    regstat  = (registerfile ==reg1)
    registerstatus.append(regstat)
#to get the values of memory result from simulation     
    f_data=open("data.txt", "r")
    
    for line in f_data:
        data.append(line)


    for z in range (len(data)) :
        
        ind=data[z].find(":")
        data[z]=data[z][ind+1:].strip()

    
    del data[:3]    
    f_data.close()        

#to get the values of register files that we expect
    
    with open(dataanswers[i]) as datafile:
        for line in datafile:
            reg2.append(line)
    for q in range (len(reg2)) :
        ind=reg2[q].find(":")
        reg2[q]=reg2[q][ind+1:].strip()

    datastat  = (data ==reg2)
    datastatus.append(datastat)


for i in range (int(no_of_testcases)):

    print ("The Report of Testcase No : " + str((i+1) )+ " is  \n   registerfile :" + str(registerstatus[i]) + '\n'+ "   datamemory :" + str(datastatus[i]) + '\n' )


input("press any key to exit")