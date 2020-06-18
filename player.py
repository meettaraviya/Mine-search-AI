from minesweeper import MineSweeper

import numpy as np


class Player:  # interface for a player
    def __init__(self, to_probs):  # both should be functions like in dice.py
        self.to_probs = to_probs

    def play(self, ms: MineSweeper, debug: bool = False):

        raise NotImplementedError


class GreedyPlayer(Player):
    """For each move, calculate the distribution and make the move corresponding to the position with minimum probability of having a mine"""


    def play(self, ms: MineSweeper, debug: bool = False):

        prev_square = None

        max_score = ms.H * ms.W - ms.N

        while ms.score < max_score and not ms.game_over:

            if debug:
                print(f"Score: {ms.score}\n")
                print("Game grid:\n")
                ms.print()

            probs = self.to_probs(ms)

            if debug:
                print("Mine distribution:\n")
                out = ""

                for i in range(ms.H):
                    for j in range(ms.W):
                        out += f"|{probs[i, j]:.3f}"

                    out += "|\n"

                print(out)

            mi, mj = probs.argmax()//ms.W, probs.argmax() % ms.W

            for i in range(ms.H):
                for j in range(ms.W):
                    if not ms.revealed[i, j] and probs[i, j] < probs[mi, mj]:
                        mi, mj = i, j

            # if probs[mi, mj] == 0:
            #     prev_square = "#"
            #     moves = []

            #     for mi_, mj_ in zip(*np.where(probs == 0)):
            #         if not ms.revealed[mi_, mj_]:
            #             moves.append((mi_, mj_))

            # else:
            moves = [(mi, mj)]

            if debug:
                print(f"Moves = {moves}")
                print("\n-" + "------"*ms.W+"\n")

            for i, j in moves:
                prev_square = ms.reveal(i, j)

                if ms.game_over:
                    break



        
        if debug:
            print("Final game grid:\n")
            ms.print()

        if ms.game_over:
            if debug:
                print("BOOM!! GAME OVER.")
                print()
                print(f"Score = {ms.score}")
            return False, ms.score

        else:
            if debug:
                print("AI WINS!")
                print(f"Score = {ms.score}")
            return True, ms.score


class OptimizedGreedyPlayer(Player):
    """For each move, calculate the distribution and make the move corresponding to the position with minimum probability of having a mine"""
    """If there are locations with probability zero, reveal all of them one by one"""

    def play(self, ms: MineSweeper, debug: bool = False):

        prev_square = None

        max_score = ms.H * ms.W - ms.N

        while ms.score < max_score and not ms.game_over:

            if debug:
                print(f"Score: {ms.score}\n")
                print("Game grid:\n")
                ms.print()

            probs = self.to_probs(ms)

            if debug:
                print("Mine distribution:\n")
                out = ""

                for i in range(ms.H):
                    for j in range(ms.W):
                        out += f"|{probs[i, j]:.3f}"

                    out += "|\n"

                print(out)

            mi, mj = probs.argmax()//ms.W, probs.argmax() % ms.W

            for i in range(ms.H):
                for j in range(ms.W):
                    if not ms.revealed[i, j] and probs[i, j] < probs[mi, mj]:
                        mi, mj = i, j

            if probs[mi, mj] == 0:
                prev_square = "#"
                moves = []

                for mi_, mj_ in zip(*np.where(probs == 0)):
                    if not ms.revealed[mi_, mj_]:
                        moves.append((mi_, mj_))

            else:
                moves = [(mi, mj)]

            if debug:
                print(f"Moves = {moves}")
                print("\n-" + "------"*ms.W+"\n")

            for i, j in moves:
                prev_square = ms.reveal(i, j)

                if ms.game_over:
                    break



        
        if debug:
            print("Final game grid:\n")
            ms.print()

        if ms.game_over:
            if debug:
                print("BOOM!! GAME OVER.")
                print()
                print(f"Score = {ms.score}")
            return False, ms.score

        else:
            if debug:
                print("AI WINS!")
                print(f"Score = {ms.score}")
            return True, ms.score
