from ..interpreter.interpreter import parse, unparse

def findme(pair,pair_list): 
  x = [i for i in range(len(pair_list)) if pair_list[i][0]==pair[1]]
  return x[0]

def add_placeholder(line):
  keywords = ['cases','add1','add#','goto','non_label']
  if line[0] in keywords:
    return(['non_label']+line)
  elif line[0][0] in ['1','#']:
    return(['non_label']+line)  
  else:
    return(line)

def flatten(tuple):
  b = len(tuple)
  if b > 1 and tuple[1] == "cases":
    n = tuple[2]
    x = ones(n)+'#####'
    return [[tuple[0],x], [tuple[0]+'@1',tuple[3]], [tuple[0]+'@2',tuple[4]], [tuple[0]+'@3',tuple[5]]]
  elif b > 1 and tuple[1]=='add1':
    return([[tuple[0],ones(tuple[2])+'#']])
  elif b > 1 and tuple[1]=='add#':
    return([[tuple[0],ones(tuple[2])+'##']])
  elif b > 1 and tuple[1]=='goto':
    return [[tuple[0],tuple[2]]]
  elif tuple[1][0] in ['1', '#']:
    k = parse(tuple[1])
    m = len(k)
    return([[tuple[0],k[j]] for j in range(m)])


def ones(n):
  return(unparse(['1' for i in range(n)])) 

def resolve(index,pair_list):
  pair_in_list = pair_list[index]
  #print("pair_in_list " + str(pair_in_list))
  first_char = pair_in_list[1][0]
  #print(first_char)
  if first_char == '1' or first_char == '#':
    return pair_in_list[1]
  elif pair_in_list[1]=='end':
    n = len(pair_list) - index
    return(ones(n)+'###')
  else:
    k = findme(pair_in_list,pair_list)
    if k > index:
      return(ones(k-index)+'###')
    if k < index:
      return(ones(index-k)+'####')


def sanity(line_list):
  w = [add_placeholder(line) for line in line_list]
  #print("[add_placeholder(line) for line in line_list] is")
  #print(w)
  s1 = [flatten(line) for line in w]
  #print('[flatten(line) for line in w] is')
  #print(s1)
  t1 = [item for sublist in s1 for item in sublist]
  #print('[item for sublist in s1 for item in sublist] is')
  #print(t1)
  n = len(t1)
  #print('len of t1 = ' + str(n))
  u1 = [resolve(i,t1) for i in range(n)] 
  return(unparse(u1))
