from PIL import Image
import numpy as np
import scipy.signal as ss


class MineSweeper:

    ICONS = np.array(Image.open('res/squares.bmp').convert('RGB'))

    def __init__(self, N: int, H: int, W: int, seed: int = None):

        self.N, self.H, self.W = N, H, W
        
        if seed is None:
            seed = np.random.randint(2**32)

        np.random.seed(seed)
        self.seed = seed

        locs = np.random.choice(H*W, N, False)
        self.__field = np.zeros(H*W, dtype=bool)
        self.__field[locs] = True
        self.__field = self.__field.reshape(H, W)

        self.revealed = np.zeros((H, W), dtype=bool)

        self.__counts = (ss.convolve2d(self.__field, np.ones((3, 3)), mode='same') - self.__field).astype(int)


    @staticmethod
    def beginner(seed: int = None):
        return MineSweeper(10, 9, 9, seed=seed)

    @staticmethod
    def intermediate(seed: int = None):
        return MineSweeper(40, 16, 16, seed=seed)

    @staticmethod
    def expert(seed: int = None):
        return MineSweeper(99, 16, 30, seed=seed)

    @staticmethod
    def from_file(infile: str, validate: bool = True):
        with open(infile) as inp:

            field = []
            revealed = []
            given_counts = []

            for line in inp.readlines():
                syms = line.split('|')[1:-1]

                field.append([])
                revealed.append([])
                given_counts.append([])

                for sym in syms:
                    revealed[-1].append(sym in "@X012345678.")

                    if sym in "@O":
                        field[-1].append(True)
                    elif revealed[-1][-1]:
                        field[-1].append(False)
                    else:
                        field[-1].append(None)

                    if sym in "012345678":
                        given_counts[-1].append(int(sym))
                    else:
                        given_counts[-1].append(None)

        ms = MineSweeper.__new__(MineSweeper)
        ms.__field = np.array(field).astype(bool)
        ms.N = ms.__field.sum()
        ms.H, ms.W = ms.__field.shape

        ms.revealed = np.array(revealed)

        calc_counts = (ss.convolve2d(ms.__field, np.ones((3, 3)), mode='same') - ms.__field).astype(int)

        if validate:
            assert ((calc_counts == given_counts) | np.equal(given_counts, None)).all(), "Invalid field"
            assert (ms.__field & ms.revealed).sum() <= 1, "More than one mines clicked on"

        ms.__counts = calc_counts

        return ms

    def __str__(self):
        out = ""

        for i in range(self.H):
            for j in range(self.W):
                out += f"|{self.get(i, j)}"

            out += "|\n"

        return out

    def neighbors(self, i:int, j:int):
        nbrs = []

        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if 0 <= i + di < self.H and 0 <= j + dj < self.W and (di != 0 or dj != 0):
                    nbrs.append((i + di, j + dj))

        return nbrs

    def print(self, outfile: str = None):

        if outfile is None:
            print(str(self))

        else:
            with open(outfile, 'w') as out:
                out.write(str(self))

    def get(self, y: int, x: int):
        if self.revealed[y, x]:
            if self.__field[y, x]:
                return "@"
            else:
                return str(self.__counts[y, x])
        else:
            return " "

    def draw(self, outfile: str = None):
        img = np.zeros((self.H*16, self.W*16, 3), dtype=np.uint8)

        for i in range(self.H):
            for j in range(self.W):
                if not self.revealed[i][j]:
                    k = 0
                elif self.__field[i][j]:
                    k = 4
                else:
                    k = 15 - self.__counts[i][j]

                img[i*16:(i+1)*16, j*16:(j+1)*16, :] = MineSweeper.ICONS[k*16:(k+1)*16, :, :]

        if outfile is None:
            Image.fromarray(img).show()

        else:
            Image.fromarray(img).save(outfile)

    def reveal(self, y: int, x: int):
        self.revealed[y, x] = True
        return self.get(y, x)


if __name__ == '__main__':
    ms = MineSweeper.from_file('eg.field')
    ms.draw()
