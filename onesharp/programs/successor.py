from ..tools.ones import ones
from ..programs.move import move

# successor
# =========
# reg     : positive integer, the index of the register for whose contents
#         :   the successor will be calculated
# tmp     : positive integer, the index of the temporary register
# returns : string, the 1# program which will find the successor of the
#         :   (nonnegative) backward binary integer in register ``reg''
#         :   and place the successor back into register ``reg'' while using
#         :   register ``tmp'' as temporary scratch space
def successor(reg, tmp):
  p = ones(reg)+'#####'      # Cases on register ``reg''
  p += '11111 11111 111###'  # Go forward thirteen
  p += '11111 11111###'      # Go forward ten 
  p += ones(tmp)+'#'         # Append ``1'' to register ``tmp''
  p += move(reg, tmp)        # Move the remaining contents of register ``reg''
                             #   to register ``tmp''; seven instructions
  p += '1111###'             # Go forward four
  p += ones(tmp)+'##'        # Append ``#'' to register ``tmp''
  p += '11111 11111 111####' # Go backward thirteen
  p += ones(tmp)+'#'         # Append ``1'' to register ``tmp''
  p += move(tmp, reg)        # Move the contents of register ``tmp'' to
                             #   register ``reg''
  return p
