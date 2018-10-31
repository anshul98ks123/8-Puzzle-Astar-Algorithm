f = open('data.txt', 'r')

initial_state = [x for x in f.readline().split(' ')][:9]
final_state = [x for x in f.readline().split(' ')][:9]

def manhattenDist(position1, position2):
  dx = int(abs(position1 - position2) / 3)
  dy = abs(position1 % 3 - position2 % 3)
  return dx + dy;

order_nielson = [0, 1, 2, 5, 8, 7, 6, 3]
possible_moves = [-1, 1, -3, 3]

def heuristic(current_state):
  Sn = int(current_state[4] != "_")
  Pn = 0

  finalMap = {}
  finalPos = {}
  
  # calculate S(n)
  for i, index in enumerate(order_nielson):
    nextIndex = order_nielson[(i + 1) % 8]
    finalMap[final_state[index]] = final_state[nextIndex]
  
  for i,index in enumerate(order_nielson):
    nextIndex = order_nielson[(i + 1) % 8]

    if(current_state[index] == "_"):
      continue

    if(current_state[index] not in finalMap):
      continue
      
    if(current_state[nextIndex] != finalMap[current_state[index]]):
      Sn += 2

  # calculate P(n)
  for i in range(9):
    finalPos[final_state[i]] = i
  
  for i in range(9):
    if(current_state[i] != '_'):
      Pn += manhattenDist(i, finalPos[current_state[i]])
  
  return (Pn + 3 * Sn)

def FindBest(Open):
  score = 100000000
  best = 0

  for index,i in enumerate(Open):
    if heuristic(list(i)) < score:
      score = heuristic(list(i))
      best = index
  
  return best

def Solvable(initial_state, final_state):
  finalPos = {}

  for i in range(9):
    finalPos[final_state[i]] = i

  inversions = 0

  for i in range(8):
    for j in range(i+1, 8):
      if finalPos[initial_state[i]] > finalPos[initial_state[j]]:
        inversions += 1

  return (inversions % 2 == 0)

def Astar(initial_state, final_state):
  print("final  =  ", final_state)
  print("initial = ", initial_state)

  if not Solvable(initial_state, final_state):
    print("\nProblem unsolvable")
    return

  current_state = initial_state
  current_perm = "".join(initial_state)

  Open = [current_perm]
  Closed = []
  iteration = 0

  while len(Open) > 0:
    iteration += 1
    index = FindBest(Open)

    current_state = list(Open[index])
    current_cost = heuristic(current_state)

    Open = Open[:index] + Open[index+1:]
    Closed.append("".join(current_state))

    empty_pos = current_state.index("_")

    print("\nheuristic = ", heuristic(current_state))
    print("current = ", current_state)

    if "".join(current_state) == "".join(final_state):
      break
    
    for i in possible_moves:
      temp_state = current_state.copy()
      newpos = empty_pos + i

      if abs(i) == 1 and int(newpos/3) != int(empty_pos/3):
        continue

      if newpos < 0 or newpos >= 9:
        continue

      temp_state[empty_pos], temp_state[newpos] = temp_state[newpos], temp_state[empty_pos]
      temp_perm = "".join(temp_state)

      if (temp_perm not in Closed) and (temp_perm not in Open):
        Open.append(temp_perm)
    
  print("\nFinal state needed = ", final_state)
  print("Final state reached = ", current_state)

Astar(initial_state, final_state)