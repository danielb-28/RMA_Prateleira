#!/usr/bin/env python
import math

import matplotlib.pyplot as plt

import rospy

import numpy as np

from geometry_msgs.msg import Pose

from geometry_msgs.msg import PoseArray

import os

import sys

# Main ================================================================================
def main():

    # rospy.init_node('a_star')
    
    # print(rospy.get_param_names())

    argv = sys.argv

    print(len(argv))
    print(argv)

    assert(len(argv) == 9), "numero invalido de argumentos"
    
    Pontos = list(list())
    
    # xOrigem = rospy.get_param("/a_star/xOrigem")
    # yOrigem = rospy.get_param("/a_star/yOrigem")
    
    # xDestino = rospy.get_param("/a_star/xDestino")
    # yDestino = rospy.get_param("/a_star/yDestino")
    
    # NomeMapa = rospy.get_param("/a_star/NomeMapa")                      # Nome do a ser percorrido
    # Animacao = rospy.get_param("/a_star/Animacao")
    
    Proporcional = 3#0.28                         # Metros/pxl

    xOrigem = float(argv[1])
    yOrigem = float(argv[2])

    xDestino = float(argv[5])
    yDestino = float(argv[6])
    
    NomeMapa = 'mapa.pgm'
    Animacao = True

    show_animation = Animacao
    
    dir_atual = os.path.dirname(__file__)
    NomeMapa = os.path.join(dir_atual, NomeMapa)

    print(__file__ + "\nInicio A*")

    with open(NomeMapa, 'r') as arq:
        Dim = arq.readlines()[2].split(' ')     # Tamanho do Mapa em pxl
    
    ErroDim = 0                                 # Reconfiguração da matriz proveniente do mapa
    if Dim[0] != Dim[1]:
        ErroDim = abs(int(Dim[0]) - int(Dim[1]))
        print(ErroDim)
    
    # Localização dos obstáculos
    ox, oy = [], []
    
    M = np.loadtxt(NomeMapa, delimiter=',', skiprows= 4).reshape(int(Dim[1]), int(Dim[0]))  # Lê matriz externa, mapa.yaml reduzido por conta do processamento
    
    Mapa = []
    for i in range(len(M)):
        Mapa.append([])
        for j in range(len(M[0])):
            Mapa[i].append(int(M[i][j]))
        if len(M[0]) < len(M):
            for k in range(ErroDim):
                Mapa[i].append(0)
        
    if len(M) < len(M[0]): Mapa.append(np.zeros(len(M[0])))
    #print(Mapa)
    
    for i in range(len(Mapa)):
        for j in range(len(Mapa[0])):
            if Mapa[-1-i][j] == 0:         # 0 é a cor preta no .pgm lido como texto, ou seja, obstáculo
                oy.append(i)
                ox.append(j)

    # Pontos iniciais convertidos de [m] para pxls
    sx = (xOrigem*Proporcional)        # X inicial
    sy = (yOrigem*Proporcional)        # Y inicial
    gx = (xDestino*Proporcional)       # X final
    gy = (yDestino*Proporcional)       # Y final
    grid_size = 0.7 *Proporcional                  # Distâncias entre as esquinas
    robot_radius = (1*Proporcional)    # Tamanho do robô

    show_animation = Animacao   # Verifica se deve ou não realizar o plot
    if show_animation:          # Plot dos obstáculos, origem e destino
        plt.plot(ox, oy, ".k")
        plt.plot(sx, sy, "og")
        plt.plot(gx, gy, "xb")
        plt.grid(True)
        plt.axis("equal")
        
    a_star = AStarPlanner(ox, oy, grid_size, robot_radius, show_animation)
    rx,ry = a_star.planning(sx, sy,gx, gy)

    # for i in range(len(rx)):
    #     Pontos.append([(rx[-1-i] - sx)*Proporcional, (ry[-1-i] - sy)*Proporcional]) # Armazena os pontos gerados

    # Publicacao do caminho encontrado

    # pub = rospy.Publisher('Checkpoints', PoseArray, queue_size = 10)

    # Mensagem = PoseArray()
    # Mensagem.header.stamp = rospy.Time.now()
    # Mensagem.header.frame_id = "map"

    #taxa = rospy.Rate(0.5)
    #print(Pontos)

    for i in range(len(Pontos)):
        #taxa.sleep()
        pose_atual = Pose()
        pose_atual.position.x = Pontos[i][0] 
        pose_atual.position.y = Pontos[i][1] 
        #Mensagem.poses.append(pose_atual)

    rx.insert(0, gx)
    ry.insert(0, gy)

    trajetoria = "trajetoria"
    arquivoTrajetoria = open(trajetoria + ".csv", "w")
    for i in range(len(rx)):
        if i == 0:
            arquivoTrajetoria.write(str(rx[-i-1]/Proporcional) + ',' + str(ry[-i-1]/Proporcional) + ', ' + str(argv[3]) + ', ' + str(argv[4]) + '\n')
        elif i < len(rx)-1: 
            arquivoTrajetoria.write(str(rx[-i-1]/Proporcional) + ',' + str(ry[-i-1]/Proporcional) + ', 1.2, ' + str(argv[8]) + '\n')
        else:
            arquivoTrajetoria.write(str(rx[-i-1]/Proporcional) + ',' + str(ry[-i-1]/Proporcional) + ', ' + str(argv[7]) + ', ' + str(argv[8]) + '\n')
        #print(str(rx[-i-1]) + ',' + str(ry[-i-1]) + ',3\n')
    arquivoTrajetoria.close()
    
    #while not rospy.is_shutdown():
        #pub.publish(Mensagem)
    if show_animation:  # Plot dos checkpoints e ligando os pontos
        plt.plot(rx, ry, "-r")
        plt.pause(0.001)
        plt.show(block=False)
    #taxa.sleep()

    arquivo_obstaculos = open("obstaculos.csv", "w") 
    for i in range(len(ox)):
        arquivo_obstaculos.write(str(ox[i]/Proporcional) + ", " + str(oy[i]/Proporcional) + "\n")

    arquivo_obstaculos.close()
        
        
# Planejador A*  ====================================================================================

class AStarPlanner:

    def __init__(self, ox, oy, resolution, rr, show_animation):
        """
        Inicializa o mapa para o planejador A*

        ox: Posição X da lista de obstáculos em pxl
        oy: Posição Y da lista de obstáculos em pxl
        resolution: Passo da discretização dos caminhos em pxl
        rr: Raio do robô em pxl
        """

        self.resolution = resolution
        self.rr = rr
        self.min_x, self.min_y = 0, 0
        self.max_x, self.max_y = 0, 0
        self.obstacle_map = None
        self.x_width, self.y_width = 0, 0
        self.motion = self.get_motion_model()
        self.calc_obstacle_map(ox, oy)
        self.show_animation = show_animation

    class Node:
        def __init__(self, x, y, cost, parent_index):
            self.x = x  # index of grid
            self.y = y  # index of grid
            self.cost = cost
            self.parent_index = parent_index

        def __str__(self):
            return str(self.x) + "," + str(self.y) + "," + str(
                self.cost) + "," + str(self.parent_index)

    def planning(self, sx, sy, gx, gy):
        """
        Planejador em si

        Entrada:
            s_x: Posição X de início em pxl
            s_y: Posição X de início em pxl
            gx: Posição X de saída em pxl
            gy: Posição X de saída em pxl

        Saída:
            rx: Lista de posições X dos checkppoints
            ry: Lista de posições y dos checkppoints
        """

        start_node = self.Node(self.calc_xy_index(sx, self.min_x),
                               self.calc_xy_index(sy, self.min_y), 0.0, -1)
        goal_node = self.Node(self.calc_xy_index(gx, self.min_x),
                              self.calc_xy_index(gy, self.min_y), 0.0, -1)

        open_set, closed_set = dict(), dict()
        open_set[self.calc_grid_index(start_node)] = start_node

        while 1:
            if len(open_set) == 0:
                print("Open set is empty..")
                break

            c_id = min(
                open_set,
                key=lambda o: open_set[o].cost + self.calc_heuristic(goal_node,
                                                                     open_set[
                                                                         o]))
            current = open_set[c_id]

            # Plota caso configurado assim
            if self.show_animation:  
                plt.plot(self.calc_grid_position(current.x, self.min_x),
                         self.calc_grid_position(current.y, self.min_y), "xc")
                # Para que se possa parar a plotagem com 'ESC'
                plt.gcf().canvas.mpl_connect('key_release_event',
                                             lambda event: [exit(
                                                 0) if event.key == 'escape' else None])
                if len(closed_set.keys()) % 10 == 0:
                    plt.pause(0.001)

            if current.x == goal_node.x and current.y == goal_node.y:
                print("Caminho Encontrado!")
                goal_node.parent_index = current.parent_index
                goal_node.cost = current.cost
                break

            # Remove the item from the open set
            del open_set[c_id]

            # Add it to the closed set
            closed_set[c_id] = current

            # expand_grid search grid based on motion model
            for i, _ in enumerate(self.motion):
                node = self.Node(current.x + self.motion[i][0],
                                 current.y + self.motion[i][1],
                                 current.cost + self.motion[i][2], c_id)
                n_id = self.calc_grid_index(node)

                # Verifica se pode passar pela esquina
                if not self.verify_node(node):
                    continue

                if n_id in closed_set:
                    continue

                if n_id not in open_set:
                    open_set[n_id] = node  
                else:
                    if open_set[n_id].cost > node.cost:
                        open_set[n_id] = node

        rx, ry = self.calc_final_path(goal_node, closed_set)

        return rx, ry

    def calc_final_path(self, goal_node, closed_set):
        # Depois de encontrar o destino, ele calcula a menor rota até ele
        rx, ry = [self.calc_grid_position(goal_node.x, self.min_x)], [
            self.calc_grid_position(goal_node.y, self.min_y)]
        parent_index = goal_node.parent_index
        while parent_index != -1:
            n = closed_set[parent_index]
            rx.append(self.calc_grid_position(n.x, self.min_x))
            ry.append(self.calc_grid_position(n.y, self.min_y))
            parent_index = n.parent_index

        return rx, ry

    @staticmethod
    def calc_heuristic(n1, n2):
        w = 1.0  # Peso da Heurística
        d = w * math.hypot(n1.x - n2.x, n1.y - n2.y)
        return d

    def calc_grid_position(self, index, min_position):
        """
        Calcula a posição da esquina

        :param index:
        :param min_position:
        :return:
        """
        pos = index * self.resolution + min_position
        return pos

    def calc_xy_index(self, position, min_pos):
        return round((position - min_pos) / self.resolution)

    def calc_grid_index(self, node):
        return (node.y - self.min_y) * self.x_width + (node.x - self.min_x)

    def verify_node(self, node):
        px = self.calc_grid_position(node.x, self.min_x)
        py = self.calc_grid_position(node.y, self.min_y)

        if px < self.min_x:
            return False
        elif py < self.min_y:
            return False
        elif px >= self.max_x:
            return False
        elif py >= self.max_y:
            return False

        # Checagem de colisão
        if self.obstacle_map[node.x][node.y]:
            return False

        return True

    def calc_obstacle_map(self, ox, oy):

        self.min_x = round(min(ox))
        self.min_y = round(min(oy))
        self.max_x = round(max(ox))
        self.max_y = round(max(oy))
        print("min_x:", self.min_x)
        print("min_y:", self.min_y)
        print("max_x:", self.max_x)
        print("max_y:", self.max_y)

        self.x_width = round((self.max_x - self.min_x) / self.resolution)
        self.y_width = round((self.max_y - self.min_y) / self.resolution)
        print("x_width:", self.x_width)
        print("y_width:", self.y_width)

        # Geração dos obstáculos no mapa
        self.obstacle_map = [[False for _ in range(self.y_width)]
                             for _ in range(self.x_width)]
        for ix in range(self.x_width):
            x = self.calc_grid_position(ix, self.min_x)
            for iy in range(self.y_width):
                y = self.calc_grid_position(iy, self.min_y)
                for iox, ioy in zip(ox, oy):
                    d = math.hypot(iox - x, ioy - y)
                    if d <= self.rr:
                        self.obstacle_map[ix][iy] = True
                        break

    @staticmethod
    def get_motion_model():        # Heurística do A*, mede as direções possíveis e seus custos
        # dx, dy, custo
        motion = [[1, 0, 1],
                  [0, 1, 1],
                  [-1, 0, 1],
                  [0, -1, 1],
                  [-1, -1, math.sqrt(2)],
                  [-1, 1, math.sqrt(2)],
                  [1, -1, math.sqrt(2)],
                  [1, 1, math.sqrt(2)]]

        return motion




if __name__ == '__main__':

    try:
        main()
    except rospy.ROSInterruptException:
        pass

    
