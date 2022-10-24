from ..tools.instruction_set import enqueue_one as eo
from ..tools.instruction_set import enqueue_sharp as es
from ..tools.instruction_set import jump_forward as jf
from ..tools.instruction_set import jump_backward as jb
from ..tools.instruction_set import dequeue_and_branch as db
from ..tools.labels_to_offsets import labels_to_offsets

# add_unary
# =========
# regA    : positive integer, the index of the register containing the first
#         :   addend and the register in which the sum will be written
# regB    : positive integer, the index of the register containing the second
#         :   addend which will be returned empty
# returns : string, the 1# program that when executed will sum the unary
#         :   numbers contained in regA and regB, writing the result into
#         :   regA and leaving regB empty
def add_unary(regA=1, regB=2):
  p =  '<add_loop>'
  p +=   db(regB)
  p +=   jf('<empty>')
  p +=   jf('<one>')
  p +=   jf('<sharp>')
  p +=   '<empty>'
  p +=     jf('<end>')
  p +=   '<one>'
  p +=     eo(regA)
  p +=     jb('<add_loop>')
  p +=   '<sharp>'
  p +=     jf('<error>')
  p += '<error>'
  p += '<end>'
  return labels_to_offsets(p)
