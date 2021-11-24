from board_C4 import Board
from game_C4 import Game
from player_C4y import AutomaticPlayer, ManualPlayer, RandomPlayer

class ManualVsManualSimulation:
    """ Play against your friend (or more likely yourself)! """
    def run(self):
        # Creating the ships MANUALLY for the 2 players Alice and Bob

        # Creating the players
        alice = ManualPlayer(name="Alice")
        bob = ManualPlayer(name="Bob")

        # Creating and launching the game
        game = Game(player1=alice, player2=bob)
        game.play()


class ManualVsRandomSimulation:
    """ Try to defeat a RandomPlayer! """
    def run(self):

        # Creating a manual player

        alice = ManualPlayer(name="Paul Bilokon (Manual)")
        
        # Creating a random player
        bob = RandomPlayer(name="Bob (Random)")

        # Creating and launching the game
        game = Game(player1=alice, player2=bob)
        game.play()


class RandomVsRandomSimulation:
    """ Two RandomPlayers battling it out! Whose will have the better luck? """
    def run(self):
        # Creating two random players
        alice = RandomPlayer(name="Alice (Random)")
        bob = RandomPlayer(name="Bob (Random)")

        # Creating and launching the game
        game = Game(player1=alice, player2=bob)
        game.play()


class ManualVsAutomaticSimulation:
    """ Play against your AI player! """
    def run(self):
        # Creating a manual player with automatically generated board
        board = Board()
        alice = ManualPlayer(board=board, name="Alice (Manual)")
        
        # Creating a manual player
        bob = AutomaticPlayer(name="Bob (Automatic)")

        # Creating and launching the game
        game = Game(player1=alice, player2=bob)
        game.play()


class RandomVsAutomaticSimulation:
    """ A RandomPlayer vs your smarter AI player! """
    def run(self):
        # Creating one random player and one AI player
        alice = RandomPlayer(name="Alice (Random)")
        bob = AutomaticPlayer(name="Bob (Automatic)")

        # Creating and launching the game
        game = Game(player1=alice, player2=bob)
        game.play()


class AutomaticVsAutomaticSimulation:
    """ Get your AI players to battle each other! """
    def run(self):
        # Creating two AI players
        alice = AutomaticPlayer(name="Alice (Automatic)")
        bob = AutomaticPlayer(name="Bob (Automatic)")

        # Creating and launching the game
        game = Game(player1=alice, player2=bob)
        game.play()
