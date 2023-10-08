from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import resource

#Amelie Sharples aes2367

#### SKELETON CODE ####
# The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """

    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception(
                "Config contains invalid/duplicate entries : ", config)

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i: 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        i = self.blank_index
        copy = self.config[:]
        puzzle = PuzzleState(copy, self.n, parent=self,
                             action="Up", cost=self.cost + 1)
        if(i == 0 or i == 1 or i == 2):
            return None
        swap_num = puzzle.config[i-3]
        puzzle.blank_index = i-3
        puzzle.config[i] = swap_num
        puzzle.config[i-3] = 0
        return puzzle

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        i = self.blank_index
        copy = self.config[:]
        puzzle = PuzzleState(copy, self.n, parent=self,
                             action="Down", cost=self.cost + 1)
        if(i == 6 or i == 7 or i == 8):
            return None
        swap_num = puzzle.config[i+3]
        puzzle.blank_index = i+3
        puzzle.config[i] = swap_num
        puzzle.config[i+3] = 0
        return puzzle

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        i = self.blank_index
        copy = self.config[:]
        puzzle = PuzzleState(copy, self.n, parent=self,
                             action="Left", cost=self.cost + 1)
        if(i == 0 or i == 3 or i == 6):
            return None
        swap_num = puzzle.config[i-1]
        puzzle.blank_index = i-1
        puzzle.config[i] = swap_num
        puzzle.config[i-1] = 0
        return puzzle

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        i = self.blank_index
        copy = self.config[:]
        puzzle = PuzzleState(copy, self.n, parent=self,
                             action="Right", cost=self.cost + 1)
        if(i == 2 or i == 5 or i == 8):
            return None
        swap_num = puzzle.config[i+1]
        puzzle.blank_index = i+1
        puzzle.config[i] = swap_num
        puzzle.config[i+1] = 0
        return puzzle

    def expand(self):
        """ Generate the child nodes of this node """

        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt
# Students need to change the method to have the corresponding parameters


def writeOutput(path_to_goal, cost_of_path, nodes_expanded, search_depth,
                max_search_depth, running_time, max_ram_usage):
    with open('output.txt', 'w') as f:
        f.write('path_to_goal: ' + str(path_to_goal) + '\n')
        f.write('cost_of_path: ' + str(cost_of_path) + '\n')
        f.write('nodes_expanded: ' + str(nodes_expanded) + '\n')
        f.write('search_depth: ' + str(search_depth) + '\n')
        f.write('max_search_depth: ' + str(max_search_depth) + '\n')
        f.write('running_time: {:.8f}\n'.format(running_time))
        f.write('max_ram_usage: ' + str(format(max_ram_usage, '.8f')) + '\n')
    f.close()
    return


def pathToGoal(initial_state, state):
    path = []
    cost = 0
    while state is not initial_state:
        path.append(state.action)
        state = state.parent
        cost = cost + 1
    path.reverse()
    return path, cost


def stateInExplored(child, explored):
    for item in explored:
        if item.config == child.config:
            return 1
    return 0


def bfs_search(initial_state):
    start_time = time.time()
    start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    frontier = Q.Queue()
    frontier.put(initial_state)
    nodes_expanded = 0
    max_ram_usage = 0
    explored = {}
    frontier_dic = {}

    while not frontier.empty():
        state = frontier.get()
        explored[tuple(state.config)] = state.config
        curr_ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss-start_ram) / (2**20)
        if(curr_ram_usage > max_ram_usage):
            max_ram_usage = curr_ram_usage

        if test_goal(state) == 0:
            end_time = time.time()
            running_time = end_time - start_time
            path_to_goal, cost_of_path = pathToGoal(initial_state, state)
            search_depth = cost_of_path
            max_search_depth = cost_of_path+1
            writeOutput(path_to_goal, cost_of_path, nodes_expanded,
                        search_depth, max_search_depth, running_time,
                        max_ram_usage)
            return state

        nodes_expanded = nodes_expanded+1

        for child in state.expand():
            if tuple(child.config) not in explored and tuple(child.config) not in frontier_dic:
                frontier_dic[tuple(child.config)] = child.config
                frontier.put(child)

    return None


def dfs_search(initial_state):
    start_time = time.time()
    start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    frontier = []
    frontier.append(initial_state)
    nodes_expanded = 0
    max_search_depth = 0
    max_cost = 0
    explored = {}
    frontier_dic = {}
    max_ram_usage = 0

    while frontier != None:
        state = frontier.pop()
        explored[tuple(state.config)] = state.config
        
        curr_ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss-start_ram) / (2**20)
        if(curr_ram_usage > max_ram_usage):
            max_ram_usage = curr_ram_usage
        
        if test_goal(state) == 0:
            end_time = time.time()
            running_time = end_time - start_time
            path_to_goal, cost_of_path = pathToGoal(initial_state, state)
            search_depth = cost_of_path
            writeOutput(path_to_goal, cost_of_path, nodes_expanded,
                        search_depth, max_search_depth, running_time, 
                        max_ram_usage)
            return state

        nodes_expanded = nodes_expanded+1
            
        listChildren = state.expand()
        listChildren.reverse()
        for child in listChildren:
            if tuple(child.config) not in explored and tuple(child.config) not in frontier_dic:
                frontier_dic[tuple(child.config)] = child.config
                frontier.append(child)
                if(child.cost > max_cost):
                    max_search_depth = child.cost
                    max_cost = child.cost

    return None


def A_star_search(initial_state):
    start_time = time.time()
    start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    frontier = Q.PriorityQueue()
    frontier.put((calculate_total_cost(initial_state), -1,  initial_state))
    explored = {tuple(initial_state.config): initial_state.config}
    frontier_dic = {tuple(initial_state.config): initial_state.cost}
    nodes_expanded = 0
    max_search_depth = 0
    max_cost = 0
    max_ram_usage = 0
    nodesAddedIn = 0

    while not frontier.empty():
        state = frontier.get()[2]

        

        if test_goal(state) == 0:
            end_time = time.time()
            running_time = end_time - start_time
            path_to_goal, cost_of_path = pathToGoal(initial_state, state)
            search_depth = cost_of_path
            max_search_depth = max_search_depth
            writeOutput(path_to_goal, cost_of_path, nodes_expanded,
                        search_depth, max_search_depth, running_time, 
                        max_ram_usage)
            return state

        nodes_expanded = nodes_expanded + 1

        for child in state.expand():
            if tuple(child.config) not in explored and tuple(child.config) not in frontier_dic:
                item = (calculate_total_cost(child), nodesAddedIn, child)
                frontier.put(item)
                frontier_dic[tuple(child.config)] = child.config
                nodesAddedIn += 1
                
                curr_ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss-start_ram) / (2**20)
                if(curr_ram_usage > max_ram_usage):
                    max_ram_usage = curr_ram_usage
                
                if(child.cost > max_cost):
                    max_search_depth = child.cost
                    max_cost = child.cost

    return None


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    total_cost = state.cost
    i = 0
    for item in state.config:
        if item != 0:
            total_cost = total_cost + calculate_manhattan_dist(i, item, state.n)
        i = i + 1
    return total_cost


def calculate_manhattan_dist(i, value, n):
    """calculate the manhattan distance of a tile"""
    val_row = int(i / n)
    val_col = i % n
    true_row = int(value/n)
    true_col = value % n
    return (abs(val_row-true_row) + abs(val_col - true_col))


def test_goal(state):
    """test the state is the goal state or not"""
    i = 0
    for item in state.config:
        if item != i:
            return 1
        i = i+1
    return 0

# Main Function that reads in Input and Runs corresponding Algorithm


def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, board_size)
    start_time = time.time()

    if search_mode == "bfs":
        bfs_search(hard_state)
    elif search_mode == "dfs":
        dfs_search(hard_state)
    elif search_mode == "ast":
        A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    print("Program completed in %.3f second(s)" % (end_time-start_time))


if __name__ == '__main__':
    main()
