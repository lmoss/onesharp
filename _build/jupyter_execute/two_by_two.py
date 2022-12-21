#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lmoss/onesharp/blob/main/two_by_two.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Two-by-Two Encoding
# 
# This notebook shows that every 1# program may be modified to get a program with the special feature that when it runs, the case statement 1##### is never called on an empty R1.  (This technical feature will be put to use later, when we prove the undecidability of Post's Correspondence Problem).
# 
# The work here also is a good illustration of the use of the Sanity tool.

# In[1]:


#@title
get_ipython().system('python -m pip install -U setuptools')
get_ipython().system('python -m pip install -U git+https://github.com/lmoss/onesharp/')
from onesharp.interpreter.interpreter import *
from onesharp.tools.sanity import *


# The two-by-two encoding takes the symbol 1 and replaces it by 11, and the symbol # and replaces it by 1#.  Then a word in a given register is replace by the letter-by-letter encoding, followed by an "end of register" marker ##.   For example, if R1 has 1#1, then we encode this by 111#11##.  
# 
# We want to translate programs into ones which work on the encoded words, and we want to be sure that the translated programs have the feature that we are looking for. The basic idea in the programs below is that we can grab the symbols in R1 in a "two-by-two" fashion, and since we have an "end-of-register" marker ##, we will never do a case statement on an empty register.
# 
# For simplicity, we are going to work only with programs that are tidy and which only use R1, and which are then run on all empty registers.  This is what we need for the later use of this encoding, and these conditions could be relaxed a bit.
# 

# ## Encoding and decoding register 1
# 

# In[2]:


decode_idea = [ # this is sanity code for decoding an encoded R1
    ['top', 'cases', 1, 'empty', 'found_a_one', 'found_a_sharp'],
    ['empty','1###'],
    ['found_a_one', 'cases', 1, 'empty', 'one_one', 'one_sharp'],
    ['found_a_sharp', 'cases', 1, 'empty', 'empty', 'sharp_sharp'],
    ['one_one', '1#'],
    ['goto', 'top'],
    ['one_sharp', '1##'],
    ['goto', 'top'],
    ['sharp_sharp', 'goto', 'end']
]
decode = sanity(decode_idea)
#onesharp(decode,['111###'])

def atomic_replace(x):
  if x == '1':
    return '11'
  if x == '#':
    return '1#'
    
def encode(w):
  a = [atomic_replace(x) for x in w]
  b = unparse(a)
  c = b + '##'
  return(c)        


# ## Changing the instructions ```1#``` and ```1##``` 

# In[3]:


two_by_two_addone_idea = [ # this is sanity code for 1#, run on encoded R1
    ['top', 'cases', 1, 'empty', 'found_a_one', 'found_a_sharp'],
    ['empty','1###'],
    ['found_a_one', 'cases', 1, 'empty', 'one_one', 'one_sharp'],
    ['found_a_sharp', 'cases', 1, 'empty', 'empty', 'sharp_sharp'],
    ['one_one', '1#1#'],
    ['goto', 'top'],
    ['one_sharp', '1#1##'],
    ['goto', 'top'],
    ['sharp_sharp', '1#1#1##1##'], ## note that the 1#1# adds 11 before the end
    ['goto', 'end']
]

two_by_two_addone = sanity(two_by_two_addone_idea)

two_by_two_addsharp_idea = [ # this is sanity code for 1##, again run on encoded R1
    ['top', 'cases', 1, 'empty', 'found_a_one', 'found_a_sharp'],
    ['empty','1###'],
    ['found_a_one', 'cases', 1, 'empty', 'one_one', 'one_sharp'],
    ['found_a_sharp', 'cases', 1, 'empty', 'empty', 'sharp_sharp'],
    ['one_one', '1#1#'],
    ['goto', 'top'],
    ['one_sharp', '1#1##'],
    ['goto', 'top'],
    ['sharp_sharp', '1#1##1##1##'], ## note that the 1#1## adds 11 before the end
    ['goto', 'end']
]

two_by_two_addone = sanity(two_by_two_addone_idea)

two_by_two_addsharp = sanity(two_by_two_addsharp_idea)


# ## Changing the transfer instructions

# In[4]:


def numbered(parsed): ## words on a parsed program
  n = len(parsed)
  x = [['a'+str(i+1),parsed[i]] for i in range(n)]
  return(x)

def resolve_transfer(program,instruction,index): # for use on an instruction in a numbered, parsed program  
  if instruction_type(instruction[1]) == 'forward':
     offset = len(instruction[1]) - 3
     #return([instruction[0], 'goto', str(index+offset)])
     if index+offset -1 == len(program):
       return([instruction[0], 'goto', 'end']) # note the special handling here
     else:
       return([instruction[0], 'goto', program[index+offset-1][0]])
  if instruction_type(instruction[1]) == 'backward':
     offset = len(instruction[1]) - 4
     return([instruction[0], 'goto', program[index-offset-1][0]])   
  else:
     return(instruction)   

def resolve_all_transfers(parsed): #for use on a parsed, numbered program 
  k = len(parsed)
  answer = [resolve_transfer(parsed,parsed[i-1],i) for i in range(1,k+1)]
  return(answer)

def replace_add_instruction(x):
  if x[1] == '1#':
    return([x[0],two_by_two_addone])
    ## this had been   return(two_by_two_addone])
    # but due to the fact that sanity expects 
    # input like ['1#1##'] rather than ['4', '1#1##'], the numbers are out
  elif  x[1] == '1##':   
    return([x[0],two_by_two_addsharp]) 
  else:
    return(x)

def replace_all_add_instructions(parsed): #for use on a parsed, numbered program 
  answer = [replace_add_instruction(i) for i in parsed]
  return(answer)


# ## Changing the case instruction ```1#####```, and the overall modification program

# In[5]:


def modify(p): # this modifies a program
  # onesharp(onesharp(modify,[p]),[encoded(x)]) = encoded(onesharp(p,[x]))
  p_one = parse(p)
  p_two = numbered(p_one)
  p_three =  resolve_all_transfers(p_two) 
  p_four =replace_all_add_instructions(p_three)
  N = len(p_four)
  temp = []
  r = p_four
  #print(r)
  for i in range(N):
    #print(r[i])
    if r[i][1] == '1#####':
       temp = temp +  [[r[i][0], 'cases', 1, str(i)+'empty', str(i)+'found_a_one', str(i)+'found_a_sharp'],
       [str(i)+'empty','1###'],
       [str(i)+'found_a_one', 'cases', 1, str(i)+'empty', str(i)+'one_one', str(i)+'one_sharp'],
       [str(i)+'found_a_sharp', 'cases', 1, str(i)+'empty', str(i)+'empty', str(i)+'sharp_sharp'],
       [str(i)+'one_one', 'goto', r[i+2][0]],
       [str(i)+'one_sharp', 'goto', r[i+3][0]],
       [str(i)+'sharp_sharp','1##1##'], # key point! return end marker to R1
       ['goto', r[i+1][0]]]
    else:
       temp = temp + [r[i]]
  #print(temp)
  #print(len(temp))   
  #print()
  #return(temp)
  santemp = sanity(temp)
  return(santemp)


# ## Testing our work

# In[6]:


# this checks that everything works correctly

mod_diag = modify(diag)
#print(mod_diag)
w = encode('1#1##')
x = onesharp(mod_diag,[w]) 
y = onesharp(decode, [x])
print(y)
print(onesharp(diag,['1#1##']))


# In[ ]:




