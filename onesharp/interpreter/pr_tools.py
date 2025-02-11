#

def oneone(n):
  return '1'* n

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
#import sys

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
   p = (oneone(to_increment) + 
     '#####' + 
     '111###' +
     '111###' +
     '1111111111111111111111111###'+
     '1111111111111111111111111111111111111111###' +
     oneone(to_use) + '##' + 
     oneone(to_increment) + '#####' + 
     '111###' +
     '111111111111111111###' +
     '1111111111111111111###' +
     oneone(to_use) + '#' + 
     oneone(to_increment) + '#####' + 
     '111111###' +
     '111###' +
     oneone(to_use) + '##' + 
     '1111####' +
     oneone(to_use) + '#' + 
     '111111####' +
     oneone(to_use) + '#####' + 
     '111111###' +
     '111###' +
     oneone(to_increment) + '##' + 
     '1111####' +
     oneone(to_increment) + '#' +  
     '111111####' +
     '1111111111111111111###'  +
     oneone(to_use) + '##' +  
     '111111111111111111111####' +
     oneone(to_use) + '#' +  
     oneone(to_increment) + '#####' +  
     '111111###' +
     '111###' +
     oneone(to_use) + '##' +  
     '1111####' +
     oneonoe(to_use) + '#' + 
     '111111####' +
     oneone(to_use) + '#####' +  
     '111111###' +
     '111###' +
     oneone(to_increment) + '##' +  
     '1111####' +
     oneone(to_increment) + '#' + 
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
    return(oneone(n+amount)+'#')
  elif instruction_type(inst) == 'add#':  
    n = number_help(inst)
    return(oneone(n+amount)+'##')
  elif instruction_type(inst) == 'cases':  
    n = number_help(inst)
    return(oneone(n+amount)+'#####')
def bump(prog,amount):
  par = parse(prog)
  t = [bump_instr(instr,amount) for instr in par]
  return(unparse(t))

def clear_prog(n):
   a = oneone(n) + '#####'
   b = '111###'
   c = '1###'
   d = '111####'
   return(a+b+c+d)

def move_prog(n,m):
   a = oneone(n) + '#####'
   b = '111111###'
   c = '111###'
   d = oneone(m)+'##'
   e = '1111####'
   f = oneone(m)+'#'
   g = '111111####'
   return(a+b+c+d+e+f+g)

def copy_prog(n,m,p):
   a = oneone(n) + '#####'
   b = '11111111###'
   c = '1111###'
   d = oneone(m)+'##'
   d1 = oneone(p) + '##'
   e = '11111####'
   f = oneone(m)+'#'
   f1 = oneone(p) + '#'
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
               oneone(arity) + '##' ],
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
 
   
