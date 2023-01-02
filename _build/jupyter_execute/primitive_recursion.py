#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lmoss/onesharp/blob/main/primitive_recursion.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Primitive Recursion
# 
# This notebook enables one to enter primitive recursive definitions and convert them to 1#.
# 
# It is mainly under development, but one could play with it now.  In addition, you can find your homework problems solved at the bottom of this notebook.
# 
# What I have here works: entering a primitive recursive term in the correct syntax, we can translate that term to a 1# program.   I did this for all the terms in the homework.  However, the work here is sub-optimal in the sense that the 1# program associated to a term uses way more registers than what seems to be necessary.  For example the program to determine whether or not an input number is prime uses 57 registers. 
# 
# I also wonder what it slowing down the run of the 1# programs.  My guess is that one or two optimizations to the Python algorithms should produce better 1# code.  But I don't really know this.
# 
# To start, enter the next few code cells below and then look at the definitions below.
# 

# In[1]:


get_ipython().system('python -m pip install -U setuptools')
get_ipython().system('python -m pip install -U git+https://github.com/lmoss/onesharp.git@main')
from onesharp.interpreter.interpreter import onesharp, step_by_step
from onesharp.tools.sanity import sanity


# In[ ]:


from onesharp.interpreter.interpreter import *
from onesharp.tools.sanity import sanity


# The next cell contains functions specific to this notebook, this time pertaining to primitive recursive terms themselves.
# 

# In[ ]:


from onesharp.tools.sanity import sanity

def all_equal(list):
  a = list[0]
  b = [x == a for x in list]
  return(all(b))


def arity(t):
  if t == 's_prog':
    return(1)
  if t[0] == 'proj':
    return(t[2])
  if t == 'z':
    return(1)
  if t == 'z_empty':
    return(0)
  if t[0] == 'pr':
    k = arity(t[1])
    j = arity(t[2])
    if j== 2 + k:
      return(k+1)
  if t[0] == 'comp':
    f = t[1]
    g_list = t[2:]
    if arity(f)== len(g_list) and all_equal([arity(v) for v in g_list]):
      return(arity(t[2]))   

def new_program(t,n):
  if t=='s_prog':
    return(copy_1_2_3+ successor_prog(2,3))
  if t[0] == 'proj':
    return(proj_prog(t[1],t[2]))
  if t == 'z':
    return('11##')
  if t == 'z_empty':
    return('1##') 
  if t[0] == 'pr':
    f = new_program(t[1],essentially_used(t))
    g = new_program(t[2],essentially_used(t))
    p = primitive_recursion(f, g, arity(t),essentially_used(t))
    return(p)
  if t[0] == 'comp':       
    g = new_program(t[1],essentially_used(t))
    hs = [new_program(u,essentially_used(t)) for u in t[2:]]
    k = arity(t[2])
    p = compose(g,hs,k, essentially_used(t))
    return(p)

def in_place_program(t):
  if t=='s_prog':
    return(copy_1_2_3+ successor_prog(2,3))
  if t[0] == 'proj':
    return(proj_prog(t[1],t[2]))
  if t == 'z':
    return('11##')
  if t == 'z_empty':
    return('1##') 
  if t[0] == 'pr':
    f = in_place_program(t[1])
    g = in_place_program(t[2])
    p = primitive_recursion(f, g, arity(t),essentially_used(t))
    return(p)
  if t[0] == 'comp':       
    g = in_place_program(t[1])
    hs = [in_place_program(u) for u in t[2:]]
    k = arity(t[2])
    p = compose(g,hs,k, essentially_used(t))
    return(p)

def essentially_used(t):
    if t=='s_prog':
      return(3)
    if t[0]== 'proj':
      return(t[2])
    if t == 'z':
      return(1)
    if t == 'z_empty':
      return(0)
    if t[0] == 'comp':
      outer = t[1]
      n1 = essentially_used(outer) 
      n2 = n1 + (len(t) -0)
      n3 = max([essentially_used(u) for u in t[2:]])
      n = max([n1,n2])+2
      return(n)
    if t[0] == 'pr':
      g = t[1]
      h = t[2]     
      n1 = essentially_used(g)
      n2 = essentially_used(h)
      n = max([n1,n2]) +2
      return(n)
import sys
def program(t):
  n = arity(t)
  first = in_place_program(t)
  second = unparse([clear_prog(i) for i in range(1,n+1)])
  third = move_prog(n+1,1)
  return(first+second+third)

#@title
def syntax_check(t):
  if t == 's_prog':
    return('True')
  if t[0] == 'proj':
    if t[1] <= t[2]:
      print(str(t))
      print("is a good term, and its arity is " + str(arity(t)))  
      print()
      return('True')
    else:
      print('Error in the expression below:')
      print(t)
      print()
      return(False)
  if t == 'z':
    return('True')
  if t == 'z_empty':
    return('True')
  if t[0] == 'pr':
    bool1 = syntax_check(t[1])
    bool2 = syntax_check(t[2])
    boolean = bool1 and bool2
    if boolean:
       k = arity(t[1])
       j = arity(t[2])
       if j== 2 + k:
          print(str(t))
          print("is a good term, and its arity is " + str(arity(t)))  
          print()
          return(True)
       else:
              print('Error in the primitive recursion (sub)term below:')
              print(t)
              print()
              print('The arity of the first term is ' + str(k))
              print('The arity of the second term is ' + str(j) +',')
              print('and we need the second arity to exceed the first by 2.')
              print()
    else: 
       print()
       print('Thus, there is an error in the pr term')       
       print(t)  
  if t[0] == 'comp':
    f = t[1]
    b1 = syntax_check(t[1])
    #print('b1: ' + str(b1))
    if b1 == False:
      print('Error in the sub-expression below:')
      print(t[1])
      return(False)
    g_list = t[2:]
    b2 = all_equal([syntax_check(v) for v in g_list])   
    #print('b2: ' + str(b2)) 
    if (b1 == True) and (b2 == False):
      print('One of the expressions is not a term:')
      print(g_list)
      return(False)
    else:
      b3 = all_equal([arity(v) for v in g_list])
      #print('b3: ' + str(b3)) 
    if b3 == False:
      print('The expressions below are terms, but their arities are not all equal:')
      print(g_list)
      return(False)
    b4 = b2 and b3
    #print('b4: ' + str(b4)) 
    if b4 == True:
      k = len(g_list)
      b5 = (k == arity(f)) 
      #print('b5: ' + str(b5)) 
      if b5 == False:
        print("Arity match error: The arity of ")
        print(str(f)) 
        print('is '+ str(arity(f)) + ', and it ')
        print("should equal " + str(k) + ", the number of terms which follow it.")
        return(False)  
      else:
        print(str(t))
        print("is a good term, and its arity is " + str(arity(t)))  
        print()        
        return(True)           

   
   
pr = 'pr'
proj = 'proj'
comp = 'comp'
s = 's_prog'
z = 'z'
z_empty = 'z_empty'



ddd = '1#####111111###111111111###11#####11111111111###1111111111###111111####11#####111111111111111###111111###11111###11#####111###1111111111111####1###1#####111###11####111####11#####1111###11####111####1#'
## ddd is used in the compare program just below
def compare_prog(a,b): #uses a+1, a+2, a+3
  p = copy_prog(a,a+1,a+2) + copy_prog(b,a+2,a+3) +  bump(ddd,a) 
  return(p)
  # SHOULD ONLY BE USED WHEN b is not a+1 and not a+2
  # checks if Register a and Register b have the same thing, 
  # preserving them.   At the end, R(a+1) either has 
  # 1 (if original Rn and Rm are the same) or is empty (if they aren't)
  # This program also writes to R(a+2) and R(a+3).  So when it is 
  # called, all of registers a+1, a+2, and a+3 should be empty

def successor_prog(to_increment,to_use):
  # gives a program to increment the register 'to_increment' by 1, using 
  # the register 'to_use'
   p = (ones(to_increment) + 
     '#####' + 
     '111###' +
     '111###' +
     '1111111111111111111111111###'+
     '1111111111111111111111111111111111111111###' +
     ones(to_use) + '##' + 
     ones(to_increment) + '#####' + 
     '111###' +
     '111111111111111111###' +
     '1111111111111111111###' +
     ones(to_use) + '#' + 
     ones(to_increment) + '#####' + 
     '111111###' +
     '111###' +
     ones(to_use) + '##' + 
     '1111####' +
     ones(to_use) + '#' + 
     '111111####' +
     ones(to_use) + '#####' + 
     '111111###' +
     '111###' +
     ones(to_increment) + '##' + 
     '1111####' +
     ones(to_increment) + '#' +  
     '111111####' +
     '1111111111111111111###'  +
     ones(to_use) + '##' +  
     '111111111111111111111####' +
     ones(to_use) + '#' +  
     ones(to_increment) + '#####' +  
     '111111###' +
     '111###' +
     ones(to_use) + '##' +  
     '1111####' +
     ones(to_use) + '#' + 
     '111111####' +
     ones(to_use) + '#####' +  
     '111111###' +
     '111###' +
     ones(to_increment) + '##' +  
     '1111####' +
     ones(to_increment) + '#' + 
     '111111####' +
     '1###'
     )
   return(p) 
  
z_prog = '11##'
one_prog = '11#'
#@title
# s is an index of the successor function in bb
successor = '1#####111###111###1111111111111111111111111###1111111111111111111111111111111111111111###11##1#####111###111111111111111111###1111111111111111111###11#1#####111111###111###11##1111####11#111111####11#####111111###111###1##1111####1#111111####1111111111111111111###11##111111111111111111111####11#1#####111111###111###11##1111####11#111111####11#####111111###111###1##1111####1#111111####1###'

def maxie(l):
  if l == []:
    return(0)
  else:
    return(max(l))
def height(tree):
  n = maxie([height(u) +1 for u in tree.children])
  return(n)
def all_equal(list):
  if (len(list)==0 or len(list)==1):
    return(True)
  else:
    b = all_equal(list[1:])  
    if b == False:
      return(False)
    else:
      return(list[0]==list[1])

def bump_instr(inst, amount):
  if instruction_type(inst) in ['forward','backward']:  
    return(inst) 
  elif instruction_type(inst) == 'add1':  
    n = number_help(inst)
    return(ones(n+amount)+'#')
  elif instruction_type(inst) == 'add#':  
    n = number_help(inst)
    return(ones(n+amount)+'##')
  elif instruction_type(inst) == 'cases':  
    n = number_help(inst)
    return(ones(n+amount)+'#####')
def bump(prog,amount):
  par = parse(prog)
  t = [bump_instr(instr,amount) for instr in par]
  return(unparse(t))

def clear_prog(n):
   a = ones(n) + '#####'
   b = '111###'
   c = '1###'
   d = '111####'
   return(a+b+c+d)

def move_prog(n,m):
   a = ones(n) + '#####'
   b = '111111###'
   c = '111###'
   d = ones(m)+'##'
   e = '1111####'
   f = ones(m)+'#'
   g = '111111####'
   return(a+b+c+d+e+f+g)

def copy_prog(n,m,p):
   a = ones(n) + '#####'
   b = '11111111###'
   c = '1111###'
   d = ones(m)+'##'
   d1 = ones(p) + '##'
   e = '11111####'
   f = ones(m)+'#'
   f1 = ones(p) + '#'
   g = '11111111####'
   return(a+b+c+d+d1+e+f+f1+g+move_prog(p,n))  

def proj_prog_official(ind,upper):
  index = [k+1 for k in range(ind-1)]    
  #print(index)
  first_part = [clear_prog(j) for j in index]
  #print(first_part)
  if ind == 1:
    middle = []
  else: 
    middle=[move_prog(ind,1)]
  second_index =  [k+ind+1 for k in range(upper-ind)] 
  #print(second_index)
  last_part = [clear_prog(j) for j in second_index]   
  together = first_part + middle + last_part
  done = unparse(together)
  if ind == 1 and upper==1:
    return('1###')
  else:
    return(done)   

def proj_prog(ind,upper):
  return(copy_prog(ind,upper+1, upper+2))

# the function below doesn't seem to be used
def copy_all_forward(n,m):
  # copies 1 to m, 2 to m+1, . . . n to m+n-1
  a = [copy_prog(i,m+i-1, m+i) for i in range(1,n+1)]
  return(unparse(a))


def compose(outer_fn,proglist,argument_number,used_reg):
  ## note that the outer_fn has to be 'in place'!
  k = len(proglist) # number of functions
  # the outer_fn is k-ary
  q = unparse([clear_prog(i) for i in range(1,k+1)])
  outer_fn = outer_fn + q + move_prog(k+1,1)
  arg = argument_number # = common arity in the proglist
  max_list =   [max_register(p) for p in proglist]
  m = maxie(max_list)
  #free_reg = used_reg + 1
  free_reg = m + 1
  a = [proglist[i] + move_prog(arg+1,free_reg+i+1) for i in range(0,k)]
  b = unparse(a)
  c = [move_prog(free_reg+i+1,argument_number+i+1) for i in range(0,k)]
  d = unparse(c)
  f = bump(outer_fn,argument_number)
  e = b + d + f   
  return(e)

# <g,h>(x-bar,0) = g(x-bar)
# <g,h>(x-bar,n+1) = h(x-bar,n,<g,h>(x-bar,n))
# k-1 is the number of xs, so the arity of <g,h> is k
# k+1 is the number of arguments to g
# k is the number of arguments to the function we are building
#free is large enough so that neither g nor h use it or any larger register.
# g and h are assumed to preserve their inputs
def primitive_recursion(g,h,arity,used_reg):
  free = max([max_register(g),max_register(h)])+1
  #free = used_reg +1
  free_plus_one = free + 1
  plan = [['top',move_prog(arity,free) +
               g + 
               move_prog(arity,arity+1) + 
               ones(arity) + '##' ],
          [compare_prog(free,arity)],
          ['decision', 'cases', free_plus_one, 'main_loop','clear_out_free', 'end' ],
          ['clear_out_free', clear_prog(free)],
          ['goto', 'end'],
          ['main_loop',h + 
               clear_prog(arity+1) + 
               move_prog(arity+2,arity+1) + 
               successor_prog(arity,free+2) +
               compare_prog(free,arity)],
          ['goto', 'decision'],
        ]
  trial = sanity(plan)
  return(trial)   
 
   


# # Primitive recursive terms, and the functions which they denote
# 
# 
# _Primitive recursive functions_ are functions $N^k\to N$, where $N$ is the set of natural numbers.   So there are primitive functions of arity $1$, $2$, etc.  There are also primitive recursive functions of arity $0$ (for a technical reason.)
# 
# _Primitive recursive terms_ are terms that denote primitive recursive functions.
# 
# We start with _basic primitive recursive function terms_, as shown below:
# 
# 
# ```z``` : this denotes the one-place function with value 0.
# 
# ```z_empty```: this denotes the zero-place function with value 0.
# 
# ```s``` : this denotes the one-place successor function: $f(n) = n+1$.
# 
# ```[proj, i, j]``` with i <= j: this is the ith projection on j variables.
# For example,
# ```
# [proj, 4, 6](3,6,5,7,9,13) = 7. 
# ```
# Indeed, every primitive recursive term has an _arity_, and if $t$ is of arity $k$, then $t$ denotes a function $N^k\to N$.  Technically, we should distinguish between the terms and the functions which they denote, but we usually will not do this.
# 
# The two term constructors are
# 
# ```[comp, f, g_1, . . . , g_k]```
# 
# ```[pr, f, g]```
# 
# In these, ```comp``` stands for composition, and ```pr``` stands for primitive recursion.
# 
# In the composition term ```[comp, f, g_1, . . . , g_k]```, all the terms ```g_i``` must have the same arity, say $n$.  The term ```f``` must have arity $k$ (the number of $g$s).  The term ```[comp, f, g_1, . . . , g_k]``` has arity $n$.  The function which this term denotes is defined as follows.
# For numbers $\overline{x} = x_1$, $\ldots$, $x_n$, 
# $$
# [comp, f, g_1, . . . , g_k](\overline{x}) =
# f(g_1(\overline{x}), \ldots, g_k(\overline{x})).
# $$
# 
# For the primitive recursive terms 
# ```[pr, f, g]```, we require that there is a number $n$ such that 
# the arity of $f$ is $n-1$ and the arity of $g$ is $n+1$.  Then the 
# arity of the term 
# ```[pr, f, g]``` is $n$.  Its denotation is the function with the following properties:
# $$
# [pr, f, g](\overline{x},0) = f(\overline{x})\\
# [pr, f, g](\overline{x},m+1) = g(\overline{x},m,[pr, f, g](\overline{x},m))\\
# $$

# # Examples of primitive recursive terms and functions
# 
#  You can assign names to them, as shown below. The main functions in the notebook are
# 
# You might look over the following example of terms before reading what to do with them.

# In[ ]:


add = [pr,[proj,1,1], [comp, s, [proj, 3,3]]]
#onesharp(program(add), ['11','#1#1'])

mul = [pr, z, [comp, add,[proj, 3,3],[proj, 1, 3]] ]
q = program(mul)
#onesharp(q, ['11','1#1'])

exp = [pr, [comp, s, z], [comp, mul, [proj, 3,3],[proj, 1, 3]] ]
pred = [pr, z_empty, [proj,1,2]]
monus = [pr, [proj, 1,1], [comp, pred, [proj,3,3]]]

two_place_fn_value_one = [comp, s,[comp,z,[proj,1,2]]]  
zero_place_fn_value_one = [comp, s, z_empty]  

sgn =[pr, z_empty,two_place_fn_value_one]
sgn_bar =[pr, zero_place_fn_value_one, [comp,z,[proj,1,2]]]

chi_greater = [comp,sgn, monus] ## characteristic function of >
chi_lesser_or_equal = [comp,sgn_bar, monus] #|characteristic function of (> or =)
chi_lesser = [comp,chi_greater,[proj,2,2],[proj,1,2]] ## characteristic function of <
chi_greater_or_equal = [comp, chi_lesser_or_equal,[proj,2,2],[proj,1,2]] ## characteristic function of >=

## solution to exercise 5a below
chi_equals = [comp, mul, chi_lesser_or_equal, chi_greater_or_equal ]

#print(arity(pred))
#predProg = print(program(pred))
#onesharp(program(exp),['1#1','11'])
#onesharp(program([comp, pred, [proj,2,2]]), ['11','#1#1'])
#print(successor)


# In[ ]:


onesharp(program(exp),['111','111'])


# ## Basic functions in this notebook
# 
# As you can see, you enter terms as ordinary Python strings.
# In particular, you can assign terms to variables, just as we have been doing with programs.
# 
# Here are some other functions in this notebook:
# 
# 
# 
# ```arity(t)```
# 
# ```program(t)```
# 
# ```in_place_program(t)```
# 
# #### Special note: the in_place_programs in this notebook do not halt in the sense of the course.  Instead, they _preserve their inputs_.  For example, run the program associated with _add_ below as shown below it.  (That is, take away the # from the beginning of the lines after the definition. The 2 inputs are preserved and the result goes in register 3.)
# 

# ## Syntax check
# 
# ###If you want to see a primitive recursive term written out "all the way", you can just enter it.
# 
# ### You can enter a line like the ones below to check that an expression really is a term, or to find an error.
# 
# #### The output can be long because the function ```syntax_check``` is recursive, and thus reports information about all the subterms of whatever you enter.
# 
# 

# In[ ]:


#print(exp)

#syntax_check(mul)
#syntax_check([comp, mul, mul])


# ## How to run insepct the terms and run the 1# programs.
# 
# The Python function ```program(t)``` compiles a primitive recursive term to a 1# program.  You can look at these by entering, e.g., ```program(add)```.   Then you can run these programs just as we have been doing all along.

# In[ ]:


onesharp(program(chi_equals),['1#1','##1'])


# ![](https://github.com/lmoss/onesharp/blob/main/images/drum.png?raw=1)

# <img src="https://github.com/lmoss/onesharp/blob/main/drum.jpg?raw=1" width="200" height="160">

# In[ ]:


### exercise 5b below
g = [comp, chi_equals, [proj,2,3], [comp, mul, [proj,1,3],[proj,3,3]]] 
# g tells if first x third = second
#print(arity(g))
#print(onesharp(program(g),['11','1##1','11']))

## for future use
greater_than_one = [comp, chi_greater, [proj,1,1], [comp, s, z]]
# gives output 1 if the input is >1 and gives output 0 if the input is 0 or 1

first_and_third_greater_than_one = [comp, mul,
                                      [comp, greater_than_one, [proj,1, 3]],
                                      [comp, greater_than_one, [proj,3, 3]]
                                     ]

first_third_second_proper = [comp, mul, g, first_and_third_greater_than_one]
# g tells if first x third = second, and both the first and third are >1

#onesharp(program(first_third_second_proper),['11','#11','#1'])

#onesharp(program(first_third_second_proper),['#','#','#1'])


# #### I am going to change exercise 5(c) a little.
# 
# I will get h_proper so that h_proper(m,p,n) = 1 if m > 1 and for some q <= n,
# q > 1 and m q = p.   That is, I have changed h a litte so that it incorporates information about the ">1" conditions.

# In[ ]:


## exercise 5c below


g3 = [comp, g, [proj, 1, 2], [comp, z, [proj, 1, 2]], [proj, 2, 2]]
p = program(g3)
onesharp(p, ['11','11111'])
k1 = [comp, add, [proj,4,4], 
      [comp, first_third_second_proper, [proj,1,4], [proj,2,4], [comp,s, [proj,3,4]]]]
k = [comp, sgn, k1] 

h_proper = [pr, g3, k1]

#onesharp(program(h_proper),['11','11','11'])
#onesharp(program(h_proper),['1#1','1111','11'])
## this asks if there is a number <= 3 such that 
## (a) the number is > 1
## and (b) if you multiply 5 by the number, you get 15.
## Since there is such a number (namely 2), we output 1.


# In[ ]:


# exercise 5d and 5e

proper_divisor = [comp, h_proper, [proj,1,2], [proj,2,2], [comp, pred, [proj,2,2]]]

#print(arity(proper_divisor))
#print(onesharp(program(proper_divisor),['11','11']))
#print(onesharp(program(proper_divisor),['11','#11']))
#print(onesharp(program(proper_divisor),['11','1##1']))

#print(onesharp(program(proper_divisor),['1','111']))
#print(onesharp(program(proper_divisor),['#1','111']))
#print(onesharp(program(proper_divisor),['11','111']))

#print(onesharp(program(proper_divisor),['##1','111']))
#print(onesharp(program(proper_divisor),['1#1','111']))
#print(onesharp(program(proper_divisor),['#11','111']))
#print(onesharp(program(proper_divisor),['111','111']))


# In[ ]:



pd_inverse_zero = [comp, proper_divisor, [proj,2,2],[proj,1,2]]
pd_inverse = [comp, mul, pd_inverse_zero, [comp, greater_than_one, [proj,2,2]]]

running_total_of_pd_inverse = [pr, [comp, z, [proj, 1, 1]], 
                                [comp, add, [proj, 3,3], 
                                [comp, pd_inverse, [proj, 1, 3], [proj,2, 3]]]]
#print(arity([comp, add, [proj, 2,2], pd_inverse]))                                  
#print(arity(running_total_of_pd_inverse))



# In[ ]:


print(onesharp(program(running_total_of_pd_inverse),['1','1']))
print(onesharp(program(running_total_of_pd_inverse),['#1','#1']))
print(onesharp(program(running_total_of_pd_inverse),['11','11']))
print(onesharp(program(running_total_of_pd_inverse),['##1','##1']))
print(onesharp(program(running_total_of_pd_inverse),['1#1','1#1']))

print(onesharp(program(running_total_of_pd_inverse),['#11','#11']))
print(onesharp(program(running_total_of_pd_inverse),['111','111']))
print(onesharp(program(running_total_of_pd_inverse),['###1','###1']))
print(onesharp(program(running_total_of_pd_inverse),['1##1','1##1']))
print(onesharp(program(running_total_of_pd_inverse),['#1#1','#1#1']))
print(onesharp(program(running_total_of_pd_inverse),['11#1','11#1']))


# In[ ]:


# End of the work on prime(n)

prime =[comp,sgn_bar, [comp, running_total_of_pd_inverse, [proj, 1,1], [proj, 1,1]]]
prime_prog = program(prime)

# Gives output 1 if the input is a prime,
# and gives output # if the output is not a prime.


# <img src="https://github.com/lmoss/onesharp/blob/main/drum.jpg?raw=1" width="200" height="160">

# ## Testing the 'prime' primitive recursive term

# In[ ]:


list = ['1', '#1', '11', '##1', 
             '1#1', '#11', '111', '###1', 
            '1##1', '#1#1', '11#1', '##11', 
             '1#11', '#111', '1111']
for i in range(15):
  x = list[i]
  b = onesharp(prime_prog,[list[i]])
  if b == '1':
    print(x + ' is prime')
  else:
    print(x + ' is not prime')  


# In[ ]:


ddd


# In[ ]:


ones(5)


# In[ ]:


unparse(parse(diag))


# In[ ]:


diag


# In[ ]:


onesharp('1#',[])


# In[ ]:


diag


# In[ ]:


ddd


# In[ ]:


diag


# In[ ]:


moveprog(1,3)


# In[ ]:




