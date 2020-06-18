from minesweeper import MineSweeper
from player import GreedyPlayer, OptimizedGreedyPlayer

import numpy as np

import argparse
import os

def states_to_string(state_array):
	string = "{\n\tstates = ( "
	for s in state_array:
		string += '"' + str(s) + '"' + " "
	string += ");\n}\n"
	return string

def recursive(values):
	if len(values) == 1:
		string = "("
		for v in values[0]:
			string += str(v) + " "
		return string + ")"
	else:
		mid = int(len(values)/2)
		string = "("
		string += recursive(values[:mid]) 
		string += recursive(values[mid:]) + ")" 
		return string


def draw_network(H: int, W: int, mines:int, network_file):
	X = []
	X_dict = {}
	X_states = [0,1]
	X_states_string = states_to_string(X_states)
	C = []
	upper_limit = mines + 1
	C_states = list(range(upper_limit + 1))
	C_states_string = states_to_string(C_states)
	N = []
	N_states = list(range(9))
	N_states_string = states_to_string(N_states)
	for i in range(H):
		for j in range(W):
			x_var_name = "X_" + str(i) + "_" + str(j)
			c_var_name = "C_" + str(i) + "_" + str(j)
			n_var_name = "N_" + str(i) + "_" + str(j)
			X_dict[x_var_name] = True
			X.append(x_var_name)
			C.append(c_var_name)
			N.append(n_var_name)
	with open(network_file, "w") as f1:
		f1.write("net\n{\n}\n")
		for x in X:
			f1.write("node " + x + "\n")
			f1.write(X_states_string)
		for c in C:
			f1.write("node " + c + "\n")
			f1.write(C_states_string)
		for n in N:
			f1.write("node " + n + "\n")
			f1.write(N_states_string)
		for x in X:
			t = " ( 0.5 0.5 );\n}\n"
			f1.write("potential ( " + str(x) + " )\n{\n" )
			f1.write("\tdata =" + t)
		for idx,c in enumerate(C):
			if idx == 0:
				f1.write("potential ( C_0_0 | X_0_0)\n{\n\t")
				f1.write("data = ")
				arr_0 = [0] * len(C_states)
				arr_0[0] = 1
				arr_1 = [0] * len(C_states)
				arr_1[1] = 1
				temp = "(("
				for t in arr_0:
					temp += str(t) + " "
				temp += ")("
				for t in arr_1:
					temp += str(t) + " "
				temp += "));\n}\n"
				f1.write(temp)
			else:
				f1.write("potential ( " + c + " | " + X[idx] + " " + C[idx-1] + " )\n{\n\tdata = ")
				string = "("
				for i in [0,1]:
					string += "("
					for j in C_states:
						s = i + j
						arr = [0] * len(C_states)
						if s >= len(C_states):
							arr[-1] = 1
						else:
							arr[s] = 1
						string += "( "
						for a in arr:
							string += str(a) + " "
						string += ")"
					string += ")"
				string += ");\n"
				f1.write(string)
				f1.write("}\n")
		for idx,n in enumerate(N):
			h = int(n.split("_")[1])
			w = int(n.split("_")[2])
			possible_neighbors = [(h-1,w), (h+1, w), (h, w+1), (h, w-1), (h-1, w-1), (h-1, w+1), (h+1, w-1), (h+1, w+1)]
			neighbors = []
			for p in possible_neighbors:
				if p[0] < 0 or p[1] < 0:
					continue
				elif p[0] >= H or p[1] >= W:
					continue
				else:
					neighbors.append("X_" + str(p[0]) + "_" + str(p[1]))
			f1.write("potential ( " + n + " |")
			neighbor_string = ""
			for neighbor in neighbors:
				neighbor_string += " " + neighbor
			neighbor_string += " " + ")\n{\n\tdata = "
			f1.write(neighbor_string)
			total = 2 ** len(neighbors)
			binary = []
			for i in range(total):
				binary.append("{0:b}".format(i))
			sums = []
			for b in binary:
				s = sum(int(digit) for digit in str(b))
				sums.append(s)
			values = []
			for s in sums:
				arr = [0] * 9
				arr[s] = 1
				values.append(arr)
			string = recursive(values)
			f1.write(string)
			f1.write(";\n}\n")

#draw_network(8, 8, 10, "minesweeper.net")




