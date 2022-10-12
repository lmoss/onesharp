import pandas as pd
import numpy as np
from IPython.display import display

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

def ones(n):
    w = ['1' for i in range(n)]
    return(unparse(w))    

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

