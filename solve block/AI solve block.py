import sys
import copy


class Puzzle:
    def __init__(self, start, goal):
        self.start = [[int(j) for j in i] for i in start]
        self.goal = [[int(j) for j in i] for i in goal]
        self.trace = []
        self.empty = [-1, -1]
        self.visited = []
        # set the start point of the empty block
        for i in range(len(start)):
            for j in range(len(start[0])):
                if start[i][j] == "0":
                    self.empty = [i, j]
                    return

    def getEmpty(self):
        return self.empty

    def solveDFS(self):
        self.dfs([], self.empty, self.start)

    def dfs(self, trace, empty, state):
        # print(trace)
        # print("Curr State: ", state)
        # Check if the State is already visited
        if self.isVisited(state):
            # print("visited")
            return

        # Append current state to the trace
        trace.append(copy.deepcopy(state))
        self.visited.append(copy.deepcopy(state))

        # If End Goal is reached
        if state == self.goal:
            print("Reached")
            self.trace = copy.deepcopy(trace)
            return

        # Up Down Left Right slide
        # Down
        if empty[0] > 0:
            state[empty[0]][empty[1]], state[empty[0]-1][empty[1]
                                                         ] = state[empty[0]-1][empty[1]], state[empty[0]][empty[1]]
            self.dfs(trace, [empty[0]-1, empty[1]], state)
            state[empty[0]-1][empty[1]], state[empty[0]][empty[1]
                                                         ] = state[empty[0]][empty[1]], state[empty[0]-1][empty[1]]
        # Up
        if empty[0] < len(state)-1:
            state[empty[0]][empty[1]], state[empty[0]+1][empty[1]
                                                         ] = state[empty[0]+1][empty[1]], state[empty[0]][empty[1]]
            self.dfs(trace, [empty[0]+1, empty[1]], state)
            state[empty[0]+1][empty[1]], state[empty[0]][empty[1]
                                                         ] = state[empty[0]][empty[1]], state[empty[0]+1][empty[1]]
        # Right
        if empty[1] > 0:
            state[empty[0]][empty[1]], state[empty[0]][empty[1] -
                                                       1] = state[empty[0]][empty[1]-1], state[empty[0]][empty[1]]
            self.dfs(trace, [empty[0], empty[1]-1], state)
            state[empty[0]][empty[1]-1], state[empty[0]][empty[1]
                                                         ] = state[empty[0]][empty[1]], state[empty[0]][empty[1]-1]
        # Left
        if empty[1] < len(state[0])-1:
            state[empty[0]][empty[1]], state[empty[0]][empty[1] +
                                                       1] = state[empty[0]][empty[1]+1], state[empty[0]][empty[1]]
            self.dfs(trace, [empty[0], empty[1]+1], state)
            state[empty[0]][empty[1]+1], state[empty[0]][empty[1]
                                                         ] = state[empty[0]][empty[1]], state[empty[0]][empty[1]+1]

    def isVisited(self, state):
        for st in self.visited:
            # check if every number is same in st and state mat
            if st == state:
                return True
        return False

    def getTrace(self):
        return self.trace

    def solveBFS(self):
        queue = []
        self.visited = []
        queue.append([self.start, self.empty, []])

        # BFS
        while (len(queue) != 0):
            state = queue.pop(0)
            # Check if state is already visited
            if self.isVisited(state[0]) == False:
                state[2].append(copy.deepcopy(state[0]))
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
                        [newState, [empty[0]-1, empty[1]], copy.deepcopy(state[2])])
                # Up
                if empty[0] < len(state[0])-1:
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]+1][empty[1]
                                                                       ] = newState[empty[0]+1][empty[1]], newState[empty[0]][empty[1]]
                    queue.append(
                        [newState, [empty[0]+1, empty[1]], copy.deepcopy(state[2])])
                # Right
                if empty[1] > 0:
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]][empty[1] -
                                                                     1] = newState[empty[0]][empty[1]-1], newState[empty[0]][empty[1]]
                    queue.append(
                        [newState, [empty[0], empty[1]-1], copy.deepcopy(state[2])])
                # Left
                if empty[1] < len(state[0][0])-1:
                    newState = copy.deepcopy(state[0])
                    newState[empty[0]][empty[1]], newState[empty[0]][empty[1] +
                                                                     1] = newState[empty[0]][empty[1]+1], newState[empty[0]][empty[1]]
                    queue.append(
                        [newState, [empty[0], empty[1]+1], copy.deepcopy(state[2])])


def fillState(state, fileName):
    with open(fileName, 'r') as file:
        for line in file:
            state.append(line.split())
        if len(start) > 0:
            state.pop()


start = []
goal = []

fillState(start, sys.argv[1])
fillState(goal, sys.argv[2])
print(goal)
print(start)
p = Puzzle(start, goal)
# p.getEmpty()
# p.solveDFS()
p.solveBFS()
trace = p.getTrace()
for state in trace:
    for i in range(len(state)):
        print(state[i])
    print("Next state: ")
