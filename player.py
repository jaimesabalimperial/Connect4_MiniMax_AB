from board import Board
import numpy as np

class Player():
    """ Class representing the player
    """
    count = 0  # for keeping track of number of players
    
    def __init__(self, name=None):
        """ Initialises a new player with its board.

        Args:
            name (str): Player's name
        """
        
        Player.count += 1
        if name is None:
            self.name = f"Player {self.count}"
        else:
            self.name = name

    def __str__(self):
        return self.name

    def _get_diagonals(self,board,row,col):
        """Retrieves positive and negative diagonals from a cell in a grid.
        
        Args:
            board {Board()}: current board state.
            row {int}: row of cell to evaluate
            col {int}: column of cell to evaluate
        
        Returns:
            diags {list}: Positive and negative diagonal arrays that cross at the cell (row,col).
        
        """

        pos_diag1 = np.fliplr(np.flipud(board.state[:row+1,:col+1])).diagonal()[::-1] #first half of positive diagonal
        pos_diag2 = board.state[-(board.height-row):,-(board.width-col):].diagonal()[1:] #second half

        #concatenate both halves to get full positive diagonal from point
        pos_diag = np.concatenate((pos_diag1, pos_diag2)) 

        neg_diag1 = np.flipud(board.state[:row+1, col:]).diagonal()#first half of negative diagonal
        neg_diag2 = np.fliplr(board.state[-(board.height-row):,:-(board.width-col-1)]).diagonal()[1:][::-1] #second half

        #concatenate both halves to get full positive diagonal from point
        neg_diag = np.concatenate((neg_diag2, neg_diag1))

        diags = [pos_diag, neg_diag] #input diagonals in list

        return diags

    def get_value(self, board, line):
        """Retrieves value of a row, column, or diagonal (line) from the disctionary
        containing the streaks within it. 
        
        Args:
            board {Board()}: current board state.
            line {np.ndarray}: array containing row, column or diagonal to evaluate.

        Returns:
            value {int}: Evaluated value of heuristic from row, column or diagonal as input. 
        """
        value = 0
        streaks_dict = board.streak_check_heuristic(line)
        for player, streaks in streaks_dict.items(): 
            for streak in streaks:
                 #exponentially higher value for larger assigned to larger streaks
                if player == "Max":
                    value += (80/board.k)**(streak) #add for Max() player streaks.
                elif player == "Min":
                    value -= (80/board.k)**(streak) #subtract for Min() player streaks.

        return value
    
    def heuristic(self, board):
        """Calculates the heuristic value of a specific state for the current player (Min or Max) by iterating
        over all columns, rows, and diagonals of each cell and calculating a value for them. 

           Value of streaks are: 
                - one: 2
                - two: 20
                - three: 400
        
        Args:
            board {Board()}: board object to indicate current state of game.
            
        Returns:
            value {int}: Evaluated value of heuristic from current state of board. """

        value = 0
        state = board.state #initialise board state
        #calculate heuristic by considering each players' current streaks
        # ---> heuristic is calculated as +-10^{streak-1}, where the + corresponds to Max() and - to Min()
        #check horizontal streaks
        for row in range(board.height):
            board_row = state[row,:]
            value += self.get_value(board, board_row)

        #check vertical streaks
        for col in range(board.width):
            board_col = state[:,col]
            value += self.get_value(board, board_col)

        #check diagonal streaks
        for col in range(board.height):
            for row in range(board.width):
                diags = self._get_diagonals(board,row,col)
                for board_diag in diags:
                    #only interested in adding value to diagonals that allow 
                    #for the successor states to be terminal
                    if len(board_diag) >= board.k: 
                        value += self.get_value(board, board_diag)

        return value

    
    def select_target(self):
        """ Select target coordinates to attack.
        
        Abstract method that should be implemented by any subclasses of Player.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        raise NotImplementedError


class MiniMaxPlayer(Player):
    def __init__(self, max_depth=5, name=None):
        super().__init__(name)

        self.max_depth = max_depth
        self.is_min = None
        self.states_visited = 0


    def max(self, board, depth=0):
        """Function used to recursively retrieve heuristic from a node that corresponds to 
        Max()'s turn by using the raw MiniMax algorithm.
        
        Args:
            board {Board()}: board object to indicate current state of game.
            depth {int}: current depth in search tree. 
        
        Returns: 
            best_value {int}: best value evaluated from child nodes. 
            best_move {int}: best action to be taken from current node. 
        """
        if board.is_terminal():
            return -float("inf"), None
        elif depth == self.max_depth:
            return self.heuristic(board), None
        #elif board.game_moves == 0:
        #    return self.heuristic(board), board.width // 2 + 1

        #initialise best value to be infinite and negative such that any action will be chosen at first
        best_value = -float("inf")  
        best_move = None

        #iterate over all valid actions and retrieve best score and thus move
        actions = board.get_actions()
        for action in actions:
            self.states_visited += 1
            next_state, move = action
            val = self.min(next_state, depth+1)[0]

            if val > best_value:
                best_value = val
                best_move = move

        #print(best_value, best_move)

        return best_value, best_move

    def min(self, board, depth=0):
        """Function used to recursively retrieve heuristic from a node that corresponds to 
        Min()'s turn by using the raw MiniMax algorithm.
        
        Args:
            board {Board()}: board object to indicate current state of game.
            depth {int}: current depth in search tree. 
        
        Returns: 
            best_value {int}: best value evaluated from child nodes. 
            best_move {int}: best action to be taken from current node. 
        """
        if board.is_terminal():
            return float("inf"), None
        elif depth == self.max_depth:
            return self.heuristic(board), None

        #initialise best value to be infinite and positive such that any action will be chosen at first
        best_value = float("inf")
        best_move = None

        #iterate over all possible actions and retrieve best score and thus move
        actions = board.get_actions()
        for action in actions:
            self.states_visited += 1
            next_state, move = action
            #child_state.print()
            val = self.max(next_state, depth+1)[0]

            if val < best_value:
                best_value = val
                best_move = move
        
        #print(best_value, best_move)

        return best_value, best_move

    def select_target(self, board):
        """Selects best action by using the raw MiniMax algorithm.
        
        Args:
            board {Board()}: board object to indicate current state of game.

        Returns:
            best_move {int} : optimum action evaluated to be used to make a move in the game.
        """
        if not self.is_min:
            best_move = self.max(board)[1]
        else:
            best_move = self.min(board)[1]

        #print(best_move)
        return best_move

class AlphaBetaPlayer(Player):
    def __init__(self, name=None, max_depth=5,  manual=False):
        super().__init__(name)
        ## Alpha is minimum value secured by Max, for herself

        self.max_depth = max_depth
        self.is_min = None
        self.first = True
        self.alpha = None
        self.beta = None
        self.manual = manual
        self.states_visited = 0


    def max(self, board, alpha, beta, depth=0):
        """Function used to recursively retrieve heuristic from a node that corresponds to 
        Max()'s turn by using alpha-beta pruning.
        
        Args:
            board {Board()}: board object to indicate current state of game.
            alpha {int}: Minimum value secured by Max()
            beta {int}: Maximum value imposed by Min()
            depth {int}: current depth in search tree. 
        
        Returns: 
            best_value {int}: best value evaluated from child nodes. 
            best_move {int}: best action to be taken from current node. 
        """
        if board.is_terminal():
            return -float("inf"), None
        elif depth == self.max_depth:
            return self.heuristic(board), None
        #elif board.game_moves == 0:
        #    return self.heuristic(board), board.width // 2 + 1
        
        #initialise best value to be infinite and 
        #negative such that any action will be chosen at first
        best_value = -float("inf")  
        best_move = None

        #iterate over all possible actions and retrieve best score and thus move
        actions = board.get_actions()
        for action in actions:
            self.states_visited += 1
            next_state, move = action
            val = self.min(next_state, alpha, beta, depth+1)[0]

            if val > best_value: #update best value if current evaluated value from move is lower than best
                best_value = val
                best_move = move

            alpha = max(alpha, best_value) #update beta if best value is lower than beta

            #if alpha >= beta, no use in continuing loop as current best move won't be subsituted
            #by subsequent child nodes
            if alpha >= beta: 
                break

        #print(best_value, best_move)

        return best_value, best_move

    def min(self, board, alpha, beta, depth=0):
        """Function used to recursively retrieve heuristic from a node that corresponds to 
        Min()'s turn by using alpha-beta pruning.
        
        Args:
            board {Board()}: board object to indicate current state of game.
            alpha {int}: Minimum value secured by Max()
            beta {int}: Maximum value imposed by Min()
            depth {int}: current depth in search tree. 
        
        Returns: 
            best_value {int}: best value evaluated from child nodes. 
            best_move {int}: best action to be taken from current node. 
        """
        if board.is_terminal():
            return float("inf"), None
        elif depth == self.max_depth:
            return self.heuristic(board), None

        #initialise best value to be infinite and positive such that any action will be chosen at first
        best_value = float("inf")
        best_move = None

        #iterate over all possible actions and retrieve best score (and thus corresponding move)
        actions = board.get_actions()
        for action in actions:
            self.states_visited += 1
            next_state, move = action
            #child_state.print()
            val = self.max(next_state, alpha, beta, depth+1)[0]

            if val < best_value:
                best_value = val
                best_move = move

            beta = min(beta, best_value) #update beta if best value is lower than beta

            #if alpha >= beta, no use in continuing loop as current best move won't be subsituted
            #by subsequent child nodes
            if alpha >= beta: 
                break
        
        #print(best_value, best_move)

        return best_value, best_move

    def select_target(self, board):
        """Selects best action by using alpha-beta pruning with the MiniMax algorithm.
        
        Args:
            board {Board()}: board object to indicate current state of game.

        Returns:
            best_move {int} : optimum action evaluated to be used to make a move in the game.
        """
        self.states_visited = 0

        if not self.is_min:
            best_move = self.max(board, alpha = -float("inf"), beta = float("inf"))[1]
        else:
            best_move = self.min(board, alpha = -float("inf"), beta = float("inf"))[1]

        print(best_move)
        return best_move

class ManualPlayer(Player):
    """ A player playing manually via the terminal
    """
    def __init__(self, name=None, max_depth = 5, AB=True, MiniMax = False):
        """ Initialise the player with a board and other attributes.
        
        Args:
            name (str): Player's name
            max_depth {int}: maximum depth allowed in searching for optimum action in MiniMax
                             (or alpha-beta pruning) algorithm.

            AB {bool}: If True action selection will be determined using alpha-beta pruning.
            MiniMax {bool}: If True action selection will be determined using minimax.
        """
        super().__init__(name)
        self.max_depth = max_depth
        self.states_visited = None
        
        if AB:
            self.player= AlphaBetaPlayer(name=self.name, max_depth=self.max_depth)
        elif MiniMax:
            self.player= MiniMaxPlayer(name=self.name, max_depth=self.max_depth)

    def select_target(self, board):
        """ Read coordinates from user prompt.
        
        Args:
            board {Board()}: board object to indicate current state of game.
        Returns:
            col {int} : column number to be used to make a move in the game.
        """
        while True:
            try:
                best_move = self.player.select_target(board)
                self.states_visited = self.player.states_visited
                print("Best action determined by AI: ", best_move)
                target_col = int(input("Enter the target column value: "))
                return target_col
            except ValueError as error:
                print(error)


if __name__ == '__main__':
    player = MiniMaxPlayer()
    board = Board()
    print(board.state)
    print(player.heuristic(board))
    #print(player.heuristic(board))
    #print(player._get_diagonals(board, 1, 0))
