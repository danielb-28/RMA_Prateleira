import math
from sys import maxsize
import matplotlib.pyplot as plt
import numpy as np
show_animation = True

class State:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.state = "."
        self.t = "new"  # tag for state
        self.h = 0
        self.k = 0

    def cost(self, state):
        if self.state == "#" or state.state == "#":
            return maxsize

        return math.sqrt(math.pow((self.x - state.x), 2) +
                         math.pow((self.y - state.y), 2))

    def set_state(self, state):
        """
        .: new
        #: obstacle
        e: oparent of current state
        *: closed state
        s: current state
        """
        if state not in ["s", ".", "#", "e", "*"]:
            return
        self.state = state


class Map:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.map = self.init_map()

    def init_map(self):
        map_list = []
        for i in range(self.row):
            tmp = []
            for j in range(self.col):
                tmp.append(State(i, j))
            map_list.append(tmp)
        return map_list

    def get_neighbors(self, state):
        state_list = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                if state.x + i < 0 or state.x + i >= self.row:
                    continue
                if state.y + j < 0 or state.y + j >= self.col:
                    continue
                state_list.append(self.map[state.x + i][state.y + j])
        return state_list

    def set_obstacle(self, point_list):
        for x, y in point_list:
            if x < 0 or x >= self.row or y < 0 or y >= self.col:
                continue

            self.map[x][y].set_state("#")


class Dstar:
    def __init__(self, maps):
        self.map = maps
        self.open_list = set()

    def process_state(self):
        x = self.min_state()

        if x is None:
            return -1

        k_old = self.get_kmin()
        self.remove(x)

        if k_old < x.h:
            for y in self.map.get_neighbors(x):
                if y.h <= k_old and x.h > y.h + x.cost(y):
                    x.parent = y
                    x.h = y.h + x.cost(y)
        elif k_old == x.h:
            for y in self.map.get_neighbors(x):
                if y.t == "new" or y.parent == x and y.h != x.h + x.cost(y) \
                        or y.parent != x and y.h > x.h + x.cost(y):
                    y.parent = x
                    self.insert(y, x.h + x.cost(y))
        else:
            for y in self.map.get_neighbors(x):
                if y.t == "new" or y.parent == x and y.h != x.h + x.cost(y):
                    y.parent = x
                    self.insert(y, x.h + x.cost(y))
                else:
                    if y.parent != x and y.h > x.h + x.cost(y):
                        self.insert(y, x.h)
                    else:
                        if y.parent != x and x.h > y.h + x.cost(y) \
                                and y.t == "close" and y.h > k_old:
                            self.insert(y, y.h)
        return self.get_kmin()

    def min_state(self):
        if not self.open_list:
            return None
        min_state = min(self.open_list, key=lambda x: x.k)
        return min_state

    def get_kmin(self):
        if not self.open_list:
            return -1
        k_min = min([x.k for x in self.open_list])
        return k_min

    def insert(self, state, h_new):
        if state.t == "new":
            state.k = h_new
        elif state.t == "open":
            state.k = min(state.k, h_new)
        elif state.t == "close":
            state.k = min(state.h, h_new)
        state.h = h_new
        state.t = "open"
        self.open_list.add(state)

    def remove(self, state):
        if state.t == "open":
            state.t = "close"
        self.open_list.remove(state)

    def modify_cost(self, x):
        if x.t == "close":
            self.insert(x, x.parent.h + x.cost(x.parent))

    def run(self, start, end):

        rx = []
        ry = []

        self.open_list.add(end)

        while True:
            self.process_state()
            if start.t == "close":
                break

        start.set_state("s")
        s = start
        s = s.parent
        s.set_state("e")
        tmp = start

        while tmp != end:
            tmp.set_state("*")
            rx.append(tmp.x)
            ry.append(tmp.y)
            if show_animation:
                plt.plot(rx, ry, "-r")
                plt.pause(0.01)
            if tmp.parent.state == "#":
                self.modify(tmp)
                continue
            tmp = tmp.parent
        tmp.set_state("e")

        return rx, ry

    def modify(self, state):
        self.modify_cost(state)
        while True:
            k_min = self.process_state()
            if k_min >= state.h:
                break

def dist_ponto(x_ponto, y_ponto, m, n):
    dividendo = abs((m * x_ponto) - y_ponto + n)
    divisor = math.sqrt(m * m + 1)

    return dividendo/divisor

def criar_reta(x1, y1, x2, y2):
    delta_y = y2 - y1
    delta_x = x2 - x1
    
    if delta_x == 0:
        m = 0
    else:
        m = delta_y / delta_x # equivalente a a
        
    angulo = math.atan2(delta_y, delta_x)
    n = y2 - (m * x2)     # equivalente a c

    return m, n, angulo

def colidir(ox, oy, x1, y1, x2, y2, value=0.5, d=False, show=False, direcionalAng=[None,None]):
    # y menor horizontal
    # x menor vertical
    vertical = True if abs(x1-x2) < abs(y1-y2) else False
    
    v, h = 0, 0
    
    if d:
        if vertical: h = value
        if not vertical: v = value
    
    m, n, ang = criar_reta(x1, y1, x2, y2)
    if ang < 0: ang + math.pi * 2

    c4 = False

    if direcionalAng[0] != None:
        angAux = math.atan2(direcionalAng[1] - y1, direcionalAng[0] - x1)
        if angAux < 0: ang + math.pi * 2
        c4 = abs(angAux - ang) <= 90
    else:
        c4 = True

    for obs in zip(ox, oy):
        c1 = min([x1, x2]) - h <= obs[0] <= max([x1, x2]) + h
        c2 = min([y1, y2]) - v <= obs[1] <= max([y1, y2]) + v
        c3 = dist_ponto(obs[0], obs[1], m, n) < value
        if c1 and c2 and c3 and c4: #colidiu
            return True
    return False

def diminuir_pontos(x, y, ox, oy, apf=False):
    newPath_x, newPath_y = [x[0]], [y[0]]
    goalx, goaly = x[-1], y[-1]
    check = 1

    while newPath_x[-1] != goalx or newPath_y[-1] != goaly:
        if not colidir(ox, oy, newPath_x[-1], newPath_y[-1], goalx, goaly):
            newPath_x.append(goalx)
            newPath_y.append(goaly)
            break
        else:
            try:
                if colidir(ox, oy, newPath_x[-1], newPath_y[-1], x[check], y[check], d=True, value=0.4):
                    newPath_x.append(x[check-1])
                    if apf: newPath_x.append(x[check]) # comment ?
                    newPath_y.append(y[check-1])
                    if apf: newPath_y.append(y[check]) # comment ?
                    check += 1
                else:
                    check += 1
            except: 
                newPath_x.append(goalx)
                newPath_y.append(goaly)

    return newPath_x, newPath_y

def main():
    m = Map(100, 100)
    ox, oy = [], []
    for i in range(-50, -17):
        ox.append(25)
        ox.append(57)
        oy.append(i+70)
        oy.append(i+70)
    for i in range(25, 57):
        ox.append(i)
        ox.append(i)
        oy.append(-50+70)
        oy.append(-17+70)

    m.set_obstacle([(i, j) for i, j in zip(ox, oy)])

    start = [0, -70+70]
    goal = [65, -35+70]
    if show_animation:
        plt.plot(ox, oy, ".k")
        plt.plot(start[0], start[1], "og")
        plt.plot(goal[0], goal[1], "xb")
        plt.axis("equal")

    start = m.map[start[0]][start[1]]
    end = m.map[goal[0]][goal[1]]
    dstar = Dstar(m)
    rx, ry = dstar.run(start, end)
    rx, ry = diminuir_pontos(rx, ry, ox, oy)

    ry = (np.asarray(ry)-70).tolist()
    if show_animation:
        plt.plot(rx, ry, "-r")
        plt.show()

def runDstar(sx, sy, gx, gy, rangeY=70):
    m = Map(100, 100)
    ox, oy = [], []
    for i in range(-50, -17):
        ox.append(25)
        ox.append(57)
        oy.append(i+rangeY)
        oy.append(i+rangeY)
    for i in range(25, 57):
        ox.append(i)
        ox.append(i)
        oy.append(-50+rangeY)
        oy.append(-17+rangeY)

    m.set_obstacle([(i, j) for i, j in zip(ox, oy)])

    start = [sx, sy+rangeY]
    goal = [gx, gy+rangeY]

    start = m.map[start[0]][start[1]]
    end = m.map[goal[0]][goal[1]]
    dstar = Dstar(m)
    
    rx, ry = dstar.run(start, end)
    rx, ry = diminuir_pontos(rx, ry, ox, oy)
    ry = (np.asarray(ry)-rangeY).tolist()

    return rx, ry

if __name__ == '__main__':
    main()