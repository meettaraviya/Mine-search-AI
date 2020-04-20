import argparse

parser = argparse.ArgumentParser(
    description='Generate DICE program for minesweeper.')
parser.add_argument('count', metavar='N', type=int,
                    help='Number of mines.')
parser.add_argument('width', metavar='W', type=int,
                    help='Minefield width.')
parser.add_argument('height', metavar='H', type=int,
                    help='Minefield height.')


args = parser.parse_args()
N, W, H = args.count, args.width, args.height

