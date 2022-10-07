from ..tools.instruction_set import enqueue_one as eo
from ..tools.instruction_set import enqueue_sharp as es
from ..tools.instruction_set import jump_forward as jf
from ..tools.instruction_set import jump_backward as jb
from ..tools.instruction_set import dequeue_and_branch as db
from ..tools.labels_to_offsets import labels_to_offsets
from ..programs.move import move

# write
# =====
# reg     : positive integer, the index of the register on whose contents the
#         :   the write program will be executed and into which the output
#         :   program-text will be written (default is 1)
# tmp     : positive integer, the index of the temporary register (default is 2)
# returns : string, the 1# program with the property that when it is run with
#         :   contents ``x'' in register ``reg'' and register ``tmp'' empty,
#         :   we eventually halt with contents ``y'' in regsiter ``reg'' and
#         :   register ``tmp'' empty, where ``y'' is a program in the 1#
#         :   language such that when ``y'' is executed (with no arguments),
#         :   the result is to write ``x'' into register ``reg''
def write(reg=1, tmp=2):
  p =  '<top>'
  p +=   db(reg)
  p +=   jf('<empty>')
  p +=   jf('<one>')
  p +=   '<sharp>'
  for _ in range(reg):
    p +=   eo(tmp)
  p +=     es(tmp)
  p +=     es(tmp)
  p +=     jb('<top>')
  p +=   '<one>'
  for _ in range(reg):
    p +=   eo(tmp)
  p +=     es(tmp)
  p +=     jb('<top>')
  p +=   '<empty>'
  p +=     move(tmp, reg)
  return labels_to_offsets(p)
