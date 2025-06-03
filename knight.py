import copy
import string

from chessboard import Chessboard

class Knight(Chessboard):
    
    def __init__(self, start_pos='d4', end_pos='h8'):
        super().__init__()
        self.start = start_pos
        self.end = end_pos
        self.best_path = None
        self.lowest_counter = float('inf')


    @staticmethod
    def convert_board_notation(pos: str):
        """
        Convert position (e.g. H8) to DataFrame readable index (e.g. (0, 7))
        """
        if len(pos) != 2 or pos[0].lower() not in string.ascii_lowercase[:8] or pos[1] not in string.digits[1:9]:
            raise ValueError("Invalid position.")
        
        col = string.ascii_lowercase.index(pos[0].lower())
        row = 8 - int(pos[1])

        return row, col
    
    @staticmethod
    def convert_chess_notation(pos):
        """
        Convert DataFrame index (e.g. (0, 7)) to board position (e.g. H8)
        """
        row = 8 - pos[0]
        col = string.ascii_lowercase[pos[1]]
        
        return f"{col}{row}"



    def draw_board(self):
        """
        Draw the start and end possition of the Knight, together with its best path taken
        """
        # Start
        self.chessboard.iloc[self.convert_board_notation(self.start)] = 'S'

        # Path(s)
        if self.best_path is not None:
            for i in range(len(self.best_path)):
                tile = self.best_path[i]
                self.chessboard.iloc[self.convert_board_notation(tile)] = i+1

        # End
        self.chessboard.iloc[self.convert_board_notation(self.end)] = 'E'


    def valid_moves(self, pos):
        """
        Returns a list of valid move from current position
        """
        possible_moves = [
            (2, 1), (2, -1),
            (-2, 1), (-2, -1),
            (1, 2), (-1, 2),
            (-1, 2), (-1, -2)
        ]

        valid = list()
        for move in possible_moves:
            new_pos = [a + b for a, b in zip(pos, move)]

            # Check if new_pos is still in the board
            if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                valid.append(tuple(new_pos))

        return valid
    

    def move(self, start_pos=None, end_pos=None, counter=0, path=None, visited=None):
        """
        Move chess piece
        Record best solution and lowest number of moves
        """
        # Check for default case / initialisation
        if start_pos is None:
            start_pos = self.start
        if end_pos is None:
            end_pos = self.end
        if path is None:
            # path = [start_pos]
            path = list()
        if visited is None:
            visited = set()
 
        # Check for board_notation of positions
        if isinstance(start_pos, str):
            start_pos = self.convert_board_notation(start_pos)
        if isinstance(end_pos, str):
            end_pos = self.convert_board_notation(end_pos)


        # From recursive
        visited.add(tuple(path))

        # Check for end condition
        if start_pos == end_pos:
            if counter < self.lowest_counter:
                self.lowest_counter = counter
                self.best_path = path

            return 0

        for next_pos in self.valid_moves(start_pos):
            new_path = copy.deepcopy(path)
            new_pos_chess = self.convert_chess_notation(next_pos)
            new_path.append(new_pos_chess)

            # Ignore if len of new path > lowest counter
            if len(new_path) > self.lowest_counter:
                continue

            # Ignore if path has been visited
            if tuple(new_path) in visited:
                continue

            # Ignore if position has been visited by current path
            if new_pos_chess in path:
                continue

            visited.add(tuple(new_path)) 

            self.move(next_pos, end_pos, len(new_path), new_path, visited)