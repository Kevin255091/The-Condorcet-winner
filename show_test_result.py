import os
from matplotlib import pyplot as plt
import numpy as np
import sys
import time

def drawPlot():
    plt.axis('on')
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()

if len(sys.argv) != 2:
	print ('Usage : python show_test_result.py <result_file>')
	sys.exit(0)

os.chdir(os.getcwd())
filename = sys.argv[1]

with open(filename) as f:
    v_num, f_num = [int(x) for x in f.readline().split()]
    v_pos = [float(x) for x in f.readline().split()]
    f_pos = [float(x) for x in f.readline().split()]
    comm_size = [int(x) for x in f.readline().split()]
    b_voter = []
    t_voter = []
    base    = 1
    for i in range(len(comm_size)):
        b_voter.append(base)
        t_voter.append(base + comm_size[i] - 1)
        base += comm_size[i]

    j = 0
    h = 0
    shifted_f_pos = []
    left_v = []
    right_v = []
    overlap = []

    line = f.readline().rstrip('\n')
    if line == "It is not envy-free." :
        result = "nonEnvyFree"
        voter_index, facility_index = (int(x) for x in f.readline().split())
    if line == "It is a Condorcet Winner." :
        result = "CondorcetWinner"
    if line == "It is not a Condorcet Winner." :
        result = "simpleRival"
        max_margin = int(f.readline())
        j, h = (int(x) for x in f.readline().split())
        count = h-j+1
        i = 0
        for line in f:
            tmp = line.split()
            shifted_f_pos.append(float(tmp[0]))
            left_v.append(int(tmp[1]))
            right_v.append(int(tmp[2]))
            overlap.append(int(tmp[3]))
            i = i+1
            if i == count:
                break

min_pos = v_pos[0]
max_pos = v_pos[0]

for pos in v_pos :
    if pos < min_pos:
        min_pos = pos
    if pos > max_pos:
        max_pos = pos

for pos in f_pos :
    if pos < min_pos:
        min_pos = pos
    if pos > max_pos:
        max_pos = pos

borders = []
for i in range(len(f_pos)-1) :
    borders.append((v_pos[t_voter[i]-1]+v_pos[b_voter[i+1]-1])/2)
 
plt.hlines(0, min_pos-1, max_pos+1)  # Draw a horizontal line
plt.xlim(min_pos-1, max_pos+1)
plt.ylim(-6,10)

y1 = np.zeros(np.shape(v_pos))   # Make all y values the same
y2 = np.zeros(np.shape(f_pos))
y3 = np.zeros(np.shape(borders))

plt.plot(v_pos, y1, '.', ms=25, color='k')
plt.plot(borders, y3, '|', ms=25, color='k')

overhang = 0.8
arrow_params = {'overhang':overhang}
for x in f_pos:
    plt.arrow(x, -3, 0, 2.3, head_width=0.08, head_length=0.3, fc='k', ec='k', **arrow_params)

if result == "CondorcetWinner" :
    plt.text(3, 9, 'It is a Condorcet Winner.', fontsize=16)
    drawPlot()
    sys.exit(0)

if result == "nonEnvyFree" :
    plt.text(3, 9, 'It is not envy-free.', fontsize=16)
    plt.text(3, 8, 'The voter at sky blue circle prefers to facility pointed by orange arrow.', fontsize=16)
    plt.plot(v_pos[voter_index-1], 0, '.', ms=25, color='xkcd:sky blue')
    plt.arrow(f_pos[facility_index-1], -3, 0, 2.3, head_width=0.08, head_length=0.3, fc='tab:orange', ec='tab:orange', **arrow_params)
    drawPlot()
    sys.exit(0)

y4 = np.zeros(np.shape(shifted_f_pos))

for i in range(len(f_pos)) :
    if i+1 >= j and i+1 <= h :
        change_voters_pos = v_pos[b_voter[i]-1 : t_voter[i]]
        y5 = np.zeros(np.shape(change_voters_pos))
        plt.plot(change_voters_pos, y5, '.', ms=25, color='tab:orange')

for x in f_pos:
    plt.arrow(x, -3, 0, 2.3, head_width=0.08, head_length=0.3, fc='tab:orange', ec='tab:orange', **arrow_params)

for x in shifted_f_pos:
    plt.arrow(x, -3, 0, 2.3, head_width=0.08, head_length=0.3, fc='xkcd:sky blue', ec='xkcd:sky blue', **arrow_params)

for i in range(h-j+1) :
    choose_new_voters_pos = v_pos[left_v[i]-1 : right_v[i]]
    y6 = np.zeros(np.shape(choose_new_voters_pos))
    if overlap[i] == 1:
        plt.plot(choose_new_voters_pos, y6, '.', ms=25, color='k')
        plt.arrow(shifted_f_pos[i], -3, 0, 2.3, head_width=0.08, head_length=0.3, fc='k', ec='k', **arrow_params)
        continue
    plt.plot(choose_new_voters_pos, y6, '.', ms=25, color='xkcd:sky blue')

for i in range(len(f_pos)) :
    if i+1 < j or i+1 > h :
        plt.arrow(f_pos[i], -3, 0, 2.3, head_width=0.08, head_length=0.3, fc='k', ec='k', **arrow_params)

plt.text(3, 9, 'Black circle   : voter not voting', fontsize=16)
plt.text(3, 8, 'Orange circle  : voter voting to original decision', fontsize=16)
plt.text(3, 7, 'SkyBlue circle : voter voting to new decision', fontsize=16)
plt.text(3, 6, 'Orange arrow  : origin facility position', fontsize=16)
plt.text(3, 5, 'SkyBlue arrow : shift facility position', fontsize=16)
plt.text(3, 4, 'Black arrow : overlapping facilities position', fontsize=16)

drawPlot()

