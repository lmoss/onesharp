from ..tools.instruction_set import enqueue_one as eo
from ..tools.instruction_set import enqueue_sharp as es
from ..tools.instruction_set import jump_forward as jf
from ..tools.instruction_set import jump_backward as jb
from ..tools.instruction_set import dequeue_and_branch as db
from ..tools.labels_to_offsets import labels_to_offsets
from ..programs.clear import clear
from ..programs.move import move
from ..programs.copy import copy
from ..programs.add_unary import add_unary

# mult_unary
# ==========
# regA    : positive integer, the index of the register containing the
#         :   first factor and the register in which the product will be written
#         :   at the end of the computation
# regB    : positive integer, the index of the register containing the second
#         :   factor which will be returned empty
# tmpA    : positive integer, the first temporary register which should be
#         :   passed empty and will be returned empty
# tmpB    : positive integer, the second temporary register which should be
#         :   passed empty and will be returned empty
# tmpCopy : positive integer, the third temporary register which should be
#         :   passed empty and will be returned empty
# returns : string, the 1# program with that when executed will multiply the
#         :   unary numbers contained in regA and regB, writing the result into
#         :   regA and leaving regB empty
def mult_unary(regA=1, regB=2, tmpA=3, tmpB=4, tmpCopy=5):
  p =  '<mult_loop>'
  p +=   db(regA)
  p +=   jf('<empty>')
  p +=   jf('<one>')
  p +=   jf('<sharp>')
  p +=   '<empty>'
  p +=     jf('<epilogue>')
  p +=   '<one>'
  p +=     copy(regB, tmpB, tmpCopy)
  p +=     add_unary(tmpA, tmpB)
  p +=     jb('<mult_loop>')
  p +=   '<sharp>'
  p +=     jf('<error>')
  p += '<epilogue>'
  p +=   move(tmpA, regA)
  p +=   clear(regB)
  p += '<error>'
  return labels_to_offsets(p)
