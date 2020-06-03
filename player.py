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

        for n_safe_left in range(ms.H*ms.W-ms.N, 0, -1):

            if debug:
                print(f"Safe spots left: {n_safe_left}\n")
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

            if debug:
                print(f"Move = {mi}, {mj}")
                print("\n-" + "------"*ms.W+"\n")

            prev_square = ms.reveal(mi, mj)

            if prev_square == "@":
                break

        if debug:
            print("Final game grid:\n")
            ms.print()

            if prev_square == "@":
                print("BOOM!! GAME OVER.")
                print()
                print(f"Number of safe places left = {n_safe_left}")
                print(f"Score = {ms.W*ms.H-ms.N-n_safe_left}")
                return False

            else:
                print("AI WINS!")
                print(f"Score = {ms.W*ms.H-ms.N-n_safe_left}")
                return True


class OptimizedGreedyPlayer(Player):
    """For each move, calculate the distribution and make the move corresponding to the position with minimum probability of having a mine"""
    """If there are locations with probability zero, reveal all of them one by one"""

    def play(self, ms: MineSweeper, debug: bool = False):

        prev_square = None

        n_safe_left = ms.H*ms.W - ms.N

        while n_safe_left > 0 and prev_square != "@":

            if debug:
                print(f"Safe spots left: {n_safe_left}\n")
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

                if prev_square == "@":
                    break

                n_safe_left -= 1

        score = ms.W*ms.H-ms.N-n_safe_left
        
        if debug:
            print("Final game grid:\n")
            ms.print()

        if prev_square == "@":
            if debug:
                print("BOOM!! GAME OVER.")
                print()
                print(f"Number of safe places left = {n_safe_left}")
                print(f"Score = {score}")
            return False, score

        else:
            if debug:
                print("AI WINS!")
                print(f"Score = {score}")
            return True, score
