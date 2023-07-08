import sys
global var_list, label_list
global instruction_dict, dict_A, dict_B, dict_C, dict_D, dict_E, dict_F, register
global read
global variable_count
global empty_line_count
global last_empty_line_count
empty_line_count = 0
variable_count = 0
last_empty_line_count = 0
var_list = {}
label_list = {}
instruction_dict = {"addf": "00000", "subf": "00001", "movf": "00010", "add": "10000", "sub": "10001", "mov": "10011", "ld": "10100", "st": "10101", "mul": "10110", "div": "10111",
    "rs": "11000", "ls": "11001", "xor": "11010", "or": "11011", "and": "11100", "not": "11101", "cmp": "11110", "jmp": "11111", "jlt": "01100", "jgt": "01101", "je": "01111", "hlt": "01010"}
register = {"R0": "000", "R1": "001", "R2": "010", "R3": "011",
    "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}
dict_A = {"F_Addition": "00000", "F_Subtraction": "00001", "add": "10000",
    "sub": "10001", "mul": "10110", "xor": "11010", "or": "11011", "and": "11100"}
dict_B = {"movf": "00010", "mov": "10010", "ls": "11001", "rs": "11000"}
dict_C = {"mov": "10011", "div": "10111", "cmp": "11110", "not": "11101"}
dict_D = {"ld": "10100", "st": "10101"}
dict_E = {"jmp": "11111", "jlt": "01100", "jgt": "01101", "je": "01111"}
dict_F = {"hlt": "01010"}


def last_count():
    global last_empty_line_count
    for i in range(len(read)):
        if read[-(i+1)] == '':
            pass
        else:
            break
    last_empty_line_count = i


def dectobi(x):
    i = int(x)
    b = ""
    while(i >= 1):
        r = i % 2
        i = i//2; b += str(r)
    b = b[::-1]
    y = ""
    while(len(y) < 8-len(b)):
        y += "0"
    return y+b


def variables():
    global variable_count
    global empty_line_count
    global read, read2
    var_at_start = 1
    for i in range(len(read)):
        words = read[i].split()
        if (len(words)) > 0:
            if words[0] == 'var':
                if(var_at_start):
                    if len(words) != 2:
                            print("Error at line ", i+1,
                                  " : variable definition incorrect ")
                            exit()
                    if str(words[1][0]).isnumeric() == False and (words[1] in instruction_dict) == False and (words[1] in register) == False and (words[1] in label_list) == False:
                        if len(words) != 2:
                            print("Error at line ", i+1,
                                  " : variable definition incorrect ")
                            exit()
                        else:
                            if(words[1] in register or words[1] == 'FLAGS'):
                                print("Error at line ", i+1,
                                      " : invalid variable name")
                                exit()
                            if(words[1] in var_list):
                                print(
                                    "ERROR at line ", i+1, " : Multiple declarations of variables ", words[1])
                                exit()
                            var_list[words[1]] = -1
                            variable_count += 1
                    else:
                        print("Error at line ", i+1,
                              " : invalid variable declaration ")
                        exit()
                else:
                    print("Error at line ", i+1,
                          " : invalid variable declaration ")
                    exit()
            else:
                var_at_start = 0
        elif len(words) == 0:
            empty_line_count += 1
        count = 0
    if(variable_count):
        for i in var_list:
            var_list[i] = dectobi(len(read2)-variable_count+count)
            count += 1


def labels():
    global read, read2
    for i in range(len(read)):
        if len(read[i]) > 0:
            words = read[i].split()
            first_word = words[0]  # splitting first word into letters

            if(first_word[-1] == ':' and len(first_word) == 1):
                print("ERROR at line ", i+1,
                      " : invalid label definition (label name cant be null)")
                exit()
            elif (first_word[-1] == ':') and ((first_word[0:-1] in instruction_dict) or (first_word[0:-1] in register)):
                print("ERROR at line ", i+1, " : keyword used as label")
                exit()
            elif(first_word[-1] == ':' and first_word[-2] == ':'):
                print("ERROR at line ", i+1,
                      " : invalid label definition(label name cant be ':')")
                exit()
            elif(''.join(first_word[0:-1:]) in register or ''.join(first_word[0:-1:]) == 'FLAGS'):
                print("ERROR at line ", i+1, " : Invalid label name")
                exit()
            elif(words[0][0:-1] in label_list):
                print("ERROR at line ", i+1, " : label must be unique")
                exit()
            elif(len(words) == 1 and first_word[-1] == ':'):
                print("ERROR at line ", i+1, " : label statement empty")
                exit()
            elif(first_word[-1] == ':' and 'var' in words):
                print("ERROR at line ", i+1, " : General Syntax Error")
                exit()
            elif(first_word[-1] == ':'):
                if str(first_word[0]).isnumeric() == False:
                    label_list[words[0][:-1:]] = -1
                    read[i] = ' '.join(words[1::])
    for i in range(len(read2)):
        if(len(read2[i]) > 0):
            words = read2[i].split()
            first_word = words[0]
            if(first_word[-1] == ':'):
                label_list[words[0][:-1:]] = dectobi(i-variable_count)
                read2[i] = ' '.join(words[1::])


def float_bin(number, places=5):
    whole, dec = str(number).split(".")
    if int(dec) == 0:

        b = bin(int(whole)).lstrip("0b")
        b = str(b)
        exp = bin(len(b[1::])).lstrip("0b")
        if len(exp) != 3:
            for i in range(0, (3-len(exp))):
                exp = '0'+exp
        mantissa = b[1::]

        if len(mantissa) != 5:
            for l in range(0, (5-len(mantissa))):
                mantissa = mantissa+'0'

        if len(mantissa) == 5:
            return exp+mantissa
        else:
            return '11111111'

    whole, dec = str(number).split(".")
    whole = int(whole)
    dec = int(dec)
    res = bin(whole).lstrip("0b") + '.'

    for x in range(places):
        if dec == 0:
            break
        whole, dec = str((decimal_converter(dec)) * 2).split(".")
        dec = int(dec)
        res += whole
    r = res.split('.')[0]+res.split('.')[1]
    for_exp = res.split('.')[0]
    exp = bin(len(for_exp)-1).lstrip("0b")

    if len(exp) != 3:
            for i in range(0, (3-len(exp))):
                exp = '0'+exp

    mantissa = r[1::]
    if len(mantissa) != 5:
        for l in range(0, (5-len(mantissa))):
            mantissa = mantissa+'0'

    if len(mantissa) == 5:
        return exp+mantissa
           #return "00000000"+exp+mantissa
    else:
        return '11111111'


def decimal_converter(num):
    while num > 1:
        num /= 10
    return num


def float_bin1(number, places=5):
    whole, dec = str(number).split(".")
    if int(dec) == 0:

        b = bin(int(whole)).lstrip("0b")
        b = str(b)
        exp = bin(len(b[1::])).lstrip("0b")
        if len(exp) != 3:
            for i in range(0, (3-len(exp))):
                exp = '0'+exp
        mantissa = b[1::]

        if len(mantissa) != 5:
            for l in range(0, (5-len(mantissa))):
                mantissa = mantissa+'0'

        if len(mantissa) == 5:
            return 1
        else:
            return 0

    whole, dec = str(number).split(".")
    whole = int(whole)
    dec = int(dec)
    res = bin(whole).lstrip("0b") + '.'

    for x in range(places):
        if dec == 0:
            break
        whole, dec = str((decimal_converter(dec)) * 2).split(".")
        dec = int(dec)
        res += whole
    r = res.split('.')[0]+res.split('.')[1]
    for_exp = res.split('.')[0]
    exp = bin(len(for_exp)-1).lstrip("0b")

    if len(exp) != 3:
            for i in range(0, (3-len(exp))):
                exp = '0'+exp

    mantissa = r[1::]
    if len(mantissa) != 5:
        for l in range(0, (5-len(mantissa))):
            mantissa = mantissa+'0'

    if len(mantissa) == 5:
        return 1
           #return "00000000"+exp+mantissa
    else:
        return 0


def check_typeA(words, i):
    regs = list(register.keys())
    if len(words) != 4:
        print("ERROR at line ", i+1, " : invalid syntax")
        exit()
    elif 'FLAGS' in words:
        print("ERROR at line ", i+1, " : invalid usage of FLAGS register")
        exit()
    else:
        if ((words[1] not in regs) or (words[2] not in regs) or (words[3] not in regs)):
            print("ERROR at line ", i+1, ": invalid register")
            exit()


def check_typeB(words, i):
    regs = list(register.keys())
    if len(words) != 3:
        print("ERROR at line ", i+1, " : invalid syntax")
        exit()
    elif 'FLAGS' in words:
        print("ERROR at line ", i+1, " : invalid usage of FLAGS register")
        exit()
    else:
        if (words[1] not in regs):
            print("ERROR at line ", i+1, " : invalid register")
            exit()


def check_typeC(words, i):
    #print(words[0])
    if(len(words) != 3):
        print("SYNTAX ERROR")
        exit()
    else:
        if words[0] == 'mov':

            if(words[1] not in register):
                print("ERROR at line ", i+1, " : invalid use of FLAGS register")
                exit()
            elif(words[2] == 'FLAGS'):
                print("ERROR at line ", i+1, " : Inavlid use of FLAGS register")
                exit()
            elif(words[2] not in register and words[2] != 'FLAGS'):
                print("Error at line ", i+1, " : SYNTAX ERROR")
                exit()

        else:
            if ('FLAGS' in [words[1], words[2]]):
                print("ERROR at line ", i+1, " : Invalid use of FLAGS register")
                exit()
            if (words[1] and words[2] not in register):
                print("Error at line ", i+1, " : SYNTAX ERROR")
                exit()


def check_typeD(words, i):
    if(len(words) != 3):
        print("Error at line ", i+1, " : SYNTAX ERROR*")
        exit()
    else:
        if(words[1] not in register):
            print("ERROR at line ", i+1, " : not a valid register")
            exit()
        elif(words[1] == 'FLAGS'):
            print("ERROR at line ", i+1, " : Inavlid use of FLAGS register")
            exit()
        if(words[2] in label_list):
            print("ERROR at line ", i+1, " : Misuse of variable as label")
            exit()
        elif(words[2] not in var_list):
            print("ERROR at line ", i+1, " : Variable " +
                  "'" + words[2]+"'"+" is not defined")
            exit()


def check_typeE(str, j):
    if(len(str) == 2):
        for i in range(len(str)):
               if str[1] in label_list:
                    return
               elif str[1] in var_list:
                    print("ERROR at line ",j+1," : Misuse of variable as label")
                    exit(0)  
               else:
                    print("ERROR at line ",j+1," : Label is undefined")
                    exit(0)  
    else:
        print("Error at line ",j+1," : invalid instruction")
        exit(0)


def counter():
    global read, read2
    counter = 0
    for i in range(len(read)):
        if read[i] =="hlt":
            counter += 1
        if(counter >1):
            print("ERROR at line: ",i+1,"multiple hlt declarations")
            exit()


def instructions():
    global read, read2
    if(read2[-1]) != 'hlt':
        print("ERROR: hlt absent")
        exit()
    main = list(instruction_dict.keys())
    for i in range(len(read)):
        words = read[i].split()
        if(len(read[i])) >0:
            if  (words[0] =='var' or (words[0] in main)):
                if (words[0] in list(dict_A.keys())):
                    check_typeA(words, i)
                elif (words[0] in list(dict_B.keys()) and words[-1][0] =='$'):   #<= 255 and >= 0
                       if ('.' in words[-1]):
                            if(float_bin1(words[-1][1::],5) ==0):
                                print("ERROR at line ",i+1 ," : Illegal immediate value")
                                exit()
                       elif(0 >int(words[-1][1::]) or int(words[-1][1::])>255):
                            print("ERROR at line ",i+1 ," : Illegal immediate value")
                            exit()
                       else:
                            check_typeB(words, i)
                elif (words[0] in list(dict_C.keys())):
                    check_typeC(words, i)
                elif (words[0] in list(dict_D.keys())):
                    check_typeD(words, i)

                elif (words[0] in list(dict_E.keys())):
                    check_typeE(words, i)
            else:
                print("ERROR at line ",i+1," : invalid instruction ")
                exit()


def machine_code(read):
    for i in range(len(read)):
        if(len(read[i]) >0):
            inst = read[i].split()
            if(inst[0] not in label_list):
                if(inst[0] in dict_A.keys()):
                    print(dict_A[inst[0]]+"00"+register[inst[1]]+ \
                          register[inst[2]]+register[inst[3]])
                elif (inst[0] in dict_B.keys() and inst[-1][0] =='$' and '.' in inst[-1]):
                    print(dict_B[inst[0]]+register[inst[1]]+ \
                          float_bin(inst[2][1::]))
                elif(inst[0] in dict_B.keys() and inst[-1][0] =='$'):
                       print(dict_B[inst[0]]+register[inst[1]]+dectobi(inst[2][1::]))
                elif(inst[0] in dict_C.keys()):
                    print(dict_C[inst[0]]+"00000"+register[inst[1]]+register[inst[2]])
                elif(inst[0] in dict_D.keys()):
                    print(dict_D[inst[0]]+register[inst[1]]+var_list[inst[2]])
                elif(inst[0] in dict_E.keys()):
                    print(dict_E[inst[0]]+"000"+label_list[inst[1]])
                elif(inst[0] in dict_F.keys()):
                    print(dict_F[inst[0]]+"00000000000")
                    exit()

#read = sys.stdin.read().split("\n")
read=open("inputA.txt").read().split("\n")
read = [w.strip() for w in read]
read2 = [w for w in read if w !='']           
last_count()
#print(last_empty_line_count)
if(len(read)-last_empty_line_count >256):
    print("ERROR: Instructions must be less than 256")
    exit()
variables()
labels()
counter()
instructions()
machine_code(read)
