# Reading decision text file and display
import os
from matplotlib import pyplot as plt
import numpy as np
import sys

if len(sys.argv) != 2:
	print ('Usage : python show_decision.py <decision_file>')
	sys.exit(0)

os.chdir(os.getcwd())

filename = sys.argv[1]

with open(filename) as f:
    v_num, f_num = map(int, f.readline().split())
    v_pos        = [float(x) for x in f.readline().split()]
    f_pos        = [float(x) for x in f.readline().split()]
    comm_size    = [int(x)   for x in f.readline().split()]
    
    b_voter = []
    t_voter = []
    base    = 1
    for i in range(len(comm_size)):
        b_voter.append(base)
        t_voter.append(base + comm_size[i] - 1)
        base += comm_size[i]

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

plt.hlines(0, min_pos-1, max_pos+1)  # Draw a horizontal line
plt.xlim(min_pos-1, max_pos+1)
plt.ylim(-6, 10)

y1 = np.zeros(np.shape(v_pos))   # Make all y values the same
y2 = np.zeros(np.shape(f_pos))

plt.plot(v_pos, y1, '.', ms=25, color='k')

borders = []
for i in range(len(f_pos)-1) :
    borders.append((v_pos[t_voter[i]-1]+v_pos[b_voter[i+1]-1])/2)
y3 = np.zeros(np.shape(borders))
plt.plot(borders, y3, '|', ms=25, color='k')

overhang = 0.8
arrow_params = {'overhang':overhang}
for x in f_pos:
    plt.arrow(x, -3, 0, 2.3, head_width=0.08, head_length=0.3, fc='k', ec='k', **arrow_params)

plt.axis('on')

mng = plt.get_current_fig_manager()
mng.window.state('zoomed')

plt.show()
