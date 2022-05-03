# -*- coding: utf-8 -*-
import rospy
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from curves.bezier import Bezier
from curves import bSpline
import psutil
import os
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def rotacionar(x1, y1, x2, y2):
    a = definir_angulo(x1, y1, x2, y2)
    return a

def rotationMatrix(psi0, x1, y1, z1):
    r = [[np.cos(psi0), np.sin(psi0) * -1, 0], [np.sin(psi0), np.cos(psi0), 0], [0, 0, 1]]
    pos_local = np.dot(np.transpose(np.asarray(r)), np.asarray([x1, y1, z1]))
    return pos_local

def intersecao_arrays(a1, a2):
    # quer descobrir oq esta no a1 mas n ta no a2
    direc = 0
    
    if a1[0][0] == a2[0][0]: # obstaculo na vertical
        minValue1 = float("inf")
        minValue2 = float("inf")

        minValue1 = [value[1] for value in a1 if minValue1 > value[1]]
        minValue2 = [value[1] for value in a2 if minValue2 > value[1]]
        # for value in a1:
        #     if minValue1 > value[1]:
        #         minValue1 = value[1]

        # for value in a2:
        #     if minValue2 > value[1]:
        #         minValue2 = value[1]

        if minValue1 < minValue2: # Ta subindo
            print("SUBINDO")
            direc = 0
        else: 
            print("DESCENDO")
            direc = 1
    else: # obstaculo na horizontal
        minValue1 = float("inf")
        minValue2 = float("inf")

        minValue1 = [value[0] for value in a1 if minValue1 > value[0]]
        minValue2 = [value[0] for value in a2 if minValue2 > value[0]]

        if minValue1 < minValue2: # Ta subindo
            print("INDO PARA DIREITA")
            direc = 2
        else: 
            print("INDO PARA ESQUERDA")
            direc = 3

    for a in a1:
        if a not in a2:
            return a, direc

def simulate_points(x1, x2, y1, y2, juntos=False):
    aux = math.ceil(max(abs(x1 - x2), abs(y1 - y2)))
    aux *= 2
    a1 = np.linspace(x1, x2, int(aux))
    a2 = np.linspace(y1, y2, int(aux))

    if juntos:
        jj = []
        for i in range(len(a1)):
            jj.append([a1[i], a2[i]])

        return jj
    else:
        return a1, a2

def suavizar_curva(x, y):
    curv = bSpline.B_spline(x, y)
    xnew, ynew = curv.get_curv()

    return xnew, ynew

def smooth_bspline(px, py, cx, cy, nx, ny, gx, gy, v=0):
    if v == 0:
        curv = bSpline.B_spline([px, cx, nx, gx], [py, cy, ny, gy])
        xnew, ynew = curv.get_curv()
        return xnew, ynew
    else:
        XS = np.concatenate(([px], [cx, nx], [gx]), axis=0)
        YS = np.concatenate(([py], [cy, ny], [gy]), axis=0)
        k = XS.size
        TS = np.linspace(0, 1, k)
        tt = np.linspace(0, 1, 100)
        tcx = interpolate.splrep(TS, XS)
        tcy = interpolate.splrep(TS, YS)
        xx = interpolate.splev(tt, tcx)
        yy = interpolate.splev(tt, tcy)

        return xx, yy

def tam_obs_dim(tam):
    if tam % 2 == 0 : tam += 1
    return np.linspace(tam-int(tam/2), tam+int(tam/2), tam) - tam

def memory_usage():
    # return the memory usage in percentage like top
    process = psutil.Process(os.getpid())
    mem = process.memory_percent()
    return mem

def distancia_rota(pathx, pathy=[]):
    distancia = 0
    if len(pathy) == 0:
        px, py = [], []
        for i in range(len(pathx)):
            px.append(pathx[i][0])
            py.append(pathx[i][1]) 
            for q in range(0, len(px)-1):
                distancia += math.sqrt(((px[q+1] - px[q])**2) + ((py[q+1] - py[q])**2))
        return distancia, px, py
    else:
        for q in range(0, len(pathx)-1):
            distancia += math.sqrt(((pathx[q+1] - pathx[q])**2) + ((pathy[q+1] - pathy[q])**2))
        return distancia

def completness(rotaX, rotaY, ox, oy, value=0.5):
    for rx, ry in zip(rotaX, rotaY):
        for obsx, obsy in zip (ox, oy):
            if dist_euclidiana(rx, ry, obsx, obsy) <= value:
                return True

    return False

def minValue(matriz, zero=False):
    menor = float("inf")
    index = [0, 0]
    for r in range(len(matriz)):
        for n in range(len(matriz[0])):
            if zero:
               if menor > matriz[r][n] > 0:
                    index = [r, n] 
                    menor = matriz[r][n]  
            else:
                if menor > matriz[r][n]:
                    index = [r, n] 
                    menor = matriz[r][n]
    return menor, index

def maxValue(matriz):
    maior = -float("inf")
    index = [0, 0]
    for r in range(len(matriz)):
        for n in range(len(matriz[0])):
            if maior < matriz[r][n]:
                index = [r, n] 
                maior = matriz[r][n]
    return maior, index

def colidir(ox, oy, newPath_x, newPath_y, goalx, goaly):
    print("pontos " + str(goalx) + " "+ str(goaly) + " "+ str(newPath_x) + " "+ str(newPath_y))

    if (goalx-newPath_x) == 0:
        print("colidiu por divisao por zero")
        return True
    m = (goaly-newPath_y) / (goalx-newPath_x)
    n = goaly - m*goalx

    for i in range(len(ox)):
        if (abs(ox[i]- newPath_x) < abs(goalx - newPath_x)+1 and abs(oy[i] - newPath_y) < abs(goaly - newPath_y)+1):
            print("testando colisao" + str(ox[i]) + " " + str(oy[i]) + " "+ str(goalx) + " "+ str(goaly) + " "+ str(newPath_x) + " "+ str(newPath_y))
            if intersecao_ponto(ox[i], oy[i], m, n) | intersecao_ponto(ox[i], oy[i], m-10, n) | intersecao_ponto(ox[i], oy[i], m+10, n):
                if ( ( (goalx-newPath_x)*(ox[i]-newPath_x) ) >= 0 and ( (goaly-newPath_y)*(oy[i]-newPath_y) ) >= 0):
                    print("colidiu")
                    return True
                else:
                    print("esta alinhado mas fora do caminho")
    print("nao colidiu")
    return False

def diminuir_pontos(x, y, z, h, ox, oy, apf=False):
    newPath_x, newPath_y, newPath_z, newPath_h = [x[0]], [y[0]], [z[0]], [h[0]]
    goalx, goaly = x[-1], y[-1]
    check = 1

    while newPath_x[-1] != goalx and newPath_y[-1] != goaly:
        if not colidir(ox, oy, newPath_x[-1], newPath_y[-1], x[-check], y[-check]):
            newPath_x.append(x[-check])
            newPath_y.append(y[-check])
            newPath_z.append(z[-check])
            newPath_h.append(h[-check])
            check = 1
        else:
            if check < len(x):
                check += 1
            else:
                newPath_x.append(x[-check])
                newPath_y.append(y[-check])
                newPath_z.append(z[-check])
                newPath_h.append(h[-check])
                check = 1
               
    return newPath_x, newPath_y, newPath_z, newPath_h
                
def criar_reta(x1, y1, x2, y2):
    delta_y = y2 - y1
    delta_x = x2 - x1
    
    if delta_x == 0:
        m = 0
    else:
        m = delta_y / delta_x # equivalente a a
        
    angulo = math.atan2(delta_y, delta_x)
    n = y2 - (m * x2)     # equivalente a c
    # b sempre vai ser -1

    return m, n, angulo

def intersecao_ponto(x_ponto, y_ponto, m, n):
    aux = abs((m * x_ponto) - y_ponto + n)
    print("intersec " + str(aux))
    if aux < 10:
        return True # o ponto cruza a linha
    else:
        return False # o ponto nao cruza a linha

def intersecao_reta(x1, y1, x2, y2):
    if ((y2 - y1) + (x2 - x1)) == 0:
        return False # as retas nao se cruzam
    else: 
        return True # as retas se cruzam

def dist_euclidiana(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

def dist_euclidiana3D(x1, y1, z1, x2, y2, z2):
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) + math.pow(z2 - z1, 2))

def triangulo(ca=None, co=None, hip=None, alfa=None, oqquer="hip"):
    if oqquer == "alfa":
        if ca == None:
            alfa = math.asin(co/hip)
        elif co == None:
            alfa = math.acos(ca/hip)
        else:
            alfa = math.atan(co/ca)

        return alfa
    
    if oqquer == "hip":
        hip = math.pow(ca, 2) + math.pow(co, 2)
        
        return hip
    
    if oqquer == "co":
        if alfa == None:
            co = math.pow(hip, 2) / math.pow(ca, 2)
        else:
            co = math.sin(math.radians(alfa)) * hip

        return co
        
    if oqquer == "ca":
        if alfa == None:
            ca = math.pow(hip, 2) / math.pow(co, 2)
        else:
            ca = math.cos(math.radians(alfa)) * hip

        return ca
 
def dist_ponto(x_ponto, y_ponto, m, n):
    dividendo = abs((m * x_ponto) - y_ponto + n)
    divisor = math.sqrt(m * m + 1)

    return dividendo/divisor

def getBezier(start_x, start_y, start_yaw, end_x, end_y, end_yaw, offset=2, t=0.86):
    b = Bezier(start_x, start_y, start_yaw, end_x, end_y, end_yaw, offset, t)
    p = b.calc_4points_bezier_path()

    assert p.T[0][0] == start_x, "path is invalid"
    assert p.T[1][0] == start_y, "path is invalid"
    assert p.T[0][-1] == end_x, "path is invalid"
    assert p.T[1][-1] == end_y, "path is invalid"

    return p.T[0], p.T[1]

def definir_angulo(x1, y1, x2, y2):
    delta_y = y2 - y1
    delta_x = x2 - x1
    
    angle = math.atan2(delta_y, delta_x)
    
    return angle

def smooth_reta(path_x, path_y, offset=2):
    n = len(path_x)
    
    newPath_x = [path_x[0]]
    newPath_y = [path_y[0]]
    for i in range(1, n-2, 2):
        _, _, angulo1 = criar_reta(path_x[i-1], path_y[i-1], path_x[i], path_y[i])
        _, _, angulo2 = criar_reta(path_x[i+1], path_y[i+1], path_x[i+2], path_y[i+2])

        c1, c2 = getBezier(path_x[i], path_y[i], angulo1, path_x[i+1], path_y[i+1], angulo2, offset)
        [newPath_x.append(valor_x) for valor_x in c1]
        [newPath_y.append(valor_y) for valor_y in c2]
    
    newPath_x.append(path_x[-1])
    newPath_y.append(path_y[-1])
    
    return newPath_x, newPath_y

def newSmooth(path_x, path_y, offset=2):
    newPath_x = [path_x[0]] 
    newPath_y = [path_y[0]]
    # print(path_y)
    _, _, angulo1 = criar_reta(path_x[0], path_y[0], path_x[1], path_y[1])
    # print(math.degrees(math.atan2(0.1, 0)))
    # print(math.degrees(angulo1))

    _, _, angulo2 = criar_reta(path_x[2], path_y[2], path_x[3], path_y[3])

    c1, c2 = getBezier(path_x[0], path_y[0], angulo1, path_x[3], path_y[3], angulo2, offset)
    [newPath_x.append(valor_x) for valor_x in c1]
    [newPath_y.append(valor_y) for valor_y in c2]

    return newPath_x, newPath_y

def distanciaTotalRota(xx, yy):
    distance =  0
    for q in range(0, len(xx)-1):
        distance += math.sqrt(((xx[q+1] - xx[q])**2) + ((yy[q+1] - yy[q])**2))
    return distance

def passos_locais(path_x, path_y):
    proximoPasso = {"x": [], "y": [], "a": []}
    aux = 0
    for i in range(1, len(path_x)-1):
        proximoPasso["x"].append(path_x[i] - path_x[i-1])
        proximoPasso["y"].append(path_y[i] - path_y[i-1])
        _, _, a1 = criar_reta(path_x[i-1], path_y[i-1], path_x[i], path_y[i])
        auxiliar = ((math.pi/2)-(a1-aux)) if i == 1 else (aux-a1)
        proximoPasso["a"].append(auxiliar)
        aux = a1

    return proximoPasso

def draw_cylinder(center_x,center_y,radius,height_z):
    z = np.linspace(0, height_z, 10)
    theta = np.linspace(0, 2*np.pi, 20)
    theta_grid, z_grid=np.meshgrid(theta, z)
    x_grid = radius*np.cos(theta_grid) + center_x
    y_grid = radius*np.sin(theta_grid) + center_y
    return x_grid,y_grid,z_grid

def cuboid_data(o, size=(1,1,1)):
    X = [[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
         [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
         [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
         [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
         [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
         [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]
    X = np.array(X).astype(float)
    for i in range(3):
        X[:,:,i] *= size[i]
    X += np.array(o)
    return X

def draw_bar(positions,sizes=None,colors=None, **kwargs):
    if not isinstance(colors,(list,np.ndarray)): colors=["C0"]*len(positions)
    if not isinstance(sizes,(list,np.ndarray)): sizes=[(1,1,1)]*len(positions)
    g = []
    for p,s,c in zip(positions,sizes,colors):
        g.append( cuboid_data(p, size=s) )
    return Poly3DCollection(np.concatenate(g),  
                            facecolors=np.repeat(colors,6), **kwargs)
