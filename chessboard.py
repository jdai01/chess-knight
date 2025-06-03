import pandas as pd
import string

class Chessboard():
    
    def __init__(self):
        self.chessboard = pd.DataFrame(
            data=[[' ']*8 for _ in range(8)],
            columns=list(string.ascii_uppercase[:8]),
            index=list(range(8, 0, -1))  # Row labels 8 to 1 (like a chessboard)
        )