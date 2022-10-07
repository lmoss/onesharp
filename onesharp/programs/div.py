from ..tools.instruction_set import enqueue_one as eo
from ..tools.instruction_set import enqueue_sharp as es
from ..tools.instruction_set import jump_forward as jf
from ..tools.instruction_set import jump_backward as jb
from ..tools.instruction_set import dequeue_and_branch as db
from ..tools.labels_to_offsets import labels_to_offsets
from ..programs.clear import clear
from ..programs.move import move
from ..programs.copy import copy
from ..programs.compare import compare

# div
# =======
# dividend      : positive integer, the index of the register in which the
#               :   dividend is passed in unary and to which the result is
#               :   written at the end of the computation (default 1)
# divisor       : positive integer, the index of the register in which the
#               :   divisor is passed in unary; on a successful return of the
#               :   1# div program, this register will be empty (default 2)
# divisor_tmp   : positive integer, the index of the temporary divisor register
#               :   that allows us to preserve the divisor across destructive
#               :   register-compare operations; this register must be passed
#               :   empty and, on a successful return of the 1# div program,
#               :   it will remain empty (default 3)
# quotient      : positive integer, the index of the register in which we build
#               :   up the quotient during the division computation; this
#               :   register must be passed empty and, on a successful return
#               :   of the 1# div program, this register will remain empty
#               :   (default 4)
# remainder     : positive integer, the index of the counter register that we
#               :   use to repeatedly count up to the divisor during the divison
#               :   operation; this register must be passed in empty and, on a
#               :   successful return of the 1# div program, this register will
#               :   remain empty (default 5)
# remainder_tmp : positive integer, the index of the temporary remainder
#               :   register that allows us to preserve the current remainder
#               :   across destructive register-compare operations; this
#               :   this register must be passed empty and, on a succesful
#               :   return of the 1# div program, it will remain empty
#               :   (default 6)
# copy_tmp      : positive integer, the index of the register that is used
#               :   as the temporary in for copy operations; it should be
#               :   passed empty and the 1# program will return with it empty
#               :   (default 7)
# error         : positive integer, the index of the error register; this
#               :   register should be passed empty and it will be returned
#               :   containing a one in some error events, but very few
#               :   potential errors are actually caught; for example, there is
#               :   not logic present to check for a zero divisor (default 8)
#               :
# returns       : string, the 1# program which divides the contents of register
#               :   ``dividend'' by register ``divisor'' and writes the result
#               :   back into register ``dividend''
#
#   examples
#   ========
#     >>> onesharp(div(1,2,3,4,5,6,7,8), ['111','11'])
#     '1#1'
#     >>> onesharp(div(1,2,3,4,5,6,7,8), ['111111','111'])
#     '11#'
#
def div(
  dividend     =1,
  divisor      =2,
  divisor_tmp  =3,
  quotient     =4,
  remainder    =5,
  remainder_tmp=6,
  copy_tmp     =7,
  error        =8
):
  p =  '<continue>'
  p +=   db(dividend)
  p +=   jf('<dividend_empty>')
  p +=   jf('<dividend_one>')
  p +=   jf('<dividend_sharp>')
  p +=   '<dividend_empty>'
           # Division complete
  p +=     move(quotient, dividend)
  p +=     es(dividend)
  p +=     move(remainder, dividend)
  p +=     clear(divisor)
  p +=     jf('<break>')
  p +=   '<dividend_one>'
  p +=     eo(remainder)
  p +=     copy(divisor, divisor_tmp, copy_tmp)
  p +=     copy(remainder, remainder_tmp, copy_tmp)
  p +=     compare(divisor_tmp, remainder_tmp)
  p +=     db(divisor_tmp)
  p +=     jf('<not_equal>')
  p +=     jf('<yes_equal>')
  p +=     jf('<error>') # Compare should never return a sharp
  p +=     '<not_equal>'
  p +=       jb('<continue>')
  p +=     '<yes_equal>'
  p +=       clear(remainder)
  p +=       eo(quotient)
  p +=       jb('<continue>')
  p +=   '<dividend_sharp>'
           # Error since we expect the dividend to be in unary
  p +=     jf('<error>')
  p += '<error>'
  p +=   eo(error)
  p += '<break>'
  return labels_to_offsets(p)
