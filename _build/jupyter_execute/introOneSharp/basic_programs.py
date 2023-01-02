#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lmoss/lmoss.github.io/blob/main/introOneSharp/basic_programs.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Three simple programs
# 

# We have seen the syntax of commands of 1# in 
# [a previous notebook](syntax-guide).  Now we present some of the simplest programs in the language, programs which we will see again and again in what follows.
# 
# 
# 

# ## Move
# 
# A good way to learn about the different commands is to examine simple programs.  Among these is a program called ```move_2_1```.   It is designed to move the contents of R2 onto the end of R1, emptying out R2 in the process.  Written out in full it is 
# 
# ```11#####111111###111###1##1111####1#111111####```
# 
# You can try the program out by (a) moving the interprer down, using the appropriate commands in the notebook; (b) entering ```move_2_1``` as the program and some random words in R1 and R2 and then running ```move_2_1``` on those inputs.
# 
# Since it is hard to understand a program of 1#, we have tools to help.  First, we can *parse* the program.  Parsing means dividing the program into instructions.

# The program move_2_1 is a loop, and we can further add to the explanations in the chart.

# Even better, we can get an parse with glosses, as follows:

# In[1]:


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
# Suppose we want to modify ```move_2_1``` to get ```move_3_4```, a program which would copy the contents of R3 onto the end of R4 (and empty R4) in the process.
# Here is a way to do this which shows off some command-line tools that are part of the working environment of this course.

# In[ ]:


parse(move_2_1)


# pre_program = ['111#####', '111111###', '111###', '1111##', '1111####', '1111#', '111111####']

# In[ ]:


unparse(pre_program)


# We can check this out by entering it into the interpreter.  We could either copy the output line (without the quotes), and go up to the top of this notebook.  Alternatively, we could move the interpreter down to here using an up-arrow command that you will need to find.

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

# ### Exercise 8 
# 
# Write a program p that adds a 1 to the *beginning* of R1, assuming that R2 is empty.  (For example, if R1 has ```##1``` to start, then running p would result in R1 having ```1##1```.)   Of course, your program may use R2!

# In[ ]:





# In[ ]:




