import sys
sys.path.append("C:\\Users\\martb\\Desktop\\MSC AI\\Symb AI\\cw2\\python_cw3_mb1221\\battleship")
import numpy as np




class Board:
    """ Class representing the board of the player. 
            
    Acts as an interface between the player and its ships.
    """
    def __init__(self, size=(7,7), k=4):
        """ Initialises a Board given a list of ships. 
        
        Args:
            ships (list[Ship]): List of ships for the board. Auto-generates 
                ships if not given.
            size (tuple[int, int]): (width, height) of the board (in terms of 
                number of cells). Defaults to (10, 10).
            ships_per_length (dict): A dict with the length of ship as keys and
                the count as values. Defaults to 1 ship each for lengths 1-5.
                
        Raises:
            ValueError if the number of ships is False
        """
        self.width = size[0]
        self.height = size[1]
        
        # Set of cells that have been checked for each player
        # Used for visualising the board
        self.board_k = np.zeros((self.width, self.height))
        self.player1_cells = []
        self.player2_cells = []
        self.k = k
        
    def add_move_to_board(self, player, cell):
        x,y = cell
        self.board_k[y][x] = player
        
        if player == 1:
            self.player1_cells.append(cell)
        else:
            self.player2_cells.append(cell)
        
    def winner_check(self):
        """ Check whether someone has won the game.
        
        Returns:
            bool : return True if all ships on the board have sunk.
               return False otherwise.
        """
        #Column check
        board = self.board_k
        for col in range(self.width):
            board_col = board[:,col]
            winner = self.streak_check(board_col)
            if winner > 0:
                return winner
        #Row check
        for row in range(self.height):
            board_row = board[row,:]
            winner = self.streak_check(board_row)
            if winner > 0:
                return winner

        diags = [board[::-1,:].diagonal(i) for i in range(-3,4)]
        diags.extend(board.diagonal(i) for i in range(3,-4,-1))
        all_diags = [n.tolist() for n in diags if len(n) >= self.k]
        for diag in all_diags:
            winner = self.streak_check(diag)
            if winner > 0:
                return winner
        return 0



    def streak_check(self, input):
        player = 0
        streak = 0
        for cell in input:
            if cell == player:
                streak += 1
            else: 
                player = cell
                streak = 1
            if streak == self.k and player > 0:
                return player
        return 0

    def get_cell(self, column_nr):
        column = self.board_k[:,column_nr-1]
        if 1 in column or 2 in column:
            y_coord = np.where(column)[0].max() + 1
            cell = (column_nr-1, y_coord )
            return cell
        else: 
            return(column_nr-1, 0)
  
    def print(self):
        """ Visualise the board on the terminal.
        
        Args:
            show_ships (bool): Shows the ships on the board. Defaults to False. 
            
        Returns:
            None
        """
        array_board = self._build_array()
        board_str = self._array_to_str(array_board)
        print(board_str)

    def _build_array(self):
        """ Generate an array representation of the Board for visualisation."""
        array_board = [[' ' for _ in range(self.width)] for _ in range(self.height)]

        for cells in self.player1_cells:
            x_1, y_1 = cells
            array_board[self.height - (y_1+1)][x_1] = 'X'

        for cells in self.player2_cells:
            x_2, y_2 = cells
            array_board[self.height - (y_2+1)][x_2] = '0'

        return array_board
    
    def _array_to_str(self, array_board):
        """ Convert an array representation of the Board to string 
            representation to facilitate visualisation.
        """
        list_lines = []

        array_first_line = [str(code) for code in range(1, self.width + 1)]
        first_line = ' ' * 6 + (' ' * 5).join(array_first_line) + ' \n'

        for index_line, array_line in enumerate(array_board, 1):
            number_spaces_before_line = 2 - len(str(index_line))
            space_before_line = number_spaces_before_line * ' '
            list_lines.append(f'{space_before_line}{self.height - index_line + 1} |  ' + '  |  '.join(array_line) + '  |\n')

        line_dashes = '   ' + '-' * 6 * self.width + '-\n'

        board_str = first_line + line_dashes + line_dashes.join(list_lines) + line_dashes

        return board_str


if __name__ == '__main__':
    # SANDBOX for you to play and test your methods

    
    # Automatic board


    
    