#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lmoss/onesharp/blob/main/introOneSharp/haltDef.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# ## When does a program halt?
# 
# $\one\hash$ has programs which contain *infinite loops* such as
# 
# 1###1####
# 
# This program never finishes. If you run this in an interpreter, you will need to figure out how to stop the execution.    Most of the time, we are interested in programs which do finish. Actually, we are interested in programs which finish in a special way.
# 
# This last example had nothing to do with the words in the input registers before we ran the program.  But usually the input registers make a difference to whether the program halts or not.
# 
# 
# ```{admonition} Definition
# :class: tip
# We say that a program $p$ *halts* on some inputs if at some point during the execution of $p$, the control transfers to right below the last instruction of $p$. In more detail, suppose that $p$ has n instructions. The formal definition is given below, after we discuss the remaining types of instructions.
# 
# In contrast, we say that p *halts improperly* if at some point during the execution of $p$, the control tranfers either to a point before the beginning of $p$ or to points more than one instruction beyond the last instruction of $p$.
# ```
# 
# To see the difference, consider the following two programs: 
# $\one\one\hash\hash\hash$ and $\one\hash$.
# 
# 
# The first says "Go forward 2," and the second "Add $\one$ to R1."
# 
# The first halts, while the second halts improperly.

# ```{exercise}
# :label: on-halting
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
# ````

# ```{exercise}
# {ref}`on-halting` was concerned with programs run on all empty registers.  Find a program $p$ and words $w_1$, $w_2$, and $w_3$ so that 
# 
# (a) When started with $w_1$ in R1, $p$ halts improperly.
# 
# (b) When started with $w_2$ in R1, $p$ halts improperly.
# 
# (c) When started with $w_3$ in R1, $p$ goes into an infinite loop inside $p$.
# ```

# ## Halting: the formal definitions
# 
# There are five ways that the run of a program $p$ on some register contents could halt.
# 
# 1. Instruction $n$ of $p$ (the last instruction) is of the form ```1```<sup>$k$</sup>```#``` or ```1```<sup>$k$</sup>```##```, and at some point in the run of $p$, we reach this last instruction.
# 
# 2. Some instruction of $p$, say instruction number $i$, is of the form ```1```<sup>$k$</sup>```###```; and also $i + k = n + 1$; and finally that at some point in the run of $p$, we reach instruction $i$.
# 
# 3. Instruction $n$ of $p$ (the last instruction) is of the form form ```1```<sup>$k$</sup>```#####```, and at some point in the run of $p$, we reach this last instruction with Rk empty.
# 
# 4. Instruction $n-1$ of $p$ (the next-to-last instruction) is of the form form ```1```<sup>$k$</sup>```#####```, and at some point in the run of $p$, we reach this instruction with Rk containing a word beginning with $\one$.
# 
# 5.  Instruction $n-2$ of $p$ (the second-to-last instruction) is of the form form ```1```<sup>$k$</sup>```#####```, and at some point in the run of $p$, we reach this instruction with Rk containing a word beginning with $\hash$.
# 

# In[ ]:




