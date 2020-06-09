from minesweeper import MineSweeper
from player import GreedyPlayer, OptimizedGreedyPlayer

import numpy as np

import argparse
import os

def get_basic_figaro(ms: MineSweeper, name):
	out="import com.cra.figaro.algorithm.factored._\nimport com.cra.figaro.algorithm.sampling._\nimport com.cra.figaro.language._\nimport com.cra.figaro.library.compound._\n"
	out+="\n"
	out+=f"object {name}"+"{\n"
	out += f"private val count_init = Constant(0)\n"
	prev = "init"
	algo_arguments = ""
	for i in range(ms.H):
		for j in range(ms.W):
			out+=f"private val x_{i}_{j} = Select(0.5->1,0.5->0)\n"
			out+= f"private val count_{i}_{j} = If(x_{i}_{j}===1,Apply(count_{prev}, (i: Int) => i+1),count_{prev})\n"
			prev = f"{i}_{j}"
			algo_arguments+=f"x_{i}_{j},"

	out+="def main(args: Array[String]){\n\n"
	algo_arguments = algo_arguments[:-1]+")\n"
	out+="val alg = VariableElimination("+algo_arguments
	#out+="val alg = Importance(25,"+algo_arguments
	out+=f"count_{ms.H-1}_{ms.W-1}.observe({ms.N})\n"
	return out

def neighbors_constrain_figaro(ms: MineSweeper, nbrs, h, w, count):
	prev = f"{h}_{w}_init"
	out = f"val nbr_{prev} = Constant(0)\n"
	for i in range(len(nbrs)):
		y,x = nbrs[i]
		out+=f"val nbr_{h}_{w}_{i} = If(x_{y}_{x}===1,Apply(nbr_{prev}, (i: Int) => i+1),nbr_{prev})\n"
		prev=f"{h}_{w}_{i}"
	val = len(nbrs)-1
	out+=f"nbr_{h}_{w}_{val}.observe({count})\n"
	return out

def to_program_figaro(ms: MineSweeper, name,outfile = None):
	out = get_basic_figaro(ms, name)
	end = ""
	for i in range(ms.H):
		for j in range(ms.W):
			if ms.revealed[i, j]:
				out+=f"x_{i}_{j}.observe(0)\n"
				nbrs = ms.neighbors(i, j)
				count = int(ms.get(i, j))
				out += neighbors_constrain_figaro(ms, nbrs, i, j, count)
			end+=f"println(alg.probability(x_{i}_{j},1))\n"


	out+="alg.start()\n"
	out+=end
	out+="alg.kill()\n"
	out+="}\n}"
	if outfile is None:
		print(out)

	else:
		with open(outfile, 'w') as result:
			result.write(out)


call_id_dict = {}

def to_probs_figaro(ms: MineSweeper):

	call_id = call_id_dict.get(ms.seed, 0)
	probs = np.zeros((ms.H, ms.W))
	print()
	codefile = f"src/main/scala/test_run/ms_{ms.seed}_{call_id}.scala"
	codefilerun = f"'runMain ms_{ms.seed}_{call_id}'"
	name = f"ms_{ms.seed}_{call_id}"
	to_program_figaro(ms, name, outfile = codefile)
	output = os.popen(f"sbt {codefilerun}").read()
	try:
		prob = output.split("\n")[5:]
		prob = prob[:-2]
		count=0
		for i in range(ms.H):
			for j in range(ms.W):
				val = prob[count]
				probs[i,j] = float(val)
				#print(float(val))
				count+=1
	except Exception:
		print(f"Cannot parse output of figaro when run on {codefile}.")
		print(output)
		exit(1)
	call_id+=1
	call_id_dict[ms.seed] = call_id
	return probs

if __name__ == '__main__':


	parser = argparse.ArgumentParser(description='Solve MineSweeper using Figaro.')
	parser.add_argument('mine_count', metavar='N', type=int, help='Number of mines.')
	parser.add_argument('width', metavar='W', type=int, help='Minefield width.')
	parser.add_argument('height', metavar='H', type=int, help='Minefield height.')
	parser.add_argument('--game_count', metavar='G', type=int, help='Number of games.', default=1)
	parser.add_argument('--player', type=str, help="Player's algorithm.", choices=["GreedyPlayer", "OptimizedGreedyPlayer"], default="OptimizedGreedyPlayer")


	args = parser.parse_args()
	N, H, W = args.mine_count, args.height, args.width

	Player = globals()[args.player]
	player = Player(to_probs_figaro)

	n_won = 0

	for seed in range(args.game_count):
		print(f"\n-"+"------"*W+"\n")
		print(f"GAME #{seed+1}")
		print(f"\n-"+"------"*W+"\n")
		ms = MineSweeper(N, H, W, seed=seed)
		result = player.play(ms, debug=True)
		n_won += result

	print(f"\n-"+"------"*W+"\n")
	print(f"\nAI won {n_won}/{args.game_count} games.")
