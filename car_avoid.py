import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import animation
import time

NUM = 80
MAX_SPEED = 4
obstacle_map = np.zeros([NUM,  NUM])
positions = np.ones(NUM, dtype=np.int)*-1
speeds = np.zeros(NUM)
flags = np.zeros(NUM)
player_x = np.zeros(1, dtype=np.int)
player_y = np.zeros(1, dtype=np.int)
p_obstacle = 0.8
# line1_x = [-1]
# line1_y = [-1]


def init():
    for i in range(NUM):
        init_obstacle(i)
    player_x[0] = random.randint(0, NUM - 1)


def init_player():
    player_x[0] = random.randint(0, NUM - 1)
    player_y[0] = 0


def init_obstacle(index):
    if random.random() < p_obstacle:
        flags[index] = 1
        if random.random() < 0.5:
            speeds[index] = random.randint(1, MAX_SPEED)
            positions[index] = 0
        else:
            speeds[index] = - random.randint(1, MAX_SPEED)
            positions[index] = NUM - 1
        obstacle_map[index, positions[index]] = 1
    else:
        flags[index] = 0


def add_obstacle():
    while 1:
        if sum(flags) < NUM * p_obstacle:
            temp = random.randint(0, NUM - 1)
            if flags[temp] == 0:
                flags[temp] = 1
                init_obstacle(temp)
        else:
            break


def play():
    for i in range(NUM):
        temp_position = positions[i] + speeds[i]
        obstacle_map[i, positions[i]] = 0
        if temp_position > NUM - 1 or temp_position < 0:
            positions[i] = -1
            flags[i] = 0
        else:
            positions[i] = temp_position
            obstacle_map[i, positions[i]] = 1
    for i in range(NUM):
        if flags[i] == 0:
            positions[i] = -1
    add_obstacle()
    action = 0
    if action == 0:
        temp_y = player_y[0] + 1
        if temp_y <= NUM - 1:
            player_y[0] = temp_y
        else:
            player_x[0] = random.randint(0, NUM - 1)
            player_y[0] = 0
    elif action == 1:
        temp_x = player_x[0] - 1
        if temp_x <= 0:
            player_x[0] = 0
        else:
            player_x[0] = temp_x
    elif action == 2:
        temp_x = player_x[0] + 1
        if temp_x >= NUM - 1:
            player_x[0] = NUM - 1
        else:
            player_x[0] = temp_x
    if flags[player_y[0]] == 1 and positions[player_y[0]] == player_x[0]:
        reward = -1
        init_player()
    else:
        if action == 0:
            reward = 1
        elif action == 1 or action == 2:
            reward = 0.5
        else:
            reward = -0.5
    print('r:', reward)
    # print('y', player_y[0])
    # time.sleep(8)
    return reward


def init_plot():
    line1.set_data([], [])
    line2.set_data([], [])


def animate(i):
    line1_x = []
    line1_y = []
    r = play()
    for j in range(NUM):
        if flags[j] == 1:
            line1_x.append(positions[j])
            line1_y.append(j)
    line1.set_data(line1_x, line1_y)
    line2 .set_data(player_x[0], player_y[0])
    return line1, line2

init()
s_t = np.stack((obstacle_map, obstacle_map, obstacle_map, obstacle_map), axis=2)
fig = plt.figure()
fig_plot = fig.add_subplot(1, 1, 1, xlim=(-1, NUM - 1 + 1), ylim=(-1, NUM - 1 + 1))
line1, = fig_plot.plot([], [], 'o', color='blue')
line2, = fig_plot.plot([], [], 'o', color='red')
anim = animation.FuncAnimation(fig, animate, init_func=init_plot(), frames=1000, interval=100-)
plt.show()
