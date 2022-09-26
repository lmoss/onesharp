from ..tools.ones import ones

def is_positive_integer(n):
  return type(n) == int and n > 0

def is_string(s):
  return type(s) == str

def enqueue_one(register):
  assert is_positive_integer(register)
  return ones(register) + '#'

def enqueue_sharp(register):
  assert is_positive_integer(register)
  return ones(register) + '##'

def jump_forward(offset):
  if is_positive_integer(offset):
    return ones(offset) + '###'
  elif is_string(offset):
     return offset + '###'
  else:
     assert False # ``offset'' must be a positive integer or label string

def jump_backward(offset):
  if is_positive_integer(offset):
    return ones(offset) + '####'
  elif is_string(offset):
    return offset + '####'
  else:
    assert False # ``offset'' must be a positive integer or label string

def dequeue_and_branch(register):
  assert is_positive_integer(register)
  return ones(register) + '#####'

def no_operation():
  return jump_forward(1)

def dequeue(register):
  p =  dequeue_and_branch(register)
  p += no_operation()
  p += no_operation()
  return p
