import math
import numpy as np
import random
from itertools import product
import os

class TIC_TAC_TOE:
    def __init__(self):
        self.row = 3; self.col = 3
        self.symbols = ['_', 'O', 'X']
        self.char_x = self.symbols[2]
        self.char_o = self.symbols[1]
        self.grid = [['_' if i < 2 else " " for j in range(self.col)] for i in range(self.row)]
        # " " for aesthetic purposes

    def current_board_state(self):
        print("---Current Board State---")
        for row in self.grid: print("|".join(row))
            
    def game_state(self): return self.grid
    
class AGENT(TIC_TAC_TOE):
    def __init__(self):
        super().__init__()
        self.draw = 0
        self.q_table = {}
        self.epsilon = {"initial": 1, "min": 0.01, "decay": 0.995}
        self.win = math.inf # maybe change to -1 and 1
        self.loss = -math.inf
        self.states_lists = None
        self.game_results = {1: "WIN", 2: "LOSS", 3: "DRAW"}
        self.game_results_pointers = [self.win, self.loss, self.draw]
    
    def reward_function(self, game_result):
        # game_result should be a result
            for key, value in self.game_results:
                if game_result == value:
                    return self.game_results_pointers[key]
                else:
                    # In INTERMEDIATE STATES = 0/draw
                    return self.game_results_pointers[2]
        
    def action_space(self, state) -> list:
        # REMEMBER That the grid includes "_" and " "
        "returns coordinates of possible moves as tuples within a list"
        count = 0; available_moves = []
        for i, row in enumerate(state):
            for j, space in enumerate(row):
                if space == 'O' or space == 'X':
                    # print(f"Occupied with a {space}")
                    pass
                else:
                    # print(f"there are {count+1} free spaces such as {space}")
                    count += 1; location_tuple = (i, j)
                    available_moves.append(location_tuple)
        return available_moves
        
    def Q_TABLE(self, actions) -> dict:
        "Q-learning is a model-free, off-policy reinforcement learning algorithm that aims to learn"
        "the optimal action-selection policy for maximizing cumulative rewards in a Markov decision process (MDP)."
        "This Q-Learning idea of two separate policies—behavior policy and target policy"
        "This function returns a tuple of lists of tuples and a dictionary of Q Table"
        # 3^9 possible Combinatorics solutions including '_',  'X' & 'O
        raw_states = product(self.symbols, repeat=9)
        # Tuples are often used because they are immutable and hashable, good for dictionary keys (e.g., in a Q-table).
        self.states_lists = [tuple(all_states) for all_states in raw_states]      
        # 2. Initialize the Q-table data structure to store Q-values for each state-action pair.
        for states in self.states_lists:
            # self.q_table[states] = {11:1, 5:10}
            self.q_table[states] = {action: 0 for action in actions}
        return self.q_table
    
    def EGP_Action_Selection(self, q_table, current_state) -> tuple:
        # EPSILON_GREEDY_POLICY
        n = random.uniform(0,1)
        if n < self.epsilon["initial"]:
            # explore
            possible_moves = self.action_space(current_state)
            # A <- random action from random space
            action = random.choice(possible_moves)
        else:
            # expolit
            return max(self.q_table[current_state], key=self.q_table[current_state].get)
        return action
    def Q_Learning_Algorithm_update_val(self, state, action,reward, next_state, q_table, alpha, gamma):
        # Q(s,a)←(1−α)⋅Q(s,a)+α⋅(r+γ⋅max a′Q(s′,a′))
        current_q_value = self.q_table[state][action]
        target_q_value = reward + gamma * max(q_table[next_state].values())
        updated_q_value = current_q_value + alpha * (target_q_value - current_q_value)
        # 
        self.q_table[state][action] = updated_q_value
    
    def softmax_action_selection(self):
        pass
    def upper_confidence_bound(self):
        pass
    def Thompson_sampling(self):
        pass
    
    def tuple_to_list(self, tuples_dict) -> list:
        state_configurations = []
        for tuple_state in tuples_dict:
             # state = ('X', 'X', 'X', 'O', 'O', '_', 'X', 'X', '_')
            rows = []
            for i in range(0,9,3):
                rows.append(list(tuple_state[i:i+3]))
            state_configurations.append(rows)
        # for i in range(len(state_configurations)): 
            # if i+1 == len(state_configurations): os.system("clear")
            # print(f"{i+1}.{state_configurations[i]}")
        return state_configurations
        
def main():
    agent_1 = AGENT()
    # states = agent_1.Q_TABLE()
    # states_in_list = agent_1.tuple_to_list(states)
    
if __name__ == "__main__":
    main()
    