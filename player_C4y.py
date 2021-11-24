import random
from board_C4 import Board
from convert import CellConverter

class Player:
    """ Class representing the player
    """
    count = 0  # for keeping track of number of players
    
    def __init__(self, name=None):
        """ Initialises a new player with its board.

        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        
        Player.count += 1
        if name is None:
            self.name = f"Player {self.count}"
        else:
            self.name = name
    
    def __str__(self):
        return self.name
    
    def select_target(self):
        """ Select target coordinates to attack.
        
        Abstract method that should be implemented by any subclasses of Player.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        raise NotImplementedError
    
class ManualPlayer(Player):
    """ A player playing manually via the terminal
    """
    def __init__(self, name=None):
        """ Initialise the player with a board and other attributes.
        
        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        super().__init__(name=name)

    def select_target(self, board):
        """ Read coordinates from user prompt.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        while True:
            try:
                target_col = int(input("Enter the target column value: "))
                return target_col
            except ValueError as error:
                print(error)

class RandomPlayer(Player):
    """ A Player that plays at random positions.

    However, it does not play at the positions:
    - that it has previously attacked
    """
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        super().__init__(name=name)

    def select_target(self, board):
        """ Generate a random cell that has previously not been attacked.
        
        Also adds cell to the player's tracker.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        column = random.randint(1, board.width)

        return column


class AutomaticPlayer(Player):
    """ Player playing automatically using a strategy."""
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
            Description of attributes:
            self.tracker (set) - a set of coordinates that have been attacked
            self.ship_found_coords (list) - a list memorising the coordinates of a ship if a ship has been found and not yet sunk 
            self.latest_attack (tuple[int, int]) - a tuple showing the latest attack (initialised to 0,0)
            self.attack_direction (int) - integer indicating the direction of the next attack 
                (1 means attack to the north, 2 means attack to the south, 3 means attack to the east and 4 means attack to the west)
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        self.tracker = set()
        self.ship_found_coords = []
        self.latest_attack = (0,0)
        self.attack_direction = 1 

        
    def select_target(self):
        """ Select target coordinates to attack.
        If a ship has been found or is currently attacked (ship_found_coords attribute is not empty), then a "smart attack" is generated
        The cell that is gotten from the generate_smart_attack() function is added to tracker and returned as the next attack cell
        Otherwise a random attack is generated, added to the tracker and returned as the next attack cell
        For both cases, the latest_attack attribute is also updated

        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        if len(self.ship_found_coords)>0:
            target_cell = self.generate_smart_attack()
            self.latest_attack = target_cell
            self.tracker.add(target_cell)
            return target_cell

        else:
            target_cell = self.generate_random_target()
            self.tracker.add(target_cell)
            self.latest_attack = target_cell
            return target_cell
    
    def generate_smart_attack(self):
        """ Select target coordinates to attack.
        According to the self.attack_direction a cell is chosen for the attack:
            If the direction = 1, the attack is one cell above to the ship's coordinates
            If the direction = 2, the attack is one cell below to the ship's coordinates
            If the direction = 3, the attack is one cell right to the ship's coordinates
            If the direction = 4, the attack is one cell left to the ship's coordinates
        After the cell has been generated its validity is checked (check_cell_valid() function)
        If the cell is valid, current cell is returned as the attack coordinate, otherwise new direction is chosen

        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        if self.attack_direction == 1:
            self.ship_found_coords.sort(key=lambda tup: tup[1])
            attack_y_coord = self.ship_found_coords[0][1] - 1 
            attack_x_coord = self.ship_found_coords[0][0]
            attack_cell = (attack_x_coord, attack_y_coord)
            if self.check_cell_valid(attack_cell):
                return attack_cell
            else:
                self.attack_direction += 1

        if self.attack_direction == 2:
            self.ship_found_coords.sort(key=lambda tup: tup[1])
            attack_y_coord = self.ship_found_coords[-1][1] + 1
            attack_x_coord = self.ship_found_coords[-1][0]
            attack_cell = (attack_x_coord, attack_y_coord)
            if self.check_cell_valid(attack_cell):
                return attack_cell
            else:
                self.attack_direction += 1

        if self.attack_direction == 3:
            self.ship_found_coords.sort(key=lambda tup: tup[0])
            attack_y_coord = self.ship_found_coords[-1][1]
            attack_x_coord = self.ship_found_coords[-1][0] + 1
            attack_cell = (attack_x_coord, attack_y_coord)
            if self.check_cell_valid(attack_cell):
                return attack_cell
            else:
                self.attack_direction += 1

        if self.attack_direction == 4:
            self.ship_found_coords.sort(key=lambda tup: tup[0])
            attack_y_coord = self.ship_found_coords[0][1]
            attack_x_coord = self.ship_found_coords[0][0] - 1
            attack_cell = (attack_x_coord, attack_y_coord)
            if self.check_cell_valid(attack_cell):
                return attack_cell
            else:
                self.attack_direction = 1
        
    
    def check_cell_valid(self,cell):
        """ Check the validity of a given cell. 
        False is returned if one of the following conditions is breached: 
            The x coordinate is less than 0 or higher than the width of the board
            The y coordinate is less than 0 or higher than the heighth of the board
            Given cell is in the tracker set
        If none of the conditions is breached, True is returned
        Args:
            cell (tuple[int, int]) - cell for which the validity is checked

        Returns:
            Boolean: Is the chosen cell valid or not
        """
        y_coord = cell[1]
        x_coord = cell[0]
        if x_coord < 1 or x_coord > self.board.width:
            return False
        if y_coord < 1 or y_coord > self.board.height:
            return False
        if cell in self.tracker:
            return False
        
        return True

    def add_adjacent_cells_to_tracker(self):
        """ Add the surrounding cells of the sunk ship to the tracker attribute
            All cells that are adjacent to the ships cells, that are found in ship_found_coordinates, are added to the tracker attribute.
        """

        for cell in self.ship_found_coords:
            x = cell[0]
            y = cell[1]
            cell_up = (x, y-1)
            cell_down = (x, y+1)
            cell_left = (x-1, y)
            cell_right = (x+1, y)
            cell_ur = (x+1, y-1) # upper right
            cell_ul = (x-1, y-1) # upper left
            cell_dr = (x+1, y+1) # down right
            cell_dl = (x-1, y+1) # down left
            cells = [cell_up, cell_down, cell_left, cell_right,
                     cell_ur, cell_ul, cell_dr, cell_dl]
            self.tracker.update(cells)
    
    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive results of latest attack.
        
        Player receives notification on the outcome of the latest attack by the 
        player, on whether the opponent's ship is hit, and whether it has been 
        sunk. 

        If the has_ship_sunk attribute is true, the latest attack cell is added to the ship_found_coords attribute
        and all adjacent cells of the sunk ship are added to the tracker attribute (because no ship can be there).
        Then the ship_found_coords list attribute is initalised to an empty list and attack_direction attribute is initialised to 1

        If the has_ship_sunk is False but is_ship_hit attribute is True, the latest_attack cell attribute is appended
        to the ship_found_coords list attribute.

        Args:
        is_ship_hit (Boolean) - Was a ship hit with the latest attack
        has_ship_sunk (Boolean) - Was a ship sunk with the latest attack

        Returns:
            None
        """
        if has_ship_sunk:
            self.ship_found_coords.append(self.latest_attack)
            self.add_adjacent_cells_to_tracker()
            self.ship_found_coords = []
            self.attack_direction = 1
            return None

        if is_ship_hit:
            self.ship_found_coords.append(self.latest_attack)
            

    def generate_random_target(self):
        """ Generate a random cell that has previously not been attacked.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        has_been_attacked = True
        random_cell = None
        
        while has_been_attacked:
            random_cell = self.get_random_coordinates()
            has_been_attacked = random_cell in self.tracker

        return random_cell

    def get_random_coordinates(self):
        """ Generate random coordinates.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)

    
