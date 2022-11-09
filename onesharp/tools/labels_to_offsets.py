import sys

# labels_to_offsets
# =================
# program : string, the ``label-enhanced'' 1# program
# lstart  : character, the label-start delimiter, default is '<'
# lend    : character, the label-end delimiter, default is '>'
# returns : string, the program with its marker labels removed and its
#         :   instruction-argument labels translated to their relevant offsets
#
#   example
#   -------
#     >>> clear_1_using_labels = \
#     ...   '<start>'+\
#     ...     '1#####'+\
#     ...     '<end>###'+\
#     ...     '<start>####'+\
#     ...     '<start>####'+\
#     ...   '<end>'
#     >>> clear_1 = labels_to_offsets( clear_1_using_labels )
#     >>> print(clear_1)
#     '1#####111###11####111####'
#
#
def labels_to_offsets(program, lstart='<', lend='>'):
  program = ''.join( program.split() ) # Remove all whitespace
  assert lstart not in ['1','#']
  assert lend not in ['1','#']
  assert lstart != lend # The label start and end delimiters must differ
  # Phase 1
  # Parse the label-containing program
  parse_of_program = []
  prog_len_in_chars = len(program)
  label__instruction_index = dict()
  char_index = 0
  if char_index < prog_len_in_chars:
    cur_char = program[char_index]
  while char_index < prog_len_in_chars:
    # Phase 1 Step 1
    # Parse label, if present
    assert cur_char in [lstart,'1']
    if cur_char == lstart:
      label = ''
      while True:
        char_index += 1
        assert char_index < prog_len_in_chars
        cur_char = program[char_index]
        assert cur_char not in ['1','#',lstart] # A label cannot contain these
        if cur_char == lend:
          break
        label += cur_char
      char_index += 1
      if char_index < prog_len_in_chars:
        cur_char = program[char_index]
      else:
        cur_char = 'EOF'
      if cur_char == 'EOF' or cur_char == lstart or cur_char == '1':
        assert label not in label__instruction_index
        label__instruction_index[label] = len(parse_of_program)
        if cur_char == 'EOF':
          break # Phase 1 complete
        elif cur_char == lstart:
          continue # Parse the next label
      elif cur_char == '#':
        parse_of_program.append([label])
      else:
        assert False # Unexpected character followed the label-end delimiter
    # Phase 1 Step 2
    # Parse the instruction argument, if present
    arg = ''
    while cur_char == '1':
      arg += '1'
      char_index += 1
      assert char_index < prog_len_in_chars # Unexpected end of program
      cur_char = program[char_index]
    if len(arg) > 0:
      parse_of_program.append([arg])
    # Phase 1 Step 3
    # Parse the opcode
    opcode = ''
    assert cur_char == '#' # Unexpected character followed instruction argument
    while cur_char == '#':
      opcode += '#'
      if len(opcode) == 6:
        assert False # Opcode can be five sharps at most
      char_index += 1
      if char_index == prog_len_in_chars:
        break
      cur_char = program[char_index]
    assert len(parse_of_program[-1]) == 1
    parse_of_program[-1].append(opcode)
  # Phase 2
  # Replace the labels with offsets
  program = ''
  for instruction_index, arg__opcode in enumerate(parse_of_program):
    arg = arg__opcode[0]
    opcode = arg__opcode[1]
    if arg in label__instruction_index:
      label_ii = label__instruction_index[arg]
      offset = label_ii - instruction_index
      if offset < 0:
        if opcode != '####':
          sys.stderr.write('Offending label: '+arg)
          assert False # We should be jumping backward, but we aren't
        offset = -offset
      elif offset > 0:
        assert opcode == '###'
      else:
        assert offset == 0 # If fails, bug internal to function
        assert False # Cannot jump to self
      arg = ''.join(['1' for _ in range(offset)])
    # Confirm we have a valid arg; that is, we don't have an undefined label
    for char in arg:
      if char != '1':
        sys.stderr.write('offsets_to_labels: encountered undefined label: '+arg)
        assert False
    program += arg + opcode
  return program
