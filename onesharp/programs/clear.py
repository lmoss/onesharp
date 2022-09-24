from ..tools.ones import ones

# clear
# =====
# reg     : positive integer, the index of the register to clear
# returns : string, the 1# program to clear register ``reg''
def clear(reg):
  p = ones(reg)+'#####' # Cases on register ``reg''
  p += '111###'         # Go forward three
  p += '11####'         # Go backward two
  p += '111####'        # Go backward three
  return p
