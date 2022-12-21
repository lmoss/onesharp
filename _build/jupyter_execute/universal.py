#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lmoss/onesharp/blob/main/universal.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Universal Programs
# 
# This lesson will teach you about  <i>universal programs</i>:
# these are programs that take 1# programs as inputs and run
# them.  
#  
# 

# To start, enter the following cell:

# In[1]:


#@title
get_ipython().system('python -m pip install -U setuptools')
get_ipython().system('python -m pip install -U git+https://github.com/lmoss/onesharp.git@main')
from onesharp.interpreter.interpreter import *


# In[2]:


u = universal
u


# This program <i>u</i> has the following feature. Let p be any
# program of 1#, or indeed any word on {1,#}. Let x be any word on {1,#},
# including possibly the empty word. Then the following are equivalent: <ol>
# <li> If p is started with all empty registers, then eventually we halt
# with x in R1. <li> If <i>u</i> is started with p in R1 and all other
# registers are empty, then eventually we halt with x in R1. </ol> <br> <p>
# <p>
# This means that <i>if</i> running p on all empty registers
# eventually gives some output in R1 (and all other registers empty),
# then that same output would be the result of running <i>u</i> with p
# in R1 and all other registers empty.
# And in the other direction, <i>if</i> running p with
# all empty registers gives some output, say x,
#  in R1 (and all registers 
# empty
# at the end), then we would get the same output x in R1 
# when we run <i>u</i> with p in R1 and all other registers empty.
# 
# 
# <br><p>
# Here is a specific example of this. Try running <i>u</i> with 1# 1## in
# R1.  The result is 1#, and this is what happens when we run 1# 1## on all
# empty registers.  So the universal program <i>u</i> takes 1# 1## and
# simulates a run of that program. <br> <p> For another example,
#   suppose we start <i>u</i> with <i>self</i> in R1 
# (and all other registers empty).  You can check for yourself that
# we eventually get <i>self</i> in R1. 
# (Note: the computation might take several minutes.)  
# This confirms the basic
# property because running <i>self</i> with all registers empty
# gives <i>self</i>.   
#  <br>
# <p>
# We can even run  <i>u</i> on programs that contain <i>u</i> itself.
# For this, we return to our first example, concerning the word 1# 1##.
# As we know, 
# <br><p><center>
#  &phi;<sub><i>u</i></sub>(1# 1##) = 1#.
# </center><br><p>
# Recall also that 
# <br><p><center>
#  &phi;<sub><i>write</i></sub>(1# 1##) = 1# 1## 1# 1## 1##
# </center><br><p>
# It follows that 
#  <br><p><center>
#  &phi;<sub>1# 1## 1# 1## 1## + <i>u</i></sub>( ) = 1#.
# </center><br><p>
# And from this we conclude that 
# <br><p><center>
#  &phi;<sub><i>u</i></sub>(1# 1## 1# 1## 1## + <i>u</i>) = 1#
# </center><br><p>
# This is something you can try for yourself.   
# 
# 
# 

# <img src="https://github.com/lmoss/onesharp/blob/main/drum.jpg?raw=1" width="200" height="160">

# 
# ### The plan for this lesson
# 
# <p>
# The goal of this lesson is for you to write a universal program
# yourself.   The next sections guide you, using a series of exercises.
# <br>
# <p>
# We hasten to make two remarks: first of all, it would be more
# instructive for you to forget about the rest of this lesson 
# entirely and to just write your own universal program.   But this
#  most readers would probably appreciate the hints and will find
# enough of a challenge in the construction of a long working program.
# Second, the sections to come do not guide you to write a program thatt
# is <i>exactly</i> like <i>u</i> above.   The  <i>u</i> 
# above was designed to be as short as possible.
# In fact, we leave you with a challenge: write a universal
# program with the smallest number of instructions.  The one above has 
# 300.

# ### Simplification
# 
# We are going to simplify the requirements in order to make
# it easier to write a universal program.  So we'll outline how
# to write a program that is <i>close</i> to a universal program,
# but not quite a universal program.
# <p>
# We'll write a program <i>u</i> that acts like a universal
# program, but only for programs which use only R1, R2, and R3.
# In more detail:
#  <br> <p>Let p be any
# program of 1# which only uses R1, R2, and R3.
# Let x be any word on {1,#},
# including possibly the empty word. Then the following are equivalent: <ol>
# <li> If p is started with all empty registers, then eventually we halt
# with x in R1. <li> If <i>u</i> is started with p in R1 and all other
# registers are empty, then eventually we halt with x in R1. </ol> 
# <p>
# Once again, the work of this section sketches a construction of 
# such a program <i>u</i>.   You will need to do much of the work yourself
# in actually getting the program from the sketch.  And even when we
# have <i>u</i>, it will not be quite what we want for this lesson overall,
# because <i>u</i> will only behave right on programs which use the first
# three registers.  
# Later on, we'll come
# back and drop this simplification to get a program which is truly 
# universal.
# <p>
# At this point, we are ready to sketch a method for you to
# write a universal program subject to this simplification.
# <p>
# We are going to use registers as follows:
#  <CENTER>
# <TABLE BORDER  Cellpadding="3">
#  <TR><TD BGCOLOR="#B0E0E6">R1: the input program <i>p</i>  </TD>   </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R2: an instruction number 1<sup>n</sup>
#         </TD>   
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R3: the <i>n</i>th instruction of <i>p</i>    
# </TD>   </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R4: the contents of R1   </TD>   </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R5: the contents of R2  </TD>   </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R6: the contents of R3  </TD>   </tr>
# </table>
# </center>
# <br><p>
# That is, we are going to <strong>simulate</strong> the 
# computation of a register machine on a program p by
# using six registers.   Our universal program <i>u</i> is 
# what does the simulation, and it works step-by-step.  That is,
# <i>u</i> mimics what a register machine would really do.
# The only difference is that one step of a real register machine
# would be done by <i>many</i> steps of our universal program.
# <br><p>
# The registers above hold what is sometimes called a <strong>snapshot
# of a register machine run</strong>. 
# This means that they hold all of the relevant information about a register
# machine computation at one particular point in time: they tell what program is
# running, which instruction would be run next and what number instruction it is,
# and also the contents of all of the registers that the program is using.
# Now a real register machine goes from snapshot to snapshot in <i>one</i> step,
# but the universal machine that we are building will take <i>many</i> steps to
# go from one snapshot to the next.  
# <br><p>
# Our universal program is composed of a few sub-programs.
# We shall illustrate the ideas behind several sub-programs by making a
# large chart.   This chart shows just one example
# of how a universal program could work, when we take
# <i>p</i>
# to be the prorgram <center>
# 1##  + <i>write </i>
# </center>
# <br>
# <p>
# Now to make life easier, we'll write out this program and indicate
# the instruction numbers above them:
# <center>
# <TABLE BORDER  Cellpadding="3">
# <tr>
# <td> 1 </td>
# <td> 2 </td>
# <td> 3 </td>
# <td> 4 </td>
# <td> 5 </td>
# <td> 6 </td>
# <td> 7 </td>
# <td> 8 </td>
# <td> 9 </td>
# </tr>
# <tr BGCOLOR="#FFFFCC">
# <td> 1## </td>
# <td> 1##### </td>
# <td> 111111111### </td>
# <td> 11111### </td>
# <td> 11# </td>
# <td> 11##</td>
# <td> 11##</td>
# <td> 111111####</td>
# <td> 11#</td>
# </tr>
# <tr>
# <td> 10 </td>
# <td> 11 </td>
# <td> 12 </td>
# <td> 13 </td>
# <td> 14 </td>
# <td> 15 </td>
# <td> 16 </td>
# <td> 17 </td>
# <td> 18 </td>
# </tr>
# <TR BGCOLOR="#FFFFCC">
# </td>
# <td> 11##</td>
# <td>111111111####</td>
# <td>11#####</td>
# <td>111111###</td>
# <td>111###</td>
# <td>1##</td>
# <td>1111####</td>
# <td>1#</td>
# <td>111111####</td>
# </tr>
# </table>
# </center>
# <br>
# <p>
# What we are going to show is tables of what the various
# registers show after different parts of a run of a universal program
# <i>u</i> on this program 1## + <i>write</i>.
# We hasten to add that the universal program exhibited above
# does <i>not</i> conform to the tables. (This is because
# registers work differently in it.  Also,  the program
# above is designed to work even without our simplifying
# assumption.)
# <br><p> 
# Here are the tables; we'll have some words below about them.
# <br>
#  <left>
# <TABLE BORDER  Cellpadding="3">
#  <TR><TD BGCOLOR="#B0E0E6">R1: the input program <i>p</i>  </TD>   
# <TD BGCOLOR="#FF8COO">  p  </TD>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <td BGCOLOR="#66FF99">  <i>p</i> </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R2: an instruction number 1<sup>n</sup>
#         </TD>   
# <TD BGCOLOR="#FF8COO"> </TD>
#          <TD BGCOLOR="#F5F5DC">  1 </td>
#          <td BGCOLOR="#66FF99">  1 </td>
#          <TD BGCOLOR="#F5F5DC">  11 </td>
#          <td BGCOLOR="#66FF99">  11 </td>
#          <TD BGCOLOR="#F5F5DC">  11111 </td>
#          <td BGCOLOR="#66FF99">  11111 </td>
#          <TD BGCOLOR="#F5F5DC">  1<sup>6</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>6</sup> </td>
#          <TD BGCOLOR="#F5F5DC">  1<sup>7</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>7</sup> </td>
#          <TD BGCOLOR="#F5F5DC">  1<sup>8</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>8</sup> </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R3: the <i>n</i>th instruction of <i>p</i>    
# <TD BGCOLOR="#FF8COO"> </TD>
#          <TD BGCOLOR="#F5F5DC">   </td>
#          <td BGCOLOR="#66FF99"> 1##  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 1#####  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 11#  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 11##  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 11##  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 1<sup>6</sup> ####    </td>
#    </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R4: the contents of R1   </TD>   
# <TD BGCOLOR="#FF8COO"> </TD>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC"> #   </td>
#          <td BGCOLOR="#66FF99"> #   </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">   </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">   </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99">    </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R5: the contents of R2  </TD>   
# <TD BGCOLOR="#FF8COO"> </TD>
#          <TD BGCOLOR="#F5F5DC">     </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">     </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">     </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  1   </td>
#          <td BGCOLOR="#66FF99"> 	1   </td>
#          <TD BGCOLOR="#F5F5DC">  1#   </td>
#          <td BGCOLOR="#66FF99"> 	1#   </td>
#          <TD BGCOLOR="#F5F5DC">  1##   </td>
#          <td BGCOLOR="#66FF99">  1##  </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R6: the contents of R3  </TD>   
# <TD BGCOLOR="#FF8COO"> </TD>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
# </tr>
# </table>
# </left>
# 
# <br>
# continuing
# <br>
#  <left>
# <TABLE BORDER  Cellpadding="3">
#  <TR><TD BGCOLOR="#B0E0E6">R1: the input program <i>p</i>  </TD>   
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <td BGCOLOR="#66FF99">  <i>p</i> </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R2: an instr number 1<sup>n</sup>
#         </TD>   
#          <TD BGCOLOR="#F5F5DC">  11 </td>
#          <td BGCOLOR="#66FF99">  11 </td>
#          <TD BGCOLOR="#F5F5DC">  111 </td>
#          <td BGCOLOR="#66FF99">  111 </td>
#          <TD BGCOLOR="#F5F5DC">  1<sup>12</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>12</sup> </td>
#          <TD BGCOLOR="#F5F5DC">  1<sup>14</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>14</sup> </td>
#          <TD BGCOLOR="#F5F5DC">  1<sup>17</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>17</sup> </td>
#          <TD BGCOLOR="#F5F5DC">  1<sup>18</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>18</sup> </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R3: the <i>n</i>th instruction of <i>p</i>    
#          <TD BGCOLOR="#F5F5DC">   </td>
#          <td BGCOLOR="#66FF99"> 1#####  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 1<sup>9</sup> ###  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 11#####  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 111###  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 1#  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 1<sup>6</sup> ####    </td>
#    </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R4: the contents of R1   </TD>   
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99">   </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">   </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">   </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  1  </td>
#          <td BGCOLOR="#66FF99">  1  </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R5: the contents of R2  </TD>   
#          <TD BGCOLOR="#F5F5DC">  1##   </td>
#          <td BGCOLOR="#66FF99">  1##  </td>
#          <TD BGCOLOR="#F5F%DC"> 1##    </td>
#          <td BGCOLOR="#66FF99">  1##  </td>
#          <TD BGCOLOR="#F5F5DC"> 1##    </td>
#          <td BGCOLOR="#66FF99"> 1##   </td>
#          <TD BGCOLOR="#F5F5DC">  1##   </td>
#          <td BGCOLOR="#66FF99"> 	1##   </td>
#          <TD BGCOLOR="#F5F5DC">  ##   </td>
#          <td BGCOLOR="#66FF99"> 	##   </td>
#          <TD BGCOLOR="#F5F5DC">  ##   </td>
#          <td BGCOLOR="#66FF99">  ##  </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R6: the contents of R3  </TD>   
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
# </tr>
# </table>
# </left>
# <br>
# and going further in the <i>move<sub>2,1</sub></i> part
# at the end of <i>write</i>
#  <left>
# <TABLE BORDER  Cellpadding="3">
#  <TR><TD BGCOLOR="#B0E0E6">R1: the input program <i>p</i>  </TD>   
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <td BGCOLOR="#66FF99">  <i>p</i> </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R2: an instruction number 1<sup>n</sup>
#         </TD>   
#          <TD BGCOLOR="#F5F5DC">  1<sup>12</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>12</sup> </td>
#          <TD BGCOLOR="#F5F5DC">  1<sup>15</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>15</sup> </td>
#          <TD BGCOLOR="#F5F5DC">  1<sup>16</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>16</sup> </td>
#          <TD BGCOLOR="#F5F5DC">  1<sup>12</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>12</sup> </td>
#          <TD BGCOLOR="#F5F5DC">  1<sup>15</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>15</sup> </td>
#          <TD BGCOLOR="#F5F5DC">  1<sup>16</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>16</sup> </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R3: the <i>n</i>th instruction of <i>p</i>    
#          <TD BGCOLOR="#F5F5DC">   </td>
#          <td BGCOLOR="#66FF99"> 11#####  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 1##  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 1<sup>4</sup>####  </td>
#          <TD BGCOLOR="#F5F5DC">   </td>
#          <td BGCOLOR="#66FF99"> 11#####  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 1##  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 1<sup>4</sup>####  </td>
#    </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R4: the contents of R1   </TD>   
#          <TD BGCOLOR="#F5F5DC">  1  </td>
#          <td BGCOLOR="#66FF99">  1  </td>
#          <TD BGCOLOR="#F5F5DC">  1  </td>
#          <td BGCOLOR="#66FF99"> 1  </td>
#          <TD BGCOLOR="#F5F5DC">   1#  </td>
#          <td BGCOLOR="#66FF99">  1#  </td>
#          <TD BGCOLOR="#F5F5DC"> 1#  </td>
#          <td BGCOLOR="#66FF99">  1#  </td>
#          <TD BGCOLOR="#F5F5DC"> 1#  </td>
#          <td BGCOLOR="#66FF99">  1#  </td>
#          <TD BGCOLOR="#F5F5DC">  1##  </td>
#          <td BGCOLOR="#66FF99">  1##  </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R5: the contents of R2  </TD>   
#          <TD BGCOLOR="#F5F5DC">  ##   </td>
#          <td BGCOLOR="#66FF99">  ##  </td>
#          <TD BGCOLOR="#F5F5DC"> #    </td>
#          <td BGCOLOR="#66FF99">  #  </td>
#          <TD BGCOLOR="#F5F5DC"> #    </td>
#          <td BGCOLOR="#66FF99"> #   </td>
#          <TD BGCOLOR="#F5F5DC">  #  </td>
#          <td BGCOLOR="#66FF99"> 	#   </td>
#          <TD BGCOLOR="#F5F5DC">     </td>
#          <td BGCOLOR="#66FF99"> 	  </td>
#          <TD BGCOLOR="#F5F5DC">     </td>
#          <td BGCOLOR="#66FF99">    </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R6: the contents of R3  </TD>   
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
# </tr>
# </table>
# </left>
# <br>
# <p>
# and concluding
# <br>
#  <Left>
# <TABLE BORDER  Cellpadding="3">
#  <TR><TD BGCOLOR="#B0E0E6">R1: the input program <i>p</i>  </TD>   
#          <TD BGCOLOR="#F5F5D">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#66FF99">  <i>p</i> </td>
#          <TD BGCOLOR="#F5F5DC">  <i>p</i> </td>
#          <TD BGCOLOR="#FFFFOO">  1## </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R2: an instruction number 1<sup>n</sup>
#         </TD>   
#          <TD BGCOLOR="#F5F5DC">  1<sup>12</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>12</sup> </td>
#          <TD BGCOLOR="#F5F5DC">  1<sup>13</sup> </td>
#          <td BGCOLOR="#66FF99">  1<sup>13</sup> </td>
#          <TD BGCOLOR="#F5F5DC">  1<sup>19</sup> </td>
#          <TD BGCOLOR="#FFFFOO"> </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R3: the <i>n</i>th instruction of <i>p</i>    
#          <TD BGCOLOR="#F5F5DC">   </td>
#          <td BGCOLOR="#66FF99"> 11#####  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99"> 1<sup>6 ###  </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <TD BGCOLOR="#FFFFOO">    </td>
#    </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R4: the contents of R1   </TD>   
#          <TD BGCOLOR="#F5F5DC">  1##  </td>
#          <td BGCOLOR="#66FF99">  1##  </td>
#          <TD BGCOLOR="#F5F5DC">  1##  </td>
#          <td BGCOLOR="#66FF99">  1##  </td>
#          <TD BGCOLOR="#F5F5DC">  1##  </td>
#                   <TD BGCOLOR="#FFFFOO">    </td>
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R5: the contents of R2  </TD>   
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">    </td>
#           <TD BGCOLOR="#FFFFOO">    </td>
# 
# </tr>
#  <TR><TD BGCOLOR="#B0E0E6">R6: the contents of R3  </TD>   
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <td BGCOLOR="#66FF99">    </td>
#          <TD BGCOLOR="#F5F5DC">  </td>
#          <TD BGCOLOR="#FFFFOO">    </td>
# </tr>
# </table>
# </left>
# As promised, here are some words of explanation.
# <br><p>
# As you can see, there are four different colors of the columns.
# The colors indicate the <strong>sub-programs</strong> of <i>u</i>.
# The columns themselves indicate the register contents when one
# of the sub-programs <strong>begins</strong>.
# <br><p>
# The first color shown is orange.
# This  is the the easiest to explain.         The orange sub-program is 11#.
# So it adds a 1 to R2, indicating that at the
# very beginning of the execution of
# the input program, the instruction to look at first is instruction 1.
# <br><p>
# The beige columns alternate with the green ones.
# The purpose of the beige program is to take the input program
# (in R1) and the next instruction number (R2), and to
# look up the appropriate  
# instruction and put it into R3.  This is similar to a program
# which we saw earlier on.  But we need to be sure that the contents
# of R1 and R2 are not destroyed at the end.  (So you will probably need
# to use registers beyond R6 for all of this.)    The way to understand
# the beige columns is that they tell the contents of the various registers
# at the <strong>beginning</strong> of the operation of the "beige
# sub-program".  You will need to write that sub-program.
# It is a fairly straightforward modification of a program which you
# already have seen, the one that gives the <i>n</i>the instruction of
# an input program.   But there are some differences: you need to be
# sure that the output goes in R3, that the input is preserved, and that
# if the contents of R2 is one more than the length of the input program in R1,
# then the program "knows" about this and transfers over to the yellow sub-program
# shown at the end.
# <br><p>
# The main action of the steps is done in the green columns;
# more precisely, 
# the columns shown are the <strong>beginnings</strong> of the
# "green" sub-program, and then the results of that sub-program
# are the beige columns which follow.
# The exact action depends on what kind of instruction is in R3 in 
# the given green column.  For example, if R3 has 11#, then
# in the next beige column we add a # to R5 (not R2: it is R5
# that models what is in R2 of the <i>real</i> machine when we run 
# program).   We also must add 1 to  R2 in simulating the execution
# of  11#, since after 11#, we go to the very next instruction.
# This is how the green columns work when we execute an instruction
# 11#.   The other cases are left for you to think about.
# Note also that each time the green sub-program runs, R3 is emptied 
# at the end.
# <br><p>
# The last column color is the yellow one at the very end.
# Before the yellow one starts up, the beige program
# has determined (in some sense) that 
#   our program <i>p</i> has 18 instructions and we have 
#   come to a point where we ask for instruction 19.  Thus, 
#   the input program has halted.   We therefore want to
#   take the contents of R1 as run by the input program
#   (this is the word in R4), and  move this to R1.
#   Also, we would like to clear out the contents of
#   whichever registers are not empty.  We do this so that 
#   the program we are writing will itself come to a good halt
#   on its input.
# <br>
# <p>
# It might seem silly to have R1 unchanged throughout.
# But this isn't really what is happening at all.
# In the course of the beige subprograms, parts of R1 are copied
# to other registers, and the copied back.   So at the 
# <i>end</i> of the beige sub-programs, we have the original
# program p back in R1.   
# <br><p>
# Similarly, it might seem weird to have R6 completely unused
# in running a universal program on <i>p</i>.  This is due
# to the fact that our program <i>p</i> only uses R1 and R2.
# If we worked with an example program that used R3, then R6
# would not have remained empty in the tables.
# 
# 
# 
# 
# 

# ## Coding unboundedly many registers into one
# 
# The simplified form of the universal program that we just saw could be modified to work on programs with any fixed finite number of registers.  But we want one universal programs that works on *all* programs, without a pre-established bound.  For this, we need a new idea.  
# 
# We now call upon a technique introduced in a separate notebook in this course, the technique of [two-by-two encoding](two_by_two.ipynb).  That notebook shows how we can add an *end of register marker* to R1, and the work with a simple encoding of symbols by pairs.   We took the end of register marker to be ```##```, and we encoded ```1``` by ```11``` and ```#``` by ```1#```.  
# 
# All of that work was for R1 alone.   But we could do the same work for all of the other registers.  
# 
# Following this, the idea is to simply run all of the encoded registers into one.  
# 
# 

# For an example of what we mean, suppose that we were dealing with the following snapshot:
# 
#  <CENTER>
# <TABLE BORDER  Cellpadding="3">
#  <TR><TD BGCOLOR="#B0E0E6">R1: 11# </td>  
#   <TD BGCOLOR="#B0E0E6">R2:  </td>  
#  <TD BGCOLOR="#B0E0E6">R3: ## </td>  
#  <TD BGCOLOR="#B0E0E6">R4:   </td>  
#    <TD BGCOLOR="#B0E0E6">R5:   </td>  
#  <TD BGCOLOR="#B0E0E6">R6: 1 </td>  
#  <TD BGCOLOR="#B0E0E6">R7: #</td>  
#   <TD BGCOLOR="#B0E0E6">R8: ##1 </td> 
#   </tr>
# </table>
# </center>
# 
# (We understand also that all of the other registers are empty.)
# 
# Encoding things as we have explained allows us to code the eight registers, as in the table below:
# 
# <CENTER>
# <TABLE BORDER  Cellpadding="3">
#  <TR> <td> Contents </td>
#  <TD BGCOLOR="#B0E0E6">R1: 11# </td>  
#   <TD BGCOLOR="#B0E0E6">R2:  &nbsp;&nbsp;&nbsp; </td>  
#  <TD BGCOLOR="#B0E0E6">R3: ## </td>  
#  <TD BGCOLOR="#B0E0E6">R4:   </td>  
#    <TD BGCOLOR="#B0E0E6">R5:   </td>  
#  <TD BGCOLOR="#B0E0E6">R6: 1 </td>  
#  <TD BGCOLOR="#B0E0E6">R7: #</td>  
#   <TD BGCOLOR="#B0E0E6">R8: ##1 </td> 
#   </tr>
#    <TR><td>Encoded as</td>
#    <TD BGCOLOR="#FFFFCC">11111###</td>  
# <TD BGCOLOR="#FFFFCC">## </td>  
# <TD BGCOLOR="#FFFFCC">R3:## </td>  
# <TD BGCOLOR="#FFFFCC">##</td>  
# <TD BGCOLOR="#FFFFCC">##</td>  
# <TD BGCOLOR="#FFFFCC">11## </td>  
# <TD BGCOLOR="#FFFFCC">1# ##</td>  
# <TD BGCOLOR="#FFFFCC">1#1#11## </td> 
# </table>
# </center>
# 
# One important point is that the empty registers still get an end-of-register marker ```##```.
# 
# Therefore we would encode the contents of these registers by the single word
# 
# ```11 11 1# ## ## 1# 1# ## ## ## 11 ## 1# ## 1# 1# 11 ##```
# 
# Without spaces, this is
# 
# ```11111#####1#1#######11##1###1#1#11##```
# 
# The point is that with some additional work, we can use this single word as an encoded form of *all* the registers in our program.

# <img src="https://github.com/lmoss/onesharp/blob/main/drum.jpg?raw=1" width="200" height="160">

# # Project
# 
# Your project is to work in groups to write a universal program.
# I think that groups of 4 or 5 are optimal.  If you prefer to work alone,
# then it would be ok to do so, but I think it would be better to work with others.
# <p>
# Probably you will want to follow the ideas above and to write the
# various sub-programs that were described.    But you don't really have
# to follow the outline at all; you are free to depart from it.
# <br>
# <p>
# Here is what each group needs to do:
# <ol>
# <li>   Make a plan on how to divide up the work of writing the
# different sub-programs.   The parts are not all equally hard.
# The beige program could be the hardest, especially if you follow 
# my comment below on it.
# 
# <li>  You will need to meet, or at least to email each other, so that
# you can be sure that the different sub-programs do what they are supposed to.
# You'll get started next time during our class time.
# (So I'll be here, but you can meet somewhere else if you like.)
# <li>  You also will need to have a plan on how to assemble everything together.
# The various sub-programs will need to "talk to each other"
# via goto statments.  
# I can definitely help with ideas on joining programs.  
# One good way is 
# to use the 
# Sanity parser.   And one way that probably does not work well would be 
# to simply
# put two flowcharts together.   
# <li>  The group overall will need to turn in a program along with an explanation of
# the various parts.  You should say clearly what the parts do, and also give some
# examples of how they run.   If you have made flowcharts, it would be good
# to hand those in as well.  
# <li> You should test your overall program.  It would be good to run
# your program on 1#,  on <i>diag</i>, and on <i>1#1## + u</i>.
# <li>  At various points, you will be tempted to worry about what would happen
# if the input program does <i>not</i> halt.    (For example, what should your
# program do if the input program is just 1111#### ?)
# Strictly speaking, the universal program should itself diverge on this input.
# But for our purposes, it's fine to ignore this point.
#   You need not worry about this at all, only about the case
# when the input program really does halt. 
# <li>  Above, we worked with the simplifying assumption that
# the input program only uses R1, R2, and R3.  You should get a program
# <i>u</i> that woks on all input programs.   
# <li>  Your final draft should say who did what.
# <li>
#   It is important to write well.   
#  Your goal should be to write something that could be understood by
#  someone else in the class.    
#   <li> I would be happy to 
# look at drafts or to talk about how things are going at any point.
# Hopefully this will not take so long, and hopefully you'll get started
# fairly soon.
# </ol>  
#   
#   
#   
#   
# <hr>
# 
# <h3>A remark on the beige and green sub-programs</h3>
# <p>
# The way I have described things makes the green sub-programs
# a little harder than they have to be.   That is, if we have an instruction in 
# R3, say 111###, the first thing to do would seem to be to work with it
# in order to decide which kind of instruction it is.  (In this case, 
# the instruction is
# a transfer instruction, of course.)    Now you certainly can write the 
# green sub-program to start out by <i>parsing</i> the instruction in R3
# and then working on a case-by-case basis.   However, this is not
# the only way to do things.   If you are careful with the
# beige program, the one that gives the <i>n</i>th instruction in the
# input program, then the parsing could be done automatically.
# What I mean here is that the beige program could be written in 
# such a way that it incorporates the parsing as it goes.
# <br>
# <p>
# If you are successful in getting a beige program that does what
# we want, then this would be <strong>much</strong> more work
# than all of the rest combined.   
# 

# 
# ### A remark on the beige and green sub-programs
# 
# The way I have described things makes the green sub-programs
# a little harder than they have to be.   That is, if we have an instruction in 
# R3, say 111###, the first thing to do would seem to be to work with it
# in order to decide which kind of instruction it is.  (In this case, 
# the instruction is
# a transfer instruction, of course.)    Now you certainly can write the 
# green sub-program to start out by <i>parsing</i> the instruction in R3
# and then working on a case-by-case basis.   However, this is not
# the only way to do things.   If you are careful with the
# beige program, the one that gives the <i>n</i>th instruction in the
# input program, then the parsing could be done automatically.
# What I mean here is that the beige program could be written in 
# such a way that it incorporates the parsing as it goes.
# <br>
# <p>
# If you are successful in getting a beige program that does what
# we want, then this would be <strong>much</strong> more work
# than all of the rest combined. 

# The group overall will need to turn in a program along with an explanation of
# the various parts.  You should say clearly what the parts do, and also give some
# examples of how they run.   If you have made flowcharts, it would be good
# to hand those in as well.  
# 
# You should test your overall program.  It would be good to run
# your program on 1#,  on <i>diag</i>, and on <i>1#1## + u</i>.
# 
#  At various points, you will be tempted to worry about what would happen
# if the input program does <i>not</i> halt.    (For example, what should your
# program do if the input program is just 1111#### ?)
# Strictly speaking, the universal program should itself diverge on this input.
# But for our purposes, it's fine to ignore this point.
# You need not worry about this at all, only about the case
# when the input program really does halt. 
# 
# Above, we worked with the simplifying assumption that
# the input program only uses R1, R2, and R3.  You should get a program
# *u* that woks on all input programs.   
# 
# Your final draft should say who did what.
# 
# It is important to write well.    Your goal should be to write something that could be understood by
# someone else in the class.    
# 

# <img src="https://github.com/lmoss/onesharp/blob/main/basses.jpg?raw=1" width="200" height="160">

# ## Implementing add# instructions
# 
# To see how some of this would work, we want to discuss how add1 instructions like 1##, 11##, etc. are implemented.
# 
# When we execute such a instruction, we'll assume as above that R4 contains the encoded contents of all the registers. We'll also assume that R5 contains a number in unary, call it m. We want a sub-program that will update R4 by adding 1§# onto the end of the mth encoded register. Here is such a program:
# 
# 11111##### 1### 1### 1### 1111##### 1111111111111111### 1111111### 111111## 1111##### 1### 1### 111111## 111111111111### 111111# 1111##### 1### 111### 111111## 11111111111111#### 111111# 1111111111111111#### 111111## 111111## 1### 11111##### 111111111### 1### 111111##### 111111111111111111111111#### 111### 1111111## 1111#### 1111111# 111111#### 111111##### 111111### 11111111### 111111##### 1### 1### 1### 1111111# 1111111## 111111111### 1111111# 111111##### 1### 111### 1111111## 111111111111111#### 1111111# 11111111111111111#### 1111111## 1111111## 1111 ##### 111111### 111### 1111111## 1111#### 1111111# 111111#### 1111111 ##### 111111### 111### 1111## 1111#### 1111# 111111####
# 
# You should try it out to make sure that it works right. Some good test cases would include the case when R4 is empty, as it would be in the beginning of a run.
# 
# So far, we have described how add# instructions would be implemented in a universal program. All of the same work goes for add1 instructions, of course, with just a few changes.
# 
# It would take a bit more work to handle the case instructions, but again, this is pretty similar.
# 

# <img src="https://github.com/lmoss/onesharp/blob/main/pianotrumpet.jpg?raw=1" width="200" height="160">

# # Universal programs of more than one argument

# <img src="https://github.com/lmoss/onesharp/blob/main/basses.jpg?raw=1" width="200" height="160">

# ### Exercise 1 
# 
# What is $\varphi_u(\textit{self})$?
# 
# Incidentally, running u on self takes 22,376,608 steps, whereas running self on empty registers takes 3,322.
# 
# 

# ## Exercise 2 
# 
# Write a program trade which looks like it trades places with its input in R1. (Of course, a program cannot literally trade places with its input. But here is what we mean: running trade with p in R1 and all other registers empty does the same thing as running p with trade in R1 and all other registers empty.)
# 
# [Hint: You will need a universal program, and also an application of the Recursion Theorem.]
# 
# This exercise was given earlier, at the end of Lesson 4. But the solution really requires our work on universal programs.
# 

# ## Exercise 3 
# 
# Write a program self1 which writes itself to R1 but only uses that register. That is, self1 does not use any register besides R1.
# 
# [Hint: you will need the technique of coding several registers into R1.]
