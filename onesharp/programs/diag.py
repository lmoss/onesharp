from ..tools.instruction_set import enqueue_one as eo
from ..tools.instruction_set import enqueue_sharp as es
from ..tools.instruction_set import jump_forward as jf
from ..tools.instruction_set import jump_backward as jb
from ..tools.instruction_set import dequeue_and_branch as db
from ..tools.labels_to_offsets import labels_to_offsets
from ..programs.move import move

# diag
# ====
# reg     : positive integer, the index of the register on whose contents the
#         :   the diag program will be executed and to which the output
#         :   write-program-text will be prepended
# tmpA    : positive integer, the index of the first temporary register
# tmpB    : positive integer, the index of the second temporary register
# returns : string, the 1# program with the property that when it is run with
#         :   contents ``x'' in register ``reg'' and registers ``tmpA'' and
#         :   ``tmpB'' empty, a halt is eventually reached with contents ``y''
#         :   in regsiter ``reg'' and registers ``tmpA'' and ``tmpB'' empty,
#         :   where ``y'' is equal to phi_{write}(x) + x
def diag(reg, tmpA, tmpB):
  p =  '<top>'
  p +=   db(reg)
  p +=   jf('<empty>')
  p +=   jf('<one>')
  p +=   '<sharp>'
  for _ in range(reg):
    p +=   eo(tmpA)
  p +=     es(tmpA)
  p +=     es(tmpA)
  p +=     es(tmpB)
  p +=     jb('<top>')
  p +=   '<one>'
  for _ in range(reg):
    p +=   eo(tmpA)
  p +=     es(tmpA)
  p +=     eo(tmpB)
  p +=     jb('<top>')
  p +=   '<empty>'
  p +=     move(tmpA, reg)
  p +=     move(tmpB, reg)
  return labels_to_offsets(p)
