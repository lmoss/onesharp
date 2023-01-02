#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lmoss/onesharp/blob/main/T_predicate.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # The T predicate
# 
# 
# 

# In[1]:


#@title
import pandas as pd
import numpy as np

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
    def __init__(self, instr_number, regs, proceed,verbose,
                 program_length, step_number,display_formal_snapshot,partial_trace):
        self.instr_number = instr_number
        self.regs = regs
        self.proceed = proceed
        self.verbose = verbose
        self.program_length = program_length
        self.step_number = step_number
        self.display_formal_snapshot = display_formal_snapshot
        self.partial_trace = partial_trace
        
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
    truth_value = snapshot.display_formal_snapshot
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
            print_snapshot(snapshot,truth_value)
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

def print_snapshot(snap,truth_value):
    regdf = pd.DataFrame([[snap.regs[n]] for n in range(len(snap.regs))],columns=["contents"])
    regdf.index = np.arange(1, len(regdf) + 1)
    def make_pretty(styler):
        styler.set_properties(**{'background-color': '#FFFFCC'})
        styler.set_properties(**{'text-align': 'left'})
        #styler.set_caption("at the start")
        #styler.hide(axis='index')
        return styler
    display(regdf.style.pipe(make_pretty))  
    if truth_value == True:
        print()
        w = word_representation(snap)
        print('The formal snapshot is ' + w)
        print()
        snap.partial_trace = snap.partial_trace + w + '#1'


def step_by_step_with_snapshots(word_prog, register_inputs):
    step_by_step_prelim(word_prog,register_inputs,True)

def step_by_step(word_prog, register_inputs):
    step_by_step_prelim(word_prog, register_inputs,False)

def step_by_step_prelim(word_prog, register_inputs,display_formal_snapshot):
    truth_value = display_formal_snapshot
    word_prog = word_prog.replace(" ", "")
    register_inputs = [word.replace(" ", "") for word in register_inputs]
    if program_checker(word_prog) and input_checker(register_inputs):
        print('First, here is the program:')
        parse_explain(word_prog)
        print()
        regs = pad(word_prog, register_inputs)
        prog = parse(word_prog)
        N = len(prog)
        snap = Snapshot(1, regs,True,True,N,1,truth_value,'')
        print('The computation starts with the register contents shown below.')
        print('The registers include those those which you entered as part of the input')
        print('and also others mentioned in the input program.')
        print_snapshot(snap,display_formal_snapshot)
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
            print()
            print_snapshot(snap,display_formal_snapshot)
            print('The trace is shown below:') ##
            print(snap.partial_trace) ##
            print()
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
        snap = Snapshot(1, regs,True,False, N, 1,False,'')
        while snap.proceed:
            snap = one_step(prog, snap)
            snap.step_number = (snap.step_number)+1
        if (snap.instr_number == (N + 1)) and all(
                snap.regs[i] == "" for i in range(1, len(snap.regs))):
            return ((snap.regs)[0])
        else:            
            print("This is undefined.")
            print("The register contents at the end are shown below.")
            print_snapshot(snap,False)
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

def ones(n):
    w = ['1' for i in range(n)]
    return(unparse(w)) 

clear_1 = '1#####111###11####111####'

move_2_1 = '11#####111111###111###1##1111####1#111111####'

copy_1_2_3 = '1#####11111111###1111###11##111##11111####11#111#11111111####111#####111111###111###1##1111####1#111111####'

length = '1#####1111111###11####11#1#####111###111111####111####11#####111111###111###1##1111####1#111111####'

write = '1#####111111111###11111###11#11##11##111111####11#11##111111111####11#####111111###111###1##1111####1#111111####'

diag = '1#####11111111111###111111###11##111#111##111##1111111####11#111#111##1111####111#####111111###111###1##1111####1#11####11#####111111###111###1##1111####1#11####'

self = '1#1##1##1##1##1##1#1#1#1#1#1#1#1#1#1#1#1##1##1##1#1#1#1#1#1#1##1##1##1#1#1##1##1#1#1#1##1#1#1#1##1##1#1#1#1##1##1#1#1#1#1#1#1#1##1##1##1##1#1#1##1#1#1#1##1#1#1#1##1##1#1#1#1#1##1##1##1##1#1#1#1##1##1##1##1##1#1#1#1#1#1#1##1##1##1#1#1#1##1##1##1#1##1##1#1#1#1#1##1##1##1##1#1##1#1#1##1##1##1##1#1#1##1##1##1##1##1#1#1#1#1#1#1##1##1##1#1#1#1##1##1##1#1##1##1#1#1#1#1##1##1##1##1#1##1#1#1##1##1##1##1#####11111111111###111111###11##111#111##111##1111111####11#111#111##1111####111#####111111###111###1##1111####1#11####11#####111111###111###1##1111####1#11####'

multiply = '111##1111##11#####11111111###1111###11111##111111##11111####11111#111111#11111111####111111#####111111###111###11##1111####11#111111####111#####11111111###1111###111111##1111111##11111####111111#1111111#11111111####1111111#####111111###111###111##1111####111#111111####11111#####111111###111111111###111111#####11111111111###1111111111###111111####111111#####111111111111111###111111###11111###111111#####111###1111111111111####1###11111#####111###11####111####111111#####1111###11####111####11111#11111#####111###1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111###1#1#####11111111###1111###11111##111111##11111####11111#111111#11111111####111111#####111111###111###1##1111####1#111111####1111#####111111###111###111111##1111####111111#111111####11111#####111###111111###111111111###111111#####11111111111111111111111111111111111###11111111111111111111111111###111111111111111111111111111###111111#####11111111111111111111111###1111111111111111111111111111###111111111111111111111###111111#####111111111111111111111###111111111111111111###1111111111111111111###11111#####111###111111###111111111###111111#####11111111111###1111111111111111###111111111###111111#####1111111111111###1111111111###11111111111###111111#####111###11111111###1###1111111#111111111111111111111111111111111####1111111##11111111111111111111111111111111111####1111111#111111111111111111111####1111111##11111111111111111111111####1###1111111#####111111###111###11111##1111####11111#111111####11111#####111111###111###1111##1111####1111#111111####111#####1111111111111###1111111111###11111#111#####111111###111###11111##1111####11111#111111####1111###11111##1111111111111####11111#11111#####111111###111###111##1111####111#111111####1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111####1#####111###11####111####11#####111###11####111####111#####111###11####111####1111#####111111###111###1##1111####1#111111####'

universal = '1#####1###11###11####111111#1#####111###111111###1111111###11111#####1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111###1###1####111#111111111####111##1#####1111###11###11111###111#11111#####1111111111111111111111111111111111111111111111###111111111###111##1#####1111###11###11111###111#11111#####1111111111111111111111111111111111111###111111111###111##1#####1111###11###11111###111#11111#####1111111111111111111111111111111111111111111111###111111111###111##1#####1111###11###11111###111#11111#####111111111111111111111111111111111111111111111111111111###111111111###111##1#####1111###11###11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111###111#11111#####1111111111###1###111#####111111###111###1111##1111####1111#111111####11111111111111111111111111111111111111111111111111111111111111####111#####1###11###1111###11111#1111#111111####11111##1111##111#####1111111###1111###1111##11111##11111####1111#1111111####111111111111111111111111111111111111111111111111111111111111111111111111111###111#####1###11###11111###11111#1111#111111#1111111####1111##111#####111111###111###1111##1111####1111#111111####11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111####111#####1###11###1111###1111#11111#111111####11111#11111#1111##111#####111111###111###1111##1111####1111#111111####11111#####11111111###11###1###111111#####111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111###1###1###11111111####111111#####1111###111#11111#1111####111#####111###111111#111####1#####111111###111###111##1111####111#111111####1111#####111111###111###1##1111####1#111111####111#####111111###111###1##1111####1#111111####111111111111111111111111111111111111111111111111111111111####11#####111###11111###111111111111###11##11##111111####111#11#####1###111###111##11###111#11111111111111####111##11#####11111111111111111111111111111111111111111111111111111111111111111111###1###111##11111#####1###1111111111111111111111####11111#####1111111111111111111111111111###111111111111111111111111111###11111#####111###11###111111111111111111111111111111111111111111111###11#####111111111111111111###111111111###111#11#####1###1###111#111##111##111111111111111111111111111111111111111111111111111111111###111#11#####1###111###111##11###111#111111111111111111####111#111#1111111111111111111111111111111111111111111111###11#####111111111111111111###111111111###111#11#####1###1###111##111##111##11111111111111111111111111111111111###111#11#####1###111###111##11###111#111111111111111111####111#111##111111111111111111111111###11111#####1###1###11111#####1###1###11#####11111111111111111111111###111###111##1111111111111###11#####1###11111###1###11111#111111#111111###11111#11111#111111#111111#1###11#####111111###111###111##1111####111#111111####111#####111111###111###11##1111####11#111111####1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111####11#####1###1###11#####1###1###11#####11111111111111###11###11111111###11#####1###111###1#11111111####1##1111111111####11#####111###11####111####111111#####11###11####1111#####111###11####111####'

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


# ## Snapshot and trace
# 
# To start, review the definitons of *snapshot* and *trace*.
# 
# ##### We encode a word on {1,#}, say a1, . . . a_n by 1 a_1 1 a_2 . . . 1 a_n.
# That is, we put the symbol 1 between all symbols of the word that we want to encode.
# 
# ##### We encode a sequence of words by adding the separator ## after the enconding of each word in the sequence.
# 
# #### We encode a snapshot by taking a number n and turning it into unary notation, and then following it by a sequence encoding some words.  The idea is that the number n should be an instruction number in a program, and the encoded words should be the conents of the registers.

# <img src="https://github.com/lmoss/onesharp/blob/main/harp.jpg?raw=1" width="200" height="160">

# ## New interface
# 
# Here is a new interface for running program which includes a "mode" capability that includes the option of seeing all the snapshots and the overall trace.

# In[2]:


#title Text Register Machine <br> The entries for the program and registers must be words on the alphabet {1,#}, without quotes.
def end_strip(list): ## removes the tail of empty registers
  if list == []:
    return(list)
  elif list[-1] == '':
    return(end_strip(list[:-1]))
  else:
    return(list)
def remove_multiple_blanks(my_str):
   return(my_str.replace(" ", ""))


program = '1#' #@param {type:"string"}
R1 = '1#1#' #@param {type:"string"}
R2 = '' #@param {type:"string"}
R3 = '' #@param {type:"string"}

## For more registers, add lines here like
## R4 = '' #@param {type:"string"}
## You also must modify the definition of 'a' below accordingly.

mode = 'step by step with snapshots and trace' #@param ["output only", "step by step","step by step with snapshots and trace"]

# First, we delete the last batch of empty registers
# to simplify the output 
a = [R1,R2,R3]
a = [remove_multiple_blanks(x) for x in a]

non_empty_registers = end_strip(a)
if mode == 'output only':
  onesharp(program,non_empty_registers)
if mode == 'step by step':
  step_by_step(program,non_empty_registers)
if mode == 'step by step with snapshots and trace':
  step_by_step_with_snapshots(program,non_empty_registers)


# If you want to expand the interface to handle more than three registers, open the code and look around.
# 
# You can also run things in the notebook cells as we have been doing it.  See below for an example of how we would see the snapshots in a step_by_step execution.

# In[3]:


#@title
step_by_step_with_snapshots('1#1#',['##'])


# In[4]:


#@title
step_by_step_with_snapshots(diag,['1#'])


# ### We also want to check that various relations leading up to the T predicate are computable.  This part is work in progress, with the results obtained so far shown below.

# In[5]:


def snapshot_check(w):  ## tells True or False if the input is a snapshot
  index = w.index('##')
  front = w[:index] ## divide the string by the first occurrence of ##
  back = w[index:]
  first_truth_value = all([(x == '1') for x in front]) 
  ## first_truth_value tells if all symbols in the front are 1
  j = len(back)
  indices_of_sharp = [(2*i) for i in range(j//2) if back[2*i]=='#']
  second_truth_value = all([(back[1 + i] == '#') for i in indices_of_sharp])
  ## the second truth value tells the separators ## are done correctly 
  return(first_truth_value and second_truth_value)

def halting_snapshot_check(p,w):  
  ## tells True or False if the input is a snapshot
  # which suggests that the program p has halted properly
  # So we check that p is a program, 
  # that the number at the front of w is 1 + (the number of instructions in p),
  # and that in w, all registers after R1 are empty
  parsed_p = parse(p)
  N = len(parsed_p)
  #print('N =' + str(N))
  index = w.index('##')
  front = w[:index] ## divide the string by the first occurrence of ##
  #print('len front = '+ str(len(front)))
  length_check = (N + 1 == len(front))
  #print(length_check)
  back = w[index:]
  first_truth_value = all([(x == '1') for x in front]) 
  ## first_truth_value tells if all symbols in the front are 1
  j = len(back)
  indices_of_sharp = [(2*i) for i in range(j//2) if back[2*i]=='#']
  second_truth_value = all([(back[1 + i] == '#') for i in indices_of_sharp])
  ## the second truth value tells the separators ## are done correctly 
  w2 = back[2:]
  #print('w2' +w2)
  index2 =w2.index('##') 
  #print(index2)
  back2 = w2[index2:]
  #print(back2)
  emptiness_check = all(x=='#' for x in back2)
  #print(emptiness_check)
  return(first_truth_value and second_truth_value and length_check and emptiness_check)


# In[6]:


snapshot_check('111##1#11#1111##')


# In[7]:


print([0,1,2,3,4,5][2:])
print(parse('1#1#'))
halting_snapshot_check('1#1#','111##1#1#1111##1###')


# <img src="https://github.com/lmoss/onesharp/blob/main/pianotrumpet.jpg?raw=1" width="200" height="160">

# In[8]:


import math

def log2int(x):
  return(math.frexp(x)[1] - 1)

def length(n):
  return(log2int(n+1))

def index(n,m): ## this is what I write as (n)_m
  a = (n+1)%(2**(m+1))
  b = 2**m
  if a < b:
    return(0)
  else:
    return(1)

def convert_numeral_to_onesharp(x):
   if x == 0:
     return('#')
   else:
     return('1')    

def s(n):
  k = length(n)  
  s = [convert_numeral_to_onesharp(index(n,k-i-1)) for i in range(k)] 
  t = "".join(s) 
  return(t)

def s_inverse(w):
  n = len(w)
  a = (2**n - 1)
  b = [(2** (n-i-1)) for i in range(n) if (w[i] == '1')]
  c = sum(b)
  d = c+a
  return(d)


# We can check that ```s``` and ```s_inverse``` really are inverses.

# In[9]:


s(s_inverse('##111##1'))


# In[10]:


s_inverse(s(4234))


# In[11]:


for n in range(256):
  print((n,s(n), s_inverse(s(n))))
 


# In[12]:


s(55)


# In[13]:


a = ['1#','','1','','']
first_index = a.index('')
reversed_list = a[::-1]
first_index_in_reversed = reversed_list.index('')
last_index = len(a) -1 - first_index_in_reversed
last_index
print(a[:last_index-1])


# In[14]:


a = ['1#1#', '11', '','#','']
print(a)
first_index = a.index('')
reversed_list = a[::-1]
print(reversed_list)
first_index_in_reversed = reversed_list.index('')
last_index = len(a) -1 - first_index_in_reversed
print(last_index)
non_empty_registers = a[:last_index]
print(non_empty_registers)

