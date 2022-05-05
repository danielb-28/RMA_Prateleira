import math
from utils import *

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
            # if show: print(str(x1) + " - " + str(y1))
            # if show: print(str(x2) + " - " + str(y2))
            # if show: print(obs)
            # if show: print(dist_ponto(obs[0], obs[1], m, n))
            # if value == 1:
            #     print("x " + str(obs[0]) + " y " + str(obs[1]))
            # print(obs[0])
            # print(obs[1])
            # print(dist_ponto(obs[0], obs[1], m, n))
            # print("-----")
            return True
    return False
    
def diminuir_pontos(x, y, z, h, ox, oy, apf=False):
    newPath_x, newPath_y, newPath_z, newPath_h= [x[0]], [y[0]], [z[0]], [h[0]]
    goalx, goaly = x[-1], y[-1]
    check = 1

    while newPath_x[-1] != goalx or newPath_y[-1] != goaly:
        if not colidir(ox, oy, newPath_x[-1], newPath_y[-1], goalx, goaly):
            newPath_x.append(goalx)
            newPath_y.append(goaly)
            newPath_z.append(z[-1])
            newPath_h.append(h[-1])
            print("--------------------")
            break
        else:
            try:
                if colidir(ox, oy, newPath_x[-1], newPath_y[-1], x[check], y[check], d=True, value=0.4):
                    # print("colidiu")
                    # print( str(newPath_x[-1]) + " - " + str(newPath_y[-1]))
                    # print( str(x[check]) + " - " + str(y[check]))
                    newPath_x.append(x[check-1])
                    newPath_y.append(y[check-1])
                    newPath_z.append(z[check-1])
                    newPath_h.append(h[check-1])
                    if apf: 
                        newPath_x.append(x[check])
                        newPath_y.append(y[check])
                        newPath_z.append(z[check])
                        newPath_h.append(h[check])
                    
                    check += 1
                else:
                    check += 1
            except: 
                newPath_x.append(goalx)
                newPath_y.append(goaly)
                newPath_z.append(goalz)
                newPath_h.append(goalh)

    return newPath_x, newPath_y, newPath_z, newPath_h
