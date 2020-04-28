from PIL import Image
import numpy as np
import argparse

img = Image.open('squares.bmp').convert('RGB')
img_data = np.array(img)

icon_map = {
	"0": 15,
	"1": 14,
	"2": 13,
	"3": 12,
	"4": 11,
	"5": 10,
	"6": 9,
	"7": 8,
	"8": 7,
	" ": 0,
	"F": 1,
	"?": 2,
	"@": 3,
	"X": 4,
	"O": 5,
	"!": 6
}




def draw(field, show=True, outfile=None):
	img = np.zeros((len(field)*16,len(field[0])*16, 3), dtype=np.uint8)

	H = len(field)
	W = len(field[0])

	for i in range(H):
		for j in range(W):
			k = icon_map[field[i][j]]
			img[i*16:(i+1)*16, j*16:(j+1)*16, :] = img_data[k*16:(k+1)*16, :, :]

	if show:
		Image.fromarray(img).show()

	if outfile is not None:
		# import scipy.misc
		# scipy.misc.imsave(outfile, img)
		Image.fromarray(img).save(outfile)




if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Generate DICE program for minesweeper.')
	parser.add_argument("--infile", type=argparse.FileType('r'), default=None)
	parser.add_argument("--show", type=bool, default=True)
	parser.add_argument("--outfile", type=argparse.FileType('w'), default=None)

	args = parser.parse_args()

	if args.infile is None:

		field = [
			"    ",
			" 22 ",
			" 22 ",
			"    ",
		]

	else:

		field = [line.strip('\n') for line in args.infile.readlines()]

	draw(field, outfile=args.outfile, show=args.show)
