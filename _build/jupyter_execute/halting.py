#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lmoss/onesharp/blob/main/halting.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # How programs "halt"
# 
# 1# has programs with infinite loops such as 
# 
# ```1###1####```
# 
# This program never finishes. Most of the time, we are interested in programs which do finish. Actually, we are interested in programs which finish in a special way.
# 
# We say that a program p *halts* if at some point during the execution of p, the control transfers to right below the last instruction of p. In more detail, suppose that p has n instructions. The formal definition is given below, after we discuss the remaining types of instructions.
# 
# In contrast, we say that p *stops improperly* if at some point during the execution of p, the control tranfers either to a point before the beginning of p or to points more than one instruction beyond the last instruction of p.
# 
# To see the difference, consider the following two programs:
# ```11###``` and ```1#```
# 
# The first says 
# "Go forward 2,"
# and the second 
# "Add 1 to R1."
# 
# 
# The first halts, while the second stops improperly.
# 
# 

# ### Exercise 1 
# 
# Which of the following programs halt when run on all empty registers? Which stop improperly? Why?
# 
# 1. 11###111###1####
# 
# 2. 11###111###11####
# 
# 3. 11###111###111####
# 
# 4. 1111###1111###1####11###11####
# 
# [It would be better to try to solve this problem without running the programs.]

# ## Exercise 2
# 
# Exercise 1 was concerned with programs run on all empty registers.  Find a program $p$ and words $w_1$, $w_2$, and $w_3$ so that 
# 
# (a) When started with $w_1$ in R1, $p$ halts improperly.
# 
# (b) When started with $w_2$ in R1, $p$ halts improperly.
# 
# (c) When started with $w_3$ in R1, $p$ goes into an infinite loop inside $p$.

# ### Halting: the formal definitions
# 
# There are five ways that p could halt.
# 
# 1. Instruction n of p (the last instruction) is of the form ```1```<sup>$k$</sup>```#``` or ```1```<sup>$k$</sup>```##```, and at some point in the run of p, we reach this last instruction.
# 
# 2. Some instruction of p, say instruction number i, is of the form ```1```<sup>$k$</sup>```###```; and also i + k = n + 1; and finally that at some point in the run of p, we reach instruction i.
# 
# 3. Instruction n of p (the last instruction) is of the form form ```1```<sup>$k$</sup>```#####```, and at some point in the run of p, we reach this last instruction with Rk empty.
# 
# 4. Instruction n-1 of p (the next-to-last instruction) is of the form form ```1```<sup>$k$</sup>```#####```, and at some point in the run of p, we reach this instruction with Rk containing a word beginning with 1.
# 
# 5.  Instruction n-2 of p (the second-to-last instruction) is of the form form ```1```<sup>$k$</sup>```#####```,and at some point in the run of p, we reach this instruction with Rk containing a word beginning with #.
# 

# # Tidy programs
# 
# We next come to an important definition concerning programs. 
# 
# Here are some examples of what we are after.  if the last line of a program $p$ is ```1#```, then that line transfers control outside of $p$, but only one line below the end. On the other hand, if a program $q$ has exactly $10$ lines, then we do not want line $8$ to be ```1111###```, since executing this line would take us to "line 12".  So a run of $q$ which reached line $8$ would not halt.
# We would prefer to rewrite $q$ to point to an infinite loop inside of the program.
# (There are reasons that we prefer programs to have explicit infinite loops instead of pointing to unwanted places.  One such reason appears in Exercise 4 below.  Other reasons for this preference will be revealed in due course.) What we are after here is a formal definition of tidiness, something that we will frequently use.
# 
# We say that a program $p$ is *tidy* if no instruction can possibly take us outside the program, except for going "one instruction below the end" of $p$.  
# 
# Here is the formal definition:  Suppose that $p$ has $N$ lines.  Here are the requirements for $p$ to be tidy:
# 
# (a) If line $i$ is a forward transfer instruction 
# ```1```<sup>$k$</sup>```###```, then $i +k \leq N+1$.
# 
# (b) If line $i$ is a backward transfer instruction ```1```<sup>$k$</sup>```####```, then $i-k \geq 1$.
# 
# (c) If line $i$ is a case instruction ```1```<sup>$k$</sup>```#####```, then $k+2 \leq N$.
# 
# Here is a comment on condition (c).
# Suppose that $p$ had $N$ lines, and line $N$ were a case instruction
# ```1```<sup>$k$</sup>```#####```. If Rk stared with a ```#```, then executing ```1```<sup>$k$</sup>```#####``` would take us to line $N+3$, and there is no such line.
# For the same reason, lines $N-1$ and $N-2$ cannot be case instructions.
# 
# 

# ### Strong equivalence
# 
# Programs $p$ and $q$ are *strongly equivalent* if for all $n$ and all sequences $w_1, w_2, \ldots, w_n$ of words, running $p$ with inputs $w_1, w_2, \ldots, w_n$ and running $q$ with the same inputs would do the same thing: one of these would halt if and only if the other halted, and in this case the contents of all registers at the end is the same for both programs.

# #Strong equivalence to tidy programs
# 
# *Proposition* 
# Every program is strongly equivalent to a tidy program.

# ## Exercise 3
# 
# Prove this proposition. (Alternatively, write a program in either Python or 1# which found a tidy version of an input program.)

# ## Exercise 4
# 
# If $p$ is tidy, show that $p$ is strongly equivalent to any program of the form
# 
#  ```1###``` ```1###``` $\cdots$ ```1###``` ```p``` ```1###``` ```1### ```$\cdots$ ```1###```
# 
# Show that all three parts of the definition of tidiness are needed in order to show this fact.  
# 
