#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lmoss/onesharp/blob/main/getting_started.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # <span style="color:blue">Getting stared with 1#</span> 
# Lawrence S. Moss,
# Indiana University
# 
# To start, click on 'Open in Colab', and then click on the triangle.

# In[ ]:


#@title
import pandas as pd
from IPython.display import display
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
    snapshot.proceed = 0< snapshot.instr_number <= len(p)
    if snapshot.verbose == True:
        print_snapshot(snapshot)
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

def print_snapshot(snap):
    regdf = pd.DataFrame([[snap.regs[n]] for n in range(len(snap.regs))],columns=["contents"])
    regdf.index = np.arange(1, len(regdf) + 1)
    def make_pretty(styler):
        styler.set_properties(**{'background-color': '#FFFFCC',
                                 'color': 'black'})
        styler.set_properties(**{'text-align': 'left'})
        #styler.set_caption("at the start")
        #styler.hide(axis='index')
        return styler
    display(regdf.style.pipe(make_pretty))  

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
                styler.set_properties(**{'background-color': '#C9DFEC',
                                         'color': 'black'})        
                styler.set_properties(**{'text-align': 'left'})
                return styler
    display(df.style.pipe(make_pretty))
    #display(df)
    

length = '1#####1111111###11####11#1#####111###111111####111####11#####111111###111###1##1111####1#111111####'

write = '1#####111111111###11111###11#11##11##111111####11#11##111111111####11#####111111###111###1##1111####1#111111####'

diag = '1#####11111111111###111111###11##111#111##111##1111111####11#111#111##1111####111#####111111###111###1##1111####1#11####11#####111111###111###1##1111####1#11####'

self = '1#1##1##1##1##1##1#1#1#1#1#1#1#1#1#1#1#1##1##1##1#1#1#1#1#1#1##1##1##1#1#1##1##1#1#1#1##1#1#1#1##1##1#1#1#1##1##1#1#1#1#1#1#1#1##1##1##1##1#1#1##1#1#1#1##1#1#1#1##1##1#1#1#1#1##1##1##1##1#1#1#1##1##1##1##1##1#1#1#1#1#1#1##1##1##1#1#1#1##1##1##1#1##1##1#1#1#1#1##1##1##1##1#1##1#1#1##1##1##1##1#1#1##1##1##1##1##1#1#1#1#1#1#1##1##1##1#1#1#1##1##1##1#1##1##1#1#1#1#1##1##1##1##1#1##1#1#1##1##1##1##1#####11111111111###111111###11##111#111##111##1111111####11#111#111##1111####111#####111111###111###1##1111####1#11####11#####111111###111###1##1111####1#11####'

multiply = '111##1111##11#####11111111###1111###11111##111111##11111####11111#111111#11111111####111111#####111111###111###11##1111####11#111111####111#####11111111###1111###111111##1111111##11111####111111#1111111#11111111####1111111#####111111###111###111##1111####111#111111####11111#####111111###111111111###111111#####11111111111###1111111111###111111####111111#####111111111111111###111111###11111###111111#####111###1111111111111####1###11111#####1  11###11####111####111111#####1111###11####111####11111#11111#####111###1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111###1#1#####11111111###1111###11111##111111##11111####11111#111111#11111111####111111#####111111###111###1##1111####1#111111####1111#####111111###111###111111##1111####111111#111111####11111#####111###111111###111111111###111111#####11111111111111111111111111111111111###11111111111111111111111111###111111111111111111111111111###111111#####11111111111111111111111###1111111111111111111111111111###111111111111111111111###111111#####111111111111111111111###111111111111111111###1111111111111111111###11111#####111###111111###111111111###111111#####11111111111###1111111111111111###111111111###111111#####1111111111111###1111111111###11111111111###111111#####111###11111111###1###1111111#111111111111111111111111111111111####1111111##11111111111111111111111111111111111####1111111#111111111111111111111####1111111##11111111111111111111111####1###1111111#####111111###111###11111##1111####11111#111111####11111#####111111###111###1111##1111####1111#111111####111#####1111111111111###1111111111###11111#111#####111111###111###11111##1111####11111#111111####1111###11111##1111111111111####11111#11111#####111111###111###111##1111####111#111111####1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111####1#####111###11####111####11#####111###11####111####111#####111###11####111####1111#####111111###111###1##1111####1#111111####'

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


# Welcome to our first tutorial lesson on 1#. You will learn the basics of the language here and also see some small programs.
# 
# This lesson is written on a lower level than the lessons which come after it. The only abstract concept comes at the end, as does the only and mathematical notation. The rest of the lesson is a concrete introduction to 1#.
# 
# If you are familiar with any machine model in the theory of computations, such as Turing Machines, or classical register machines, you probably will want to skim through this lesson quickly.
# 
# But this introductory lesson is really intended for people with no background on these matters. If this is you, please work slowly, doing the exercises as you go.
# 

# To begin, here is an *interpreter* for 1#.  Even before learning how the language works, we want to see how to run programs by entering them into the interpreter along with inputs.

# In[ ]:


def end_strip(list): ## removes the tail of empty registers
  if list == []:
    return(list)
  elif list[-1] == '':
    return(end_strip(list[:-1]))
  else:
    return(list)
def remove_multiple_blanks(my_str):
   return(my_str.replace(" ", ""))


program = '11#####111111###111###1##1111####1#111111####' #@param {type:"string"}
R1 = '#1111' #@param {type:"string"}
R2 = '11#' #@param {type:"string"}
#R3 = '' #@param {type:"string"}

## For more registers, add lines here like
## R4 = '' #@param {type:"string"}
## You also must modify the definition of 'a' below accordingly.

# First, we delete the last batch of empty registers
# to simplify the output 
a = [R1,R2]
a = [remove_multiple_blanks(x) for x in a]

onesharp(program,a)


# Please copy the following *program* of 1# into the program line of the interpreter above.
# 
# ```11#####111111###111###1##1111####1#111111####```
# 
# Now enter some words in the first two *input registers*. These two registers appear in the interpreter as R1 and R2.  The registers hold *words*.  For us in this course, words are just sequences  composed of the symbols ```1``` and ```#```, such as ```11###11#1``` and ```#1###1###111#11```.
# 
# The empty word is a perfectly good word, so you could also enter it into R1 or R2 just by leaving the register blank or by entering one or more spaces.
# 
# 
# Next, run your program by clicking the triangle in the upper-left above.  (Another way to run the program is to type shift-return on a keyboard.) The output is shown below the interpreter, above the current cell.
# 
# You should then clear the input and output registers, and then enter some new words in R1 and R2.  Again, click the triangle to run the program.
#  You might now enter some words in R3 to see if it makes a difference.
# 
# What you should find after doing this is that the output in R1 at the end is the input in R1 followed by the input in R2. And as a result of the same computation, R2 is emptied out. We usually will say *concatenated* instead of *followed by*.
# 
# ---
# 
# The overall point is that the program ```11#####111111###111###1##1111####1#111111####``` may be run on words which are input in the registers. This program does not change when we run it, but the contents of the registers do change. Our first order of business is to understand programs like the one we've just seen. It turns out that this program is composed of seven instructions. We'll get to the instructions soon, but first we have an exercise for you to try.

# ### Exercise 1 
# 
# Here is another 1# program. It takes its input from the first two registers. Enter some words in R1 and R2 input boxes, and then run the program. Your job is to try to figure out what the program does.
# 
# ```1##### 11111111### 1111### 111## 1111## 11111#### 111# 1111# 11111111#### 111##### 111111### 111### 1## 1111#### 1# 111111#### 1111##### 111111### 111### 1## 1111#### 1# 111111#### 11##### 111111### 111### 1## 1111#### 1# 111111####```

# <img src="https://github.com/lmoss/onesharp/blob/main/drum.jpg?raw=1" width="200" height="160">

# # The 1# instruction set
# 
# So far, we have seen two *programs* of 1#. Programs are composed of *instructions*. In fact, programs are just sequences of instructions run together. There are only five kinds of 1# instructions.  Now is the time to introduce them.
# 
# We begin our journey with the first two types of instructions of the language.
# 
# | Instruction      | Meaning |
# | ----------- | ----------- |
# | 1#      | Add 1 to R1       |
# | 11#   | Add 1 to R2      |
# | 111#   | Add 1 to R3      |
# 
# 
# These instructions that a 1 to the end of the word in the specified register.
# 
# 
# | Instruction      | Meaning |
# | ----------- | ----------- |
# | 1##      | Add # to R1       |
# | 11##   | Add # to R2      |
# | 111##   | Add # to R3      |
# 		
# 
# These add a # to the end (the right side) of the word in the specified register.  We can summarize the two kinds of instructions which we have seen, and also extend them:
# 
# | Instruction      | Meaning |
# | ----------- | ----------- |
# | 1^n #      | Add 1 to Rn       |
# | 1^n ##   | Add # to Rn      |
# 
# The programs of 1# are just sequences of instructions run together.  There is no punctuation between the instructions. However, we do have an important comment. So to move around in a program, we have two other kinds of instructions
# 
# | Instruction      | Meaning |
# | ----------- | ----------- |
# | 1^n ###   | Go forward n instructions     |
# | 1^n ####   | Go backward n instructions     |
# 
# Here is the last kind of instruction:
# 
# | Instruction      | Meaning |
# | ----------- | ----------- |
# | 1^n #####   | Cases on register n     |
# 
# Here is what it does:
# 
# If Rn is empty, we go to the very next instruction.
# 
# If the first symbol of Rn is 1, we delete that symbol and go to the second instruction after the case instruction.
# 
# If the first symbol of Rn is #, we delete that symbol and go to the third instruction after the case instruction.
# 
# The 'cases' instructions are the most complex to understand, and it will help to look an example in detail.   But first we have some exercises on the 1^n# and 1^n## instructions.

# ### Exercise 2 
# 
# Again, start with 1 in R1 and R2, 1# in R3, and the other registers empty.
# What happens in each register if we run 111##?
# Try to figure this out for yourself, and then check your work by actually running the program.

# ### Exercise 3
# 
# As before, start with 1 in R1 and R2, 1# in R3, and the other registers empty.
# What happens in each register if we run the same program p from Exercise 2 above?
# 

# ### Exercise 4 
# 
# Write a program which, when started with all registers empty, gives 1 in R1 and R2, 1# in R3, and the other registers empty.

# <img src="https://github.com/lmoss/onesharp/blob/main/harp.jpg?raw=1" width="200" height="160">

# # Example: A simple loop
# 
# A good way to learn about the different commands is to examine simple programs.  Among these is a program called ```move_2_1```.   It is designed to move the contents of R2 onto the end of R1, emptying out R2 in the process.  Written out in full it is 
# 
# ```11#####111111###111###1##1111####1#111111####```
# 
# You can try the program out by (a) moving the interprer down, using the appropriate commands in the notebook; (b) entering ```move_2_1``` as the program and some random words in R1 and R2 and then running ```move_2_1``` on those inputs.
# 
# Since it is hard to understand a program of 1#, we have tools to help.  First, we can *parse* the program.  Parsing means dividing the program into instructions.

# In[ ]:


parse(move_2_1)


# Even better, we can get an parse with glosses, as follows:

# In[ ]:


parse_explain(move_2_1)


# The program ```move_2_1``` is a loop, and we can further add to the explanations in the chart.
# 

# In[ ]:


#@title
j = [['11#####', 'cases on R2', ],
 ['111111###', "register 2 is empty: go forward 6 to instruction 8 (we're done)"],
 ['111###', 'first symbol is a 1: go forward 3 to instruction 6 (to the tan section)'],
 ['1##', 'first symbol is a #: add # to R1'],
 ['1111####', 'go backward 4 to instruction 1 (to the top)'],
 ['1#', 'add 1 to R1'],
 ['111111####', 'go backward 6 to instruction 1 (to the top)']
]
 
df = pd.DataFrame(j,columns=["instruction", 'explanation'])
df.index = np.arange(1, len(df) + 1)
df.style.set_properties(**{'border': '1.3px solid green',
                          'color': 'magenta'})
n = len(df.columns)
df.style.set_properties(**{'text-align': 'left'})
#df.style.apply(lambda x: ["background-color: red"]*n if x['instruction']== 'Reading' else ["background-color: white"]*n, axis = 1)
#df.style.apply(lambda x: ["background-color: #B0E0E6"]*n if x['instruction'] in ['1##','1111####'] elif ["background-color: #D4B48C"]*n if x['instruction'] in ['1#','111111####'] else ["background-color: #FFFFCC"]*n, axis = 1)
df.style.apply(lambda x: ["background-color: #B0E0E6"]*n if x['instruction'] in ['1##','1111####']  else ["background-color: #FFFFCC"]*n, axis = 1)
df.style.apply(lambda x: 
               ["background-color: #B0E0E6"]*n if x['instruction'] in ['1##','1111####'] 
               else ["background-color: #D4B48C"]*n if x['instruction'] in ['1#','111111####']
               else ["background-color: #FFFFCC"]*n, axis = 1)


# 
# 
# If R2 is empty, it goes to line 8.  Since the program itself only has 7 lines, this means that we have transferred *out* of the program.  We say that the program *halts* at that point.
# 
# If the first symbol of R2 is a 1, then the second instruction after the case instruction at the top transfers us down to line 6. This part of the program would then add a 1 to R1 and return to the very beginning of the program.
# 
# If the first symbol of R2 is a #, then we delete that # and go three steps forward, to line 4.  This part of the program would then add a # to R1 and return to the very beginning of the program.
# 
# The point is that by going around loop repeatedly, we transfer the contents of R2 symbol-by-symbol to R1.
# Similarly, whenever m and n are different numbers, we can build a program ```move_m_n```. This program would write the contents of Rm onto the end of Rn, emptying Rm in the process.
# 
# 
# 
# 

# # Modifying our simple loop
# 
# Suppose we want to modify ```move_2_1``` to get ```move_3_4```, a program which would copy the contents of R3 onto the end of R4 (and empty R4) in the process.
# Here is a way to do this which shows off some command-line tools that are part of the working environment of this course.

# In[ ]:


parse(move_2_1)


# When you enter the cell above, you get the program ```move_2_1``` as a Python *list* of instructions. We have seen the explanation of this parse above.  What we want to do in ```move_3_4``` is to change the overall "case" instruction in the beginning from ```11#####``` to ```111#####```.   And each time our program writes to a register, we want that register to be R4, not R1.  So we make two changes.

# In[ ]:


pre_program = ['111#####', '111111###', '111###', '1111##', '1111####', '1111#', '111111####']


# To turn this into a program, we have a tool called "unparse".

# In[ ]:


unparse(pre_program)


# We can check this out by entering it into the interpreter.  We could either copy the output line (without the quotes), and go up to the top of this notebook.  Alternatively, we could move the interpreter down to here using an up-arrow command that you will need to find.
# 

# ### Exercise 5
# 
# Write a program which takes the contents of R1 and adds them to the ends of *both* R2 and R3.
# 

# ### Exercise 6
# 
# Write a program that clears out R1, leaving it empty.
# 

# ### Exercise 7
# 
# Write a program that clears R3 and then swaps the contents of R1 and R2 (using the now-empty R3).
# 
# 

# ### Exercise 8 
# 
# Write a program p that adds a 1 to the *beginning* of R1, assuming that R2 is empty.  (For example, if R1 has ```##1``` to start, then running p would result in R1 having ```1##1```.)   Of course, your program may use R2!

# <img src="https://github.com/lmoss/onesharp/blob/main/basses.jpg?raw=1" width="200" height="160">

# # Running programs in notebook cells rather than in an interpreter
# 
# Because notebooks like this are composed of cells, we also want to run programs in a command-line fashion.
# 
# There are two programs that do this.  They are 
# ```step_by_step``` and ```onesharp```.  These are illustrated in the next two cells.  Both of these programs are written in Python, not in 1#.  They both require as inputs a 1# program followed by a sequence of register words.

# In[ ]:


onesharp('1#11#####1###1###',['1#1','#'])


# In[ ]:


step_by_step('1#11#####1###1###',['1#1','#'])


# The last computation started with two inputs.  Try changing those inputs to see what happens.  As practice with the definition of *halt*, you might try yourself to predict what will happen before running it.  You can add the symbols 1 or #, and you also can delete symbols.  But you should not delete the quote marks.  Also, you can change the program the same way.   The idea is that you should explore this function *step_by_step* by trying it out on simple inputs.  

# Here is an explanation of the form of the command ```step_by_step``` that we have been using.   
# 
# The first argument could be a 1# program surrounded by single quotes or double-quotes.   If you use single quotes, you need to be sure to use the correct ones; on my screen they look straight, not slanted.   You could also use a concatenation of quoted expressions (see below).  But if you forget the quotes, you will get an error because the Python program that is running all of this will balk at 1# expressions without quotes around them.
# 
# In addition, you can name expressions ahead of time using assignment statements like 
# 
# ```p = '1#'```
# 
# 
# and then enter (for example)
# 
#  ```step_by_step(p,['11'])```.
# 
# ---
# 
# The program ```step_by_step``` begins with a parse of your program, and so if you input a word that is not a sequence of 1# expressions, it will stop without further ado.
# 
# The second argument to ```step_by_step``` is a list of words.   A list in Python is enclosed by square brackets \[ and \], not by parentheses.  The words that go in the list are used in R1, R2, . . . in that order.  It is understood that any register not represented by any input starts with the empty string.   You can also represent the empty string by ' '.  And the empty list  of registers is denoted by two square brackets with nothing inside,  [  ].
# 
# All in all, the examples below show different formats for the input to our function step_by_step.
# 
# 

# In[ ]:


p= '1#'
q = '#1'
step_by_step(p,[q,q,p])


# In[ ]:


step_by_step(p+q+p,[])
# This is a comment.
# the symbol + is used for concatenation of strings in Python.
# Since p and q are strings, we can concatenate them


# So far in this notebook, we have only seen the function ```step_by_step```.   If we want to run things "in one fell swoop", we could use the function ```onesharp(p,[r1,r2, . . ., rn])```.   It also takes two arguments, the first a program and the second a (possibly-empty) sequence of input words.

# In[ ]:


clear_1 = '1##### 111### 11#### 111####'
onesharp(clear_1,['1111###1111##########'])
# You can also run the line above slowly by running
# step_by_step(clear_1,['1111###1111##########'])


# <img src="https://github.com/lmoss/onesharp/blob/main/pianotrumpet.jpg?raw=1" width="200" height="160">

# # Summary
# 
# ### Here is the full set of instructions of 1#:
# 
# 
# | Instruction      | Meaning |
# | ----------- | ----------- |
# | 1^n #      | Add 1 to Rn       |
# | 1^n ##   | Add # to Rn      |
# | 1^n ###   | Go forward n instructions     |
# | 1^n ####   | Go backward n instructions     |
# | 1^n #####   | Cases on Rn |
# 
# All numbers in this chart are written in unary.
# Registers are processed as queues: symbols enter on the right and exit on the left.
# 
# The first two types of instructions add symbols to the right ends of the registers.
# 
# Here is a review of how the case instruction ```1^n #####``` works.
# 
# If Rn is empty, we go to the very next instruction.
# 
# If the first symbol of Rn is 1, we delete that symbol and go to the second instruction after the case instruction.
# 
# If the first symbol of Rn is #, we delete that symbol and go to the third instruction after the case instruction.
# 

# ### Useful command-line tools
# 
# | Instruction      | Meaning |
# | ----------- | ----------- |
# | ```onesharp(p,[r1, . . .,rn])``` | runs the program ```p``` on the list of words  ```[r1, . . .,rn]```     |
# | ```step_by_step(p,[r1, . . .,rn])```   | parses p and shows all steps in the run  |
# | ```parse(p)```  | expresses ```p``` as a list of instructions    |
# | ```parse_explain(p)```   | gives a table of the parse with glosses     |
# | ```unparse(p)```   | inverse of ```parse(p)``` |
# 

# ### Useful operations inside a Jupyter notebook
# 
# 1. Show the Table of Contents.
# 
# 2. Stop a program that is either in an infinite loop or otherwise is going too long.
# 
# 3. Insert code cells above or below the current cell.
# 
# 4. Insert text cells above or below the current cell.
# 
# 5. Add a comment to a cell using # as the first character in a line.
# 
# 6. Moving a cell up or down in the notebook.
# 
# 7. Delete a cell.
# 
# 8. Open a new notebook.  
