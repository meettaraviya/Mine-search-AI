import numpy as np

def valid(i, j, H, W):
	return 0<=i<H and 0<=j<W 

def generate(N, H, W):
	locs = set(np.random.choice(W*H, N, False))
	field = [[0 for _i in range(W)] for _j in range(H)]

	for i in range(H):
		for j in range(W):
			if i*W + j in locs:
				field[i][j] = "O"

	print(field)
	for i in range(H):
		for j in range(W):

			if field[i][j] != 'O':
				count = 0

				for di in range(-1, 2):
					for dj in range(-1, 2):
						count += valid(i+di, j+dj, H, W) and field[i+di][j+dj]=='O'

				field[i][j] = str(count)

	print(field)
	return field


