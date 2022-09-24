from ..tools.ones import ones
from ..programs.move import move

# add
# ===
# dst     : positive integer, the index of the destination register which also
#         :   must contain the first addend
# src     : positive integer, the index of the source register which must
#         :   contain the second addend
# tmp     : positive integer, the index of the temporary register
# returns : string, the 1# program which will calculate the sum, in backward
#         :   binary, of the contents of registers ``dst'' and ``src'' and store
#         :   the result back into register ``dst'' while using register ``tmp''
#         :   as temporary scratch space
def add(dst, src, tmp):
  p = ones(dst)+'#####'  # Cases on register ``dst''
  p += '111###'          # Go forward three
  p += '11111 1###'      # Go forward six
  p += '11111 1111###'   # Go forward nine
  p += ones(src)+'#####' # Cases on register ``src''
                         # Go forward thirty-five
  p += '11111 11111 11111 11111 11111 11111 11111###'
                         # Go forward twenty-six
  p += '11111 11111 11111 11111 11111 1###'
                         # Go forward twenty-seven
  p += '11111 11111 11111 11111 11111 11###'
  p += ones(src)+'#####' # Cases on register ``src''
                         # Go forward twenty-three
  p += '11111 11111 11111 11111 111###'
                         # Go forward twenty-eight
  p += '11111 11111 11111 11111 11111 111###'
                         # Go forward twenty-one
  p += '11111 11111 11111 11111 1###'
  p += ones(src)+'#####' # Cases on register ``src''
                         # Go forward twenty-one
  p += '11111 11111 11111 11111 1###'
                         # Go forward eighteen
  p += '11111 11111 11111 111###'
                         # Go forward nineteen
  p += '11111 11111 11111 1111###'
  p += ones(dst)+'#####' # Cases on register ``dst''
  p += '111###'          # Go forward three
  p += '11111 1###'      # Go forward six
  p += '11111 1111###'   # Go forward nine
  p += ones(src)+'#####' # Cases on register ``src''
                         # Go forward eleven
  p += '11111 11111 1###'
                         # Go forward sixteen
  p += '11111 11111 11111 1###'
  p += '11111 1111###'   # Go forward nine
  p += ones(src)+'#####' # Cases on register ``src''
                         # Go forward thirteen
  p += '11111 11111 111###'
  p += '11111 11111###'  # Go forward ten
                         # Go forward eleven
  p += '11111 11111 1###'
  p += ones(src)+'#####' # Cases on register ``src''
  p += '111###'          # Go forward three
  p += '11111 111###'    # Go forward eight
  p += '1###'            # Go forward one; no op
  p += ones(tmp)+'#'     # Append ``1'' to register ``tmp''
                         # Go backward thirty-three
  p += '11111 11111 11111 11111 11111 11111 111####'
  p += ones(tmp)+'##'    # Append ``#'' to register ``tmp''
                         # Go backward thirty-five
  p += '11111 11111 11111 11111 11111 11111 11111####'
  p += ones(tmp)+'#'     # Append ``1'' to register ``tmp''
                         # Go backward twenty-one
  p += '11111 11111 11111 11111 1####'
  p += ones(tmp)+'##'    # Append ``#'' to register ``tmp''
                         # Go backward twenty-three
  p += '11111 11111 11111 11111 111####'
  p += move(tmp, dst)    # Move the contents of register ``tmp'' to register
                         #   ``dst''
  return p
