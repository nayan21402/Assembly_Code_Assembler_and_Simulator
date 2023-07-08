registers = {"000": 0, "001": 0, "010": 0, "011": 0,"100": 0, "101": 0, "110": 0, "111": '0000000000000000'}
variables = {}
pc = 0
def bitodec(num):
    sum = 0
    j = 7
    for i in range(len(num)):
        sum += int(num[i])*(2**j)
        j -= 1
    return sum

def binaryToDecimal(binary):
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal

def decimaltobinary(x):
    i = int(x)
    b = ""
    while(i >= 1):
        r = i % 2; i = i//2; b += str(r)
    b = b[::-1]
    y = ""
    while(len(y) < 16-len(b)):
        y += "0"
    return y+b

def print_registers(registers):
    count = 0
    print(decimaltobinary(pc),end=' ')
    for i in registers:
        
        print(decimaltobinary(registers[i]), end=' ')
        #print(registers[i],end=' ')
        count+=1
        if(count==len(registers)-1):
            break
        
    print(registers["111"])
    

def check_code(inst):
    global pc
    reset_flag=1
    if inst[0:5]=='10000':                           #addition 
        r2=registers[inst[10:13]]
        r3=registers[inst[13:]]
        r1=r2+r3
        if r1>255:
            temp=registers["111"]
            temp=list(temp)
            temp[-4]='1'
            temp=''.join(temp)
            registers["111"]=temp 
            registers[inst[10:13]]=r2                #sets others as the same
            registers[inst[13:16]]=r3
            registers[inst[7:10]]=255               #sets r1 to max value
            reset_flag=0
        else:
            registers[inst[10:13]]=r2
            registers[inst[13:16]]=r3
            registers[inst[7:10]]=r1

    elif inst[0:5]=="10001":                         #subtraction
        r2=registers[inst[10:13]]
        r3=registers[inst[13:]]
        r1=r2-r3

        if r1<0:
            temp=registers["111"]
            temp=list(temp)
            temp[-4]='1'
            temp=''.join(temp)
            registers["111"]=temp 
            registers[inst[10:13]]=r2                #sets others as the same
            registers[inst[13:16]]=r3
            registers[inst[7:10]]=0                  #sets r1 to max value
            reset_flag=0
        else:
            registers[inst[10:13]]=r2
            registers[inst[13:16]]=r3
            registers[inst[7:10]]=r1
    elif inst[0:5]=="10110":                         #multiply
        r2=registers[inst[10:13]]
        r3=registers[inst[13:]]
        r1=r2*r3

        if r1>255:
            temp=registers["111"]
            temp=list(temp)
            temp[-4]='1'
            temp=''.join(temp)
            registers["111"]=temp
            registers[inst[10:13]]=r2                #sets others as the same
            registers[inst[13:16]]=r3
            registers[inst[7:10]]=255                  #sets r1 to max value 
            reset_flag=0
        else:
            registers[inst[10:13]]=r2
            registers[inst[13:16]]=r3
            registers[inst[7:10]]=r1
            
    elif inst[0:5]=="11010":                         #xor
        r2=registers[inst[10:13]]
        r3=registers[inst[13:]]
        r1=r2^r3

        if r1<0:
            temp=registers["111"]
            temp=list(temp)
            temp[-4]='1'
            temp=''.join(temp)
            registers["111"]=temp 
            registers[inst[10:13]]=r2                #sets others as the same
            registers[inst[13:16]]=r3
            registers[inst[7:10]]=0                  #sets r1 to max value
            reset_flag=0            
        else:
            registers[inst[10:13]]=r2
            registers[inst[13:16]]=r3
            registers[inst[7:10]]=r1
    elif inst[0:5]=="11011":                         #or
        r2=registers[inst[10:13]]
        r3=registers[inst[13:]]
        r1=r2|r3
        if r1<0:
            temp=registers["111"]
            temp=list(temp)
            temp[-4]='1'
            temp=''.join(temp)
            registers["111"]=temp 
            registers[inst[10:13]]=r2                #sets others as the same
            registers[inst[13:16]]=r3
            registers[inst[7:10]]=0                  #sets r1 to max value
            reset_flag=0
        else:
            registers[inst[10:13]]=r2
            registers[inst[13:16]]=r3
            registers[inst[7:10]]=r1

    elif inst[0:5]=="11100":                         #and
        r2=registers[inst[10:13]]
        r3=registers[inst[13:]]
        r1=r2&r3

        if r1<0:
            temp=registers["111"]
            temp=list(temp)
            temp[-4]='1'
            temp=''.join(temp)
            registers["111"]=temp 
            registers[inst[10:13]]=r2                #sets others as the same
            registers[inst[13:16]]=r3
            registers[inst[7:10]]=0                  #sets r1 to max value
            reset_flag=0
        else:
            registers[inst[10:13]]=r2
            registers[inst[13:16]]=r3
            registers[inst[7:10]]=r1

    #TYPE B
    elif(inst[0:5]=="10010"): #type B mov
        registers[inst[5:8]]=bitodec(inst[8:])

    elif(inst[0:5]=="11001"): #ls
        registers[inst[5:8]]=registers[inst[5:8]]*(2**bitodec(inst[8:]))  

    elif(inst[0:5]=="11000"): #rs
        registers[inst[5:8]]=registers[inst[5:8]]//(2**bitodec(inst[8:]))  

    elif(inst[0:5]=="10011"): #mov immediate
        registers[inst[10:13]]=registers[inst[13:]]

    elif(inst[0:5]=="11101"): #invert
        registers[inst[13:]]=255-registers[inst[10:13]]
        
    elif(inst[0:5]=="10111"): #divide
        registers["000"]=registers[inst[10:13]]//registers[inst[13:]]
        registers["001"]=registers[inst[10:13]]%registers[inst[13:]] 

    elif(inst[0:5]=="11110"): #compare	
        if(registers[inst[10:13]]==registers[inst[13:]]):
            l=list(registers["111"])
            l[-1]='1'
            registers["111"]=''.join(l)
        elif(registers[inst[10:13]]>registers[inst[13:]]):
            l=list(registers["111"])
            l[-2]='1'
            registers["111"]=''.join(l)
        elif(registers[inst[10:13]]<registers[inst[13:]]):
            l=list(registers["111"])
            l[-3]='1'
            registers["111"]=''.join(l)  
        reset_flag=0
    
    elif(inst[0:5]=='10100'):					 #ld(load)					
        if inst[8:-1] not in variables:
            variables[inst[8:]]=0
        registers[inst[5:8]]=variables[inst[8:]]

    elif(inst[0:5]=='10101'): #st (store)
        if inst[8:-1] not in variables:
            variables[inst[8:]]=0
        variables[inst[8:]]=registers[inst[5:8]]

    elif(inst[0:5]=='01010'):  #hlt
        print_registers(registers)
        exit()

    elif(inst[0:5]=='11111'): #jmp (unconditional jump)
        pc=bitodec(inst[8:])-1

    elif(inst[0:5]=='01100'): #jlt (jump if less than)
        if(registers['111'][-3]=='1'):
            pc=bitodec(inst[8:])-1
        reset_flag=0

    elif(inst[0:5]=='01111'): #jgt (jump if greater than)
        if(registers['111'][-2]=='1'):
            pc=bitodec(inst[8:])-1
        reset_flag=0

    elif(inst[0:5]=='01111'): #je (jump if equal)
        if(registers['111'][-1]=='1'):
            pc=bitodec(inst[8:])-1
        reset_flag=0
    else:
        print(inst[0:5],"doesn't exist")
    if(reset_flag==1):
        registers['111']='0000000000000000'
    print_registers(registers)

inst = open("inputS.txt").read().split('\n')

while(1):
    check_code(inst[pc])
    pc+=1

