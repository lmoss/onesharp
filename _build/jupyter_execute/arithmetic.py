#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lmoss/onesharp/blob/main/arithmetic.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# ## Programs for Arithmetic
# 
# The main point of working with 1# is that it gives an explicit treatment of some of the most important results of the theory of computation. This was the reason the language was formulated and developed. Nobody ever intended 1# to be used very widely.
# 
# At the same time, once we have 1# or some other programming language, it will be of some interest to check that we really can use it to do computation. This lesson is mainly a verification that you can use 1# to send a rocket to the moon. That is, it hints that one could theoretically use 1# to do any numerical computations that could be done with any computer. So this backs up the claim that our very simple language 1# is computationally complete.
# 
# For the most part, this lesson is optional. The specific results on arithmetic are not going to be used later. The definitions of primitive recursive function and computable function are important in computability theory. But if you already know them from other sources and are willing to believe that 1# is a Turing-complete formalism, then you should feel free to work through this lesson quickly, or even to skip it altogether. .
# 
# 

# In[1]:


get_ipython().system('python -m pip install -U setuptools')
get_ipython().system('python -m pip install -U git+https://github.com/lmoss/onesharp.git@main')
from onesharp.interpreter.interpreter import *


# # bb representation
# 
# Before we get look at arithmetic, we have to decide on how numbers are to be represented. There are lots of ways to do this, and we need to settle on a choice.
# 
# We've already seen the unary representation of numbers. We could continue on with this. The main reason against it has to do with zero: we would like our words to be non-empty words, and so we cannot use the empty word to represent zero. One way around this is to represent the number n by the unary n + 1. This could be confusing, and so we'll use a different representation of numbers. Ours is called the backwards binary or bb representation.
# 
# As a first step, you should remember or look up the binary or base 2 representation of numbers. Here are some examples:
# 
# <TABLE width=75%>
# <td>
# <TABLE BORDER >
#         <TR  BGCOLOR="#FAEBD7">
#                 <TH>Decimal</TH> <TH>binary</TH> </tr>
#  <TR BGCOLOR="#FAEBD7"><TD>0</TD> <TD>0</TD> </TR>
#   <TR BGCOLOR="#FAEBD7"><TD>1</TD> <TD>1</TD> </TR>
#    <TR BGCOLOR="#FAEBD7"><TD>2</TD> <TD>10</TD> </TR>
#  <TR BGCOLOR="#FAEBD7"><TD>3</TD> <TD>11</TD> </TR>
#   <TR BGCOLOR="#FAEBD7"><TD>4</TD> <TD>100</TD> </TR>
#   <TR BGCOLOR="#FAEBD7"><TD>5</TD> <TD>101</TD> </TR>
#   <TR BGCOLOR="#FAEBD7"><TD>6</TD> <TD>110</TD> </TR>
#    <TR BGCOLOR="#FAEBD7"><TD>7</TD> <TD>111</TD> </TR>
#  <TR BGCOLOR="#FAEBD7"><TD>8</TD> <TD>1000</TD> </TR>   
#   <TR BGCOLOR="#FAEBD7"><TD>9</TD> <TD>1001</TD> </TR>
#   </td>
#   </TABLE>      
#   <td>
# <TABLE BORDER >
#         <TR  BGCOLOR="#FAEBD7">
#                 <TH>Decimal</TH> <TH>binary</TH> </tr>
#   <TR BGCOLOR="#FAEBD7"><TD>10</TD> <TD>1010</TD> </TR>
#    <TR BGCOLOR="#FAEBD7"><TD>11</TD> <TD>1011</TD> </TR>
#  <TR BGCOLOR="#FAEBD7"><TD>12</TD> <TD>1100</TD> </TR>
#   <TR BGCOLOR="#FAEBD7"><TD>13</TD> <TD>1101</TD> </TR>
#   <TR BGCOLOR="#FAEBD7"><TD>14</TD> <TD>1110</TD> </TR>
#   <TR BGCOLOR="#FAEBD7"><TD>15</TD> <TD>1111</TD> </TR>
#    <TR BGCOLOR="#FAEBD7"><TD>16</TD> <TD>10000</TD> </TR>   
#    <TR BGCOLOR="#FAEBD7"><TD>17</TD> <TD>10001</TD> </TR>    
#     <TR BGCOLOR="#FAEBD7"><TD>18</TD> <TD>10010</TD> </TR> 
#        <TR BGCOLOR="#FAEBD7"><TD>19</TD> <TD>10011</TD> </TR> 
#         </TR>
# </TABLE>        
# </td>
# </table>
# <br>
# 

# We can't use the binary representation directly, since we don't have a symbol 0 around. So we change the 0s to #s. And after that, we turn the number around, getting the backwards binary representation. Here are the first 20 numbers again, in this form:
# 
# <TABLE width=75%>
# <td>
# <TABLE BORDER >
#         <TR  BGCOLOR="#FAEBD7">
#                 <TH>Decimal</TH> <TH>bb</TH> </tr>
#  <TR BGCOLOR="#FAEBD7"><TD>0</TD> <TD>#</TD> </TR>
#   <TR BGCOLOR="#FAEBD7"><TD>1</TD> <TD>1</TD> </TR>
#    <TR BGCOLOR="#FAEBD7"><TD>2</TD> <TD>#1</TD> </TR>
#  <TR BGCOLOR="#FAEBD7"><TD>3</TD> <TD>11</TD> </TR>
#   <TR BGCOLOR="#FAEBD7"><TD>4</TD> <TD>##1</TD> </TR>
#   <TR BGCOLOR="#FAEBD7"><TD>5</TD> <TD>1#1</TD> </TR>
#   <TR BGCOLOR="#FAEBD7"><TD>6</TD> <TD>#11</TD> </TR>
#    <TR BGCOLOR="#FAEBD7"><TD>7</TD> <TD>111</TD> </TR>
#  <TR BGCOLOR="#FAEBD7"><TD>8</TD> <TD>###1</TD> </TR>   
#   <TR BGCOLOR="#FAEBD7"><TD>9</TD> <TD>1##1</TD> </TR>
#   </td>
#   </TABLE>      
#   <td>
# <TABLE BORDER >
#         <TR  BGCOLOR="#FAEBD7">
#                 <TH>Decimal</TH> <TH>bb</TH> </tr>
#   <TR BGCOLOR="#FAEBD7"><TD>10</TD> <TD>#1#1</TD> </TR>
#    <TR BGCOLOR="#FAEBD7"><TD>11</TD> <TD>11#1</TD> </TR>
#  <TR BGCOLOR="#FAEBD7"><TD>12</TD> <TD>##11</TD> </TR>
#   <TR BGCOLOR="#FAEBD7"><TD>13</TD> <TD>1#11</TD> </TR>
#   <TR BGCOLOR="#FAEBD7"><TD>14</TD> <TD>#111</TD> </TR>
#   <TR BGCOLOR="#FAEBD7"><TD>15</TD> <TD>1111</TD> </TR>
#    <TR BGCOLOR="#FAEBD7"><TD>16</TD> <TD>####1</TD> </TR>   
#    <TR BGCOLOR="#FAEBD7"><TD>17</TD> <TD>1###1</TD> </TR>    
#     <TR BGCOLOR="#FAEBD7"><TD>18</TD> <TD>#1##1</TD> </TR> 
#        <TR BGCOLOR="#FAEBD7"><TD>19</TD> <TD>11##1</TD> </TR> 
#         </TR>
# </TABLE>        
# </td>
# </table>
# 

# ### Removing superfluous #s
# 
# One touchy point about bb representations is that all bb representations should either be the word # or else end in a 1. Here is a program that strips off superfluous #s at the end of a word in R1. It uses the first three registers It also converts an empty R1 to a #.
# 
# ```1##### 1111111111 11111111111 11111111111 11111111111 1111### 111### 11## 11### 11# 1##### 1111111111 1111111111### 1111111111### 11##### 1### 1111### 111## 11## 11111111#### 111# 11## 1111111111 1#### 11##### 1### 1111### 111## 11# 1111111111 1111111#### 111# 11# 1111111111 1111111111#### 11##### 1111111111### 1111111111### 111##### 111111### 111### 1## 1111#### 1# 111111#### 1111111111 11111111111 11111111111 11111#### 1111111111 1### 111# 111##### 111111### 111### 1## 1111#### 1# 111111#### 11### 1##```
# 

# 
# 
# # The successor function
# 
# Here is a program succ which takes a bb representation of a number n and outputs the bb representation of n+1.
# 
# <TABLE CELLPADDING="3">
#         <TR BGCOLOR="#FFFFCC">
#                 <TD>1#####</TD> <TD>Cases on R1</TD>  
#         </TR>
#          <TR BGCOLOR="#FFFFCC">
#                 <TD>1111111111 111###</TD> <TD>Go forward 13</TD>  
#         </TR>
#  </TR>
#         <TR BGCOLOR="#FFFFCC">
#                 <TD>1111111111### </TD> <TD>Go forward 10
#                 to the tan section</TD>  
#         </TR>
#          <TR  BGCOLOR="#B0E0E6">
#                 <TD>11#</TD> <TD>Add 1 to R2</TD>   </TR> 
#                          <TR  BGCOLOR="#B0E0E6">
#                 <TD><i>move</i><sub>1,2</sub> </TD> <TD>from Lesson 1</TD>    </TR>
#                         <TR BGCOLOR="#B0E0E6"">
#                 <TD>1111### </TD> <TD>Go forward 4 to
#                 the <i>move</i><sub>2,1</sub>  section</TD>   </TR> 
#          <TR  BGCOLOR="#D4B48C">
#                 <TD>11##</TD> <TD>Add # to R2</TD>  </TR>                             
#            <TR  BGCOLOR="#D4B48C">
#                 <TD>1111111111 111####</TD> <TD>Go backward 13 (to the top)</TD>   </TR>                                      
# <TR  BGCOLOR="#C0C0C0">             
#    <TD>11#</TD> <TD>Add 1 to R2</TD>       </TR>                
#                           <TR  BGCOLOR="#FFFFCC">
#                 <TD><i>move</i><sub>2,1</sub> </TD> <TD>from Lesson 1</TD>                          
#         </TR>
# </TABLE>        
# 
# 
# Here is how the program works: as long as a 1 is seen in R1, a # is put in R2; the program then loops to the top. On encountering the first #, the program goes to the blue part: it adds a 1 in R2 and then copies the rest of R1 to the end of R2. If the original input is empty, a 1 is put in R2. And after all of this, R2 is moved back to R1. The full code is shown below.
# 
# 1##### 1111111111 111### 1111111111### 11# 1##### 111111### 111### 11## 1111#### 11# 111111#### 1111### 11## 1111111111 111#### 11# 11##### 111111### 111### 1## 1111#### 1# 111111####
# 
# 
# 
# 
# 

# ###Comparison
# 
# Here is a program compare which takes words in R1 and R2 and decides if they are symbol-for-symbol the same. If so, it outputs a 1 in R1; if not, it leaves R1 empty.
# 
# 1##### 111111### 111111111### 11##### 1111111111 1### 1111111111### 111111#### 11##### 1111111111 11111### 111111### 11111### 11##### 111### 1111111111 111#### 1### 1##### 111### 11#### 111#### 11##### 1111### 11#### 111#### 1#
# 
# The original contents of R1 and R2 are destroyed in the process.
# 

# <img src="https://github.com/lmoss/onesharp/blob/main/pianotrumpet.jpg?raw=1" width="200" height="160">

# #Addition
# 
# Here is a program add which adds numbers. Given m in R1 and n in R2 (represented in bb), the program computes the sum m + n (again, represented in bb) and puts it in R1. At the end, all other registers are empty (and in particular the original inputs m and n are lost).
# 
# 1##### 111### 111111### 111111111### 11##### 1111111111 11111111111 11111111111 111### 1111111111 11111111111 11111### 1111111111 11111111111 111111### 11##### 1111111111 11111111111 11### 1111111111 11111111111 1111111### 1111111111 11111111111### 11##### 1111111111 11111111111### 1111111111 11111111### 1111111111 111111111### 1##### 111### 111111### 111111111### 11##### 1111111111 1### 1111111111 111111### 111111111### 11##### 1111111111 111### 1111111111### 1111111111 1### 11##### 111### 11111111### 1### 111# 1111111111 11111111111 11111111111 1#### 111## 1111111111 11111111111 11111111111 111#### 111# 1111111111 11111111111#### 111## 1111111111 11111111111 11#### 1### 111##### 111111### 111### 1## 1111#### 1# 111111####
# 
# 
# This program implements the usual algorithm for addition using carrying. It is also possible to get a program for addition using some of the work that we'll see soon on primitive recursion.
# 
# 
# 
# 

# <img src="https://github.com/lmoss/onesharp/blob/main/harp.jpg?raw=1" width="200" height="160">

# #Multiplication
# 
# Having seen a program for addition, we next look at multiplication.
# 
# We seek a program times with the following features: Given m in R1 and n in R2 the program computes the sum m x n and puts it in R1. At the end, all other registers are empty (and in particular the original inputs m and n are lost). As with addition, we want to work with bb representations.
# 
# Recall that with addition, our program was designed to implement the usual carrying algorithm. We could do the same for multiplication, but this is not the best choice for us. Although it is more familiar, it is less general; so the ideas used in the traditional algorithm are not going to be useful in other contexts. The basic idea in our treatment is that multiplication satisfies two recursion equations:
# 
# 
# m x 0 = 0
# 
# m x (n + 1 ) = (m x n) + m
# 
# 
# These enable us to multiply as a form of iterated addition. For example, suppose we want to multiply m = 4 (##1) by n = 3 (11). We use i as a temporary index which will go from 0 (#) up to n as we do our work.
# 
# We start with i= #, and our first recursion equation tells us that m x i = #. This is our first current value. Then we compare i with n. If the two were equal, then our value # would be m x n. If not, we go ahead. (In this case, the two are not the same.) Otherwise, we first want to add # + ##1 to get ##1. This is our new current value. Second, we update i to # + 1 = 1.
# 
# We compare i with n. If the two were equal, then our value ##1 would be m x n. If not, we go ahead. (In this case, the two are not the same.) Otherwise, we first want to add ##1 + ##1 to get ###1. This is our new current value. Second, we update i to # + 1 = #1.
# 
# Continuing, we again compare i with n. If the two were equal, then our value ###1 would be m x n. If not, we go ahead. (As before, the two are not the same.) Otherwise, we first want to add ##1 + ###1 to get ##11. This is our new current value. Second, we update i to #1 + 1 = 11.
# 
# Continuing, we again compare i with n. The two are indeed equal, and our value ##11 is m x n..
# 
# 
# The description above leads to some "pseudocode":
# 
# 1. (initialization) add # to R3 and also add # to R4
# 2. copy R2 to R5 using R6
# 3. copy R3 to R6 using R7
# 4. compare R5 and 56:
# if equal, goto "cleanup", if not go ahead
# 5. copy R1 to R5 using R6
# 6. move R4 to R6
# 7. add R5 to R6, leaving the answer in R5
# 8. move R5 to R4
# 9. take the successor of R3, using R5
# 10. go back to the main loop, step 2
# 11. the "cleanup" stuff: clear R1, R2, and R3
# 12. move R4 to R1
# 
# We next want to fill in this pseudocode by actual 1# programs. For most of the steps, we use move programs from earlier. Step 4 uses compare from above, along with bump from earlier. Similarly, step 9 uses the add function from just above.
# 
# 1. add # to R3 and # to R4
# 111##
# 1111##
# 
# 2. copy R2 to R5 using R6
# 
# 11##### 11111111### 1111### 11111## 111111## 11111#### 11111# 111111# 11111111#### 111111##### 111111### 111### 11## 1111#### 11# 111111####
# 
# 3. copy R3 to R6 using R7
# 
# 111##### 11111111### 1111### 111111## 1111111## 11111#### 111111# 1111111# 11111111#### 1111111##### 111111### 111### 111## 1111#### 111# 111111####
# 
# 4. compare R5 and R6.
#  This is φbump(compare,4)
# 11111##### 111111### 111111111### 111111##### 11111111111### 1111111111### 111111#### 111111##### 111111111111111### 111111### 11111### 111111##### 111### 1111111111111#### 1### 11111##### 111### 11#### 111#### 111111##### 1111### 11#### 111#### 11111#
# 
# followed by
# 
# 11111##### 111### 1111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111### 1#
# 
# 5. copy R1 to R5 using R6
# 
# 1##### 11111111### 1111### 11111## 111111## 11111#### 11111# 111111# 11111111#### 111111##### 111111### 111### 1## 1111#### 1# 111111####
# 
# 6. move R4 to R6
# 
# 1111##### 111111### 111### 111111## 1111#### 111111# 111111####
# 
# 7.add R5 to R6, leaving the answer in R5. This is φbump(add,4)
# 
# 11111##### 111### 111111### 111111111### 111111##### 1111111111 11111111111 11111111111 111### 1111111111 11111111111 11111### 1111111111 11111111111 111111### 111111##### 1111111111 11111111111 11### 1111111111 11111111111 1111111### 1111111111 11111111111### 111111##### 1111111111 11111111111### 1111111111 11111111### 1111111111 111111111### 11111##### 111### 111111### 111111111### 111111##### 1111111111 1### 1111111111 111111### 111111111### 111111##### 1111111111 111### 1111111111### 1111111111 1### 111111##### 111### 11111111### 1### 1111111# 1111111111 11111111111 11111111111 1#### 1111111## 1111111111 11111111111 11111111111 111#### 1111111# 1111111111 11111111111#### 1111111## 1111111111 11111111111 11#### 1### 1111111##### 111111### 111### 11111## 1111#### 11111# 111111####
# 
# 8. move R5 to R4
# 
# 11111##### 111111### 111### 1111## 1111#### 1111# 111111####
# 
# 9. take the successor of R3, using R5. We modify the program succ from above.
# 
# 111##### 1111111111 111### 1111111111### 11111# 111#####111111###111### 11111##1111#### 11111#111111#### 1111### 11111## 1111111111 111#### 11111# 11111#####111111###111### 111##1111#### 111#111111####
# 
# 10. go back to the main loop, step 2
# 
# 1111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 1111111####
# 
# 11. the "cleanup" stuff: clear R1, R2, and R3; also 12: move R4 to R1
# 1##### 111### 11#### 111####
# 11##### 111### 11#### 111####
# 111##### 111### 11#### 111####
# 1111##### 111111### 111### 1## 1111#### 1# 111111####
# 
# 
# The full program is
# 
# 111##
# 1111##
# 11##### 11111111### 1111### 11111## 111111## 11111#### 11111# 111111# 11111111#### 111111##### 111111### 111### 11## 1111#### 11# 111111####
# 111##### 11111111### 1111### 111111## 1111111## 11111#### 111111# 1111111# 11111111#### 1111111##### 111111### 111### 111## 1111#### 111# 111111####
# 11111##### 111111### 111111111### 111111##### 11111111111### 1111111111### 111111#### 111111##### 111111111111111### 111111### 11111### 111111##### 111### 1111111111111#### 1### 11111##### 111### 11#### 111#### 111111##### 1111### 11#### 111#### 11111#
# 11111##### 111###
# 1111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111###
# 1#
# 1##### 11111111### 1111### 11111## 111111## 11111#### 11111# 111111# 11111111#### 111111##### 111111### 111### 1## 1111#### 1# 111111####
# 1111##### 111111### 111### 111111## 1111#### 111111# 111111####
# 11111##### 111### 111111### 111111111### 111111##### 1111111111 11111111111 11111111111 111### 1111111111 11111111111 11111### 1111111111 11111111111 111111### 111111##### 1111111111 11111111111 11### 1111111111 11111111111 1111111### 1111111111 11111111111### 111111##### 1111111111 11111111111### 1111111111 11111111### 1111111111 111111111### 11111##### 111### 111111### 111111111### 111111##### 1111111111 1### 1111111111 111111### 111111111### 111111##### 1111111111 111### 1111111111### 1111111111 1### 111111##### 111### 11111111### 1### 1111111# 1111111111 11111111111 11111111111 1#### 1111111## 1111111111 11111111111 11111111111 111#### 1111111# 1111111111 11111111111#### 1111111## 1111111111 11111111111 11#### 1### 1111111##### 111111### 111### 11111## 1111#### 11111# 111111####
# 11111##### 111111### 111### 1111## 1111#### 1111# 111111####
# 111##### 1111111111 111### 1111111111### 11111# 111#####111111###111### 11111##1111#### 11111#111111#### 1111### 11111## 1111111111 111#### 11111# 11111#####111111###111### 111##1111#### 111#111111####
# 1111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 11111111111 1111111####
# 1##### 111### 11#### 111#### 11##### 111### 11#### 111#### 111##### 111### 11#### 111#### 1111##### 111111### 111### 1## 1111#### 1# 111111####
# 
# The parts of the program that are shaded red are special to the multiplication algorithm. The point is that if we wish to write a program for something similar, we could keep the outside "shell" and just modify the red lines above. Your first exercise below asks you to do just that.
# 

# <img src="https://github.com/lmoss/onesharp/blob/main/drum.jpg?raw=1" width="200" height="160">

# ## Exercise 1 
# 
# Modify the multiplication program to compute exponentiation. This would be a program exp with the following property: when started with the bb representation of m in R1 and n in R2, the program eventually halts with the bb representation of mn in R1.
# 

# ## Exercise 2 
# 
# In our work on multiplication, we assumed addition and worked with it to get multiplication. Now forget about our program for addition, and using only the program succ for the successor function, construct a program for addition.
# 

# ##Exercise 3 
# 
# Write a program which, when started with n in bb in R1, gives n! in R1. [Here n! is the factorial function. Remember that 0! = 1 and (n+1)! = (n+1) x n!.]
# 
# 

# 
# ## Exercise 4 
# 
# Write two programs which convert back and forth from unary to binary representation.
# 

# In[ ]:




