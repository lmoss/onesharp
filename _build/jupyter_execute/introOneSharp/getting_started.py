#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lmoss/onesharp/blob/main/introOneSharp/getting_started.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# ## First steps
# 
# To start, either download this notebook and run it locally, or else click on 'Open in Colab' above.  Then click on the triangle below.  

# In[ ]:


get_ipython().system('python -m pip install -U setuptools')
get_ipython().system('python -m pip install -U git+https://github.com/lmoss/onesharp.git@main')
from onesharp.interpreter.interpreter import *


# Welcome to our first tutorial lesson on $\one\hash$. You will learn the basics of the language here and also see some small programs.
# 
# This lesson is written on a lower level than the lessons which come after it. The only abstract concept comes at the end, as does the only and mathematical notation. The rest of the lesson is a concrete introduction to $\one\hash$.
# 
# If you are familiar with any machine model in the theory of computations, such as Turing Machines, or classical register machines, you probably will want to skim through this lesson quickly.
# 
# But this introductory lesson is really intended for people with no background on these matters. If this is you, please work slowly, doing the exercises as you go.
# 

# To begin, here is an *interpreter* for $\mathtt{1\#}$.  Even before learning how the language works, we want to see how to run programs by entering them into the interpreter along with inputs.

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
R1 = '#11###1' #@param {type:"string"}
R2 = '11111#' #@param {type:"string"}
#R3 = '' #@param {type:"string"}

## For more registers, add lines here like
## R4 = '' #@param {type:"string"}
## You also must modify the definition of 'a' below accordingly.

# First, we delete the last batch of empty registers
# to simplify the output 
a = [R1,R2]
a = [remove_multiple_blanks(x) for x in a]

onesharp(program,a)


# The top line of the interpreter contains the following *program* of $\one\hash$:
# 
# ```11#####111111###111###1##1111####1#111111####```
# 
# The other two lines are the *inputs* to two *registers*.  Those inputs are the same kind of mathematical object as the program: they are *words* on the alphabet $\set{\one,\hash}$.  In this book, words are just sequences  composed of the symbols ```1``` and ```#```, such as ```11###11#1``` and ```#1###1###111#11```.  We'll have more to say about and programs soon.  But for now, modify the inputs to R1 and R2, but keep the program the same.   Click on the arrow to run the program on the inputs, and look at the *output* below the interpreter.
# 
# Another way to run the program is to type shift-return on a keyboard. The output is shown below the interpreter, above the current cell.
# 
# 
# The empty word is a perfectly good word, so you could also enter it into R1 or R2 just by leaving the register blank or by entering one or more spaces.
# 
# You can modify $\Rone$ and $\Rtwo$ as many times as you like.
# 
# What you should find after doing this is that the output is the input in $\Rone$ followed by the input in $\Rtwo$. We usually will say *concatenated* instead of *followed by*.
# 
# ---
# 
# The overall point is that the program ```11#####111111###111###1##1111####1#111111####``` may be run on words which are input in the registers. This program does not change when we run it.  Our little interpreter didn't show the step-by-step behavior of the register machine, it only showed the final output.   We'll return to the soon, after we understand what the program is doing.  It turns out that this program is composed of seven instructions. We'll get to the instructions soon, but first we have an exercise for you to try.

# ```{exercise}
# Here is another 1# program. It takes its input from the first two registers. Enter some words in R1 and R2 input boxes, and then run the program. Your job is to try to figure out what the program does.
# 
# ```1##### 11111111### 1111### 111## 1111## 11111#### 111# 1111# 11111111#### 111##### 111111### 111### 1## 1111#### 1# 111111#### 1111##### 111111### 111### 1## 1111#### 1# 111111#### 11##### 111111### 111### 1## 1111#### 1# 111111####```
# ```

# ## The $\mathtt{1\#}$ instruction set
# 
# We are going to present the full set of instructions of $\one\hash$.  There are five instruction types.  
# 
# ```{attention} 
# When we use superscripts and write, for example,  $\one^k \hash^{\ell}$ we mean $k$ copies of the symbol $\one$ followed by $\ell$ copies of the symbol $\hash$.  For example,
# 
# $
# \one^{15}\hash^4$ abbreviates $\one\one \one \one \one \one \one \one \one \one \one \one \one \one \one \hash\hash\hash\hash 
# $.
# ```

# So far, we have seen two *programs* of $\mathtt{1\#}$. Programs are composed of *instructions*. In fact, programs are just sequences of instructions run together. There are only five kinds of $\mathtt{1\#}$ instructions.  Now is the time to introduce them.
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
# These instructions add a $\mathtt{1}$ to the end of the word (the right end, as in English words) in the specified register.
# 
# 
# | Instruction      | Meaning |
# | ----------- | ----------- |
# | 1##      | Add # to R1       |
# | 11##   | Add # to R2      |
# | 111##   | Add # to R3      |
# 		
# 
# These add a $\mathtt{\#}$ to the end (again, this means the right side) of the word in the specified register.  We can summarize the two kinds of instructions which we have seen, and also extend them:
# 
# | Instruction      | Meaning |
# | ----------- | ----------- |
# | 1^n #      | Add 1 to Rn       |
# | 1^n ##   | Add # to Rn      |
# 
# The programs of $\mathtt{1\#}$ are just sequences of instructions run together.  There is no punctuation between the instructions.  To move around in a program, we have two other kinds of instructions
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
# If the first symbol of Rn is $\mbox{\mathtt{1}}$, we delete that symbol and go to the second instruction after the case instruction.
# 
# If the first symbol of Rn is $\hash$, we delete that symbol and go to the third instruction after the case instruction.
# 
# The 'cases' instructions are the most complex to understand, and it will help to look an example in detail.   But first we have some exercises on the 1^n# and 1^n## instructions.

# ```{exercise}
# :label: try-to-figure
# Again, start with $\mathtt{1}$ in R1 and R2, $\mathtt{1\#}$ in R3, and the other registers empty.
# What happens in each register if we run
# $\mathtt{111\#\#}$?
# Try to figure this out for yourself, and then check your work by actually running the program.
# ```

# ```{exercise}
# As before, start with $\one$ in R1 and R2, $\mathtt{1\#}$ in R3, and the other registers empty.
# What happens in each register if we run the same program 
# $\mathtt{111\#\#}$ from the previous exercise?
# ```

# ```{exercise}
# Write a program which, when started with all registers empty, gives $\mathtt{1}$ in R1 and R2, $\mathtt{1\#}$ in R3, and the other registers empty.
# ```

# <img src="https://github.com/lmoss/onesharp/blob/main/harp.jpg?raw=1" width="200" height="160">

# # What are programs?
# 
# ```{important}
# A *program* is a sequence of instructions run together.
# ```
# 
# We have already been using this terminology.  For example, we saw
# 
# 11#####111111###111###1##1111####1#111111####
# 
# near the top of this notebook.  This is the following sequence of instructions:
# 
# 11##### 111111### 111### 1## 1111#### 1# 111111####
# 
# Dividing a program into instructions is a very easy form of *parsing*.  In a real computer language, parsing is more difficult than it is for $\one\hash$.  
# 
# Incidentally, spaces are not significant in the interpreter above, or in the work we'll turn to shortly.  You may enter programs with spaces.
# 
# Let us emphasize something about programs.
# 
# ```{important}
# Any sequence of $\one\hash$ instructions is a program. A program doesn't come with an explanation of what "it is supposed to do".
# ```
# 

# ```{important}
# Words have to be *finite*, and so programs also must be finite.  Further, each program $p$ of $\one\hash$ can only mention finitely many registers. 
# 
# (That is, there is a finite set $F\subseteq \N$ such that if
#  $\one^k \hash$ is an instruction in $p$, then $k\in F$;
# if  $\one^k \hash\hash$ is an instruction in $p$, then $k\in F$;
# and  $\one^k \hash^5$ is an instruction in $p$, then $k\in F$.)
# ```

# # Running programs in notebook cells
# 
# Because notebooks like this are composed of cells, we also want to run programs in a command-line fashion.
# 
# There are two programs that do this.  They are 
# ```step_by_step``` and ```onesharp```.  These are illustrated in the next two cells.  Both of these programs are written in Python, not in $\mathtt{1\#}$.  They both require as inputs a $\mathtt{1\#}$ program followed by a sequence of register words.

# In[ ]:


onesharp('1#11#####1###1###',['1#1','#'])


# In[ ]:


step_by_step('1#11#####1###1###',['1#1','#'])


# The last computation started with two inputs.  Try changing those inputs to see what happens.  As practice with the definition of *halt*, you might try yourself to predict what will happen before running it.  You can add the symbols $\mathtt{1}$ or $\mathtt{\#}$, and you also can delete symbols.  But you should not delete the quote marks.  Also, you can change the program the same way.   The idea is that you should explore this function *step_by_step* by trying it out on simple inputs.  

# Here is an explanation of the form of the command ```step_by_step``` that we have been using.   
# 
# The first argument could be a $\mathtt{1\#}$ program surrounded by single quotes or double-quotes.   If you use single quotes, you need to be sure to use the correct ones; on my screen they look straight, not slanted.   You could also use a concatenation of quoted expressions (see below).  But if you forget the quotes, you will get an error because the Python program that is running all of this will balk at $\mathtt{1\#}$ expressions without quotes around them.
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
# The program ```step_by_step``` begins with a parse of your program, and so if you input a word that is not a sequence of $\one\hash$ expressions, it will stop without further ado.
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

# # The full set of instructions of 1#
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
# If the first symbol of Rn is $\mathtt{1}$, we delete that symbol and go to the second instruction after the case instruction.
# 
# If the first symbol of Rn is $\mathtt{\#}$, we delete that symbol and go to the third instruction after the case instruction.
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
# 1. Show the Table of Contents, and also hide it.
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
