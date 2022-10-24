from ..tools.instruction_set import enqueue_one as eo
from ..tools.instruction_set import enqueue_sharp as es
from ..tools.instruction_set import jump_forward as jf
from ..tools.instruction_set import jump_backward as jb
from ..tools.instruction_set import dequeue_and_branch as db
from ..tools.labels_to_offsets import labels_to_offsets
from ..programs.clear import clear
from ..programs.move import move
from ..programs.copy import copy
from ..programs.mult_unary import mult_unary

# pow_unary
# =========
# regA    : positive integer, the index of the register containing the unary
#         :   unary base that will be exponentiated and the register that the
#         :   power will be written to at the end of the computation
# regB    : positive integer, the index of the register containing the unary
#         :   exponent; the register will be returned empty
# tmpAcc  : positive integer, the first temporary register which should be
#         :   passed empty and will be returned empty
# tmpA    : positive integer, the second temporary register which should be
#         :   passed empty and will be returned empty
# tmpAA   : positive integer, the third temporary register which should be
#         :   passed empty and will be returned empty
# tmpBB   : positive integer, the fourth temporary register which should be
#         :   passed empty and will be returned empty
# tmpCopy : positive integer, the fifth temporary register which should be
#         :   passed empty and will be returned empty
# returns : string, the 1# program that when executed will exponentiate the
#         :   contents of regA to the power of regB and write the result back
#         :   into regA
def pow_unary(regA=1, regB=2, tmpAcc=3, tmpA=4, tmpAA=5, tmpBB=6, tmpCopy=7):
  p =  eo(tmpAcc)
  p += '<pow_loop>'
  p +=   db(regB)
  p +=   jf('<empty>')
  p +=   jf('<one>')
  p +=   jf('<sharp>')
  p +=   '<empty>'
  p +=     jf('<epilogue>')
  p +=   '<one>'
  p +=     copy(regA, tmpA, tmpCopy)
  p +=     mult_unary(regA=tmpAcc, regB=tmpA, tmpA=tmpAA, tmpB=tmpBB, tmpCopy=tmpCopy)
  p +=     jb('<pow_loop>')
  p +=   '<sharp>'
  p +=     jf('<error>')
  p += '<epilogue>'
  p +=   clear(regA)
  p +=   clear(regB)
  p +=   move(tmpAcc, regA)
  p += '<error>'
  return labels_to_offsets(p)
