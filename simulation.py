from board import Board
from game import Game
from player import ManualPlayer, AlphaBetaPlayer, MiniMaxPlayer

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


class ManualVsAlphaBetaSimulation:
    """ Play against your AI player! """
    def run(self):
        # Creating a manual player with automatically generated board
        board = Board()
        alice = ManualPlayer(board=board, name="Alice (Manual)")
        
        # Creating a manual player
        bob = AlphaBetaPlayer(name="Bob (Automatic)")

        # Creating and launching the game
        game = Game(player1=alice, player2=bob)
        game.play()


class ManualVsMiniMaxSimulation:
    """ Play against your AI player! """
    def run(self):
        # Creating a manual player with automatically generated board
        board = Board()
        alice = ManualPlayer(board=board, name="Alice (Manual)")
        
        # Creating a manual player
        bob = MiniMaxPlayer(name="Bob (Automatic)")

        # Creating and launching the game
        game = Game(player1=alice, player2=bob)
        game.play() 


class AutomaticVsAutomaticSimulation:
    """ Get your AI players to battle each other! """
    def run(self):
        # Creating two AI players
        alice = AlphaBetaPlayer(name="Bob (Automatic)")
        bob = AlphaBetaPlayer(name="Alice (Automatic)")

        # Creating and launching the game
        game = Game(player1=alice, player2=bob)
        game.play()
