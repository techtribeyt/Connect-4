import random
import math
import time

def get_nodes(initial_pos, time_limit):
    nodes = {}
        
    # (w, n, dict parent --> num_times_seen)
    nodes[initial_pos] = (0.0, 0.0, {initial_pos: 0})
    start_time = time.time()
    while time.time() - start_time < time_limit:        
        # root to leaf traversal - returns entire traversal path
        leaf_path = get_leaf(nodes, initial_pos)
        
        # the leaf is the last entry in the path
        leaf = leaf_path[-1]
        
        # extract stats associated with node
        _, ni, _ = nodes[leaf]
        
        # leaf expansion
        if ni > 0 and not leaf.terminal:
            # expand node & create children entries
            legal_moves = leaf.legal_moves()
            for loc in legal_moves:
                new_pos = leaf.move(loc)
                
                # so that we do not override existing data
                if new_pos not in nodes:
                    nodes[new_pos] = (0.0, 0.0, {leaf: 0})
                    
            # choose random child node to explore
            loc = random.choice(legal_moves)
            
            # randomly play that node
            child_pos = leaf.move(loc)
            
            reward = 0
            num_runs = 10
            for _ in range(num_runs):
                reward += randomly_play(child_pos)
            w, n, parent_n_dict = nodes[child_pos]
            if leaf not in parent_n_dict:
                parent_n_dict[leaf] = 0
            parent_n_dict[leaf] += 1
            nodes[child_pos] = (w + reward, n + num_runs, parent_n_dict)

        else:
            # otherwise randomly play that leaf
            reward = 0
            num_runs = 10
            for _ in range(num_runs):
                reward += randomly_play(leaf)   
        
        # update all positions in path to reflect new information
        parent = initial_pos
        for position in leaf_path:
            w, n, parent_n_dict = nodes[position]
            parent_n_dict[parent] += num_runs
            nodes[position] = (w + reward, n + num_runs, parent_n_dict)
            parent = position
    return nodes

def ucb2_agent(time_limit):
    def strat(pos):
        nodes = get_nodes(pos, time_limit)

        # set up score threshold
        player = pos.turn
        best_score = float('-inf')
        if player == 1:
            best_score = float('inf')
        next_best_move = None
   
        # for each next move
        for loc in pos.legal_moves():
            
            # get the next position
            next_pos = pos.move(loc)
                        
            # score is 0 if we have no explored
            if next_pos not in nodes:
                score = 0.0
            else:
                w, n, _ = nodes[next_pos]
                if n == 0:
                    score = 0.0
                else:
                    # expected score
                    score = w / n
            
            # update best score & best move
            if score < best_score and player == 1:
                best_score = score
                next_best_move = loc
            elif score > best_score and player == 0:
                best_score = score
                next_best_move = loc
        return next_best_move
    return strat
        
        
# selects next move at random until terminal position
def randomly_play(pos):
    cur_pos = pos
    while not cur_pos.terminal:
        moves = cur_pos.legal_moves()
        loc = random.choice(moves)

        cur_pos = cur_pos.move(loc)
    return float(cur_pos.result)
        
def get_leaf(nodes, root):
    current_node = root
    path = []
    while True:
        w, ni, _ = nodes[current_node]
        path.append(current_node)
        if ni == 0:
            return path
        
        legal_moves = current_node.legal_moves()
        next_player = current_node.turn
        
        best_score = float('-inf')
        if next_player == 1:
            best_score = float('inf')
        next_best_node = None
        
        for loc in legal_moves:
            result_position = current_node.move(loc)
            if result_position not in nodes:
                return path
            temp_w, temp_ni, temp_parent_n_count = nodes[result_position]
            if current_node not in temp_parent_n_count:
                temp_parent_n_count[current_node] = 0
            if temp_parent_n_count[current_node] == 0:
                path.append(result_position)
                return path
            

        
            # N is the number of times parent has been visited
            score = get_score(nodes[current_node][1], temp_parent_n_count[current_node], temp_w / temp_ni, next_player)
            if score < best_score and next_player == 1:
                best_score = score
                next_best_node = result_position
            elif score > best_score and next_player == 0:
                best_score = score
                next_best_node = result_position
                
        current_node = next_best_node
        if current_node is None:
            return path
            
            
def get_score(N, ni, r, player, c=2.0):
    if player == 0: return r + math.sqrt(c * math.log(N) / ni)
    return r - math.sqrt(c * math.log(N) / ni)

