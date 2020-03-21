from array import array
import os 
import time
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.ttk import Progressbar


#from PIL import ImageTk, Image


lines = ""
labels=[]
instructions=[]
ins=[]
array1 = []
array2=[]
############################

#gui





#############################

def minimize():
    window.iconify()





def runing():
    


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

    def num_name(arg): 
        switcher ={ 
            
            " 0":"$zero",
            " 1":"$at",
            " 2":"$v0", 
            " 3":"$v1", 
            " 4":"$a0",
            " 5":"$a1",
            " 6":"$a2",
            " 7":"$a3",
            " 8":"$t0",
            " 9":"$t1",
            "10":"$t2",
            "11":"$t3",
            "12":"$t4",
            "13": "$t5",
            "14":"$t6",
            "15":"$t7",
            "16":"$s0",
            "17":"$s1",
            "18":"$s2",
            "19":"$s3",
            "20":"$s4",
            "21":"$s5",
            "22":"$s6",
            "23":"$s7",
            "24":"$t8",
            "25":"$t9",
            "26":"$k0",
            "27":"$k1",
            "28":"$gp",
            "29":"$sp",
            "30":"$fp",
            "31":"$ra",

        } 
        return switcher.get(arg, "---")






    def ass2bin(assembly):
        
            
        pos = assembly.find("$")
        poss=assembly.find(" ")
        if pos == -1 and poss==1 :
            op = assembly[:poss]
            op=op.title()
            opcode=optobin(op)
            label = assembly[poss+1:poss+6]
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
    print("simulation done (good jop)")
    print("your date is :")

    f_reg=open("reg.txt", "r")
    
    for line in f_reg:
        array1.append(line)


    for i in range (len(array1)) :
        if i > 2 :
            ind=array1[i].find(":")
            reg_old=array1[i][:ind]
            reg_new=num_name(reg_old)
            array1[i]=array1[i].replace(reg_old,reg_new,1)
        

    for i in range (len(array1)) :
        if i> 2 :
            print(array1[i])

    #array1
    f_reg.close()
    
    f_data=open("data.txt", "r")
    
    for line in f_data:
        array2.append(line)


    
    
    f_data.close()



window = Tk()
regFileOut = tk.Text(window, width=40 , height=70)
regFileOut1 = tk.Text(window, width=40 , height=1)
regFileOut2 = tk.Text(window, width=40 , height=70)
label_2 = Label(window, text="the data : : ",
      bg="black",
      fg="white",
      font="none 12 bold",
      padx=340,pady=0)   




    

def click():
        string = str(AssemblyEntry.get("1.0",'end-1c'))
        lines = string.split("\n")
        for i in range(len(lines)):
            ins.append(lines[i])
        
        runing()     
        for i in range (len(array1)):
            if i> 2 :
                regFileOut.insert(tk.END, array1[i] + '\n')
        for i in range (len(array2)):
            if i> 2 :
                regFileOut2.insert(tk.END, array2[i] + '\n')     

        pc = len(ins)*4
        pcc =str(pc)        
        regFileOut1.insert(tk.END, pcc + '\n')     
        bt1.grid_forget()   
        AssemblyEntry.grid_forget() 
        label_1.grid_forget()
        label_2.grid(row=0,column=1)
        regFileOut.grid(row=1,column=0)
        regFileOut1.grid(row=3,column=0)
        regFileOut2.grid(row=1,column=1) 
#add $t1, $t2, $t3
        


window = Tk()







    
def bar(): 
    import time 
    progress['value'] = 20
    window.update_idletasks() 
    time.sleep(2) 
  
    progress['value'] = 30
    window.update_idletasks() 
    time.sleep(1) 
  
    progress['value'] = 50
    window.update_idletasks() 
    time.sleep(2) 
  
    progress['value'] = 60
    window.update_idletasks() 
    time.sleep(1) 
  
    progress['value'] = 80
    window.update_idletasks() 
    time.sleep(1) 
    progress['value'] = 100
    bt1.config(text="Success! Run Again?",fg="green")

    
def click():
        bar()
        string = str(AssemblyEntry.get("1.0",'end-1c'))
        lines = string.split("\n")
        for i in range(len(lines)):
            ins.append(lines[i])
        
        runing()     
        for i in range (len(array1)):
            if i> 2 :
                regFileOut.insert(tk.END, array1[i] + '\n')
        for i in range (len(array2)):
            if i> 2 :
                regFileOut2.insert(tk.END, array2[i] + '\n')     

        pc = len(ins)*4
        pcc =str(pc)        
        regFileOut1.insert(tk.END, pcc + '\n')
        
        
#add $t1, $t2, $t3


  
     

window.title("Group 7 Assembler")
window.attributes("-fullscreen", True)
window.configure(background="black",padx=450)



label_1 = Label(window, text="Please enter your assembly instructions here : ",
      bg="black",
      fg="white",
      font="none 16 bold"
      
      )

label_1.grid(row=0,column=5,sticky="ew",pady=15)





regFileOut = tk.Text(window, width=40 , height=7)
regFileOut1 = tk.Text(window, width=40 , height=7)
regFileOut2 = tk.Text(window, width=40 , height=7)   
AssemblyEntry = Text(window, width=60 , height=7)
AssemblyEntry.grid(row=1,column=5)
bt1=Button(window,text="Run",width=13,command=click,padx=15,pady=10)
bt1.place(x=60,y=230)
bt2=Button(window,text="Minimize window",width=15,command=minimize,padx=15,pady=10,fg="orange")
bt2.place(x=195,y=230)
bt3=Button(window, text="Quit", command=window.destroy ,padx=15,pady=10, width=5,fg="red")
bt3.place(x=345,y=230)
regFileOut.place(x=85,y=600)#reg
regFileOut1.place(x=85,y=450)#pc
regFileOut2.place(x=85,y=300)#memory

memory = Label(window, text="Data memory : ",
      bg="black",
      fg="white",
      font="none 16 bold"
      
      )

memory.place(x=-85,y=335)

PC = Label(window, text="PC : ",
      bg="black",
      fg="white",
      font="none 16 bold"
      
      )

PC.place(x=0,y=490)

regFile = Label(window, text="Register File : ",
      bg="black",
      fg="white",
      font="none 16 bold"
      
      )

regFile.place(x=-85,y=635)


# Progress bar widget 
progress = Progressbar(window, orient = HORIZONTAL, 
              length = 400, mode = 'determinate')   
progress.place(x=45,y=190)   
window.resizable(0,0)
window.mainloop()

