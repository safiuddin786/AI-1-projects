import sys
import copy
import heapq
import datetime


class Puzzle:
    def __init__(self, start, goal, limit=0):
        self.start = [[int(j) for j in i] for i in start]
        self.goal = [[int(j) for j in i] for i in goal]
        self.trace = []
        self.empty = [-1, -1]
        self.visited = []
        self.limit = limit
        # set the start point of the empty block
        for i in range(len(start)):
            for j in range(len(start[0])):
                if start[i][j] == "0":
                    self.empty = [i, j]
                    return

    def setFileName(self, fileName):
        self.fileName = fileName

    def getEmpty(self):
        return self.empty

    def solveDFS(self):
        self.dfsFound = False
        self.visited = []
        self.dfs([], self.empty, self.start, "Start")

    def dfs(self, trace, empty, state, move):
        # Check if the State is already visited
        if self.isVisited(state) or self.dfsFound:
            return

        # number of successors
        fringe = []

        # Append current state to the trace
        temp = copy.deepcopy(state)
        temp.append(move)
        trace.append(temp)
        self.visited.append(copy.deepcopy(state))

        # If End Goal is reached
        if state == self.goal:
            print("Reached")
            self.dfsFound = True
            self.trace = trace
            return

        # Up Down Left Right slide
        # Down
        if empty[0] > 0:
            state[empty[0]][empty[1]], state[empty[0]-1][empty[1]
                                                         ] = state[empty[0]-1][empty[1]], state[empty[0]][empty[1]]
            move = str(state[empty[0]][empty[1]])+"Down"
            newTrace = copy.deepcopy(trace)
            fringe.append(
                [state, "Move "+str(state[empty[0]][empty[1]])+" Down"])
            self.dfs(newTrace, [empty[0]-1, empty[1]], state, move)
            state[empty[0]-1][empty[1]], state[empty[0]][empty[1]
                                                         ] = state[empty[0]][empty[1]], state[empty[0]-1][empty[1]]
        # Up
        if empty[0] < len(state)-1:
            state[empty[0]][empty[1]], state[empty[0]+1][empty[1]
                                                         ] = state[empty[0]+1][empty[1]], state[empty[0]][empty[1]]
            move = str(state[empty[0]][empty[1]])+" Up"
            newTrace = copy.deepcopy(trace)
            fringe.append(
                [state, "Move "+str(state[empty[0]][empty[1]])+" Up"])
            self.dfs(newTrace, [empty[0]+1, empty[1]], state, move)
            state[empty[0]+1][empty[1]], state[empty[0]][empty[1]
                                                         ] = state[empty[0]][empty[1]], state[empty[0]+1][empty[1]]
        # Right
        if empty[1] > 0:
            state[empty[0]][empty[1]], state[empty[0]][empty[1] -
                                                       1] = state[empty[0]][empty[1]-1], state[empty[0]][empty[1]]
            move = str(state[empty[0]][empty[1]])+" Right"
            newTrace = copy.deepcopy(trace)
            fringe.append(
                [state, "Move "+str(state[empty[0]][empty[1]])+" Right"])
            self.dfs(newTrace, [empty[0], empty[1]-1], state, move)
            state[empty[0]][empty[1]-1], state[empty[0]][empty[1]
                                                         ] = state[empty[0]][empty[1]], state[empty[0]][empty[1]-1]
        # Left
        if empty[1] < len(state[0])-1:
            state[empty[0]][empty[1]], state[empty[0]][empty[1] +
                                                       1] = state[empty[0]][empty[1]+1], state[empty[0]][empty[1]]
            move = str(state[empty[0]][empty[1]])+" Left"
            newTrace = copy.deepcopy(trace)
            fringe.append(
                [state, "Move "+str(state[empty[0]][empty[1]])+" Left"])
            self.dfs(newTrace, [empty[0], empty[1]+1], state, move)
            state[empty[0]][empty[1]+1], state[empty[0]][empty[1]
                                                         ] = state[empty[0]][empty[1]], state[empty[0]][empty[1]+1]

        with open(self.fileName, "a") as file:
            file.write("\t"+str(len(fringe))+" successors generated\n")
            file.write("\tClosed :"+str(self.visited)+"\n")
            file.write("\tFringe :"+str(fringe)+"\n")

    def isVisited(self, state, currTrack=[]):
        if currTrack == []:
            currTrack = self.visited
        for st in currTrack:
            # check if every number is same in st and state mat
            st = st[0:3]
            if st == state:
                return True
        return False

    def getTrace(self):
        return self.trace

    def solveBFS(self):
        queue = []
        self.visited = []
        queue.append([self.start, self.empty, [], "Start"])

        # BFS
        while (len(queue) != 0):
            state = queue.pop(0)
            temp = state[-1]
            state = state[:-1]

            with open(self.fileName, "a") as file:
                file.write("Generating successors to " +
                           str(state[0])+", action: "+temp+"\n")

            # number of successors
            fringe = []

            # Check if state is already visited
            if self.isVisited(state[0]) == False:
                t = copy.deepcopy(state[0])
                t.append(temp)
                state[2].append(t)
                self.visited.append(copy.deepcopy(state[0]))
                if state[0] == self.goal:
                    print("Reached")
                    self.trace = state[2]
                    break

                # Traverse Up Down Left Right
                empty = state[1]
                # Down
                if empty[0] > 0:
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]-1][empty[1]
                                                                       ] = newState[empty[0]-1][empty[1]], newState[empty[0]][empty[1]]
                    queue.append(
                        [newState, [empty[0]-1, empty[1]], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Down"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Down"])

                # Up
                if empty[0] < len(state[0])-1:
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]+1][empty[1]
                                                                       ] = newState[empty[0]+1][empty[1]], newState[empty[0]][empty[1]]
                    queue.append(
                        [newState, [empty[0]+1, empty[1]], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Up"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Up"])

                # Right
                if empty[1] > 0:
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]][empty[1] -
                                                                     1] = newState[empty[0]][empty[1]-1], newState[empty[0]][empty[1]]
                    queue.append(
                        [newState, [empty[0], empty[1]-1], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Right"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Right"])

                # Left
                if empty[1] < len(state[0][0])-1:
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]][empty[1] +
                                                                     1] = newState[empty[0]][empty[1]+1], newState[empty[0]][empty[1]]
                    queue.append(
                        [newState, [empty[0], empty[1]+1], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Left"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Left"])

                with open(self.fileName, "a") as file:
                    file.write("\t"+str(len(fringe))+" successors generated\n")
                    file.write("\tClosed :"+str(self.visited)+"\n")
                    file.write("\tFringe :"+str(fringe)+"\n")

    def solveGreedy(self):
        queue = []
        self.visited = []
        heapq.heappush(queue, [0, self.start, self.empty, [], "Start"])

        # BFS greedy
        while (len(queue) != 0):
            state = heapq.heappop(queue)
            temp = state[-1]
            state = state[1:-1]

            with open(self.fileName, "a") as file:
                file.write("Generating successors to " +
                           str(state[0])+" action: "+temp+"\n")

            # number of successors
            fringe = []

            # Check if state is already visited
            if self.isVisited(state[0]) == False:
                t = copy.deepcopy(state[0])
                t.append(temp)
                state[2].append(t)
                self.visited.append(copy.deepcopy(state[0]))
                if state[0] == self.goal:
                    print("Reached")
                    self.trace = state[2]
                    break

                # Traverse Up Down Left Right
                empty = state[1]
                # Down
                if empty[0] > 0:
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]-1][empty[1]
                                                                       ] = newState[empty[0]-1][empty[1]], newState[empty[0]][empty[1]]
                    heapq.heappush(queue,
                                   [self.manhattanDist(newState[empty[0]][empty[1]], empty), newState, [empty[0]-1, empty[1]], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Down"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Down"])

                # Up
                if empty[0] < len(state[0])-1:
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]+1][empty[1]
                                                                       ] = newState[empty[0]+1][empty[1]], newState[empty[0]][empty[1]]
                    heapq.heappush(queue,
                                   [self.manhattanDist(newState[empty[0]][empty[1]], empty), newState, [empty[0]+1, empty[1]], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Up"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Up"])

                # Right
                if empty[1] > 0:
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]][empty[1] -
                                                                     1] = newState[empty[0]][empty[1]-1], newState[empty[0]][empty[1]]
                    heapq.heappush(queue,
                                   [self.manhattanDist(newState[empty[0]][empty[1]], empty), newState, [empty[0], empty[1]-1], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Right"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Right"])

                # Left
                if empty[1] < len(state[0][0])-1:
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]][empty[1] +
                                                                     1] = newState[empty[0]][empty[1]+1], newState[empty[0]][empty[1]]
                    heapq.heappush(queue,
                                   [self.manhattanDist(newState[empty[0]][empty[1]], empty), newState, [empty[0], empty[1]+1], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Left"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Left"])

                with open(self.fileName, "a") as file:
                    file.write("\t"+str(len(fringe))+" successors generated\n")
                    file.write("\tClosed :"+str(self.visited)+"\n")
                    file.write("\tFringe :"+str(fringe)+"\n")

    # calculate greedy hueristic
    def manhattanDist(self, val, pos):
        coords = [(val-1)//3, (val-1) % 3]
        return abs(coords[0]-pos[0])+abs(coords[1]-pos[1])

    def solveAStar(self):
        queue = []
        self.visited = []
        heapq.heappush(queue, [0, self.start, self.empty, [], "Start"])

        # BFS A*
        while (len(queue) != 0):
            state = heapq.heappop(queue)
            temp = state[-1]
            state = state[1:-1]
            with open(self.fileName, "a") as file:
                file.write("Generating successors to " +
                           str(state[0])+" action: "+temp+"\n")

            # number of successors
            fringe = []

            # Check if state is already visited
            if self.isVisited(state[0]) == False:
                t = copy.deepcopy(state[0])
                t.append(temp)
                state[2].append(t)
                self.visited.append(copy.deepcopy(state[0]))
                if state[0] == self.goal:
                    print("Reached")
                    self.trace = state[2]
                    break

                # Traverse Up Down Left Right
                empty = state[1]
                # Down
                if empty[0] > 0 and ("Up" not in temp):
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]-1][empty[1]
                                                                       ] = newState[empty[0]-1][empty[1]], newState[empty[0]][empty[1]]
                    heapq.heappush(queue,
                                   [newState[empty[0]][empty[1]]+self.manhattanDist(newState[empty[0]][empty[1]], empty), newState, [empty[0]-1, empty[1]], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Down"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Down"])

                # Up
                if empty[0] < len(state[0])-1 and ("Down" not in temp):
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]+1][empty[1]
                                                                       ] = newState[empty[0]+1][empty[1]], newState[empty[0]][empty[1]]
                    heapq.heappush(queue,
                                   [newState[empty[0]][empty[1]]+self.manhattanDist(newState[empty[0]][empty[1]], empty), newState, [empty[0]+1, empty[1]], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Up"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Up"])

                # Right
                if empty[1] > 0 and ("Left" not in temp):
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]][empty[1] -
                                                                     1] = newState[empty[0]][empty[1]-1], newState[empty[0]][empty[1]]
                    heapq.heappush(queue,
                                   [newState[empty[0]][empty[1]]+self.manhattanDist(newState[empty[0]][empty[1]], empty), newState, [empty[0], empty[1]-1], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Right"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Right"])

                # Left
                if empty[1] < len(state[0][0])-1 and ("Right" not in temp):
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]][empty[1] +
                                                                     1] = newState[empty[0]][empty[1]+1], newState[empty[0]][empty[1]]
                    heapq.heappush(queue,
                                   [newState[empty[0]][empty[1]]+self.manhattanDist(newState[empty[0]][empty[1]], empty), newState, [empty[0], empty[1]+1], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Left"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Left"])

                with open(self.fileName, "a") as file:
                    file.write("\t"+str(len(fringe))+" successors generated\n")
                    file.write("\tClosed :"+str(self.visited)+"\n")
                    file.write("\tFringe :"+str(fringe)+"\n")

    def solveUCS(self):
        queue = []
        self.visited = []
        heapq.heappush(queue, [0, self.start, self.empty, [], "Start"])

        # UCS
        while (len(queue) != 0):
            state = heapq.heappop(queue)
            temp = state[-1]
            # print(state[0])
            state = state[1:-1]
            with open(self.fileName, "a") as file:
                file.write("Generating successors to " +
                           str(state[0]) + " action: "+temp+"\n")

            # number of successors
            fringe = []

            # Check if state is already visited
            if self.isVisited(state[0]) == False:
                t = copy.deepcopy(state[0])
                t.append(temp)
                state[2].append(t)
                self.visited.append(copy.deepcopy(state[0]))
                if state[0] == self.goal:
                    print("Reached")
                    self.trace = state[2]
                    break

                # Traverse Up Down Left Right
                empty = state[1]
                # Down
                if empty[0] > 0 and ("Up" not in temp):
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]-1][empty[1]
                                                                       ] = newState[empty[0]-1][empty[1]], newState[empty[0]][empty[1]]
                    heapq.heappush(queue,
                                   [newState[empty[0]][empty[1]], newState, [empty[0]-1, empty[1]], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Down"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Down"])

                # Up
                if empty[0] < len(state[0])-1 and ("Down" not in temp):
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]+1][empty[1]
                                                                       ] = newState[empty[0]+1][empty[1]], newState[empty[0]][empty[1]]
                    heapq.heappush(queue,
                                   [newState[empty[0]][empty[1]], newState, [empty[0]+1, empty[1]], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Up"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Up"])

                # Right
                if empty[1] > 0 and ("Left" not in temp):
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]][empty[1] -
                                                                     1] = newState[empty[0]][empty[1]-1], newState[empty[0]][empty[1]]
                    heapq.heappush(queue,
                                   [newState[empty[0]][empty[1]], newState, [empty[0], empty[1]-1], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Right"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Right"])
                # Left
                if empty[1] < len(state[0][0])-1 and ("Right" not in temp):
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]][empty[1] +
                                                                     1] = newState[empty[0]][empty[1]+1], newState[empty[0]][empty[1]]
                    heapq.heappush(queue,
                                   [newState[empty[0]][empty[1]], newState, [empty[0], empty[1]+1], copy.deepcopy(state[2]), str(newState[empty[0]][empty[1]])+" Left"])
                    fringe.append(
                        [newState, "Move "+str(newState[empty[0]][empty[1]])+" Left"])

                with open(self.fileName, "a") as file:
                    file.write("\t"+str(len(fringe))+" successors generated\n")
                    file.write("\tClosed :"+str(self.visited)+"\n")
                    file.write("\tFringe :"+str(fringe)+"\n")

    def setLimit(self, limit):
        self.limit = limit

    def solveDLS(self):
        self.visited = []
        self.dfsFound = False
        self.dls([], self.empty, self.start, "Start", self.limit)

    def dls(self, trace, empty, state, move, limit):

        # number of successors
        fringe = []

        if limit == 0:
            return

        # Check if we already solved the puzzle
        # Check if the State is already visited
        if (self.dfsFound or self.isVisited(state, trace)):
            return

        # print(limit)
        # Append current state to the trace
        temp = copy.deepcopy(state)
        temp.append(move)
        trace.append(temp)
        self.visited.append(copy.deepcopy(state))

        # If End Goal is reached
        if state == self.goal:
            print("Reached")
            self.dfsFound = True
            self.trace = copy.deepcopy(trace)
            return

        limit -= 1
        # Up Down Left Right slide
        # Down
        if empty[0] > 0 and ("Up" not in move):
            newState = copy.deepcopy(state)
            newState[empty[0]][empty[1]], newState[empty[0]-1][empty[1]
                                                               ] = newState[empty[0]-1][empty[1]], newState[empty[0]][empty[1]]
            move = str(newState[empty[0]][empty[1]])+" Down"
            newTrace = copy.deepcopy(trace)
            fringe.append(
                [newState, "Move "+str(newState[empty[0]][empty[1]])+" Down"])
            self.dls(newTrace, [empty[0]-1, empty[1]], newState, move, limit)

        # Up
        if empty[0] < len(state)-1 and ("Down" not in temp):
            newState = copy.deepcopy(state)
            newState[empty[0]][empty[1]], newState[empty[0]+1][empty[1]
                                                               ] = newState[empty[0]+1][empty[1]], newState[empty[0]][empty[1]]
            move = str(newState[empty[0]][empty[1]])+" Up"
            newTrace = copy.deepcopy(trace)
            fringe.append(
                [newState, "Move "+str(newState[empty[0]][empty[1]])+" Up"])
            self.dls(newTrace, [empty[0]+1, empty[1]], newState, move, limit)

        # Right
        if empty[1] > 0 and ("Left" not in temp):
            newState = copy.deepcopy(state)
            newState[empty[0]][empty[1]], newState[empty[0]][empty[1] -
                                                             1] = newState[empty[0]][empty[1]-1], newState[empty[0]][empty[1]]
            move = str(newState[empty[0]][empty[1]])+" Right"
            newTrace = copy.deepcopy(trace)
            fringe.append(
                [newState, "Move "+str(newState[empty[0]][empty[1]])+" Right"])
            self.dls(newTrace, [empty[0], empty[1]-1], newState, move, limit)

        # Left
        if empty[1] < len(state[0])-1 and ("Right" not in temp):
            newState = copy.deepcopy(state)
            newState[empty[0]][empty[1]], newState[empty[0]][empty[1] +
                                                             1] = newState[empty[0]][empty[1]+1], newState[empty[0]][empty[1]]
            move = str(newState[empty[0]][empty[1]])+" Left"
            newTrace = copy.deepcopy(trace)
            fringe.append(
                [newState, "Move "+str(newState[empty[0]][empty[1]])+" Left"])
            self.dls(newTrace, [empty[0], empty[1]+1], newState, move, limit)

        with open(self.fileName, "a") as file:
            file.write("\tCurrent Depth: "+str(self.limit-limit)+"\n")
            file.write("\tGenerating successors to " +
                       str(state)+", action: "+move+"\n")
            file.write("\t\t"+str(len(fringe))+" successors generated\n")
            file.write("\t\tClosed :"+str(self.visited)+"\n")
            file.write("\t\tFringe :"+str(fringe)+"\n")

    def solveIDS(self):
        limit = self.limit
        self.dfsFound = False
        while (self.dfsFound == False):
            self.visited = []
            with open(self.fileName, "a") as file:
                file.write("\tStarting DLS: \n")
                file.write("\tCurrent Limit: "+str(limit)+"\n")
            self.dls([], self.empty, self.start, "Start", limit)
            limit += 1
            self.limit += 1
        return

    # def writeFile(self, method):


def fillState(state, fileName):
    with open(fileName, 'r') as file:
        for line in file:
            state.append(line.split())
        if len(start) > 0:
            state.pop()


def solve(method, p):
    methods = {
        "a*": p.solveAStar,
        "bfs": p.solveBFS,
        "dfs": p.solveDFS,
        "ucs": p.solveUCS,
        "greedy": p.solveGreedy,
        "dls": p.solveDLS,
        "ids": p.solveIDS
    }
    methods[method]()


start = []
goal = []

fillState(start, sys.argv[1])
fillState(goal, sys.argv[2])
p = Puzzle(start, goal)
trace = False
if (len(sys.argv) >= 5 and sys.argv[4].lower() == "true"):
    trace = True
method = "a*"
if (len(sys.argv) >= 4):
    method = sys.argv[3].lower()

if ("dls" in method and p.limit == 0):
    print("Specify the Limit please must be greater than 0: ")
    p.setLimit(int(input()))

fileName = "trace-"+datetime.datetime.now().strftime('%m_%d_%Y-%I_%M_%S_%p')+".txt"
p.setFileName(fileName)

with open(fileName, "w") as file:
    text = "Command-Line Arguments : ["
    # text += str(sys.argv)+"\n"
    text += "'"+sys.argv[1]+"', '"+sys.argv[2]+"'"
    if (len(sys.argv) >= 4):
        text += ", '"+sys.argv[3]+"'"
    if (len(sys.argv) >= 5):
        text += ", '"+sys.argv[4]+"'"
    text += "]\n"
    file.write(text)
    file.write("Method Selected: "+method+"\n")
    file.write("Running "+method+"\n")

solve(method, p)
# print(goal)
# print(start)
# p.getEmpty()
# p.solveDFS()
# p.solveBFS()
# p.solveGreedy()
# p.solveAStar()

trace = p.getTrace()
for state in trace:
    print("Next state: ")
    for i in range(len(state)):
        print(state[i])
