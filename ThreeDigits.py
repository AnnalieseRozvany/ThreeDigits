
import sys
import math

def h(a, b):
    return abs(int(a[0]) - int(b[0])) + abs(int(a[1]) - int(b[1])) + abs(int(a[2]) - int(b[2]))

def versionControl(queue, copy, path, digit, number, version):
    copy = ''.join(copy)
    if copy not in forbidden:
        if version == "B" or version == "D":
            queue.append((copy, path, digit))
        if version == "I":
            queue.append((copy, path, digit, number+1))
        if version == "G":
            queue.append((copy, path, digit, h(goal, copy)))
        if version == "H":
            queue.append((copy, path, digit, h(goal, copy)))
        if version == "A":
            queue.append((copy, path, digit, h(goal, copy) + len(path) - 1))
    return queue

def expand(vertex, queue, digit, operation, path, version, number):
    if operation == "subtract":
        if (vertex[digit] != "0"):
            copy = list(vertex)
            copy[digit] = str(int(copy[digit]) - 1)
            queue = versionControl(queue, copy, path, digit, number, version)
    elif operation == "add":
        if (vertex[digit] != '9'):
            copy = list(vertex)
            copy[digit] = str(int(copy[digit]) + 1)
            queue = versionControl(queue, copy, path, digit, number, version)
    return queue

def digitChecks(vertex, queue, digit, path, version, number):
    if version == "I" or version == "D":
        if digit != 2:
            queue = expand(vertex, queue, 2, "add", path + [vertex], version, number)
            queue = expand(vertex, queue, 2, "subtract", path + [vertex], version, number)
        if digit != 1:
            queue = expand(vertex, queue, 1, "add", path + [vertex], version, number)
            queue = expand(vertex, queue, 1, "subtract", path + [vertex], version, number)
        if digit != 0:
            queue = expand(vertex, queue, 0, "add", path + [vertex], version, number)
            queue = expand(vertex, queue, 0, "subtract", path + [vertex], version, number)
        return queue
    if digit != 0:
        queue = expand(vertex, queue, 0, "subtract", path + [vertex], version, number)
        queue = expand(vertex, queue, 0, "add", path + [vertex], version, number)
    if digit != 1:
        queue = expand(vertex, queue, 1, "subtract", path + [vertex], version, number)
        queue = expand(vertex, queue, 1, "add", path + [vertex], version, number)
    if digit != 2:
        queue = expand(vertex, queue, 2, "subtract", path + [vertex], version, number)
        queue = expand(vertex, queue, 2, "add", path + [vertex], version, number)
    return queue

def BFS():
    visited, queue = [], [(start, [], 4)]
    visitedNodes = []
    while queue:
        (vertex, path, digit) = queue.pop(0)
        if (vertex,digit) in visited:
            continue
        visited.append((vertex,digit))
        visitedNodes.append(vertex)
        if len(visited) >= 1000:
            return [], visitedNodes
        if vertex == goal:
            return path + [vertex], visitedNodes
        queue = digitChecks(vertex, queue, digit, path, "B", 0)
    return [], visitedNodes

def DFS():
    visited, stack = [], [(start, [], 4)]
    visitedNodes = []
    while stack:
        (vertex, path, digit) = stack.pop()
        if (vertex, digit) in visited:
            continue
        visited.append((vertex, digit))
        visitedNodes.append(vertex)
        if len(visited) >= 1000:
            return [], visitedNodes
        if vertex == goal:
            return path + [vertex], visitedNodes
        else:
            stack = digitChecks(vertex, stack, digit, path, "D", 0)
    return [], visitedNodes

def IDS_DFS(path, visited, currentDepth, number):
    visited, stack = [], [(start, [], 4, 0)]
    visitedNodes = []
    while stack:
        (vertex, path, digit, depth) = stack.pop()
        if (vertex, digit) in visited:
            continue
        visited.append((vertex, digit))
        visitedNodes.append(vertex)
        if number + len(visited) >= 1000:
            return 1, [], visitedNodes
        if vertex == goal:
            return 1, path + [vertex], visitedNodes
        elif(depth < currentDepth):
            stack = digitChecks(vertex, stack, digit, path, "I", depth)
    return 0, path, visitedNodes


def IDS():
    currentDepth, found, path, visited = 0, 0, [], []
    while len(visited) < 1001:
        found, path, list = IDS_DFS(path, visited, currentDepth, len(visited))
        visited += list
        if found == 1:
            return path, visited
        currentDepth += 1
    return [], visited

def G_expand(fringe, expandedNode, path):
    fringe.remove(expandedNode)
    vertex, path, digit, manhatten = expandedNode
    if vertex == goal:
        return 1, path + [vertex]
    fringe = digitChecks(vertex, fringe, digit, path, "G", 0)
    return 0, path


def Greedy():
    expanded, path = [], []
    fringe = [(start, path, 4, 0)]
    while len(expanded) < 1001:
        if not fringe:
            return [], expanded
        minVal = fringe[0][3]
        minIndex = 0
        for x in fringe:
            if x[3] <= minVal:
                minIndex = fringe.index(x)
                minVal = x[3]
        expanded = expanded + [fringe[minIndex][0]]
        found, path = G_expand(fringe, fringe[minIndex], path + [fringe[minIndex][0]])
        if found == 1:
            return path, expanded
    return [], expanded

def hillclimbing():
    digit, children, expanded, digits = 4, [], [start], []
    startVal = h(start, goal)
    vertex = start
    while 1:
        if digit != 0:
            children = expand(vertex, children, 0, "subtract", expanded + [vertex], "H", 0)
            digits.append(0)
            children = expand(vertex, children, 0, "add", expanded + [vertex], "H", 0)
            digits.append(0)
        if digit != 1:
            children = expand(vertex, children, 1, "subtract", expanded + [vertex], "H", 0)
            digits.append(1)
            children = expand(vertex, children, 1, "add", expanded + [vertex], "H", 0)
            digits.append(1)
        if digit != 2:
            children = expand(vertex, children, 2, "subtract", expanded + [vertex], "H", 0)
            digits.append(2)
            children = expand(vertex, children, 2, "add", expanded + [vertex], "H", 0)
            digits.append(2)
        minVal = startVal
        minIndex = 0
        for x in children:
            if x[3] <= minVal:
                minIndex = children.index(x)
                minVal = x[3]
        if minVal < startVal:
            startVal = minVal
            digit = digits[minIndex]
            digits = []
            expanded += [children[minIndex][0]]
            if children[minIndex][0] == goal:
                return expanded, expanded
            vertex = children[minIndex][0]
            children = []
        else:
            return [], expanded

def A_expand(fringe, expandedNode, path):
    fringe.remove(expandedNode)
    vertex, path, digit, manhatten = expandedNode
    if vertex == goal:
        return 1, path + [vertex]
    fringe = digitChecks(vertex, fringe, digit, path, "A", 0)
    return 0, path

def A():
    expanded, path = [], []
    fringe = [(start, path, 4, 0)]
    while len(expanded) < 1001:
        if not fringe:
            return [], expanded
        minVal = fringe[0][3]
        minIndex = 0
        for x in fringe:
            if x[3] <= minVal:
                minIndex = fringe.index(x)
                minVal = x[3]
        expanded = expanded + [fringe[minIndex][0]]
        found, path = A_expand(fringe, fringe[minIndex], path + [fringe[minIndex][0]])
        if found == 1:
            return path, expanded
    return [], expanded


def output(val):
    if not val:
        return
    path, visited = val
    if not path:
        print ("No solution found.")
    else:
        print (",".join(path))
    print (",".join(visited))

file = open(sys.argv[2],"r")
lines = file.readlines()
file.close()

l = []
for line in lines:
    l.append(line)

start = l[0].strip()
goal = l[1].strip()
if len(l) > 2:
    forbidden = l[2].split(',')
    for x in forbidden:
        x = x.strip()
else:
    forbidden = []

method = sys.argv[1]

if method == "B":
    val = BFS()
    output(val)
elif method == "D":
    val = DFS()
    output(val)
elif method == "I":
    val = IDS()
    output(val)
elif method == "G":
    val = Greedy()
    output(val)
elif method == "A":
    val = A()
    output(val)
elif method == "H":
    val = hillclimbing()
    output(val)
