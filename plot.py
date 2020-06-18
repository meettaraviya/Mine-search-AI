import numpy as np


avgtime = {}
avgtime["windows"] = np.genfromtxt("avgtimewindows.txt", delimiter=",")
avgtime["simple"] = np.genfromtxt("avgtimesimple.txt", delimiter=",")


avgscore = {}
avgscore["windows"] = np.genfromtxt("avgscorewindows.txt", delimiter=",")
avgscore["simple"] = np.genfromtxt("avgscoresimple.txt", delimiter=",")


avgwin = {}
avgwin["windows"] = np.genfromtxt("avgwinwindows.txt", delimiter=",")
avgwin["simple"] = np.genfromtxt("avgwinsimple.txt", delimiter=",")