from ..tools.ones import ones
from ..programs.move import move

# copy
# ====
# src     : positive integer, the index of the source register
# dst     : positive integer, the index of the destination register
# tmp     : positive integer, the index of the temporary register
# returns : string, the 1# program to copy the contents from register ``src'' to
#         :  register ``dst'' using register ``tmp'' as temporary scratch space
def copy(src, dst, tmp):
  p = ones(src)+'#####' # Cases on register ``src''
  p += '11111 111###'   # Go forward eight 
  p += '1111###'        # Go forward four
  p += ones(dst)+'##'   # Append ``#'' to register ``dst''
  p += ones(tmp)+'##'   # Append ``#'' to register ``tmp''
  p += '11111####'      # Go backward five
  p += ones(dst)+'#'    # Append ``1'' to register ``dst''
  p += ones(tmp)+'#'    # Append ``1'' to register ``tmp''
  p += '11111 111####'  # Go backward eight
  p += move(tmp, src)   # Move the contents of register ``tmp'' to register
                        #   ``src''
  return p
