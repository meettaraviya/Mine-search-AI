from minesweeper import MineSweeper, WindowsMineSweeper
from player import GreedyPlayer, OptimizedGreedyPlayer

import numpy as np

import argparse
import os

import time


helper_funcs_f = """
sum2(S, Q, F) :- tile(A,S), tile(B,Q), F is A+B.
sum3(S, Q, W, F) :- tile(A,S), tile(B,Q),  tile(C,W), F is A+B+C.
sum4(S, Q, W, Y, F) :- tile(A,S), tile(B,Q),  tile(C,W), tile(D, Y), F is A+B+C+D.
sum5(S, Q, W, Y, Z, F) :- tile(A,S), tile(B,Q),  tile(C,W), tile(D, Y), tile(E, Z), F is A+B+C+D+E.
sum6(S, Q, W, Y, Z, P, F) :- tile(A,S), tile(B,Q),  tile(C,W), tile(D, Y), tile(E, Z), tile(G, P), F is A+B+C+D+E+G.
sum7(S, Q, W, Y, Z, P, R, F) :- tile(A,S), tile(B,Q),  tile(C,W), tile(D, Y), tile(E, Z), tile(G, P), tile(H, R), F is A+B+C+D+E+G+H.
sum8(S, Q, W, Y, Z, P, R, U, F) :- tile(A,S), tile(B,Q),  tile(C,W), tile(D, Y), tile(E, Z), tile(G, P), tile(H, R), tile(I, U), F is A+B+C+D+E+G+H+I.
"""

call_id_dict = {}
def to_probs_problog(ms: MineSweeper):

	INT_MAX = ms.N

	prev = None
	program = f"0.5::tile(0,D); 0.5::tile(1,D) :- tile(D).\n"
	for i in range(ms.H):
		for j in range(ms.W):
			# print(ms.H)
			program += f"tile(x_{i}_{j}).\n"
	chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	program += f"rule :- "
	k = 0
	for i in range(ms.H):
		for j in range(ms.W):

			program += f"tile({chars[k]}, x_{i}_{j}), "
			k = k + 1
	program += f"{INT_MAX} is "
	for i in range(k):
		if i > 0:
			program += f" + "
		program += f"{chars[i]}"
	program += f".\n"

	program += f"result(S) :- tile(A, S), 1 is A.\n"
	program += helper_funcs_f
	program += f"evidence(rule,true).\n"


	for i in range(ms.H):
		for j in range(ms.W):
			if ms.revealed[i, j]:
				nbrs = ms.neighbors(i, j)
				print(nbrs)
				func = f"sum{len(nbrs)}"
				func_args = ", ".join([f"x_{ni}_{nj}" for ni, nj in nbrs])

				cnt = int(ms.get(i, j))
				program += f"evidence({func}({func_args}, {cnt}), true).\n"


	for i in range(ms.H):
		for j in range(ms.W):
			program += f"query(result(x_{i}_{j})).\n"

	call_id = call_id_dict.get(ms.seed, 0)
	codefile = f"ms_{ms.seed}_{call_id}.problog"
	call_id_dict[ms.seed] = call_id + 1


	with open(codefile, 'w') as out:
		out.write(program)

	try:

		output = os.popen(f"problog {codefile}").read()
		output = output[:-1]

		probs = [float(w.split("\t")[1]) for w in output.split("\n")]
		probs = np.array(probs).reshape(ms.H, ms.W)

		return probs

	except Exception:
		print(f"Cannot parse output of problog when run on {codefile}.")
		exit(1)



if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Solve MineSweeper using DICE.')
	parser.add_argument('mine_count', metavar='N', type=int, help='Number of mines.')
	parser.add_argument('width', metavar='W', type=int, help='Minefield width.')
	parser.add_argument('height', metavar='H', type=int, help='Minefield height.')
	parser.add_argument('--game_count', metavar='G', type=int, help='Number of games.', default=1)
	parser.add_argument('--player', type=str, help="Player's algorithm.", choices=["greedy", "optimized_greedy"], default="optimized_greedy")
	parser.add_argument('--seed', type=int, help="Seed for RNG.", default=np.random.randint(100))
	parser.add_argument('--variant', type=str, help="Game variant.", default="simple", choices=["windows", "simple"])


	args = parser.parse_args()
	N, H, W = args.mine_count, args.height, args.width
	
	# Player = globals()[args.player]
	if args.player == "greedy":
		Player = GreedyPlayer
	elif args.player == "optimized_greedy":
		Player = OptimizedGreedyPlayer

	if args.variant == "simple":
		Variant = MineSweeper
	elif args.variant == "windows":
		Variant = WindowsMineSweeper

	player = Player(to_probs_problog)

	n_won = 0

	np.random.seed(args.seed)

	scores = []
	start_time = time.time()

	for game_id in range(args.game_count):
		print(f"\n-"+"------"*W+"\n")
		print(f"GAME #{game_id+1}")
		print(f"\n-"+"------"*W+"\n")

		ms = Variant(N, H, W)
		# ms = MineSweeper(N, H, W)
		result, score = player.play(ms, debug=True)

		n_won += result
		scores.append(score)

	end_time = time.time()


	print(f"\n-"+"------"*W+"\n")
	print(f"\nAI won {n_won}/{args.game_count} games.")
	print(f"\nAverage score: {np.mean(scores):.2f}.")
	print(f"\nAverage time taken: {(end_time - start_time)/args.game_count} seconds.")
