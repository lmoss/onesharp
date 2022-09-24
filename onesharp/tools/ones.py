# ones
# ====
# n       : positive integer, the length of the ones string to return
# returns : string, a string containing exactly ``n'' ones
#
#   example
#   -------
#     >>> print(ones(3))
#     111
#
def ones(n):
  assert n > 0
  return ''.join(['1' for _ in range(n)])
