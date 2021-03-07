import time
def r(a):
  i = a.find('0')
  if i == -1:
    return a

  excludedNumbers = {a[j] for j in range(81) if(i//9 == j//9) or (i-j) % 9 == 0 or (i//27 == j//27 and i%9//3 == j%9//3)}

  for n in '123456789':
    if n not in excludedNumbers:
      b = r(a[:i]+n+a[i+1:])
      if b!=None:
        return b

def solve(grid):
  start = time.time()
  solved = r(grid)
  print(time.time()-start)
  return solved

  # excludedNumbers = set()
  # for j in range(81):
  #   if (i//9 == j//9) or (i-j) % 9 == 0 or (i//27 == j//27 and i%9//3 == j%9//3):
  #     excludedNumbers.add(a[j])