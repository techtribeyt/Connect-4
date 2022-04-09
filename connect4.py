class Connect4:
    def __init__(self):
        self.turn = 0
        self.result = None
        self.terminal = False
    def get_initial_position(self):
        return Position(self.turn)
                
class Position:
    def __init__(self, turn, mask = 0, position = 0, num_turns = 0):
        self.turn = turn
        self.result = None
        self.terminal = False
        self.num_turns = num_turns
        self.mask = mask
        self.position = position
        self._compute_hash()
                
    # returns new position
    def move(self, loc):
        new_position = self.position ^ self.mask
        new_mask = self.mask | (self.mask + (1 << (loc*7)))

        new_pos = Position(int(not self.turn), new_mask, new_position, self.num_turns + 1)
        new_pos.game_over()
        return new_pos
    
    # return list of legal moves
    def legal_moves(self):
        bit_moves = []
        for i in range(7):
            col_mask = 0b111111 << 7 * i
            if col_mask != self.mask & col_mask:
                bit_moves.append(i)
        return bit_moves
    
    
    def game_over(self):
        # sets result to -1, 0, or 1 if game is over (otherwise self.result is None)
        connected_4 = self.connected_four_fast()
        
        if connected_4:
            self.terminal = True
            self.result = 1 if self.turn == 1 else -1
        else:
            self.terminal = False
            self.result = None
            
        # mask when all spaces are full
        if self.mask == 279258638311359:
            self.terminal = True
            self.result = 0
            
    def connected_four_fast(self):
        other_position = self.position ^ self.mask
        
        # Horizontal check
        m = other_position & (other_position >> 7)
        if m & (m >> 14):
            return True
        # Diagonal \
        m = other_position & (other_position >> 6)
        if m & (m >> 12):
            return True
        # Diagonal /
        m = other_position & (other_position >> 8)
        if m & (m >> 16):
            return True
        # Vertical
        m = other_position & (other_position >> 1)
        if m & (m >> 2):
            return True
        # Nothing found
        return False
            
    
    def _compute_hash(self):
        position_1 = self.position if self.turn == 0 else self.position ^ self.mask
        self.hash = 2 * hash((position_1, self.mask)) + self.turn
    
    def __hash__(self):
        return self.hash
    def __eq__(self, other):
        return isinstance(other, Position) and self.turn == other.turn and self.mask == other.mask and self.position == other.position

