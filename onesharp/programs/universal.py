from ..tools.instruction_set import enqueue_one as eo
from ..tools.instruction_set import enqueue_sharp as es
from ..tools.instruction_set import jump_forward as jf
from ..tools.instruction_set import jump_backward as jb
from ..tools.instruction_set import dequeue_and_branch as db
from ..tools.instruction_set import dequeue as dq
from ..tools.labels_to_offsets import labels_to_offsets
from ..programs.clear import clear
from ..programs.move import move
from ..programs.copy import copy

# The registers used in the universal 1# program
# ==============================================
PROG_TXT         =  1 # Program text : the index of the register that contains
                      #   the text of the 1# program that we are running the
                      #   universal program on
PROG_TXT_TMP     =  2 # Program text temporary : the index of the temporary
                      #   register used when cycling through the program text
INSTR_IDX        =  3 # Instruction index : the index of the register that
                      #   contains the index of the instruction in the
                      #   the program text which we would like to execute or
                      #   which is in the process of being executed; this value,
                      #   in addition to being call the ``instruction index'',
                      #   can synonymously be called the ``program counter'' and
                      #   is encoded in unary, with an empty register meaning
                      #   zero (i.e., the first instruction in the program),
                      #   ``1'' meaning one, ``11'' meaning two, etc.)
INSTR_IDX_TMP    =  4 # Instruction index temporary : the index of the register
                      #   that is used to save the instruction index when we
                      #   are counting down on the actual instruction index
                      #   register to locate an instruction in the program text
INSTR_ONES       =  5 # Instruction ones : the index of the instruction ones
                      #   register; the process of fetching an instruction
                      #   writes the number of ones in that instruction into
                      #   the instruction ones register; e.g., after the
                      #   instruction ``1111###'' is fetched, the contents of
                      #   this register will be ``1111''
INSTR_ONES_TMP   =  6 # Instruction ones temporary : the index of the register
                      #   used to save the instruction ones register when we
                      #   are doing operations directly on that register
INSTR_SHARPS     =  7 # Instruction sharps : the index of the instruction sharps
                      #   register; the process of fetching an instruction
                      #   writes the number of sharps in that instruction into
                      #   the instruction sharps register; e.g., after the
                      #   instruction ``1111###'' is fetched, the contents of
                      #   this register will be ``###''
INSTR_ONE_SAVE   =  8 # Instruction one save : the index of the temporary
                      #   register that is used when probing the boundary
                      #   between instructions in the fetch instruction module
REG_FILE         =  9 # Register file : the index of the register into which all
                      #   the registers of the program we are executing are
                      #   encoded via the encoding defined in the TRM web
                      #   text by L. Moss
REG_FILE_TMP     = 10 # Register file temporary : the index of the temporary
                      #   register used when cycling through the contents of the
                      #   register file
ENQUEUE_VAL_REG  = 11 # Enqueue value regsiter : the index of the register into
                      #   which the value to enqueue is written before control
                      #   is transfered to the enqueue module
VAL_DEQUEUED_REG = 12 # Value dequeued register : the index of the register into
                      #   which the value dequeued from the register file is
                      #   written before a call to the dequeue module returns
COPY_TMP         = 13 # Copy temporary : the index of the temporary register
                      #   that used as scratch space during copy operations 
EXCEPTION_REG    = 14 # Exception register : the index of the exception
                      #   register; there is not much error handling
                      #   (i.e., extra code to aid debugging)
                      #   in this program but, where it is present, if an
                      #   exception occurs a 1 will be written into the
                      #   exception register

def _fetch_instruction(
  prog_txt,
  prog_txt_tmp,
  instr_idx,
  instr_idx_tmp,
  instr_ones,
  instr_sharps,
  instr_one_save,
  copy_tmp
):
  p =  '<fetch-instruction>'
  p +=   '<get-ones-loop>'
  p +=     db(prog_txt)
  p +=     jf('<epilogue>') # jf('<end>')
  p +=     jf('<handle-a-one>')
  p +=     jf('<get-sharps-prologue>')
  p +=     '<handle-a-one>'
  p +=       eo(instr_ones)
  p +=       jb('<get-ones-loop>')
  p +=   '<get-sharps-prologue>'
  p +=     es(instr_sharps)
  p +=     '<get-sharps-loop>'
  p +=       db(prog_txt)
  p +=       jf('<tests>')
  p +=       jf('<between-instructions>')
  p +=       jf('<handle-a-sharp>')
  p +=       '<handle-a-sharp>'
  p +=         es(instr_sharps)
  p +=         jb('<get-sharps-loop>')
  p +=   '<between-instructions>'
  p +=     eo(instr_one_save)
  p +=     '<tests>'
  p +=       db(instr_idx)
  p +=       jf('<epilogue>')
  p +=       jf('<reloop>')
  p +=       jf('<error>')
  p +=       '<reloop>'
  p +=         move(instr_ones, prog_txt_tmp)
  p +=         move(instr_one_save, instr_ones)
  p +=         move(instr_sharps, prog_txt_tmp)
  p +=         eo(instr_idx_tmp)
  p +=         jb('<get-ones-loop>')
  p +=   '<epilogue>'
  p +=     copy(instr_ones, prog_txt_tmp, copy_tmp)
  p +=     copy(instr_sharps, prog_txt_tmp, copy_tmp)
  p +=     move(instr_one_save, prog_txt_tmp)
  p +=     move(prog_txt, prog_txt_tmp)
  p +=     move(prog_txt_tmp, prog_txt)
  p +=     move(instr_idx_tmp, instr_idx)
  p +=   '<end><error>'
  return labels_to_offsets(p)

def _populate_register_file(
  reg_file,
  reg_file_tmp,
  up_to,
  up_to_tmp,
  copy_tmp
):
  p =  copy(up_to, up_to_tmp, copy_tmp)
  p += '<populate-register-file>'
  p +=   db(up_to_tmp)
  p +=   jf('<epilogue>')
  p +=   jf('<check-reg-init-loop>')
  p +=   jf('<error>')
  p +=   '<check-reg-init-loop>'
  p +=     db(reg_file)
  p +=     jf('<handle-empty>')
  p +=     jf('<handle-one>')
  p +=     jf('<handle-sharp>')
  p +=     '<handle-one>'
  p +=       eo(reg_file_tmp)
  p +=       db(reg_file)
  p +=       jf('<error>')
  p +=       jf('<handle-one-one>')
  p +=       jf('<handle-one-sharp>')
  p +=       '<handle-one-one>'
  p +=         eo(reg_file_tmp)
  p +=         jb('<check-reg-init-loop>')
  p +=       '<handle-one-sharp>'
  p +=         es(reg_file_tmp)
  p +=         jb('<check-reg-init-loop>')
  p +=     '<handle-sharp>'
  p +=       es(reg_file_tmp)
  p +=       db(reg_file)
  p +=       jf('<error>')
  p +=       jf('<error>')
  p +=         es(reg_file_tmp)
  p +=         jb('<populate-register-file>')
  p +=     '<handle-empty>'
  p +=       es(reg_file_tmp)
  p +=       es(reg_file_tmp)
  p +=       jb('<populate-register-file>')
  p +=   '<epilogue>'
  p +=     move(reg_file, reg_file_tmp)
  p +=     move(reg_file_tmp, reg_file)
  p +=   '<error>'
  return labels_to_offsets(p)

# _enqueue_or_dequeue
# ===================
#                :
# reg_file       : positive integer, the index of the register in which all the
#                :   registers of the program we are executing via the
#                :   universal program are encoded; we expect the registers
#                :   to be encoded using the scheme defined in the universal
#                :   program chapter of the TRM web text by L. Moss
#                :
# reg_file_tmp   : positive integer, the index of the temporary register used
#                :   when cycling through the register-file register
#                :
# reg_to_get     : positive integer, the index of the register that we are
#                :   either enqueuing a character into or dequeuing a character
#                :   from
#                :
# reg_to_get_tmp : positive integer, the index of the register that we use to
#                :   to save the contents of the ``reg_to_get'' register while
#                :   we are doing processing directly on that register
#                :
# copy_tmp       : positive integer, the index of the register that we use for
#                :   temporary scratch space during copy operations
#                :
# is_enqueue     : boolean, whether to return the 1# code module for enqueue
#                :   or dequeue; if ``True'' then enqueue, and if ``false''
#                :   then dequeue; this is the only variable in this entire file
#                :   (universal.py) which is a sort of ``meta'' variable with
#                :   respect to the 1# program that is being generated and which
#                :   isn't included in the 1# program itself; all other
#                :   variables in this file are positive integers which each
#                :   refer to the index of a Moss machine register that is
#                :   operated on in the actual 1# program that is generated
#                :   by the Python code in this file
#                :
# enqueue_val    : positive integer, the index of the register into which the
#                :   the value is passed to this module to enqueue into the
#                :   register file in the case of an enqueue operation; in the
#                :   case of a dequeue operation, this register will not be used
#                :
# val_dequeued   : positive integer, the index of the register into which the
#                :   the value will be stored that is dequeued from the register
#                :   file in the case of a dequeue operation; in the case of an
#                :   enqueue operation, this register will not be used
#                :
# returns        : string, the 1# subprogram of the universal program which will
#                :   either enqueue a character into a specified register in the
#                :   the register file or will dequeue a character from a
#                :   specified register in the register file, depending on the
#                :   value specified for the ``is_enqueue'' argument
#                :
#   Summary of the 1# code modules that are returned for enqueuing and dequeuing
#   ----------------------------------------------------------------------------
#           The enqueue and dequeue modules both begin with a call to the
#   ``_populate_regsiter_file'' module for which the index of the register that
#   will be enqueued to or dequeued from is passed. The result of this call is
#   that the register file is initialized up to the index of the register that
#   will be enqueued to or dequeued from, if it is not already. For example,
#   if the register file contains ``11 ## ##'', encoding an R1 contents of
#   ``1'', an empty R2, and the remaining registers uninitialized, and if
#   further the enqueue or dequeue operation that we are preparing to perform
#   will operate on R4, then our call to the populate-register-file module will
#   result in R3 and R4 being initialized in the regsiter file so the new
#   contents are ``11 ## ## ## ##''. Initializing the register in the register
#   file that we will operate on before we begin the operation simplifies coding
#   the operation itself in 1#.
#           After the register file has been initialized up to the register we
#   will operate on, we next cycle through the register file until we reach
#   the index of that register to operate on. Once the register has been
#   reached, the action is of course different for an enqueue versus a dequeue
#   operation. For enqueue, we continue to cycle through the current register
#   until we reach the end-of-register code ``##''. At this point we append the
#   value that we are enqueuing onto the cycle-temporary-register
#   ``reg_file_tmp'', then we copy the remaining contents of the register file
#   onto the cycle register, followed by copying the cycle register back into
#   the ``reg_file'' register. At this point the enqueue operation is complete.
#           In the case of a dequeue operation, the value encoded into the
#   register of interest in the first position is read, without copying it into
#   the cycle register. Instead it is copied into the ``val_dequeued'' register
#   to be returned to the calling module. After this operation is complete,
#   the remaining contents, if any, of the register that we just dequeued from
#   are copied onto the cycle register, and after that all of the remaining
#   contents of the register file are copied onto the cycle register, and
#   finally the contents of the cycle register are moved back into the register
#   file, to complete the cycle. At this point the dequeue operation is
#   complete.
#
def _enqueue_or_dequeue(
  reg_file,
  reg_file_tmp,
  reg_to_get,
  reg_to_get_tmp,
  copy_tmp,
  is_enqueue,
  enqueue_val,
  val_dequeued
):
  assert type(reg_file) is int and reg_file > 0
  assert type(reg_file_tmp) is int and reg_file_tmp > 0
  assert type(reg_to_get) is int and reg_to_get > 0
  assert type(reg_to_get_tmp) is int and reg_to_get_tmp > 0
  assert type(copy_tmp) is int and copy_tmp > 0
  assert type(is_enqueue) is bool and is_enqueue in [True,False]
  assert type(enqueue_val) is int and enqueue_val > 0
  assert type(val_dequeued) is int and val_dequeued > 0
  p =  '<get-register>'
  p +=   eo(reg_to_get)
  p +=   _populate_register_file(
           reg_file     = reg_file,
           reg_file_tmp = reg_file_tmp,
           up_to        = reg_to_get,
           up_to_tmp    = reg_to_get_tmp,
           copy_tmp     = copy_tmp
         )
  p +=   dq(reg_to_get)
  p +=   copy(reg_to_get, reg_to_get_tmp, copy_tmp)
  p +=   '<for-each-reg>'
  p +=     db(reg_to_get_tmp)
  p +=     jf('<get-cur-reg>')
  p +=     jf('<bypass-cur-reg>')
  p +=     jf('<error>')
  p +=     '<bypass-cur-reg>'
  p +=       db(reg_file)
  p +=       jf('<error>')
  p +=       jf('<one>')
  p +=       jf('<sharp>')
  p +=       '<one>'
  p +=         db(reg_file)
  p +=         jf('<error>')
  p +=         jf('<one-one>')
  p +=         jf('<one-sharp>')
  p +=         '<one-one>'
  p +=           eo(reg_file_tmp)
  p +=           eo(reg_file_tmp)
  p +=           jb('<bypass-cur-reg>')
  p +=         '<one-sharp>'
  p +=           eo(reg_file_tmp)
  p +=           es(reg_file_tmp)
  p +=           jb('<bypass-cur-reg>')
  p +=       '<sharp>'
  p +=         db(reg_file)
  p +=         jf('<error>')
  p +=         jf('<error>')
  p +=         jf('<sharp-sharp>')
  p +=         '<sharp-sharp>'
  p +=           es(reg_file_tmp)
  p +=           es(reg_file_tmp)
  p +=           jb('<for-each-reg>')
  p +=     '<get-cur-reg>'
  if False == is_enqueue: # Include instructions for dequeue
    p +=     db(reg_file)
    p +=     jf('<error>')
    p +=     jf('<-one->')
    p +=     jf('<-sharp->')
    p +=     '<-one->'
    p +=       db(reg_file)
    p +=       jf('<error>')
    p +=       jf('<-one-one->')
    p +=       jf('<-one-sharp->')
    p +=       '<-one-one->'
    p +=         eo(val_dequeued)
    p +=         jf('<epilogue>')
    p +=       '<-one-sharp->'
    p +=         es(val_dequeued)
    p +=         jf('<epilogue>')
    p +=     '<-sharp->'
    p +=       db(reg_file)
    p +=       jf('<error>')
    p +=       jf('<error>')
    p +=       jf('<-sharp-sharp->')
    p +=       '<-sharp-sharp->'
    p +=         es(reg_file_tmp)
    p +=         es(reg_file_tmp)
    p +=         jf('<epilogue>')
  elif True == is_enqueue: # Include instructions for enqueue
    p +=     db(reg_file)
    p +=     jf('<error>')
    p +=     jf('<--one-->')
    p +=     jf('<--sharp-->')
    p +=     '<--one-->'
    p +=       db(reg_file)
    p +=       jf('<error>')
    p +=       jf('<--one--one-->')
    p +=       jf('<--one--sharp-->')
    p +=       '<--one--one-->'
    p +=         eo(reg_file_tmp)
    p +=         eo(reg_file_tmp)
    p +=         jb('<get-cur-reg>')
    p +=       '<--one--sharp-->'
    p +=         eo(reg_file_tmp)
    p +=         es(reg_file_tmp)
    p +=         jb('<get-cur-reg>')
    p +=     '<--sharp-->'
    p +=       db(reg_file)
    p +=       jf('<error>')
    p +=       jf('<error>')
    p +=       jf('<--sharp--sharp-->')
    p +=       '<--sharp--sharp-->'
    p +=         copy(enqueue_val, reg_file_tmp, copy_tmp)
    p +=         es(reg_file_tmp)
    p +=         es(reg_file_tmp)
    p +=         jf('<epilogue>')
  else:
    assert False # ``is_enqueue'' must be either True or False
  p +=   '<epilogue>'
  p +=     move(reg_file, reg_file_tmp)
  p +=     move(reg_file_tmp, reg_file)
  p +=   '<error>'
  return labels_to_offsets(p)

def _execute_instruction(
  instr_idx,
  instr_ones,
  instr_ones_tmp,
  instr_sharps,
  reg_file,
  reg_file_tmp,
  copy_tmp,
  enqueue_val_reg,
  val_dequeued_reg
):
  p =  '<execute-instruction>'
  p +=   dq(instr_sharps)
  p +=   db(instr_sharps)
  p +=   jf('<enqueue-one>')
  p +=   jf('<error>')
  p +=     db(instr_sharps)
  p +=     jf('<enqueue-sharp>')
  p +=     jf('<error>')
  p +=       db(instr_sharps)
  p +=       jf('<jump-forward>')
  p +=       jf('<error>')
  p +=         db(instr_sharps)
  p +=         jf('<jump-backward>')
  p +=         jf('<error>')
  p +=           db(instr_sharps)
  p +=           jf('<dequeue-and-branch>')
  p +=           jf('<error>')
  p +=           jf('<error>')
  p +=   '<enqueue-one>'
  p +=     dq(instr_ones)
  p +=     eo(enqueue_val_reg)
  p +=     eo(enqueue_val_reg)
  p +=     _enqueue_or_dequeue(
             reg_file       = reg_file,
             reg_file_tmp   = reg_file_tmp,
             reg_to_get     = instr_ones,
             reg_to_get_tmp = instr_ones_tmp,
             copy_tmp       = copy_tmp,
             is_enqueue     = True,
             enqueue_val    = enqueue_val_reg,
             val_dequeued   = val_dequeued_reg
           )
  p +=     eo(instr_ones)
  p +=     eo(instr_idx) # Advance the program counter by 1
  p +=     jf('<end>')
  p +=   '<enqueue-sharp>'
  p +=     dq(instr_ones)
  p +=     eo(enqueue_val_reg)
  p +=     es(enqueue_val_reg)
  p +=     _enqueue_or_dequeue(
             reg_file       = reg_file,
             reg_file_tmp   = reg_file_tmp,
             reg_to_get     = instr_ones,
             reg_to_get_tmp = instr_ones_tmp,
             copy_tmp       = copy_tmp,
             is_enqueue     = True,
             enqueue_val    = enqueue_val_reg,
             val_dequeued   = val_dequeued_reg
           )
  p +=     eo(instr_ones)
  p +=     eo(instr_idx) # Advance the program counter by 1
  p +=     jf('<end>')
  p +=   '<jump-forward>'
  p +=     copy(instr_ones, instr_idx, copy_tmp)
  p +=     jf('<end>')
  p +=   '<jump-backward>'
  p +=     copy(instr_ones, instr_ones_tmp, copy_tmp)
  p +=     '<jb-loop>'
  p +=       db(instr_ones_tmp)
  p +=       jf('<end>')
  p +=       jf('<jb-one>')
  p +=       jf('<error>')
  p +=       '<jb-one>'
  p +=         db(instr_idx)
  p +=         jf('<error>')
  p +=         jb('<jb-loop>')
  p +=         jf('<error>')
  p +=   '<dequeue-and-branch>'
  p +=     dq(instr_ones)
  p +=     _enqueue_or_dequeue(
             reg_file       = reg_file,
             reg_file_tmp   = reg_file_tmp,
             reg_to_get     = instr_ones,
             reg_to_get_tmp = instr_ones_tmp,
             copy_tmp       = copy_tmp,
             is_enqueue     = False,
             enqueue_val    = enqueue_val_reg,
             val_dequeued   = val_dequeued_reg
           )
  p +=     eo(instr_ones)
  p +=     db(val_dequeued_reg)
  p +=     jf('<db-empty>')
  p +=     jf('<db-one>')
  p +=     jf('<db-sharp>')
  p +=     '<db-empty>'
  p +=       eo(instr_idx)
  p +=       jf('<end>')
  p +=     '<db-one>'
  p +=       eo(instr_idx)
  p +=       eo(instr_idx)
  p +=       jf('<end>')
  p +=     '<db-sharp>'
  p +=       eo(instr_idx)
  p +=       eo(instr_idx)
  p +=       eo(instr_idx)
  p +=       jf('<end>')
  p +=   '<end><error>'
  return labels_to_offsets(p)

def universal(
  prog_txt         = PROG_TXT,
  prog_txt_tmp     = PROG_TXT_TMP,
  instr_idx        = INSTR_IDX,
  instr_idx_tmp    = INSTR_IDX_TMP,
  instr_ones       = INSTR_ONES,
  instr_ones_tmp   = INSTR_ONES_TMP,
  instr_sharps     = INSTR_SHARPS,
  instr_one_save   = INSTR_ONE_SAVE,
  reg_file         = REG_FILE,
  reg_file_tmp     = REG_FILE_TMP,
  enqueue_val_reg  = ENQUEUE_VAL_REG,
  val_dequeued_reg = VAL_DEQUEUED_REG,
  copy_tmp         = COPY_TMP,
  exception_reg    = EXCEPTION_REG
):
  p =  '<program-loop>'
  p +=   _fetch_instruction(
           prog_txt       = prog_txt,
           prog_txt_tmp   = prog_txt_tmp,
           instr_idx      = instr_idx,
           instr_idx_tmp  = instr_idx_tmp,
           instr_ones     = instr_ones,
           instr_sharps   = instr_sharps,
           instr_one_save = instr_one_save,
           copy_tmp       = copy_tmp
         )
         # Check for terminal state, otherwise execute instruction
  p +=   db(instr_sharps)
  p +=   jf('<epilogue>') # jf('<end>') for debugging
  p +=   jf('<error>')
  p +=     es(instr_sharps)
  p +=     _execute_instruction(
             instr_idx        = instr_idx,
             instr_ones       = instr_ones,
             instr_ones_tmp   = instr_ones_tmp,
             instr_sharps     = instr_sharps,
             reg_file         = reg_file,
             reg_file_tmp     = reg_file_tmp,
             copy_tmp         = copy_tmp,
             enqueue_val_reg  = enqueue_val_reg,
             val_dequeued_reg = val_dequeued_reg
           )
  p +=     clear(instr_ones)
  p +=     clear(enqueue_val_reg)
  p +=     clear(val_dequeued_reg)
  p +=     jb('<program-loop>') # jf('<end>') for debugging
  p +=   '<epilogue>'
  p +=     clear(instr_idx)
           # Write the encoded value of R1 into the actual program txt reg (R1)
  p +=     clear(instr_ones)
  p +=     clear(prog_txt)
  for _ in range(prog_txt-1):
    p +=   eo(instr_ones)
  p +=     '<final-output-loop>'
  p +=       _enqueue_or_dequeue(
               reg_file       = reg_file,
               reg_file_tmp   = reg_file_tmp,
               reg_to_get     = instr_ones,
               reg_to_get_tmp = instr_ones_tmp,
               copy_tmp       = copy_tmp,
               is_enqueue     = False,
               enqueue_val    = enqueue_val_reg,
               val_dequeued   = val_dequeued_reg
             )
  p +=       db(val_dequeued_reg)
  p +=       jf('<check-reg-remaining>')
  p +=       jf('<one>')
  p +=       jf('<sharp>')
  p +=       '<one>'
  p +=         eo(prog_txt)
  p +=         jb('<final-output-loop>')
  p +=       '<sharp>'
  p +=         es(prog_txt)
  p +=         jb('<final-output-loop>')
  p +=       '<check-reg-remaining>'
               # If the reg file encodes only empty registers, we want to clear
               #   it out for a good halt, but if there are any non-empty regs,
               #   we want to leave them so we get a bad halt
  p +=         db(reg_file)
  p +=         jf('<end>')
  p +=         jf('<-one->')
  p +=         jf('<-sharp->')
  p +=         '<-one->'
  p +=           eo(exception_reg)
  p +=           jf('<end>')
  p +=         '<-sharp->'
  p +=           db(reg_file)
  p +=           jf('<error>')
  p +=           jf('<error>')
  p +=           jb('<check-reg-remaining>')
  p +=   '<end><error>'
  return labels_to_offsets(p)
