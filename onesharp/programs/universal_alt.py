from ..tools.instruction_set import enqueue_one as eo
from ..tools.instruction_set import enqueue_sharp as es
from ..tools.instruction_set import jump_forward as jf
from ..tools.instruction_set import jump_backward as jb
from ..tools.instruction_set import dequeue_and_branch as db
from ..tools.instruction_set import dequeue as dq
from ..tools.labels_to_offsets import labels_to_offsets
from ..tools.sanity import sanity
from ..programs.clear import clear
from ..programs.move import move
from ..programs.copy import copy

# _beige
# ======
#   Design and implementation of _beige function by Sarah Peterson
#   The function is used to fetch the instruction in the program text (R1)
#     that is pointed to by the program counter (R2), with the fetched
#     instruction returned in R3, and R1 and R2 remain as they were before
#     the call
def _beige():
  p = '11#####111111111111111111111111111111111111111111111111111111111###11###1#111111111#111#####111###11####111####1#####1111111111111111111111111111111###11###1#111#1#####11111111111111111111111111###11###111###111#11111####111##1#####1111111111111111111###111###111##1111####111111#1#####111111###111###111111##1111####111111#111111####111111#####111111###111###1##1111####1#111111####111#####11111111###1111###11111##11111111##11111####11111#11111111#11111111####11111111#####111111###111###111##1111####111#111111####111111111111111111111111111111111111111111111111111111111####1#####111111###111###11111##1111####11111#111111####11111#####111111###111###1##1111####1#111111####111111111#####111111###111###11##1111####11#111111####'
  return p

# _jump
# =====
#   Design and implementation of _jump function by Joshua Kim
#   The function is used to execute instructions with opcode of three and four
#     sharps (i.e., jump forward or backward)
def _jump():
  p = [
    # This program assumes that it get the nth instruction in R3 (e.g. 1111### in R3)
    # R1 has the whole program text.
    # R2 has the currently instruction number. (what instruction we are on).
    # R3 has the nth instruction.
    # R4 is emtpy.
    
    #one_loop will count the number of 1's in the instruction and put them in R4.
    ['one_loop', 'cases', 3, 'empty_one', 'one_one', 'sharp_one'],
      ['empty_one', 'goto', 'end'],  # If empty go to end
      ['one_one', '1111#'], # If one, add 1 in R4 and one_loop again.
      ['goto', 'one_loop'], 
      ['sharp_one', 'goto', 'sharp_loop_one'], # After counting all the 1's, how count the sharps.
    
    
    # This loop will count how many sharps are in the instruction.
    ['sharp_loop_one', 'cases', 3, 'empty__one', 'one__one', 'sharp__one'],
      ['empty__one', 'goto', 'one_sharp_case'], # If it is empty, instruction had one sharp, so go to one sharp cases which is adding a 1 in a register.
      ['one__one', 'goto', 'end'], # There can't be a one, so if it is a one, end.
      ['sharp__one', 'goto', 'sharp_loop_two'], # If there is a sharp, then we would go to next loop to see how many more sharps there are.
    
    # Same logic, this loop will count sharps. This one is for 2 sharps.
    ['sharp_loop_two', 'cases', 3, 'empty__two', 'one__two', 'sharp__two'],
      ['empty__two', 'goto', 'two_sharp_case'],
      ['one__two', 'goto', 'end'],
      ['sharp__two', 'goto', 'sharp_loop_three'],
    
    # This one is three sharps which is important.
    ['sharp_loop_three', 'cases', 3, 'empty__three', 'one__three', 'sharp__three'],
      ['empty__three', 'goto', 'three_sharp_case'], 
      ['one__three', 'goto', 'end'],
      ['sharp__three', 'goto', 'sharp_loop_four'], 
    
    # This one is four sharp.
    ['sharp_loop_four', 'cases', 3, 'empty__four', 'one__four', 'sharp__four'],
      ['empty__four', 'goto', 'four_sharp_case'],
      ['one__four', 'goto', 'end'],
      ['sharp__four', 'goto', 'sharp_loop_five'],
    
    # This one is five sharp.
    ['sharp_loop_five', 'cases', 3, 'empty__five', 'one__five', 'sharp__five'],
      ['empty__five', 'goto', 'five_sharp_case'],
      ['one__five', 'goto', 'end'],
      ['sharp__five', 'goto', 'end'],
    
    # This is what happens for each sharps.
    ['one_sharp_case', 'goto', 'end'],  # This is where you would put adding a 1 (one sharp case)
    ['two_sharp_case', 'goto', 'end'],  # Two sharp case
    
    
    ['three_sharp_case', move(4,2)], # Three sharp case, this is jump foward, so add the 1's we counted from the instruction to R2 which has the number of current instruction we are on.
    
    # This is the jump backward case.
    ['four_sharp_case', 'goto', 'jump_back'], # we will run cases on R4, and each time delete a 1 from R2 untill R4 is empty.
    ['jump_back', 'cases', 4, 'empty_jb', 'one_jb', 'sharp_jb'],
      ['empty_jb', 'goto', 'end'],
      ['one_jb', 'goto', 'minus_one_cases'],
      ['sharp_jb', 'goto', 'end'],
    
    # This is where deleting a 1 from R2 occurs.
    ['minus_one_cases', 'cases', 2, 'empty_MO', 'one_MO', 'sharp_mo'],
      ['empty_MO', 'goto', 'jump_back'],
      ['one_MO', 'goto', 'jump_back'],
      ['sharp_mo', 'goto', 'jump_back'],
    
    ['five_sharp_case', 'goto', 'end'],
    
    ['end', '1###']
  ]
  return sanity(p)

# _populate_register_file
# =======================
#   Design concept of _populate_register_file function by Rhodes Talaga and
#     Jacob Striebel; implementation by Jacob Striebel
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
#   Design concept of _enqueue_or_dequeue function by J. Philip Pampreen and
#     Jacob Striebel; this implementation by Jacob Striebel
#                :
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

# universal_alt
# =============
#   Design concept credit for the universal_alt function goes to all group
#     members; the implementation below is by Jacob Striebel; credit for each
#     helper function that is defined above in this file and that is
#     used by the universal_alt function is given in the helper
#     functions' header comments
def universal_alt(
  prog_txt         = 1,  # Program text : the index of the register that contains
                         #   the text of the 1# program that we are running the
                         #   universal program on
  instr_idx        = 2,  # Instruction index : the index of the register that
                         #   contains the index of the instruction in the
                         #   the program text which we would like to execute or
                         #   which is in the process of being executed; this value,
                         #   in addition to being call the ``instruction index'',
                         #   can synonymously be called the ``program counter'' and
                         #   is encoded in unary, with an empty register meaning
                         #   zero (i.e., the first instruction in the program),
                         #   ``1'' meaning one, ``11'' meaning two, etc.)
  instr_txt        = 3,  # Instruction text : the index of the register which is
                         #   used to store the text of an instruction that has
                         #   just been fetched, before the instruction is split
                         #   into its ones and sharps parts
  jump_tmp         = 4,  # Jump temporary : the index of the jump temporary
                         #   register which is used in the _jump function
  instr_ones       = 20, # Instruction ones : the index of the instruction ones
                         #   register; the process of fetching an instruction
                         #   writes the number of ones in that instruction into
                         #   the instruction ones register; e.g., after the
                         #   instruction ``1111###'' is fetched, the contents of
                         #   this register will be ``1111''
  instr_ones_tmp   = 21, # Instruction ones temporary : the index of the register
                         #   used to save the instruction ones register when we
                         #   are doing operations directly on that register
  instr_sharps     = 22, # Instruction sharps : the index of the instruction sharps
                         #   register; the process of fetching an instruction
                         #   writes the number of sharps in that instruction into
                         #   the instruction sharps register; e.g., after the
                         #   instruction ``1111###'' is fetched, the contents of
                         #   this register will be ``###''
  reg_file         = 23, # Register file : the index of the register into which all
                         #   the registers of the program we are executing are
                         #   encoded via the encoding defined in the TRM web
                         #   text by L. Moss
  reg_file_tmp     = 24, # Register file temporary : the index of the temporary
                         #   register used when cycling through the contents of the
                         #   register file
  enqueue_val_reg  = 25, # Enqueue value regsiter : the index of the register into
                         #   which the value to enqueue is written before control
                         #   is transfered to the enqueue module
  val_dequeued_reg = 26, # Value dequeued register : the index of the register into
                         #   which the value dequeued from the register file is
                         #   written before a call to the dequeue module returns
  copy_tmp         = 27  # Copy temporary : the index of the temporary register
                         #   that used as scratch space during copy operations
):
  p =      eo(instr_idx) # Initialize the program counter PC (i.e., R2) to point
                         #   to the first instruction
  p += '<program_loop>'
  p +=     _beige()    # Fetch the instruction pointed to by PC and write it
                       #   into R3
  # Execute the instruction in R3; if R3 is empty, we are in the terminal state
  p +=     db(instr_txt)
  p +=     jf('<instruction_parse_precheck_empty>')
  p +=     jf('<instruction_parse_precheck_one>')
  p +=     jf('<instruction_parse_precheck_sharp>')
  p +=     '<instruction_parse_precheck_empty>'
               # The instruction register (R3) is empty
  p +=         jf('<epilogue>')
  p +=     '<instruction_parse_precheck_one>'
               # The instruction register (R3) starts with a one: so far so good
  p +=         eo(instr_ones)
  p +=         jf('<instruction_get_ones_loop>')
  p +=     '<instruction_parse_precheck_sharp>'
               # Error: an instruction cannot begin with a sharp
  p +=         jf('<end>')
  p +=     '<instruction_get_ones_loop>'
  p +=         db(instr_txt)
  p +=         jf('<instruction_get_ones_empty>')
  p +=         jf('<instruction_get_ones_one>')
  p +=         jf('<instruction_get_ones_sharp>')
  p +=         '<instruction_get_ones_empty>'
                   # Error: the data part of an instruction must be followed by
                   #   must be followed by a sharp
  p +=             jf('<end>')
  p +=         '<instruction_get_ones_one>'
  p +=             eo(instr_ones)
  p +=             jb('<instruction_get_ones_loop>')
  p +=         '<instruction_get_ones_sharp>'
  p +=             es(instr_sharps)
  p +=             jf('<instruction_get_sharps_loop>')
  p +=     '<instruction_get_sharps_loop>'
  p +=         db(instr_txt)
  p +=         jf('<instruction_get_sharps_empty>')
  p +=         jf('<instruction_get_sharps_one>')
  p +=         jf('<instruction_get_sharps_sharp>')
  p +=         '<instruction_get_sharps_empty>'
  p +=             jf('<execute_instruction>')
  p +=         '<instruction_get_sharps_one>'
                   # Error: in a single instruction, a one cannot follow a
                   #   sharp
  p +=             jf('<end>')
  p +=         '<instruction_get_sharps_sharp>'
  p +=             es(instr_sharps)
  p +=             jb('<instruction_get_sharps_loop>')
  p +=     '<execute_instruction>'
           # We first save the full instruction text back into its regsiter
           #   instr_txt (R3) which we just clobbered when we separated data
           #   (ones) from opcode (sharps)
  p +=     copy(instr_ones, instr_txt, copy_tmp)
  p +=     copy(instr_sharps, instr_txt, copy_tmp)
           # Decode and execute
  p +=     db(instr_sharps)
  p +=     jf('<instruction_read_first_sharp_empty>')
  p +=     jf('<instruction_read_first_sharp_one>')
  p +=     jf('<instruction_read_first_sharp_sharp>')
  p +=     '<instruction_read_first_sharp_empty>'
               # Error: a legal instruction opcode cannot contain zero sharps
  p +=         jf('<end>')
  p +=     '<instruction_read_first_sharp_one>'
               # Error
  p +=         jf('<end>')
  p +=     '<instruction_read_first_sharp_sharp>'
  p +=         jf('<instruction_read_second_sharp>')
  p +=     '<instruction_read_second_sharp>'
  p +=     db(instr_sharps)
  p +=     jf('<instruction_read_second_sharp_empty>')
  p +=     jf('<instruction_read_second_sharp_one>')
  p +=     jf('<instruction_read_second_sharp_sharp>')
  p +=     '<instruction_read_second_sharp_empty>'
               ############################################
               # Opcode is a single sharp (enqueue a one) #
               ############################################
  p +=         dq(instr_ones)
  p +=         eo(enqueue_val_reg)
  p +=         eo(enqueue_val_reg)
  p +=         _enqueue_or_dequeue(
                 reg_file       = reg_file,
                 reg_file_tmp   = reg_file_tmp,
                 reg_to_get     = instr_ones,
                 reg_to_get_tmp = instr_ones_tmp,
                 copy_tmp       = copy_tmp,
                 is_enqueue     = True,
                 enqueue_val    = enqueue_val_reg,
                 val_dequeued   = val_dequeued_reg
               )
  p +=         clear(instr_ones) #eo(instr_ones)
  p +=         clear(enqueue_val_reg)
  p +=         eo(instr_idx) # Advance the program counter by one
  p +=         jb('<program_loop>')
               ############################################
               ############################################
  p +=     '<instruction_read_second_sharp_one>'
               # Error
  p +=         jf('<end>')
  p +=     '<instruction_read_second_sharp_sharp>'
  p +=         jf('<instruction_read_third_sharp>')
  p +=     '<instruction_read_third_sharp>'
  p +=     db(instr_sharps)
  p +=     jf('<instruction_read_third_sharp_empty>')
  p +=     jf('<instruction_read_third_sharp_one>')
  p +=     jf('<instruction_read_third_sharp_sharp>')
  p +=     '<instruction_read_third_sharp_empty>'
               ##############################################
               # Opcode is a double sharp (enqueue a sharp) #
               ##############################################
  p +=         dq(instr_ones)
  p +=         eo(enqueue_val_reg)
  p +=         es(enqueue_val_reg)
  p +=         _enqueue_or_dequeue(
                 reg_file       = reg_file,
                 reg_file_tmp   = reg_file_tmp,
                 reg_to_get     = instr_ones,
                 reg_to_get_tmp = instr_ones_tmp,
                 copy_tmp       = copy_tmp,
                 is_enqueue     = True,
                 enqueue_val    = enqueue_val_reg,
                 val_dequeued   = val_dequeued_reg
               )
  p +=         clear(instr_ones) #eo(instr_ones)
  p +=         clear(enqueue_val_reg)
  p +=         eo(instr_idx) # Advance the program counter by one
  p +=         jb('<program_loop>')
               ##############################################
               ##############################################
  p +=     '<instruction_read_third_sharp_one>'
               # Error
  p +=         jf('<end>')
  p +=     '<instruction_read_third_sharp_sharp>'
  p +=         jf('<instruction_read_fourth_sharp>')
  p +=     '<instruction_read_fourth_sharp>'
  p +=     db(instr_sharps)
  p +=     jf('<instruction_read_fourth_sharp_empty>')
  p +=     jf('<instruction_read_fourth_sharp_one>')
  p +=     jf('<instruction_read_fourth_sharp_sharp>')
  p +=     '<instruction_read_fourth_sharp_empty>'
               ###########################################
               # Opcode is a triple sharp (jump forward) #
               ###########################################
  p +=         clear(instr_ones)
  p +=         _jump() # This subprogram will clear out instr_txt (R3)
  p +=         jb('<program_loop>')
               ###########################################
               ###########################################
  p +=     '<instruction_read_fourth_sharp_one>'
               # Error
  p +=         jf('<end>')
  p +=     '<instruction_read_fourth_sharp_sharp>'
  p +=         jf('<instruction_read_fifth_sharp>')
  p +=     '<instruction_read_fifth_sharp>'
  p +=     db(instr_sharps)
  p +=     jf('<instruction_read_fifth_sharp_empty>')
  p +=     jf('<instruction_read_fifth_sharp_one>')
  p +=     jf('<instruction_read_fifth_sharp_sharp>')
  p +=     '<instruction_read_fifth_sharp_empty>'
               ###############################################
               # Opcode is a quadruple sharp (jump backward) #
               ###############################################
  p +=         clear(instr_ones)
  p +=         _jump() # This subprogram will clear out instr_txt (R3)
  p +=         jb('<program_loop>')
               ###############################################
               ###############################################
  p +=     '<instruction_read_fifth_sharp_one>'
               # Error
  p +=         jf('<end>')
  p +=     '<instruction_read_fifth_sharp_sharp>'
  p +=         jf('<instruction_read_hypothetical_sixth_sharp>')
  p +=     '<instruction_read_hypothetical_sixth_sharp>'
  p +=     db(instr_sharps)
  p +=     jf('<instruction_read_hypothetical_sixth_sharp_empty>')
  p +=     jf('<instruction_read_hypothetical_sixth_sharp_one>')
  p +=     jf('<instruction_read_hypothetical_sixth_sharp_sharp>')
  p +=     '<instruction_read_hypothetical_sixth_sharp_empty>'
               #################################################
               # Opcode is pentuple sharp (dequeue and branch) #
               #################################################
  p +=         dq(instr_ones)
  p +=         _enqueue_or_dequeue(
                 reg_file       = reg_file,
                 reg_file_tmp   = reg_file_tmp,
                 reg_to_get     = instr_ones,
                 reg_to_get_tmp = instr_ones_tmp,
                 copy_tmp       = copy_tmp,
                 is_enqueue     = False,
                 enqueue_val    = enqueue_val_reg,
                 val_dequeued   = val_dequeued_reg
               )
  #p +=         eo(instr_ones)     We don't need this anymore because
  #                                instr_ones is not used again for the current
  #                                instruction and it will be repopulated for
  #                                the next instruction when the next
  #                                instruction is executed,
  p +=         clear(instr_ones) # so we clear instr_ones now
  p +=         db(val_dequeued_reg)
  p +=         jf('<db-empty>')
  p +=         jf('<db-one>')
  p +=         jf('<db-sharp>')
  p +=         '<db-empty>'
  p +=             eo(instr_idx)
  p +=             jf('<dequeue_and_branch_return_from>')
  p +=         '<db-one>'
  p +=             eo(instr_idx)
  p +=             eo(instr_idx)
  p +=             jf('<dequeue_and_branch_return_from>')
  p +=         '<db-sharp>'
  p +=             eo(instr_idx)
  p +=             eo(instr_idx)
  p +=             eo(instr_idx)
  p +=             jf('<dequeue_and_branch_return_from>')
  p +=         '<dequeue_and_branch_return_from>'
  p +=         jb('<program_loop>')
               #################################################
               #################################################
  p +=     '<instruction_read_hypothetical_sixth_sharp_one>'
               # Error
  p +=         jf('<end>')
  p +=     '<instruction_read_hypothetical_sixth_sharp_sharp>'
               # Error
  p +=         jf('<end>')
  p += '<epilogue>'
  p +=     clear(instr_idx)
           # Write the encoded value of R1 into the actual program txt reg (R1)
  #p +=     clear(instr_ones) # This is now handled above
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
  #p +=           eo(exception_reg)
  p +=           jf('<end>') # Error
  p +=         '<-sharp->'
  p +=           db(reg_file)
  p +=           jf('<end>') # Error
  p +=           jf('<end>') # Error
  p +=           jb('<check-reg-remaining>')
  p += '<end>'
  return labels_to_offsets(p)
