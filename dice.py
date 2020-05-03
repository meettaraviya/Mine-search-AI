from minesweeper import MineSweeper
from player import GreedyPlayer, OptimizedGreedyPlayer

import numpy as np

import argparse
import os

helper_funcs_f = """
fun sum1(a: bool) { if a then int(INT_MAX, 1) else int(INT_MAX, 0) }
fun sum2(a: bool, b: bool) { sum1(a) + sum1(b) }
fun sum3(a: bool, b: bool, c: bool) { sum1(a) + sum2(b, c) }
fun sum4(a: bool, b: bool, c: bool, d: bool) { sum2(a, b) + sum2(c, d) }
fun sum5(a: bool, b: bool, c: bool, d: bool, e: bool) { sum2(a, b) + sum3(c, d, e) }
fun sum6(a: bool, b: bool, c: bool, d: bool, e: bool, f: bool) { sum3(a, b, c) + sum3(d, e, f) }
fun sum7(a: bool, b: bool, c: bool, d: bool, e: bool, f: bool, g: bool) { sum3(a, b, c) + sum4(d, e, f, g) }
fun sum8(a: bool, b: bool, c: bool, d: bool, e: bool, f: bool, g: bool, h: bool) { sum4(a, b, c, d) + sum4(e, f, g, h) }

"""

def to_program_dice(ms: MineSweeper, outvar: str, outfile:str = None):

	INT_MAX = ms.N + 2

	program = helper_funcs_f.replace("INT_MAX", str(INT_MAX))
	# var_names = ""

	prev = None

	for i in range(ms.H):
		for j in range(ms.W):
			program += f"let x_{i}_{j} = flip(0.5) in\n"

			if prev is None:
				program += f"let cnt_{i}_{j} = if x_{i}_{j} then int({INT_MAX}, 1) else int({INT_MAX}, 0) in\n"
				
			else:
				program += f"let cnt_{i}_{j} = if x_{i}_{j} then cnt_{prev[0]}_{prev[1]} + int({INT_MAX}, 1) else cnt_{prev[0]}_{prev[1]} in\n"

			program += f"let _ = observe(cnt_{i}_{j} != int({INT_MAX}, {INT_MAX-1})) in\n"

			prev = i, j

	for i in range(ms.H):
		for j in range(ms.W):
			if ms.revealed[i, j]:
				nbrs = ms.neighbors(i, j)
				func = f"sum{len(nbrs)}"
				func_args = ", ".join([f"x_{ni}_{nj}" for ni, nj in nbrs])

				cnt = int(ms.get(i, j))

				program += f"let _ = observe({func}({func_args}) == int({INT_MAX}, {cnt})) in\n"

	program += f"let _ = observe(cnt_{ms.H-1}_{ms.W-1} == int({INT_MAX}, {ms.N})) in\n"


	program += f"{outvar}\n"

	if outfile is None:
		print(program)

	else:
		with open(outfile, 'w') as out:
			out.write(program)


call_id_dict = {}

def to_probs_dice(ms: MineSweeper):
	call_id = call_id_dict.get(ms.seed, 0)
	probs = np.zeros((ms.H, ms.W))

	for i in range(ms.H):
		for j in range(ms.W):

			if not ms.revealed[i, j]:
			
				fieldfile = f"programs/dice/ms_{ms.seed}_{call_id}.ml"
				codefile = f"programs/dice/ms_{ms.seed}_{call_id}.ml"
				
				to_program_dice(ms, f"x_{i}_{j}", outfile=codefile)
				output = os.popen(f"bin/Dice.native {codefile}").read()
				try:
					prob = float(output.split("\n")[1].split("\t")[1])
				except Exception:
					print(f"Cannot parse output of dice when run on {codefile}.")
					exit(1)
				probs[i, j] = prob

				call_id += 1

	call_id_dict[ms.seed] = call_id
	return probs # return probabilities of having a mine


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Solve MineSweeper using DICE.')
	parser.add_argument('mine_count', metavar='N', type=int, help='Number of mines.')
	parser.add_argument('width', metavar='W', type=int, help='Minefield width.')
	parser.add_argument('height', metavar='H', type=int, help='Minefield height.')
	parser.add_argument('--game_count', metavar='G', type=int, help='Number of games.', default=1)
	parser.add_argument('--player', type=str, help="Player's algorithm.", choices=["GreedyPlayer", "OptimizedGreedyPlayer"], default="OptimizedGreedyPlayer")


	args = parser.parse_args()
	N, H, W = args.mine_count, args.height, args.width
	
	Player = globals()[args.player]
	player = Player(to_probs_dice)

	n_won = 0

	for seed in range(args.game_count):
		ms = MineSweeper(N, H, W, seed=seed)
		result = player.play(ms, debug=True)

		n_won += result

	print(f"\n-"+"------"*W+"\n")
	print(f"\nAI won {n_won}/{args.game_count} games.")
