import pandas as pd
import numpy as np
import ipywidgets as widgets
from IPython.display import display

def end_strip(list): ## removes the tail of empty registers
  if list == []:
    return(list)
  elif list[-1] == '':
    return(end_strip(list[:-1]))
  else:
    return(list)

def remove_multiple_blanks(my_str):
   return(my_str.replace(" ", ""))


class prog_two_registers_input():
    def __init__(self, 
                 program = "", 
                 rone = "", 
                 rtwo = ""
                ):
        self.program = widgets.Text(description = 'program',value = program)
        self.rone = widgets.Text(description = 'R1',value = rone)
        self.rtwo = widgets.Text(description = 'R2',value = rtwo)        
        self.program.on_submit(self.handle_submit)
        self.rone.on_submit(self.handle_submit)
        self.rtwo.on_submit(self.handle_submit)
        display(self.program, self.rone, self.rtwo)

    def handle_submit(self, text):
        self.v = text.value
        return self.v





def program_checker(str):
    m = len(str)
    x1 = str[m - 1] == '#'
    x2 = all((str[i] == '1' or str[i] == '#') for i in range(m))
    x3 = (str.find('######') == -1)
    if (x1 and x2 and x3):
        flag = True
    else:
        flag = False
        print('The input ' + str + ' is not a valid 1# program.')
        print('It is not the concatenation of a sequence of instructions in the language.')
        print('So what you are asking for is undefined.')
    return (flag)

def one_or_sharp_check(letter):
    if (letter=="1" or letter=="#"):
        return(True)
    else:
        return(False)

def word_checker(strg):
    answer = all([one_or_sharp_check(x)==True for x in strg])
    return(answer)

def input_checker(input_seq):
    seq = [word_checker(x) for x in input_seq]
    flag = all([word_checker(x) for x in input_seq])
    if not flag:
        print('The input sequence contains words with characters other than 1 and #.')
        print('So what you are asking for is undefined.')
    return(flag)
                                                                                
class Augmented:
    def __init__(self, string, remainders):
        self.string = string
        self.remainders = remainders

class Snapshot:
    def __init__(self, instr_number, regs, proceed,verbose,program_length, step_number):
        self.instr_number = instr_number
        self.regs = regs
        self.proceed = proceed
        self.verbose = verbose
        self.program_length = program_length
        self.step_number = step_number
        
def preparse(xstr):
    b = xstr.string.find('#1')
    xstr.remainders = xstr.remainders + [xstr.string[:(b + 1)]]
    xstr.string = xstr.string[(b + 1):]
    return (xstr)



def parse(y):
    tempx = Augmented(y, [])
    while tempx.string.find('#1') >= 0:
        tempx = preparse(tempx)
    return (tempx.remainders + [tempx.string])

def unparse(p):
    return (''.join(p))

def instruction_type(instruction):
    if instruction[-2:] == '1#':
        return ('add1')
    if instruction[-3:] == '1##':
        return ('add#')
    if instruction[-4:] == '1###':
        return ('forward')
    if instruction[-5:] == '1####':
        return ('backward')
    if instruction[-6:] == '1#####':
        return ('cases')

def tail(list):
    return (list[1:])

def one_step(p, snapshot): # p is parsed
    i = snapshot.instr_number
    r = snapshot.regs
    instruction = p[-1 + i]
    if snapshot.verbose:
        print('Step ' + str(snapshot.step_number) + ':')
        print('Execute instruction ' + str(i) + ':' + " " +
              instruction_gloss(instruction,i-1) 
              + '.')
        if instruction_type(instruction)=='cases':
            billy= len(instruction) - 5
            if snapshot.regs[billy-1] == "":
                print('The register is empty, so we go ahead 1 instruction.')
            elif snapshot.regs[billy-1][0] == "1":
                print('The first symbol in that register is 1,' +
                      ' so we delete that symbol and go forward 2 instructions.')
            elif snapshot.regs[billy-1][0] == "#":
                print('The first symbol in that register is #,' +
                      ' so we delete that symbol and go forward 3 instructions.')     
    t = instruction_type(instruction)
    if t == 'add1':
        snapshot.instr_number = 1 + snapshot.instr_number
        l = len(instruction)
        reg = len(instruction[:(l - 1)])
        snapshot.regs[reg - 1] = snapshot.regs[reg - 1] + '1'
    if t == 'add#':
        snapshot.instr_number = 1 + snapshot.instr_number
        l = len(instruction)
        reg = len(instruction[:(l - 2)])
        snapshot.regs[reg - 1] = snapshot.regs[reg - 1] + '#'
    if t == 'forward':
        l = len(instruction)
        offset = len(instruction[:(l - 3)])
        snapshot.instr_number = offset + snapshot.instr_number
    if t == 'backward':
        l = len(instruction)
        offset = len(instruction[:(l - 4)])
        snapshot.instr_number = (-offset) + snapshot.instr_number
    if t == 'cases':
        l = len(instruction)
        reg = len(instruction[:(l - 5)])
        if snapshot.regs[reg - 1] == '':
            snapshot.instr_number = 1 + snapshot.instr_number
        elif snapshot.regs[reg - 1][0] == '1':
            snapshot.instr_number = 2 + snapshot.instr_number
            snapshot.regs[reg - 1] = tail(snapshot.regs[reg - 1])
        elif snapshot.regs[reg - 1][0] == '#':
            snapshot.instr_number = 3 + snapshot.instr_number
            snapshot.regs[reg - 1] = tail(snapshot.regs[reg - 1])
    if 0< snapshot.instr_number <= len(p):
        snapshot.proceed = True
        if snapshot.verbose == True:
            print_snapshot(snapshot)
    else:
         snapshot.proceed = False
    return (snapshot)


def number_help(instr):
    if instruction_type(instr) == 'add1':
        return (len(instr) - 1)
    if instruction_type(instr) == 'add#':
        return (len(instr) - 2)
    if instruction_type(instr) == 'cases':
        return (len(instr)-5)
    else:
        return (0)


def max_register(p):
    return (max([number_help(instr) for instr in parse(p)]))


def pad(p, register_inputs):
    n = len(register_inputs)
    m = max_register(p)
    extras = ['' for x in range(m - n)]
    bigger = register_inputs + extras
    return (bigger)

display_formal_snapshot = False

def step_by_step_with_snapshots(word_prog, register_inputs):
    display_formal_snapshot = True
    step_by_step(word_prog,register_inputs)

def addones(word): ### needed to get out the formal snapshots: see print_snapshot below
  if word == '':
    return(word)
  else:
    x = word[0]
    y = '1'+ x
    z = word[1:]
    p = addones(z)
    return(y + p)

def word_representation(snapshot): ### needed to get out the formal snapshots: see print_snapshot below
    i = snapshot.instr_number
    r = snapshot.regs
    registers = len(r)
    a = ones(i)
    b = [addones(snapshot.regs[i]) + '##' for i in range(registers)]
    c = "".join(b)
    return(a+ '##' + c)

def print_snapshot(snap):
    regdf = pd.DataFrame([[snap.regs[n]] for n in range(len(snap.regs))],columns=["contents"])
    regdf.index = np.arange(1, len(regdf) + 1)
    def make_pretty(styler):
        styler.set_properties(**{'background-color': '#FFFFCC'})
        styler.set_properties(**{'text-align': 'left'})
        #styler.set_caption("at the start")
        #styler.hide(axis='index')
        return styler
    display(regdf.style.pipe(make_pretty))  
    if display_formal_snapshot == True:
        print()
        print('The formal snapshot here as we represent it is ' + word_representation(snap))
        
def step_by_step(word_prog, register_inputs):
    word_prog = word_prog.replace(" ", "")
    register_inputs = [word.replace(" ", "") for word in register_inputs]
    if program_checker(word_prog) and input_checker(register_inputs):
        print('First, here is the program:')
        parse_explain(word_prog)
        print()
        regs = pad(word_prog, register_inputs)
        prog = parse(word_prog)
        N = len(prog)
        snap = Snapshot(1, regs,True,True,N,1)
        print('The computation starts with the register contents shown below.')
        print('The registers include those those which you entered as part of the input')
        print('and also others mentioned in the input program.')
        print_snapshot(snap)
        print()
        while 0 < snap.instr_number < N + 1:
            snap = one_step(prog, snap)
            snap.step_number = (snap.step_number) + 1
        if snap.instr_number <= 0:
            print(
                'The computation has not halted properly ' +
                'because the control went above instruction 1 of the program.'
                 )
        elif (snap.instr_number == (N + 1)) and all(
                snap.regs[i] == ""
                for i in range(1, len(snap.regs))):
            print(
                'The computation then halts properly because' +
                ' the control is just below the last line of the program,')
            print('and because all registers other than R1 are empty.')
            if snap.regs[0] == "":
                print('The output is the empty word.')
            else:
                print('The output is ' + snap.regs[0] + '.')
        else:
            print('This computation does not halt.')
            if snap.instr_number != N + 1:
                print('This is because the program has ' + str(len(prog)) +
                  ' instructions, and control at the end is not one line ' + 
                   'below the bottom of the program.')
                print()
            else:
                not_blank = [
                    i + 1 for i in range(1, len(snap.regs))
                    if snap.regs[i] != ""
                ]
                print('Here is the list of registers whose contents ' +
                      'are not empty at this point, other than R1:' +
                      str(not_blank) + '.')
                print('The register contents at the end are shown above.')


def onesharp(word_prog, register_inputs):
    word_prog = word_prog.replace(" ", "")
    register_inputs = [word.replace(" ", "") for word in register_inputs]  
    if program_checker(word_prog) and input_checker(register_inputs):
        register_inputs = [word.replace(" ", "") for word in register_inputs]
        regs = pad(word_prog, register_inputs)
        prog = parse(word_prog)
        N = len(prog)
        snap = Snapshot(1, regs,True,False, N, 1)
        while snap.proceed:
            snap = one_step(prog, snap)
            snap.step_number = (snap.step_number)+1
        if (snap.instr_number == (N + 1)) and all(
                snap.regs[i] == "" for i in range(1, len(snap.regs))):
            return ((snap.regs)[0])
        else:            
            print("This is undefined.")
            print("The register contents at the end are shown below.")
            print_snapshot(snap)
    else:
        return('undefined')


def instruction_gloss(instr,line):
    if instruction_type(instr) == 'add1':
        return ('add 1 to R' + str(len(instr) - 1))
    if instruction_type(instr) == 'add#':
        return ('add # to R' + str(len(instr) - 2))
    if instruction_type(instr) == 'forward':
        w = len(instr) - 3
        return ('go forward ' + str(w) + ' to instruction ' + str(w+line+1))
    if instruction_type(instr) == 'backward':
        w = len(instr) - 4
        return ('go backward ' + str(w) + ' to instruction ' + str(line - w+1))
    if instruction_type(instr) == 'cases':
        return ('cases on R' + str(len(instr) - 5))

def expanded(gorp):
    pgorp = parse(gorp)
    wwgorp = [[pgorp[x],instruction_gloss(pgorp[x],x)] for x in range(len(pgorp))]
    return(wwgorp)

def parse_explain(prog):
    df = pd.DataFrame(expanded(prog),
                      columns=["instruction", 'explanation'])
    df.index = np.arange(1, len(df) + 1)
    def make_pretty(styler):
                styler.set_properties(**{'background-color': '#C9DFEC'})        
                styler.set_properties(**{'text-align': 'left'})
                return styler
    display(df.style.pipe(make_pretty))
    #display(df)

def clear(n):
   a = ones(n) + '#####'
   b = '111###'
   c = '1###'
   d = '111####'
   return(a+b+c+d)

def move(src, dst):
  p = ones(src)+'#####' # Cases on register ``src''
  p += '11111 1###'     # Go forward six
  p += '111###'         # Go forward three
  p += ones(dst)+'##'   # Append ``#'' to register ``dst''
  p += '1111####'       # Go backward four
  p += ones(dst)+'#'    # Append ``1'' to register ``dst''
  p += '11111 1####'    # Go backward six
  return p
   
def copy(n,m,p):
   a = ones(n) + '#####'
   b = '11111111###'
   c = '1111###'
   d = ones(m)+'##'
   d1 = ones(p) + '##'
   e = '11111####'
   f = ones(m)+'#'
   f1 = ones(p) + '#'
   g = '11111111####'
   return(a+b+c+d+d1+e+f+f1+g+move(p,n)) 

def findme(pair,pair_list): 
  x = [i for i in range(len(pair_list)) if pair_list[i][0]==pair[1]]
  return x[0]

def add_placeholder(line):
  keywords = ['cases','add1','add#','goto','non_label']
  if line[0] in keywords:
    return(['non_label']+line)
  elif line[0][0] in ['1','#']:
    return(['non_label']+line)  
  else:
    return(line)

def flatten(tuple):
  b = len(tuple)
  if b > 1 and tuple[1] == "cases":
    n = tuple[2]
    x = ones(n)+'#####'
    return [[tuple[0],x], [tuple[0]+'@1',tuple[3]], [tuple[0]+'@2',tuple[4]], [tuple[0]+'@3',tuple[5]]]
  elif b > 1 and tuple[1]=='add1':
    return([[tuple[0],ones(tuple[2])+'#']])
  elif b > 1 and tuple[1]=='add#':
    return([[tuple[0],ones(tuple[2])+'##']])
  elif b > 1 and tuple[1]=='goto':
    return [[tuple[0],tuple[2]]]
  elif tuple[1][0] in ['1', '#']:
    k = parse(tuple[1])
    m = len(k)
    return([[tuple[0],k[j]] for j in range(m)])


def ones(n):
  return(unparse(['1' for i in range(n)])) 

def resolve(index,pair_list):
  pair_in_list = pair_list[index]
  #print("pair_in_list " + str(pair_in_list))
  first_char = pair_in_list[1][0]
  #print(first_char)
  if first_char == '1' or first_char == '#':
    return pair_in_list[1]
  elif pair_in_list[1]=='end':
    n = len(pair_list) - index
    return(ones(n)+'###')
  else:
    k = findme(pair_in_list,pair_list)
    if k > index:
      return(ones(k-index)+'###')
    if k < index:
      return(ones(index-k)+'####')


def sanity(line_list):
  w = [add_placeholder(line) for line in line_list]
  #print("[add_placeholder(line) for line in line_list] is")
  #print(w)
  s1 = [flatten(line) for line in w]
  #print('[flatten(line) for line in w] is')
  #print(s1)
  t1 = [item for sublist in s1 for item in sublist]
  #print('[item for sublist in s1 for item in sublist] is')
  #print(t1)
  n = len(t1)
  #print('len of t1 = ' + str(n))
  u1 = [resolve(i,t1) for i in range(n)] 
  return(unparse(u1))

def list_multiply(x):
    if x == []: 
        return(identity_3) # the empty product should be the 3x3 identity
    else:
        a = x[0] # this gives the head of the input list
        b = list_multiply(x[1:]) # this multiplies the tail of the input
        return np.dot(a,b)

zero_3 = [[0,0,0],[0,0,0],[0,0,0]]
identity_3 = [[1,0,0],[0,1,0],[0,0,1]]



length = '1#####1111111###11####11#1#####111###111111####111####11#####111111###111###1##1111####1#111111####'

write = '1#####111111111###11111###11#11##11##111111####11#11##111111111####11#####111111###111###1##1111####1#111111####'

diag = '1#####11111111111###111111###11##111#111##111##1111111####11#111#111##1111####111#####111111###111###1##1111####1#11####11#####111111###111###1##1111####1#11####'

self = '1#1##1##1##1##1##1#1#1#1#1#1#1#1#1#1#1#1##1##1##1#1#1#1#1#1#1##1##1##1#1#1##1##1#1#1#1##1#1#1#1##1##1#1#1#1##1##1#1#1#1#1#1#1#1##1##1##1##1#1#1##1#1#1#1##1#1#1#1##1##1#1#1#1#1##1##1##1##1#1#1#1##1##1##1##1##1#1#1#1#1#1#1##1##1##1#1#1#1##1##1##1#1##1##1#1#1#1#1##1##1##1##1#1##1#1#1##1##1##1##1#1#1##1##1##1##1##1#1#1#1#1#1#1##1##1##1#1#1#1##1##1##1#1##1##1#1#1#1#1##1##1##1##1#1##1#1#1##1##1##1##1#####11111111111###111111###11##111#111##111##1111111####11#111#111##1111####111#####111111###111###1##1111####1#11####11#####111111###111###1##1111####1#11####'

multiply = '111##1111##11#####11111111###1111###11111##111111##11111####11111#111111#11111111####111111#####111111###111###11##1111####11#111111####111#####11111111###1111###111111##1111111##11111####111111#1111111#11111111####1111111#####111111###111###111##1111####111#111111####11111#####111111###111111111###111111#####11111111111###1111111111###111111####111111#####111111111111111###111111###11111###111111#####111###1111111111111####1###11111#####1  11###11####111####111111#####1111###11####111####11111#11111#####111###1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111###1#1#####11111111###1111###11111##111111##11111####11111#111111#11111111####111111#####111111###111###1##1111####1#111111####1111#####111111###111###111111##1111####111111#111111####11111#####111###111111###111111111###111111#####11111111111111111111111111111111111###11111111111111111111111111###111111111111111111111111111###111111#####11111111111111111111111###1111111111111111111111111111###111111111111111111111###111111#####111111111111111111111###111111111111111111###1111111111111111111###11111#####111###111111###111111111###111111#####11111111111###1111111111111111###111111111###111111#####1111111111111###1111111111###11111111111###111111#####111###11111111###1###1111111#111111111111111111111111111111111####1111111##11111111111111111111111111111111111####1111111#111111111111111111111####1111111##11111111111111111111111####1###1111111#####111111###111###11111##1111####11111#111111####11111#####111111###111###1111##1111####1111#111111####111#####1111111111111###1111111111###11111#111#####111111###111###11111##1111####11111#111111####1111###11111##1111111111111####11111#11111#####111111###111###111##1111####111#111111####1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111####1#####111###11####111####11#####111###11####111####111#####111###11####111####1111#####111111###111###1##1111####1#111111####'

universal = '1#####1###11###11####111111#1#####111###111111###1111111###11111#####1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111###1###1####111#111111111####111##1#####1111###11###11111###111#11111#####1111111111111111111111111111111111111111111111###111111111###111##1#####1111###11###11111###111#11111#####1111111111111111111111111111111111111###111111111###111##1#####1111###11###11111###111#11111#####1111111111111111111111111111111111111111111111###111111111###111##1#####1111###11###11111###111#11111#####111111111111111111111111111111111111111111111111111111###111111111###111##1#####1111###11###11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111###111#11111#####1111111111###1###111#####111111###111###1111##1111####1111#111111####11111111111111111111111111111111111111111111111111111111111111####111#####1###11###1111###11111#1111#111111####11111##1111##111#####1111111###1111###1111##11111##11111####1111#1111111####111111111111111111111111111111111111111111111111111111111111111111111111111###111#####1###11###11111###11111#1111#111111#1111111####1111##111#####111111###111###1111##1111####1111#111111####11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111####111#####1###11###1111###1111#11111#111111####11111#11111#1111##111#####111111###111###1111##1111####1111#111111####11111#####11111111###11###1###111111#####111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111###1###1###11111111####111111#####1111###111#11111#1111####111#####111###111111#111####1#####111111###111###111##1111####111#111111####1111#####111111###111###1##1111####1#111111####111#####111111###111###1##1111####1#111111####111111111111111111111111111111111111111111111111111111111####11#####111###11111###111111111111###11##11##111111####111#11#####1###111###111##11###111#11111111111111####111##11#####11111111111111111111111111111111111111111111111111111111111111111111###1###111##11111#####1###1111111111111111111111####11111#####1111111111111111111111111111###111111111111111111111111111###11111#####111###11###111111111111111111111111111111111111111111111###11#####111111111111111111###111111111###111#11#####1###1###111#111##111##111111111111111111111111111111111111111111111111111111111###111#11#####1###111###111##11###111#111111111111111111####111#111#1111111111111111111111111111111111111111111111###11#####111111111111111111###111111111###111#11#####1###1###111##111##111##11111111111111111111111111111111111###111#11#####1###111###111##11###111#111111111111111111####111#111##111111111111111111111111###11111#####1###1###11111#####1###1###11#####11111111111111111111111###111###111##1111111111111###11#####1###11111###1###11111#111111#111111###11111#11111#111111#111111#1###11#####111111###111###111##1111####111#111111####111#####111111###111###11##1111####11#111111####1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111####11#####1###1###11#####1###1###11#####11111111111111###11###11111111###11#####1###111###1#11111111####1##1111111111####11#####111###11####111####111111#####11###11####1111#####111###11####111####'
clear_1 = '1#####111###11####111####'
clear_2 = '11#####111###11####111####'
clear_3 = '111#####111###11####111####'
clear_4 = '1111#####111###11####111####'
move_1_2= '1#####111111###111###11##1111####11#111111####'
move_1_3= '1#####111111###111###111##1111####111#111111####'
move_1_4= '1#####111111###111###1111##1111####1111#111111####'
move_2_1= '11#####111111###111###1##1111####1#111111####'
move_2_3= '11#####111111###111###111##1111####111#111111####'
move_2_4= '11#####111111###111###1111##1111####1111#111111####'
move_3_1= '111#####111111###111###1##1111####1#111111####'
move_3_2= '111#####111111###111###11##1111####11#111111####'
move_3_4= '111#####111111###111###1111##1111####1111#111111####'
move_4_1= '1111#####111111###111###1##1111####1#111111####'
move_4_2= '1111#####111111###111###11##1111####11#111111####'
move_4_3= '1111#####111111###111###111##1111####111#111111####'
copy_1_2_3 = '1#####11111111###1111###11##111##11111####11#111#11111111####111#####111111###111###1##1111####1#111111####'
copy_1_2_4 ='1#####11111111###1111###11##1111##11111####11#1111#11111111####1111#####111111###111###1##1111####1#111111####'
copy_1_3_4='1#####11111111###1111###111##1111##11111####111#1111#11111111####1111#####111111###111###1##1111####1#111111####'
copy_2_3_4 = '11#####11111111###1111###111##1111##11111####111#1111#11111111####1111#####111111###111###11##1111####11#111111####'



def oneone(n):
  return '1'* n

def all_equal(list):
  a = list[0]
  b = [x == a for x in list]
  return(all(b))


def arity(t):
  if t == 's_prog':
    return(1)
  if t[0] == 'proj':
    return(t[2])
  if t == 'z':
    return(1)
  if t == 'z_empty':
    return(0)
  if t[0] == 'pr':
    k = arity(t[1])
    j = arity(t[2])
    if j== 2 + k:
      return(k+1)
  if t[0] == 'comp':
    f = t[1]
    g_list = t[2:]
    if arity(f)== len(g_list) and all_equal([arity(v) for v in g_list]):
      return(arity(t[2]))   

def new_program(t,n):
  if t=='s_prog':
    return(copy_1_2_3+ successor_prog(2,3))
  if t[0] == 'proj':
    return(proj_prog(t[1],t[2]))
  if t == 'z':
    return('11##')
  if t == 'z_empty':
    return('1##') 
  if t[0] == 'pr':
    f = new_program(t[1],essentially_used(t))
    g = new_program(t[2],essentially_used(t))
    p = primitive_recursion(f, g, arity(t),essentially_used(t))
    return(p)
  if t[0] == 'comp':       
    g = new_program(t[1],essentially_used(t))
    hs = [new_program(u,essentially_used(t)) for u in t[2:]]
    k = arity(t[2])
    p = compose(g,hs,k, essentially_used(t))
    return(p)

def in_place_program(t):
  if t=='s_prog':
    return(copy_1_2_3+ successor_prog(2,3))
  if t[0] == 'proj':
    return(proj_prog(t[1],t[2]))
  if t == 'z':
    return('11##')
  if t == 'z_empty':
    return('1##') 
  if t[0] == 'pr':
    f = in_place_program(t[1])
    g = in_place_program(t[2])
    p = primitive_recursion(f, g, arity(t),essentially_used(t))
    return(p)
  if t[0] == 'comp':       
    g = in_place_program(t[1])
    hs = [in_place_program(u) for u in t[2:]]
    k = arity(t[2])
    p = compose(g,hs,k, essentially_used(t))
    return(p)

def essentially_used(t):
    if t=='s_prog':
      return(3)
    if t[0]== 'proj':
      return(t[2])
    if t == 'z':
      return(1)
    if t == 'z_empty':
      return(0)
    if t[0] == 'comp':
      outer = t[1]
      n1 = essentially_used(outer) 
      n2 = n1 + (len(t) -0)
      n3 = max([essentially_used(u) for u in t[2:]])
      n = max([n1,n2])+2
      return(n)
    if t[0] == 'pr':
      g = t[1]
      h = t[2]     
      n1 = essentially_used(g)
      n2 = essentially_used(h)
      n = max([n1,n2]) +2
      return(n)
#import sys

def program(t):
  n = arity(t)
  first = in_place_program(t)
  second = unparse([clear_prog(i) for i in range(1,n+1)])
  third = move_prog(n+1,1)
  return(first+second+third)

#@title
def syntax_check(t):
  if t == 's_prog':
    return('True')
  if t[0] == 'proj':
    if t[1] <= t[2]:
      print(str(t))
      print("is a good term, and its arity is " + str(arity(t)))  
      print()
      return('True')
    else:
      print('Error in the expression below:')
      print(t)
      print()
      return(False)
  if t == 'z':
    return('True')
  if t == 'z_empty':
    return('True')
  if t[0] == 'pr':
    bool1 = syntax_check(t[1])
    bool2 = syntax_check(t[2])
    boolean = bool1 and bool2
    if boolean:
       k = arity(t[1])
       j = arity(t[2])
       if j== 2 + k:
          print(str(t))
          print("is a good term, and its arity is " + str(arity(t)))  
          print()
          return(True)
       else:
              print('Error in the primitive recursion (sub)term below:')
              print(t)
              print()
              print('The arity of the first term is ' + str(k))
              print('The arity of the second term is ' + str(j) +',')
              print('and we need the second arity to exceed the first by 2.')
              print()
    else: 
       print()
       print('Thus, there is an error in the pr term')       
       print(t)  
  if t[0] == 'comp':
    f = t[1]
    b1 = syntax_check(t[1])
    #print('b1: ' + str(b1))
    if b1 == False:
      print('Error in the sub-expression below:')
      print(t[1])
      return(False)
    g_list = t[2:]
    b2 = all_equal([syntax_check(v) for v in g_list])   
    #print('b2: ' + str(b2)) 
    if (b1 == True) and (b2 == False):
      print('One of the expressions is not a term:')
      print(g_list)
      return(False)
    else:
      b3 = all_equal([arity(v) for v in g_list])
      #print('b3: ' + str(b3)) 
    if b3 == False:
      print('The expressions below are terms, but their arities are not all equal:')
      print(g_list)
      return(False)
    b4 = b2 and b3
    #print('b4: ' + str(b4)) 
    if b4 == True:
      k = len(g_list)
      b5 = (k == arity(f)) 
      #print('b5: ' + str(b5)) 
      if b5 == False:
        print("Arity match error: The arity of ")
        print(str(f)) 
        print('is '+ str(arity(f)) + ', and it ')
        print("should equal " + str(k) + ", the number of terms which follow it.")
        return(False)  
      else:
        print(str(t))
        print("is a good term, and its arity is " + str(arity(t)))  
        print()        
        return(True)           

   
   
pr = 'pr'
proj = 'proj'
comp = 'comp'
s = 's_prog'
z = 'z'
z_empty = 'z_empty'



ddd = '1#####111111###111111111###11#####11111111111###1111111111###111111####11#####111111111111111###111111###11111###11#####111###1111111111111####1###1#####111###11####111####11#####1111###11####111####1#'
## ddd is used in the compare program just below
def compare_prog(a,b): #uses a+1, a+2, a+3
  p = copy_prog(a,a+1,a+2) + copy_prog(b,a+2,a+3) +  bump(ddd,a) 
  return(p)
  # SHOULD ONLY BE USED WHEN b is not a+1 and not a+2
  # checks if Register a and Register b have the same thing, 
  # preserving them.   At the end, R(a+1) either has 
  # 1 (if original Rn and Rm are the same) or is empty (if they aren't)
  # This program also writes to R(a+2) and R(a+3).  So when it is 
  # called, all of registers a+1, a+2, and a+3 should be empty

def successor_prog(to_increment,to_use):
  # gives a program to increment the register 'to_increment' by 1, using 
  # the register 'to_use'
   p = (oneone(to_increment) + 
     '#####' + 
     '111###' +
     '111###' +
     '1111111111111111111111111###'+
     '1111111111111111111111111111111111111111###' +
     oneone(to_use) + '##' + 
     oneone(to_increment) + '#####' + 
     '111###' +
     '111111111111111111###' +
     '1111111111111111111###' +
     oneone(to_use) + '#' + 
     oneone(to_increment) + '#####' + 
     '111111###' +
     '111###' +
     oneone(to_use) + '##' + 
     '1111####' +
     oneone(to_use) + '#' + 
     '111111####' +
     oneone(to_use) + '#####' + 
     '111111###' +
     '111###' +
     oneone(to_increment) + '##' + 
     '1111####' +
     oneone(to_increment) + '#' +  
     '111111####' +
     '1111111111111111111###'  +
     oneone(to_use) + '##' +  
     '111111111111111111111####' +
     oneone(to_use) + '#' +  
     oneone(to_increment) + '#####' +  
     '111111###' +
     '111###' +
     oneone(to_use) + '##' +  
     '1111####' +
     oneone(to_use) + '#' + 
     '111111####' +
     oneone(to_use) + '#####' +  
     '111111###' +
     '111###' +
     oneone(to_increment) + '##' +  
     '1111####' +
     oneone(to_increment) + '#' + 
     '111111####' +
     '1###'
     )
   return(p) 
  
z_prog = '11##'
one_prog = '11#'
#@title
# s is an index of the successor function in bb
successor = '1#####111###111###1111111111111111111111111###1111111111111111111111111111111111111111###11##1#####111###111111111111111111###1111111111111111111###11#1#####111111###111###11##1111####11#111111####11#####111111###111###1##1111####1#111111####1111111111111111111###11##111111111111111111111####11#1#####111111###111###11##1111####11#111111####11#####111111###111###1##1111####1#111111####1###'

def maxie(l):
  if l == []:
    return(0)
  else:
    return(max(l))
def height(tree):
  n = maxie([height(u) +1 for u in tree.children])
  return(n)
def all_equal(list):
  if (len(list)==0 or len(list)==1):
    return(True)
  else:
    b = all_equal(list[1:])  
    if b == False:
      return(False)
    else:
      return(list[0]==list[1])

def bump_instr(inst, amount):
  if instruction_type(inst) in ['forward','backward']:  
    return(inst) 
  elif instruction_type(inst) == 'add1':  
    n = number_help(inst)
    return(oneone(n+amount)+'#')
  elif instruction_type(inst) == 'add#':  
    n = number_help(inst)
    return(oneone(n+amount)+'##')
  elif instruction_type(inst) == 'cases':  
    n = number_help(inst)
    return(oneone(n+amount)+'#####')
def bump(prog,amount):
  par = parse(prog)
  t = [bump_instr(instr,amount) for instr in par]
  return(unparse(t))

def clear_prog(n):
   a = oneone(n) + '#####'
   b = '111###'
   c = '1###'
   d = '111####'
   return(a+b+c+d)

def move_prog(n,m):
   a = oneone(n) + '#####'
   b = '111111###'
   c = '111###'
   d = oneone(m)+'##'
   e = '1111####'
   f = oneone(m)+'#'
   g = '111111####'
   return(a+b+c+d+e+f+g)

def copy_prog(n,m,p):
   a = oneone(n) + '#####'
   b = '11111111###'
   c = '1111###'
   d = oneone(m)+'##'
   d1 = oneone(p) + '##'
   e = '11111####'
   f = oneone(m)+'#'
   f1 = oneone(p) + '#'
   g = '11111111####'
   return(a+b+c+d+d1+e+f+f1+g+move_prog(p,n))  

def proj_prog_official(ind,upper):
  index = [k+1 for k in range(ind-1)]    
  #print(index)
  first_part = [clear_prog(j) for j in index]
  #print(first_part)
  if ind == 1:
    middle = []
  else: 
    middle=[move_prog(ind,1)]
  second_index =  [k+ind+1 for k in range(upper-ind)] 
  #print(second_index)
  last_part = [clear_prog(j) for j in second_index]   
  together = first_part + middle + last_part
  done = unparse(together)
  if ind == 1 and upper==1:
    return('1###')
  else:
    return(done)   

def proj_prog(ind,upper):
  return(copy_prog(ind,upper+1, upper+2))

# the function below doesn't seem to be used
def copy_all_forward(n,m):
  # copies 1 to m, 2 to m+1, . . . n to m+n-1
  a = [copy_prog(i,m+i-1, m+i) for i in range(1,n+1)]
  return(unparse(a))


def compose(outer_fn,proglist,argument_number,used_reg):
  ## note that the outer_fn has to be 'in place'!
  k = len(proglist) # number of functions
  # the outer_fn is k-ary
  q = unparse([clear_prog(i) for i in range(1,k+1)])
  outer_fn = outer_fn + q + move_prog(k+1,1)
  arg = argument_number # = common arity in the proglist
  max_list =   [max_register(p) for p in proglist]
  m = maxie(max_list)
  #free_reg = used_reg + 1
  free_reg = m + 1
  a = [proglist[i] + move_prog(arg+1,free_reg+i+1) for i in range(0,k)]
  b = unparse(a)
  c = [move_prog(free_reg+i+1,argument_number+i+1) for i in range(0,k)]
  d = unparse(c)
  f = bump(outer_fn,argument_number)
  e = b + d + f   
  return(e)

# <g,h>(x-bar,0) = g(x-bar)
# <g,h>(x-bar,n+1) = h(x-bar,n,<g,h>(x-bar,n))
# k-1 is the number of xs, so the arity of <g,h> is k
# k+1 is the number of arguments to g
# k is the number of arguments to the function we are building
#free is large enough so that neither g nor h use it or any larger register.
# g and h are assumed to preserve their inputs
def primitive_recursion(g,h,arity,used_reg):
  free = max([max_register(g),max_register(h)])+1
  #free = used_reg +1
  free_plus_one = free + 1
  plan = [['top',move_prog(arity,free) +
               g + 
               move_prog(arity,arity+1) + 
               oneone(arity) + '##' ],
          [compare_prog(free,arity)],
          ['decision', 'cases', free_plus_one, 'main_loop','clear_out_free', 'end' ],
          ['clear_out_free', clear_prog(free)],
          ['goto', 'end'],
          ['main_loop',h + 
               clear_prog(arity+1) + 
               move_prog(arity+2,arity+1) + 
               successor_prog(arity,free+2) +
               compare_prog(free,arity)],
          ['goto', 'decision'],
        ]
  trial = sanity(plan)
  return(trial)   
 
   
