from array import array
import os 
import time





ins=[]
array1 = []
array2=[]
############################

#gui





#############################






def running():
    labels=[]
    instructions=[]


    def twos_complement(val, nbits):
        """Compute the 2's complement of int value val"""
        if val < 0:
            val = (1 << nbits) + val
        else:
            if (val & (1 << (nbits - 1))) != 0:
                # If sign bit is set.
                # compute negative value.
                val = val - (1 << nbits)
        return val
    def reg2bin(arg): 
        switcher ={ 
            "0":   "0",
            "$ze": "0",
            "$at": "1",
            "$v0": "2", 
            "$v1": "3", 
            "$a0": "4",
            "$a1": "5",
            "$a2": "6",
            "$a3": "7",
            "$t0": "8",
            "$t1": "9",
            "$t2": "10",
            "$t3": "11",
            "$t4": "12",
            "$t5": "13",
            "$t6": "14",
            "$t7": "15",
            "$s0": "16",
            "$s1": "17",
            "$s2": "18",
            "$s3": "19",
            "$s4": "20",
            "$s5": "21",
            "$s6": "22",
            "$s7": "23",
            "$t8": "24",
            "$t9": "25",
            "$k0": "26",
            "$k1": "27",
            "$gp": "28",
            "$sp": "29",
            "$fp": "30",
            "$ra": "31",

        } 
        return switcher.get(arg, "ERROR")

    def optobin(argg): 
        switcher ={ 
            "Add": "000000", 
            "Sw":  "101011", 
            "Lw":  "100011", 
            "Sll": "000000",
            "And": "000000",
            "Or":  "000000",
            "Beq": "000100",
            "J":   "000010",
            "Jal": "000011",
            "Jr":  "000000",
            "Addi":"001000",
            "Ori": "001101",
            "Slt": "000000",
        } 
        return switcher.get(argg, "Not Supported Instruction, Please Read the USer Manual")

    def bin2bin(argo,num): 
        
        argo=str(argo)
        if argo[0]=="-":
            argo = int(argo)
            argo=twos_complement(argo,num)
            argo=bin(argo)[2:]
            return argo
        else:
        
            argo = int(argo)
            argo=bin(argo)    
            argo=argo[2:]
            length = len(argo)
            adding ="00000000000000000000000000000000000000000000000000000000000000"
            if length<num:
                argo=adding[:num-length]+argo
            return argo     

    def findlabel(arr):
        #function to find labels and put them in an array
        #it return all instructions in instructions in (instrctions[] )
        #it return the labels on (labels[])
        #label addres will be the next item to the label 
        #example if label in index 0 its addres will be in index 1
        i = 0
        x=0
        for element in arr:
           
            zero =arr[x].find("$zero")
            if zero != -1:
                arr[x] = arr[x][:zero] +"$ze" +arr[x][zero+5:]
            x=x+1
        for element in arr:
            position = element.find("$")
            position2=element.find(" ")
            if position > 4 and position2 !=4 :
                #there is a label 
                labelpos = element.find(" ")
                labels.append(element[:labelpos] )
                labels.append(i)
                instructions.append(element[labelpos+1:])
            elif position==-1 and position2 >1:
                if element[:position2]=="jal" or element[:position2]=="Jal":
                    instructions.append(element)
                else:
                        labelpos = element.find(" ")
                        labels.append(element[:labelpos] )
                        labels.append(i)
                        instructions.append(element[labelpos+1:]) 
                
            
                    

            else:
                instructions.append(element)

            i=i+4 
    def runmodelsim():
        os.system("vlib work")
        os.system("vlog mipsfinal7.v")
        os.system('cmd/c"vsim -c -do "run.do" mipsfinal7 -wlf finalmips7.wlf"')

    






    def ass2bin(assembly):
        
            
        pos = assembly.find("$")
        poss=assembly.find(" ")
        if pos == -1 and poss==1 :
            op = assembly[:poss]
            op=op.title()
            opcode=optobin(op)
            label = assembly[poss+1:]
            labelindex= labels.index(label)
            labeladdress=labels[labelindex+1]
            labeladdress=bin2bin(labeladdress,32)
            labeladdress=labeladdress[4:30]
            
            return(opcode+labeladdress)

        elif pos==-1 and poss==3:
            op = assembly[:poss]
            op=op.title()
            opcode=optobin(op)
            label = assembly[poss+1:]  #hena el moshkela 
            labelindex= labels.index(label)
            labeladdress=labels[labelindex+1]
            labeladdress=bin2bin(labeladdress,32)
            labeladdress=labeladdress[4:30]
            
            return(opcode+labeladdress)


        else:
            op = assembly[:pos-1]
            op =op.title()
            #get the op code
            
            opcode = optobin(op)
            
            #Get the type and convert registers to binary 

            #R type
            if opcode=="000000":
                #differentiate between R type instructions 
                if op == "Add" or op == "And" or op =="Or" or op =="Slt":
                    rd = assembly[pos:pos+3]
                    pos1 =assembly[pos+1:].find("$")+pos+1
                    rs = assembly[pos1:pos1+3] 
                    pos2 = assembly[pos1+2:].find("$")+pos1+2
                    rt=assembly[pos2:pos2+3] 
                    shamt = "0"
                    if op == "Add":
                        funct="32"
                    elif op=="And":
                        funct="36"
                    elif op=="Or":
                        funct= "37"
                    elif op=="Slt" :
                        funct="42"           
                elif op == "Sll":
                    rd = assembly[pos:pos+3]
                    pos1 =assembly[pos+1:].find("$")+pos+1
                    rt = assembly[pos1:pos1+3]  
                    shamt = assembly[pos1+5:]
                    rs="0"
                    funct="0"
                    
                elif op =="Jr":
                    rs = assembly[pos:pos+3]
                    rt="0"
                    rd="0"
                    shamt="0"
                    funct="8"
                
                rs = reg2bin(rs)
                rt =reg2bin(rt)
                rd =reg2bin(rd)
                rs=bin2bin(rs,5)
                rt = bin2bin(rt,5)
                rd=bin2bin(rd,5)
                shamt=bin2bin(shamt,5)
                funct=bin2bin(funct,6)
                

                return(opcode+rs+rt+rd+shamt+funct)

            
        #Error     
            elif opcode=="Not Supported Instruction, Please Read the USer Manual":
                return("Not Supported Instruction, Please Read the USer Manual") 

            #I format      
            else:
                if op=="Addi" or op=="Ori":
                    rt = assembly[pos:pos+3]
                    pos1 =assembly[pos+1:].find("$")+pos+1
                    rs = assembly[pos1:pos1+3]
                    bit_16 = assembly[pos1+5:]
                    
                elif op=="Lw" or op=="Sw":
                    rt = assembly[pos:pos+3]
                    pos1 = assembly.find("(")
                    rs=assembly[pos1+1:pos1+4]
                    bit_16=assembly[pos+4:pos1]
                    
                elif op=="Beq":
                    rs = assembly[pos:pos+3]
                    pos1 =assembly[pos+1:].find("$")+pos+1
                    rt = assembly[pos1:pos1+3]
                    label = assembly[pos1+5:]   
                    labelindex= labels.index(label)
                    labeladdress=labels[labelindex+1]
                    instructionadress=instructions.index(assembly)*4
                    bit_16=labeladdress-instructionadress
                    bit_16=bit_16/4
                    bit_16=int(bit_16-1)
                    bit_16=str(bit_16)
                    

                rs=reg2bin(rs)
                rt=reg2bin(rt)
                rs=bin2bin(rs,5)
                rt=bin2bin(rt,5)
                bit_16=bin2bin(bit_16,16)
                return(opcode+rs+rt+bit_16)


    
    f_write= open("Instmem.txt","w+") 



    #method 1

    #ins  


                
    #----------------------
    #mn awel hena


        

    #l7d hena 

    findlabel(ins) 
    print("your instructions in binary is :")
    for target_list in instructions:
        inst=ass2bin(target_list)
        print(inst)
        f_write.write(inst +"\n" )
    print("end of instructions..")
    


    f_write.close()

    time.sleep(2)
    print("wait for the simulator we are working on it")
    time.sleep(1)
    print("wait")
    time.sleep(1)
    print("wait")
    time.sleep(1)
    print("wait")
    time.sleep(1)
    print("donee ")
    time.sleep(1)
    print("la wait brdo")


    time.sleep(5)

    runmodelsim()

    time.sleep(15)
    print("simulation done (good job)")
    



# put the code in ins 

f_ins=open("inputassembly.txt", "r")



for lines in f_ins:
    h=lines[len(lines)-1:]
    if lines[len(lines)-1:]=="\n":
    
        ins.append(lines[:len(lines)-1])
    else:
        ins.append(lines)
f_ins.close()

running()




    

