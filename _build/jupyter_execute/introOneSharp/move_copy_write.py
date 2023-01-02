#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lmoss/onesharp/blob/main/introOneSharp/move_copy_write.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# ```{math}
# \newcommand{\hash}{\texttt{#}}
# \renewcommand{\one}{\texttt{1}}
# \newcommand{\diag}{\texttt{diag}}
# \newcommand{\writeprog}{\texttt{write}}
# \renewcommand{\phi}{\varphi}
# \newcommand{\set}[1]{\{ #1 \}}
# \newcommand{\semantics}[1]{[\![ #1]\!]}
# \newcommand{\pair}[1]{\langle #1 \rangle}
# \newcommand\N{\mathbb{N}}
# \newcommand\floor[1]{\lfloor#1\rfloor}
# \newcommand{\bmat}{\left[\begin{array}}
# \newcommand{\emat}{\end{array}\right]}
# ```

# # Simple programs
# 
# We have seen the syntax of $\one\hash$ instructions 
# [in a previous notebook](syntax-summary).
# We turn to the simplest programs in the language.

# In[1]:


get_ipython().system('python -m pip install -U setuptools')
get_ipython().system('python -m pip install -U git+https://github.com/lmoss/onesharp.git@main')
from onesharp.interpreter.interpreter import *


# $\damn$ Let's try it 

# ## move_2_1
# 
# The first is a program called ```move_2_1```.   It is designed to move the contents of R2 onto the end of R1, emptying out R2 in the process.  Written out in full it is 
# 
# ```11#####111111###111###1##1111####1#111111####```
# 
# But we have defined ```move_2_1``` to be this program, and so you can run it as shown below.
# 
# You can try the program by entering the following line.   In it
# 

# In[2]:


onesharp(move_2_1, ['11#','####1##11111'])


# The words in the brackets are the contents of registers 1 and 2 when we start.  Again, our program moved the contents of R2 onto the end of R1, emptying R2.  You should want to change the opening contents of R1 and R2 in the cell above before going on.

# It is hard to understand a program of $\one\hash$, but we have tools to help.  First, we can *parse* the program.  Parsing means dividing the program into instructions.

# In[3]:


parse(move_2_1)


# Even better, we can get an parse with glosses, as follows:

# In[4]:


parse_explain(move_2_1)


# The program ```move_2_1``` is a loop, and we can further add to the explanations in the chart.
# 

# In[5]:


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

# ## Modifying our simple loop
# 
# Suppose we want to modify move_2_1 to get move_3_4, a program which would copy the contents of R3 onto the end of R4 (and empty R4) in the process. Here is a way to do this which shows off some command-line tools that are part of the working environment of this course.

# In[6]:


parse(move_2_1)


# When you enter the cell above, you get the program ```move_2_1``` as a Python *list* of instructions. We have seen the explanation of this parse above.  What we want to do in ```move_3_4``` is to change the overall "case" instruction in the beginning from ```11#####``` to ```111#####```.   And each time our program writes to a register, we want that register to be R4, not R1.  So we make two changes.

# In[7]:


unparse(pre_program)


# We can check this out by entering it into the interpreter.  We could either copy the output line (without the quotes), and go up to the top of this notebook.  Alternatively, we could move the interpreter down to here using an up-arrow command that you will need to find.
# 

# ```{exercise}
# Write a program which takes the contents of R1 and adds them to the ends of *both* R2 and R3.
# ```

# ```{exercise}
# Write a program that clears out R1, leaving it empty.
# ```

# ```{exercise}
# Write a program that clears R3 and then swaps the contents of R1 and R2 (using the now-empty R3).
# ```
# 

# ```{exercise}
# Write a program $p$ that adds a $\one$ to the beginning of R1, assuming that R2 is empty. (For example, if R1 has $\hash\hash\one$ to start, then running $p$ would result in R1 having $\one\hash\hash\one$.) Of course, your program may use R2!
# ```

# ## Copy
# 
# The second program in this notebook is called ```copy```.
# Like ```move```, the ```copy``` program is actually an infinite batch of programs. 
# 
# ```{attention}
# The difference between <i>moving</i> and <i>copying</i>
# for us is that when a register's contents are moved, the
# register is left empty; but if the contents are copied,
# then the register is left at the end with exactly what it had
# at the beginning.
# ```
# 
# In order to copy in this way, we need an auxilliary register.
# So while the ```move``` programs had two registers in their names, the ```copy``` programs have three.
# 
# <br><p>
# Here is the idea behind copying Rm to Rn.   We use
# an auxilliary register, say Rp.  We move Rm into Rn and Rp
# at the same time, and then be move Rp back to Rm.
# Of course, when we do this, we should have Rp empty to start
# with.   
# <p>
# Here is our program when m = 1, n = 2, p = 3:

# In[ ]:


copy_1_2_3


# ## Write

# We construct with 
# a program $\writeprog$ with 
# the following properties:
# 
# 1. When $\writeprog$ is started with $x$ in R1 
# and R2 empty, we eventually halt  with a
# word $y$
# in $\Rone$ and all other registers empty.
# 
# 2. Then $y$ is a program, and running
# $y$ with $\Rone$ empty results in $x$ back in $\Rone$ and all
# other registers empty.

# In[ ]:


write


# Here is the explicated parse:

# In[ ]:


parse_explain(write)


# Even more informatively, here is a table:
# 
# <CENTER>
# <TABLE>
#         <TR BGCOLOR="#FFFFCC">
#                 <TD>1#####</TD> <TD>Cases on R1</TD></TR>
#         <TR BGCOLOR="#FFFFCC">
#                 <TD>111111111###</TD> <TD>Go forward 9:
#                   to move<sub>2,1</sub> part</TD>  </tr>
#         <TR BGCOLOR="#FFFFCC"><TD>11111###</TD><TD>Go forward 5:
# to the brown part</TD>  
#         </TR>
#          <TR  BGCOLOR="#B0E0E6">
#                 <TD>11#</TD> <TD>Add 1 to R2: 1## adds # to R1</TD></tr>
#          <TR  BGCOLOR="#B0E0E6">
#                 <TD>11##</TD> <TD>Add # to R2</TD></tr>   
#          <TR  BGCOLOR="#B0E0E6">
#                 <TD>11##</TD> <TD>Add # to R2</TD></tr>   
#          <TR  BGCOLOR="#B0E0E6">
#                 <TD>111111####</TD> <TD>Go backward 6 (to
# the top)</TD> </TR>
#          <TR  BGCOLOR="#D4B48C">
#                 <TD>11#</TD> <TD>Add 1 to R2: 1# adds 1 to R1</TD></tr>
#          <TR  BGCOLOR="#D4B48C">
#                 <TD>11##</TD> <TD>Add # to R2</TD></tr>
#          <TR  BGCOLOR="#D4B48C">
#                 <TD>111111111####</TD> <TD>Go backward 9
# (to the top)</TD>  
#         </TR>
#         <TR BGCOLOR="#FFFFCC">
#              <TD> move<sub>2,1</sub></TD><td> from earlier in this notebook </td></TR>
# </TABLE>        
# </CENTER>

# It should be emphasized that $\writeprog$ reads from R1 
# and writes to R2; it  makes no
# use of any other register.

# ```{exercise}
# Why is the result of running $\writeprog$ on a word $x$  always a program,
# even if  $x$ is a word which is not a program?
# ```

# ```{exercise}
# Let's take a word $x$ and run $\writeprog$ on it.  Call the resulting program $p$.  If we run $p$ on a word $y$, which do we get: $x + y$ or $y + x$?
# ```

# ```{exercise}
# Modify $\writeprog$
#  to get a program $\writetotwo$
# with the following feature:
#  If $\writetotwo$ is started with  $x$ in R1 
# and R2 empty, we eventually halt  with a
# word
# $y$
# in R2 and all other registers empty; moreover, running
# $y$  with R2 empty results in $x$ back in R2  (not R1) and all
# other registers empty.
# ```
