import argparse
from minesweeper import MineSweeper
import os


def to_program(ms: MineSweeper, outfile:str = None):
	program = ""

	if outfile is None:
		print(program)

	else:
		with open(outfile, 'w') as out:
			out.write(program)


def compile(ms: MineSweeper, field_id:int = 0, call_id:int = 0):
	codefile = f"programs/dice/ms_{field_id}_{call_id}.dice"
	os.system(f"bin/Dice.native {infile}")


	return np.zeros(ms.H, ms.W) # return probabilities of having a mine

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Generate DICE program for minesweeper.')
	parser.add_argument('count', metavar='N', type=int, help='Number of mines.')
	parser.add_argument('width', metavar='W', type=int, help='Minefield width.')
	parser.add_argument('height', metavar='H', type=int, help='Minefield height.')
	parser.add_argument('--outfile', type=int, help='Output file.')


	args = parser.parse_args()
	N, H, W = args.count, args.height, args.width
