#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lmoss/onesharp/blob/main/self_writing.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Self-Replicating Programs
# 
# A self-writing replicating program is one which outputs itself, starting with all registers empty.
# At first blush it seems paradoxical that such programs would exist: there is no direct way to get the ```1#``` interpreter to spit out the program that is inside it. And anyways, it would seem that typically, a program is usually longer than its output. So how can a program output itself? This lesson shows how it is done. Even more, it will show you how such programs work and give you a chance to try your hand at writing related programs.
# 
# In order to get a program which writes itself, one must use some sort of trick or clever idea. Our goal is to explain one such clever idea, and then to see other applications of it as we go. Before you understand it, the idea will seem to be a trick, or even a fluke: we have a program, and it just so happens to output itself. But as we come to understand it better, the trick becomes tamed into a general method.
# 
# At the root of our work is something we've seen in the last lesson: the ability of ```1#``` programs to write and modify other programs.
# 
# 
# 

# In[1]:


get_ipython().system('python -m pip install -U setuptools')
get_ipython().system('python -m pip install -U git+https://github.com/lmoss/onesharp.git@main')
from onesharp.interpreter.interpreter import *


# <img src="https://github.com/lmoss/onesharp/blob/main/drum.jpg?raw=1" width="200" height="160">

# ## Diag
# 
# We begin with a program which we'll call ```diag```. When ```diag``` is run with a word x in R1, the result is 
# 
# 
# [$\![[{\tt write}]]\!$] (x) + x
# 
# Running that last program on all empty registers gives the same thing as running x on itself:
# 
# $[\![$ ```x``` $]\!]$(```x```)
# 
# in R1, assuming that
# $[\![$ ```x``` $]\!]$(```x```)
#  is defined.
# 
# 
# 

# Here is the program ```diag```:

# In[2]:


#@title
j = [['1#####', 'cases on R1', 0],
 ['11111111111###', 'go forward 11 to instruction 13 (the start of move_3_1)', 1],
 ['111111###', 'go forward 6 to instruction 9 (the tan part)', 2],
 ['11##', 'R1 started with #: add # to R2', 3],
 ['111#', 'add 1 to R3', 4],
 ['111##', 'add # to R3', 5],
 ['111##', 'add # to R3', 6],
 ['1111111####', 'go backward 7 to instruction 1', 7],
 ['11#', 'R1 started with 1: add 1 to R2', 8],
 ['111#', 'add 1 to R3', 9],
 ['111##', 'add # to R3', 10],
 ['1111####', 'go backward 4 to instruction 8', 11],
 ['111#####', 'move_3_1 (from the first lesson)', 12],
 ['111#####', 'move_2_1 (from the first lesson)', 13]
 ]

 
df = pd.DataFrame(j,columns=["instruction", 'explanation','number'])
df.index = np.arange(1, len(df) + 1)
df.style.set_properties(**{'border': '1.3px solid green',
                          'color': 'magenta'})
n = len(df.columns)
df.style.set_properties(**{'text-align': 'left'})
df.drop('number', axis=1) # !!! we want this!
#df.style.apply(lambda x: ["background-color: red"]*n if x['instruction']== 'Reading' else ["background-color: white"]*n, axis = 1)
#df.style.apply(lambda x: ["background-color: #B0E0E6"]*n if x['instruction'] in ['1##','1111####'] elif ["background-color: #D4B48C"]*n if x['instruction'] in ['1#','111111####'] else ["background-color: #FFFFCC"]*n, axis = 1)
df.style.apply(lambda x: ["background-color: #B0E0E6"]*n if x['instruction'] in ['1##','1111####']  else ["background-color: #FFFFCC"]*n, axis = 1)

df.style.hide_columns('number')
df.style.apply(lambda x: 
               ["background-color: #B0E0E6"]*n if x['number'] in [3,4,5,6,7] 
               else ["background-color: tan"]*n if x['number'] in [8,9,10,11]
               else ["background-color: #FFFFCC"]*n, axis = 1)


# 
# The three branches of the case instruction at the top take us to move3,1 (if R1 is empty), to the blue sub-program if the first symbol of R1 is a 1, and to the brown sub-program if that symbol is a #. Note that we have a big loop that takes symbols off of R1 and writes the same thing in R2 and some related words in R3. The way that the words in R3 are related to the original input in R1 is as follows: each time a 1 is removed from R1, what goes into R3 is the program which would write a 1 in R1 (this is 1#). And each time a # is removed from R1, what goes into R3 is the program which would write a # in R1 (this is 1##).
# 
# It might help to say things a bit differently on this. So here is an informal description of what diag is doing:
# Move x from R1 into R2, and also put $[\![write]\!]\!](x)$ in R3.
# Then 
# move R3 back to the now-empty R1.
# Finally, move R2 onto the end of R1.
# The official version of ```diag``` is a very slightly shortened version of this. 
# 
# The tables below show the important feature of ```diag```. You should memorize it as soon as possible for use below and in the next lesson.
# 
# Running ```diag``` on a word ```x``` and then running that on the empty register yields the same thing as running ```x``` on iself.
# 

# <img src="https://github.com/lmoss/onesharp/blob/main/basses.jpg?raw=1" width="200" height="160">

# ## Self
# 
# We now define a self-writing program, ```self```.
# 
# The idea is to apply the program ```diag``` to diag itself.
# This might seem like a strange thing to do. But as we'll see, it gives us exactly what we're looking for.
# When we run ```diag``` on itself, we get $\phi_{write}(```diag```) + ```diag``` in R1.
# This, then, is ```self```: the program which would write out ```diag``` followed by ```diag``` itself.
# 
# So when we run ```self``` on nothing, we first spell out diag into R1.
# After this, we run ```diag```. Notice that we aren't running ```diag``` on empty registers, because at this point R1 contains ```diag```.
# But running ```diag``` on ```diag``` gives us ```self```, by definition.
# 
# So we conclude that running ```self''' on nothing gives ```self```, as desired.
# 
# To summarize: running ```self``` on nothing is the same as running ```diag``` on ```diag``` itself; and this is ```self```. In symbols, That is,
# 
# $[\![\mbox{self}]\!]( \ ) = [\![ \mbox{diag} ]\!(\mbox{diag}) = \mbox{self}$.
# 
# 
# 

# In[3]:


self


# In[4]:


onesharp(self,[])


# In[5]:


onesharp(self,[])== self


# The run of ```self``` on empty registers takes 14,204 steps to output itself.

# # The idea in English
# 
# We offer another presentation of the idea behind diag and self.
# 
# Let's suppose that you want to write a self-replicating program, say s, from scratch.
# 
# Let's say that you just have on glimmer of an idea, that s should be of the following form:
# 
# First, a program x should be written to R1.
# 
# Second, a program y should be run (with x in R1 and everything else empty).
# 
# So running x on nothing will give &phixy in R1 at the end.
# 
# We therefore want to find s, x, and y so that
# 
# s= φwrite(x) + y, φs( ) = φx(y )
# and
# φx(y) = s
# We are free to find any s, x, and y that we like that meets these requirements. Wouldn't it be nice if x = y? So why don't we just try to find s and x so that
# 
# s= φwrite(x) + x,
# and also
# φx(x) = s
# Now it is clear that if we find x we then can determine s automatically, using the first equation. We only need to have x be a program with the property that
# 
# φx(x) = φwrite(x) + x,
# But again, we are free to make x be any program we like. We might as well make x have the property that for all z,
# 
# φx(z) = φwrite(z) + z,
# since if we do this, then it automatically will hold that φx(x) = φwrite(x) + x.
# 
# And now things are much easier. It is not hard to write x so that φx(z) = φwrite(z) + z for all z; this is diag.
# Finally, the reasoning we did in this small discussion shows that we can get a self replicating program by setting s = φx(x).

# <img src="https://github.com/lmoss/onesharp/blob/main/harp.jpg?raw=1" width="200" height="160">

# # Exercises
# 
# 
# The rest of this lesson consists of exercises that allow
# you to firm up your understanding of the basic ideas
# in ```diag``` and ```self``` by elaborating on 
# and extending them.
# 
# In all of these exercises, you are invited
# to check your work on the interpreter.

# ## Exercise 1
# 
# If x and y are words, let's think about 
# [ [```diag```] (```x```)] (```y```).  Is it [[ ```x``` ]](```x + y```), or 
#  [[ ```x``` ]](```y + x```)?
# 

# ## Exercise 2
# 
# Write a program which when started on all empty registers
# writes itself to R1 and also writes # to R2.
# 
# 

# ## Exercise 3
# 
# Write a program p which when started on all empty registers
# doesn't 
# write itself to R1 but rather writes itself followed by a #.
# In other words, $\phi_p(\ ) = p + \#$.
# 

# ## Exercise 4
# 
# Find an infinite sequence of programs which are all different with the property that each program in the list
# writes the next one in the list into R1.

# ## Exercise 5
# 
# Write a program p which when started on all empty registers
# doesn't 
# write itself to R1 but rather writes itself preceded by a #.
# In other words,
# $\phi_p(\ ) = \# + p$.

# ## Exercise 6
# 
# Write a self-replicating  program 
# that begins with the program to transfer ahead
# one instruction, ```1###```.

# ## Exercise 7
# 
# Write a program s which, when run with R2, R3, etc.
# empty,  ends up with R1 containing s *after* whatever
# happened to be in R1 at the start.
# In other words, for all words y,
# $\phi_s(y) = y + s$
# 

# ## Exercise 8
# 
# Write a program```selfknow```  with the property that when run with
# a string q in R1, 
# ```selfknow```  runs and halts with q in R1 if q=
# ```selfknow```, and runs and halts with ```#``` in R1 empty if q is not 
# equal to ```selfknow```.
# (So this program ```selfknow``` "knows itself".)

# ## Exercise 9
# 
# Write a program ```trade```
#  which trades places with its input in R1.
# That is, running ```trade```  with p in R1
# and all other registers empty does the same thing
# as running p with ```trade``` in R1 and all other
# registers empty.
# 
# [You will probably want to work through some later lessons
# before attempting this problem.  But it might be fun to try now.] 

# ## Exercise 10
# 
# Write two "twin'' programs s and t with the properties
# that s and t are different programs;
# running s with all registers empty gives t in R1; and 
# running t with all registers empty gives s in
# R1.

# In[ ]:




