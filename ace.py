from minesweeper import MineSweeper
from player import GreedyPlayer, OptimizedGreedyPlayer

import numpy as np
import argparse
import os
import time
import board_net

def write_to_xml(N_evidence, X_evidence, C_evidence, query, outfile):
	with open(outfile, "w") as f1:
		f1.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		f1.write('<instantiation date="Jun 4, 2005 7:07:21 AM">\n')
		for n in N_evidence:
			string = '<inst id=' + '"' + str(n) + '"' + ' value=' + '"' + str(N_evidence[n]) + '"' + '/>\n'
			f1.write(string)
		for x in X_evidence:
			string = '<inst id=' + '"' + str(x) + '"' + ' value=' + '"' + str(X_evidence[x])+ '"'  + '/>\n'
			f1.write(string)
		for c in C_evidence:
			string = '<inst id=' + '"' + str(c)+ '"'  + ' value=' + '"' + str(C_evidence[c])+ '"'  + '/>\n'
			f1.write(string)
		for q in query:
			string = '<inst id=' + '"' + str(q)+ '"'  + ' value=' + '"' + str(query[q])+ '"'  + '/>\n'
			f1.write(string)
		f1.write("</instantiation>")
	#with open(outfile, "r") as f2:
	#	print(f2.read())

def ace_get_probabilities(ms: MineSweeper):
	outfile = "bayes_net/minesweeper.inst"
	probs = np.zeros((ms.H, ms.W))
	N_evidence = {}
	X_evidence = {}
	for i in range(ms.H):
		for j in range(ms.W):
			if ms.revealed[i, j]:
				face_value = int(ms.get(i, j))
				var_name = "N_" + str(i) + "_" + str(j)
				N_evidence[var_name] = face_value
				var_name = "X_" + str(i) + "_" + str(j)
				X_evidence[var_name] = 0
	c_var_name = "C_" + str(ms.H - 1) + "_" + str(ms.W - 1)
	C_evidence = {c_var_name:ms.N}
	query = {}
	for i in range(ms.H):
		for j in range(ms.W):
			if not ms.revealed[i, j]:
				query_var_name = "X_" + str(i) + "_" + str(j)
				query = {query_var_name:1}
				write_to_xml(N_evidence, X_evidence, C_evidence, query, outfile)
				command = 'bin/evaluate ' + 'bayes_net/minesweeper.net ' + outfile
				#print(command)
				stream = os.popen(command)
				stream = stream.readlines()
				#print(stream)
				prob = float(stream[0].split("=")[1])
				probs[i, j] = prob
	return probs




if __name__ == '__main__':

        parser = argparse.ArgumentParser(description='Solve MineSweeper using DICE.')
        parser.add_argument('mine_count', metavar='N', type=int, help='Number of mines.')
        parser.add_argument('width', metavar='W', type=int, help='Minefield width.')
        parser.add_argument('height', metavar='H', type=int, help='Minefield height.')
        parser.add_argument('--game_count', metavar='G', type=int, help='Number of games.', default=1)
        parser.add_argument('--player', type=str, help="Player's algorithm.", choices=["GreedyPlayer", "OptimizedGreedyPlayer"], default="OptimizedGreedyPlayer")
        parser.add_argument('--seed', type=int, help="Seed for RNG.", default=np.random.randint(100))


        args = parser.parse_args()
        N, H, W = args.mine_count, args.height, args.width

        board_net.draw_network(H, W, N, "bayes_net/minesweeper.net")
        os.system("bin/compile bayes_net/minesweeper.net")

        Player = globals()[args.player]
        player = Player(ace_get_probabilities)

        n_won = 0

        np.random.seed(args.seed)

        scores = []
        start_time = time.time()

        for game_id in range(args.game_count):
                print(f"\n-"+"------"*W+"\n")
                print(f"GAME #{game_id+1}")
                print(f"\n-"+"------"*W+"\n")

                ms = MineSweeper(N, H, W)
                result, score = player.play(ms, debug=True)

                n_won += result
                scores.append(score)

        end_time = time.time()


        print(f"\n-"+"------"*W+"\n")
        print(f"\nAI won {n_won}/{args.game_count} games.")
        print(f"\nAverage score: {np.mean(scores):.2f}.")
        print(f"\nAverage time taken: {(end_time - start_time)/args.game_count} seconds.")
