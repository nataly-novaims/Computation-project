import heapq
 
# state = (row1, col1, row2, col2)
# when block is upright: row1==row2 and col1==col2
# we always keep the smaller pair first so same position = same state
 
def make_state(r1, c1, r2, c2):
    if (r1, c1) <= (r2, c2):
        return (r1, c1, r2, c2)
    return (r2, c2, r1, c1)
 
 
def get_neighbors(state, board):
    r1, c1, r2, c2 = state
 
    upright = (r1 == r2 and c1 == c2)
    horizontal = (r1 == r2 and c1 != c2)
 
    candidates = []
 
    if upright:
        candidates.append(("right", (r1, c1+1, r1, c1+2)))
        candidates.append(("left",  (r1, c1-2, r1, c1-1)))
        candidates.append(("down",  (r1+1, c1, r1+2, c1)))
        candidates.append(("up",    (r1-2, c1, r1-1, c1)))
 
    elif horizontal:
        candidates.append(("right", (r1, c2+1, r1, c2+1)))
        candidates.append(("left",  (r1, c1-1, r1, c1-1)))
        candidates.append(("up",    (r1-1, c1, r1-1, c2)))
        candidates.append(("down",  (r1+1, c1, r1+1, c2)))
 
    else:
        #vertical
        candidates.append(("up",    (r1-1, c1, r1-1, c1)))
        candidates.append(("down",  (r2+1, c1, r2+1, c1)))
        candidates.append(("left",  (r1, c1-1, r2, c1-1)))
        candidates.append(("right", (r1, c1+1, r2, c1+1)))
 
    result = []
    for move, (nr1, nc1, nr2, nc2) in candidates:
        if board.is_walkable(nr1, nc1) and board.is_walkable(nr2, nc2):
            result.append((move, make_state(nr1, nc1, nr2, nc2)))
 
    return result
 
 
def reached_goal(state, board):
    r1, c1, r2, c2 = state
    #block must be upright and on goal tile
    return r1 == r2 and c1 == c2 and board.is_goal(r1, c1)
 
 
def get_moves(came_from, state):
    #trace back from goal to start to rebuild move list
    moves = []
    while came_from[state] is not None:
        prev, move = came_from[state]
        moves.append(move)
        state = prev
    moves.reverse()
    return moves
 
 
#BFS - uses plain list as queue with index pointer (no deque needed)
def bfs(board, start_row, start_col):
    start = make_state(start_row, start_col, start_row, start_col)
    came_from = {start: None}
 
    queue = [start]
    index = 0
 
    while index < len(queue):
        current = queue[index]
        index = index + 1
 
        if reached_goal(current, board):
            return get_moves(came_from, current)
 
        for move, neighbor in get_neighbors(current, board):
            if neighbor not in came_from:
                came_from[neighbor] = (current, move)
                queue.append(neighbor)
 
    return None  #no solution
 
 
#heuristic for A* - Manhattan distance from block center to goal
def heuristic(state, board):
    r1, c1, r2, c2 = state
    gr, gc = board.goal
    center_r = (r1 + r2) / 2
    center_c = (c1 + c2) / 2
    return abs(center_r - gr) + abs(center_c - gc)
 
 
#A* - smarter search using heuristic to guide toward the goal
def astar(board, start_row, start_col):
    start = make_state(start_row, start_col, start_row, start_col)
    came_from = {start: None}
    g_score = {start: 0}
    heap = []
    heapq.heappush(heap, (heuristic(start, board), 0, start))
 
    while len(heap) > 0:
        f, g, current = heapq.heappop(heap)
 
        #skip if we already found a cheaper path to this state
        if g > g_score.get(current, float('inf')):
            continue
 
        if reached_goal(current, board):
            return get_moves(came_from, current)
 
        for move, neighbor in get_neighbors(current, board):
            new_g = g + 1
            if new_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = new_g
                came_from[neighbor] = (current, move)
                heapq.heappush(heap, (new_g + heuristic(neighbor, board), new_g, neighbor))
 
    return None  #no solution