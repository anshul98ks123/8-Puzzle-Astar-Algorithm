from graphics import *

f = open('data2.txt', 'r')

initial_state = [x for x in f.readline().split(' ')][:9]
final_state = [x for x in f.readline().split(' ')][:9]

order_nielson = [0, 1, 2, 5, 8, 7, 6, 3]
possible_moves = [-1, 1, -3, 3]

win = GraphWin("My Window",1300,1000)
win.setBackground('white')

def clear(win):
  for item in win.items[:]:
    item.undraw()
  win.update()

def initText(iter):
  if iter==-1:
    txt = Text(Point(470,70),"UNSOLVABLE!")
    txt.setTextColor('black')
    txt.setSize(22)
    txt.setStyle('bold')
    txt.setFace("courier")
    txt.draw(win)

  else:
    txt = Text(Point(470,70),"Iteration: ")
    txt.setTextColor('black')
    txt.setSize(22)
    txt.setStyle('bold')
    txt.setFace("courier")
    txt.draw(win)

    txt = Text(Point(565,70),iter)
    txt.setTextColor('black')
    txt.setStyle('bold')
    txt.setSize(22)
    txt.draw(win)

  txt = Text(Point(220,170),"Current")
  txt.setTextColor('black')
  txt.setStyle('bold')
  txt.setSize(22)
  txt.draw(win)

  txt = Text(Point(720,170),"Final")
  txt.setTextColor('black')
  txt.setStyle('bold')
  txt.setSize(22)
  txt.draw(win)

  txt = Text(Point(470,550),"8 PUZZLE SIMULATION")
  txt.setTextColor('black')
  txt.setStyle('bold')
  txt.setSize(24)
  txt.draw(win)

def drawPuzzle(current_state,x0,y0):
  d = 80

  for i in range(3):
    drawCol = Rectangle(Point(x0+i*d,y0),Point(x0+i*d+d,y0+3*d))
    drawCol.setOutline('red')
    drawCol.draw(win)
    drawCol = Rectangle(Point(x0+i*d+1,y0+1),Point(x0+i*d+d+1,y0+3*d+1))
    drawCol.setOutline('red')
    drawCol.draw(win)

  for i in range(3):
    drawRow = Rectangle(Point(x0,y0+i*d),Point(x0+3*d,y0+i*d+d))
    drawRow.setOutline('red')
    drawRow.draw(win)
    drawCol = Rectangle(Point(x0+i*d+1,y0+1),Point(x0+i*d+d+1,y0+3*d+1))
    drawCol.setOutline('red')
    drawCol.draw(win)

  iniX = x0+d/2
  iniY = y0+d/2
  count = 0

  for i in current_state:
    X = iniX+(count%3)*d
    Y = iniY+(count//3)*d
    txt = Text(Point(X,Y),i)
    txt.setTextColor('black')
    txt.setSize(22)
    txt.setStyle('bold')
    txt.draw(win)
    count += 1

def drawConfiguration(current_state,final_state,iter,unsolvable):
  clear(win)

  if unsolvable:
    iter = -1
  initText(iter)

  x0 = 100
  y0 = 200

  drawPuzzle(current_state,x0,y0)
  drawPuzzle(final_state,x0+500,y0)

def manhattenDist(position1, position2):
  dx = int(abs(position1 - position2) / 3)
  dy = abs(position1 % 3 - position2 % 3)
  return dx + dy;

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

def showSolution(initial_state, final_state, Parent):
  t = final_state
  Path = []

  while True:
    Path.append(t)

    if "".join(initial_state) == "".join(t):
      break
    
    t = Parent["".join(t)]

  iteration = 1
  Path.reverse()
  for state in Path:
    print("\n",list(state))
    drawConfiguration(state,final_state,iteration,False)
    iteration += 1
    time.sleep(1)
  
  time.sleep(10)

def Astar(initial_state, final_state):
  print("final  =  ", final_state)
  print("initial = ", initial_state)

  if not Solvable(initial_state, final_state):
    drawConfiguration(initial_state,final_state,-1,True)
    time.sleep(5)
    return

  Parent = {}

  current_state = initial_state
  current_perm = "".join(initial_state)

  Open = [current_perm]
  Closed = []

  while len(Open) > 0:
    index = FindBest(Open)

    current_state = list(Open[index])

    Open = Open[:index] + Open[index+1:]
    Closed.append("".join(current_state))

    empty_pos = current_state.index("_")

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
        Parent[temp_perm] = "".join(current_state)
    
  print("\nFinal state needed = ", final_state)
  print("Final state reached = ", current_state)

  showSolution(initial_state, current_state, Parent)

Astar(initial_state, final_state)