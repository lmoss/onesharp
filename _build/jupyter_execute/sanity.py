#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lmoss/onesharp/blob/main/sanity.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Tools to help write programs

# The main tool here is a Python program called Sanity.
# This tool makes it easier for someone to organize 1# programs and to write them without having to count lines for all of the forward- and backward-transfer statements.
# 
# The concept and the name come from Jon Bowman, who once took my class and felt that construction 1# programs by hand was crazy, and that counting all the 1's in a long expression "made his eyeballs bleed."
# 
# To start, run the next code cell to install the 1# Python package in your Colab environment. Then run the second code cell to import the functions from the 1# package which are used in this notebook.

# In[1]:


get_ipython().system('python -m pip install -U setuptools')
get_ipython().system('python -m pip install -U git+https://github.com/lmoss/onesharp.git@main')


# In[2]:


from onesharp.interpreter.interpreter import onesharp
from onesharp.tools.sanity import sanity
from onesharp.tools.ones import ones
from onesharp.programs.clear import clear
from onesharp.programs.move import move
from onesharp.programs.copy import copy
from onesharp.programs.successor import successor
from onesharp.programs.compare import compare
from onesharp.programs.add import add


# As a way to show what the tool does, we'll go through an example.  Let's write a program that takes a word 
# 
# $$ w = w_1 w_2 \cdots w_n $$
# 
# in R1 and reverses it.  Our program will work as follows.   It processes the letters in $w$ in order, using a loop. At the end of the $i$th iteration, we'll have $w_{i+1}\cdots w_n$ in R1, and its prefix will be in R2 *backwards*: $w_{i}\cdots w_2 w_1$.  
# 
# The $i$th step itself copies $w_i$ into R3, and then, in order to put that symbol on the *front* of $w_{i}\cdots w_2 w_1$, moves R2 on the end of R3, and then R3 back to R2.
# Once we have gone through the original $w$ in this fashion, R1 will be empty, and R2 will contain its reversal.  So we close by moving R2 back to the now-empty R1.
# 
# With this in mind, have a look at the following array 'reverse_idea', itself containing 8 arrays.

# In[3]:


reverse_idea = [
    ['top', 'cases', 1, 'move_back', 'found_a_one', 'found_a_sharp'],
    ['found_a_one','111#'],
    ['goto', 'move_phase'],
    ['found_a_sharp',  '111##'],
    ['goto', 'move_phase'],
    ['move_phase', move(2,3) + move(3,2)],
    ['goto', 'top'],
    ['move_back', move(2,1)]
]


# We have 8 *lines*. But a line is not the same as in instruction: lines 6 and 8 each contain move programs that are bigger than a single instruction.  Lines 2, 4 5, and 6 each begin with a *label*.  Labels are strings that other parts of the program could point to.  For example, the first line is a case statement 1#####, and it also contains the information that if R1 is empty, we should go to whichever line has the label 'move_phase'. (That would be the line named 'move_stuff_around'.) The first line also tells us that if R1 begins with 1 we should (delete is and) go to the line containing 'first-is_one'.   Note also that 'goto' is not a label.  
# 
# Here is how these lines are used:
# 
# 

# In[4]:


rev = sanity(reverse_idea)
# This run 'sanity' on 'reverse_idea', calling the result 'rev'.
# We can refer to it in the rest of this notebook by 'rev'.
# For example we can display our new program
rev


# Now the program which we just constructed can be run, as usual:

# In[5]:


onesharp(rev,['1####'])


# In[6]:


# Here is a way to write the program 'clear_1':
sanity([
    ['top', 'cases',1,'empty', 'one','hash'],
    ['empty', 'goto', 'end'],
    ['one','goto', 'top'],
    ['hash', 'goto', 'top'],
])


# Notice that in the last examples we had a line
# 
#    ['empty', 'goto', 'end']
# 
# In this, 'end' is not a label in any of the four lines.
# Indeed, 'end' is a special string in this program.   We can use 'end' in connection with 'goto', and also in one of the branches of a 'cases' statement.
# 
# Other things to know: instead of (for example) 11#, we can write it in words as in the third line below.   Finally, all numbers in this program must be entered without quotes.

# In[7]:


d = [
    ['top','cases',1,'empty', 'one','hash'],
    ['empty', 'goto', 'moveback'],
    ['one', 'add1', 2],
    ['111#111##'],
    ['goto', 'top'],
    ['hash', 'add#', 2],
    ['111#111##111##'],
    ['goto', 'top'],
    ['moveback', move(3,1)+move(2,1)] 
]
dg = sanity(d)


# In[8]:


onesharp(dg,['11#'])


# ###Summary: here are some examples of 'lines' that the tool can handle:
# 
#     ['top','cases',1,'empty', 'one_found','hash_found'],
#     ['empty', 'goto', 'moveback'],
#     ['one_found', 'add1', 2],
#     ['111#111##'],
#     ['goto', 'top'],
#     ['hash_found', 'add#', 2],
#     ['111#111##111##'],
#     ['goto', 'end'],
#     ['moveback', move(3,1)+move(2,1)]
#   
# A line can be snippet of 1# code surrounded by quotes.  It can also be a Python expression like 
# 
#    move(3,1) + move(2,1)
#    
# that denotes a 1# word.
# 
# A line may begin with a *label* like 'top', or 'moveback' 
# A label should not begin with '1' or '#, and it should not be one of the strings 'goto', 'end', 'add1', or 'add#'.
# 
# *Labels are optional*, except a "cases" instruction
# must have a number and then three labels.  
# 
# A line also can have the word 'goto' followed by a label or 'end'.
# 
# A line can have 'add1' or 'add#' followed by a number (without quotes).
# 
# Every label used inside a 'cases' or 'goto' statement must be the first label in some line.  Otherwise, the program will raise an error.
# 

# ### Two more example Sane programs

# In[9]:


# This code cell contains a Sane program which multiplies the contents of
#   registers one and two and stores the product back into register one

sane_multiply = [
  [move(1,4)],
  ['1##'],
  [copy(2,5,10)],
  ['111##'],
  [copy(3,6,10)],
  [compare(2,3)],
  ['multiply_loop', 'cases', 2, 'empty', 'one', 'sharp'],
    ['empty', copy(4,7,10)],
      [add(1,4,10)],
      [move(7,4)],
      [copy(5,2,10)],
      [successor(6,10)],
      [copy(6,3,10)],
      [compare(2,3)],
      ['goto', 'multiply_loop'],
    ['one', 'goto', 'epilogue'],
    ['sharp', 'goto', 'end'], # We shouldn't reach here because cmp shold never
                              #   write sharp into register two
  ['epilogue', clear(4)],
    [clear(5)],
    [clear(6)]
]
onesharp_multiply = sanity(sane_multiply)
onesharp(onesharp_multiply, ['11', '1#1']) # 11*1#1 = 1111 <==> 3*5 = 15


# In[10]:


# This code cell contains a Sane program which exponentiates the contents of
#   register one to the power of the contents of register two and stores the
#   result back into register one

sane_exponentiate = [
  [move(1,14)],
  [ones(11)+'#'],
  [move(2,12)],
  [copy(12,15,20)],
  [ones(13)+'##'],
  [copy(13,16,20)],
  [compare(12,13)],
  ['exponentiate_loop', 'cases', 12, 'empty', 'one', 'sharp'],
    ['empty', move(11,1)],
      [copy(14,2,20)],
      [onesharp_multiply],
      [move(1,11)],
      [copy(15,12,20)],
      [successor(16,20)],
      [copy(16,13,20)],
      [compare(12,13)],
      ['goto', 'exponentiate_loop'],
    ['one', 'goto', 'epilogue'],
    ['sharp', 'goto', 'end'], # We shouldn't reach here because cmp shold never
                              #   write sharp into register two
  ['epilogue', move(11,1)],
    [clear(14)],
    [clear(15)],
    [clear(16)]
]
onesharp_exponentiate = sanity(sane_exponentiate)
onesharp(onesharp_exponentiate, ['11', '1#1']) # 11^1#1 = 11##1111 <==> 3^5 = 243


# In[11]:


onesharp(onesharp_exponentiate, ['11', '###1']) # 11^###1 = 1####1#11##11 <==> 3^8 = 6561
# 6561 base 2 is 1100110100001


# In[12]:


pre_pred = [
   ['top', 'cases', 1, 'first_end', 'first_one', 'first_hash'],
   ['first_one', 'cases', 1, 'hash_is_it', 'returnA','returnB'],
   ['hash_is_it', '1##'],
   ['goto', 'second_end'],
   ['returnA', '11#11#'],
   [move(1,2) + move(2,1)],
   ['goto', 'end'], 
   ['returnB', '11#11##'],
   [move(1,2) + move(2,1)],
   ['goto', 'end'], 
   ['first_hash', 'cases', 1, 'first_end', 'hash_one', 'hash_hash'],
   ['hash_one','11##'],
   ['hash_hash','1###'],
   ['second_end', '1111#'],
   ['goto', 'end'],
   ['first_end', '111#']
 ]


# In[13]:


onesharp(sanity(pre_pred), ['#1'])


# In[14]:


pred = [
     ['top','cases', 1, 'a', 'b','c'],   
     ['a', 'goto', 'end'],
     ['b', 'cases', 1, 'oe', 'oo', 'oh'],
     ['oe', '1##'],
     ['goto', 'end'],
     ['oo', '11#11#'+move(1,2)+move(2,1)],
     ['goto', 'main'],
     ['oh', '11#11##'+move(1,2)+move(2,1)],
     ['goto', 'main'],
     ['c', 'cases', 1, 'he', 'ho', 'hh'],
     ['he', '1##'],
     ['goto', 'end'],
     ['ho', '11##11#'+move(1,2)+move(2,1)],
     ['goto', 'main'],
     ['hh', '11##11##'+move(1,2)+move(2,1)],
     ['goto', 'main'],    
     ['main', 'cases', 1, 'empty', 'one','hash'],
     ['empty', move(2,1)],
     ['goto', 'end'],
     ['one', '11##'],
     [move(1,2) + move(2,1)],
     ['goto', 'end'],
     ['hash', '11#'],
     ['borrowing', 'cases', 1, 'borrowing_empty', 'borrowing_one', 'borrowing_hash'],
     ['borrowing_empty', move(2,1)],
     ['goto', 'end'],
     ['borrowing_one', '11##'],
     [move(1,2) + move(2,1)],
     ['goto', 'end'],
     ['borrowing_hash', '11#'],
     ['goto','borrowing']
]


# In[15]:


p1 = sanity(pred)


# In[16]:


onesharp(p1,['1#'])


# In[17]:


id = [ ['all_h', 'cases', 1, 'a', 'b', 'c'],
       ['a', '1##'+clear(2)],
       ['goto', 'end'],
       ['b', '11#'],
       [move(1,2)+move(2,1)],
       ['goto', 'end'],
       ['c', '11##'],
       ['goto', 'all_h']
      ]

rectify=sanity(id)


# In[18]:


onesharp(rectify,['##1'])


# In[19]:


pr = p1 + rectify


# In[20]:


onesharp(pr,['1##'])


# In[21]:


pr

