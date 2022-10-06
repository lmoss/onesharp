from ..tools.instruction_set import enqueue_one as eo
from ..tools.instruction_set import jump_forward as jf
from ..tools.instruction_set import jump_backward as jb
from ..tools.instruction_set import dequeue_and_branch as db
from ..tools.labels_to_offsets import labels_to_offsets
from ..programs.clear import clear

# compare
# =======
# a       : positive integer, the index of the register which contains the first
#         :   string in the comparison and in which the symbol encoding the
#         :   result of the comparison will be written
# b       : positive integer, the index of the register which contains the
#         :   second string in the comparison
# returns : string, the 1# program which will compare the strings in registers
#         :   ``a'' and ``b,'' decide if they are symbol-for-symbol the same,
#         :   and if they are the same write a ``1'' back into register ``a''
#         :  but otherwise clear register ``a'' (if it is not already clear);
#         :  register``b'' will be empty when the computation is finished
def compare(a, b):
  p =  '<continue>'
  p +=   db(a)
  p +=   jf('<a_empty>')
  p +=   jf('<a_one>')
  p +=   jf('<a_sharp>')
  p +=   '<a_empty>'
  p +=     db(b)
  p +=     jf('<a_empty_b_empty>')
  p +=     jf('<a_empty_b_one>')
  p +=     jf('<a_empty_b_sharp>')
  p +=     '<a_empty_b_empty>'
             # a *does* equal b
  p +=       eo(a)
  p +=       jf('<break>')
  p +=     '<a_empty_b_one>'
             # a does *not* equal 
  p +=       clear(b)
  p +=       jf('<break>')
  p +=     '<a_empty_b_sharp>'
             # a does *not* equal b
  p +=       clear(b)
  p +=       jf('<break>')
  p +=   '<a_one>'
  p +=      db(b)
  p +=      jf('<a_one_b_empty>')
  p +=      jf('<a_one_b_one>')
  p +=      jf('<a_one_b_sharp>')
  p +=      '<a_one_b_empty>'
              # a does *not* equal b
  p +=        clear(a)
  p +=        jf('<break>')
  p +=      '<a_one_b_one>'
              # a equals b *so far*
  p +=        jb('<continue>')
  p +=      '<a_one_b_sharp>'
              # a does *not* equal b
  p +=        clear(a)
  p +=        clear(b)
  p +=        jf('<break>')
  p +=   '<a_sharp>'
  p +=     db(b)
  p +=     jf('<a_sharp_b_empty>')
  p +=     jf('<a_sharp_b_one>')
  p +=     jf('<a_sharp_b_sharp>')
  p +=     '<a_sharp_b_empty>'
             # a does *not* equal b
  p +=       clear(a)
  p +=       jf('<break>')
  p +=     '<a_sharp_b_one>'
             # a does *not* equal b
  p +=       clear(a)
  p +=       clear(b)
  p +=       jf('<break>')
  p +=     '<a_sharp_b_sharp>'
             # a equals b *so far*
  p +=       jb('<continue>')
  p += '<break>'
  return labels_to_offsets(p)
