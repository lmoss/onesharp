#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lmoss/onesharp/blob/main/coding.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Coding words by numbers

# ## Shortlex ordering on words
# 
# Here are definitions of the length function on numbers. We also have the function ```s(n)``` giving the nth word in the shortlex order on words, starting with n = 0.  We have the inverse of ```s``` also.

# We can check that ```s``` and ```s_inverse``` really are inverses.

# In[1]:



import math

def log2int(x):
  return(math.frexp(x)[1] - 1)

def length(n):
  return(log2int(n+1))

def index(n,m): ## this is what I write as (n)_m
  a = (n+1)%(2**(m+1))
  b = 2**m
  if a < b:
    return(0)
  else:
    return(1)

def convert_numeral_to_onesharp(x):
   if x == 0:
     return('#')
   else:
     return('1')    

def s(n):
  k = length(n)  
  s = [convert_numeral_to_onesharp(index(n,k-i-1)) for i in range(k)] 
  t = "".join(s) 
  return(t)

def s_inverse(w):
  n = len(w)
  a = (2**n - 1)
  b = [(2** (n-i-1)) for i in range(n) if (w[i] == '1')]
  c = sum(b)
  d = c+a
  return(d)


# In[2]:


s_inverse(s(4234))


# In[3]:


s(s_inverse('##111##1'))


# In[4]:


for n in range(256):
  print((n,s(n), s_inverse(s(n))))
 


# In[ ]:




