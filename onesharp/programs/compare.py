from ..tools.ones import ones

# compare
# =======
# dst     : positive integer, the index of the destination register which
#         :   also contains the first string in the comparison
# src     : positive integer, the index of the source register which contains
#         :   the second string in the comparison
# returns : string, the 1# program which will compare the strings in registers
#         :   ``dst'' and ``src,'' decide if they are symbol-for-symbol the
#         :   same, and if they are the same write a ``1'' back into register
#         :  ``dst'' but otherwise leave register ``dst'' empty
def compare(dst, src):
  p = ones(dst)+'#####'       # Cases on register ``dst''
  p += '11111 1###'           # Go forward six
  p += '11111 1111###'        # Go forward nine
  p += ones(src)+'#####'      # Cases on register ``src''
  p += '11111 11111 1###'     # Go forward eleven
  p += '11111 11111###'       # Go forward ten
  p += '11111 1####'          # Go backward six
  p += ones(src)+'#####'      # Cases on register ``src''
  p += '11111 11111 11111###' # Go forward fifteen
  p += '11111 1###'           # Go forward six
  p += '11111###'             # Go forward five
  p += ones(src)+'#####'      # Cases on register ``src''
  p += '111###'               # Go forward three
  p += '11111 11111 111####'  # Go backward thirteen
  p += '1###'                 # Go forward one; no op
  p += ones(dst)+'#####'      # Cases on register ``dst''
  p += '111###'               # Go forward three
  p += '11####'               # Go backward two
  p += '111####'              # Go backward three
  p += ones(src)+'#####'      # Cases on register ``src''
  p += '1111###'              # Go forward four
  p += '11####'               # Go backward two
  p += '111####'              # Go backward three
  p += ones(dst)+'#'          # Append ``1'' to register ``dst''
  return p
