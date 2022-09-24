from ..tools.ones import ones

# move
# ====
# src     : positive integer, the index of the source register
# dst     : positive integer, the index of the destination register
# returns : string, the 1# program to move the contents of register ``src'' to
#         :   register ``dst''
def move(src, dst):
  p = ones(src)+'#####' # Cases on register ``src''
  p += '11111 1###'     # Go forward six
  p += '111###'         # Go forward three
  p += ones(dst)+'##'   # Append ``#'' to register ``dst''
  p += '1111####'       # Go backward four
  p += ones(dst)+'#'    # Append ``1'' to register ``dst''
  p += '11111 1####'    # Go backward six
  return p
