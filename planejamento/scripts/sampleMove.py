# -*- coding: utf-8 -*-
import sys
import rospy
import math
import numpy as np
import matplotlib.pyplot as plt

from utils import *
from utilsUAV import *

from nav_msgs.msg import Odometry
from sensor_msgs.msg import Range
from geometry_msgs.msg import PoseArray, Pose
from tf.transformations import euler_from_quaternion

from std_msgs.msg import String, Int32
from sensor_msgs.msg import BatteryState

from datetime import datetime
import time
import statistics as stc
from sys import exit

import os 

class globalPlanner:
    def __init__(self):
        # Tags
        self.land, self.takeoff, self.hover, self.sec = 100, 200, 300, 400

        # Flags
        self.log = 0
        self.pos = 0
        self.goToHome = 0
        self.letra = ""
        self.unic = {"SM": 0, "busy": 0, "print": 0, "hover": 0, "definirRota": 0, "sec": 0, "andar": 0}

        # Mapa
        self.a, self.b, self.a1, self.b1, self.a1b1 = [], [], [], [], [] # a,b = com capa | a1,b1 = sem capa

        # Variable Values
        self.altura = 3
        self.currentPosX, self.currentPosY, self.currentPosZ, self.currentPosYaw = 0, 0, 0, 0
        self.alturaLaser = 0

        # Trajectory
        self.rotas = {}
        
        # Values to be Changed by the User -> Insert the trajectory here
        path_out_a_estrela = os.path.dirname(os.path.abspath(__file__)) + "/trajetoria.csv"
        arquivo_trajetoria = np.genfromtxt(path_out_a_estrela, delimiter=',')

        
        path_obstaculos = os.path.dirname(os.path.abspath(__file__)) + "/obstaculos.csv"
        arquivo_obstaculos = np.genfromtxt(path_obstaculos, delimiter=',')
        
        self.rotas["x"] = list(arquivo_trajetoria[:, 0])
        self.rotas["y"] = list(arquivo_trajetoria[:, 1])
        self.rotas["z"] = list(arquivo_trajetoria[:, 2])
        self.rotas["yaw"] = list(arquivo_trajetoria[:, 3])
        print(self.rotas)
        #self.rotas["x"], self.rotas["y"] = suavizar_curva(list(self.rotas["x"]), list(self.rotas["y"]))
        #self.rotas["x"], self.rotas["y"], self.rotas["z"], self.rotas["yaw"] = diminuir_pontos(self.rotas["x"], self.rotas["y"], self.rotas["z"], self.rotas["yaw"], arquivo_obstaculos[:,0], arquivo_obstaculos[:,1])
        print(self.rotas)

        # Times
        self.counts = {"total": 0, "parar": 0, "tempo": 0}
        self.tempo = {"parar": 0, "takeoff": 6, "land": 6, "wait": 0, "hover": 5, "sec": 2}

        # Start
        self.counts["total"] = time.time()
        sleeping(t=1)

        # State Machine
        self.status = 2
        self.busy, self.arrived, self.idle = 1, 2, 3

        # Subscribers
        _ = rospy.Subscriber("/uav1/odometry/odom_main", Odometry, self.callbackPosicao)
        _ = rospy.Subscriber("/uav1/odometry/odom_local", Odometry, self.callbackMain)
        _ = rospy.Subscriber("/uav1/garmin/range", Range, self.callbackLaser)

        # decolagemInicial()
        print("Espere um momento, ja iremos comecar")
        rospy.sleep(2)
        self.unic["SM"] = 1
        set_vio()

    # ---------------------------- Loop :3 ----------------------------------
    def callbackMain(self, odom):

        if self.unic["SM"] == 1:     
            self.rotinaNormal()

    # ---------------------------- Altura de acordo com o laser ----------------------------------
    def callbackLaser(self, alt):
        self.alturaLaser = alt.range

    # ---------------------------- Onde o UAV ta ----------------------------------
    def callbackPosicao(self, odom):
        _, _, yaw = euler_from_quaternion([odom.pose.pose.orientation.x, odom.pose.pose.orientation.y, odom.pose.pose.orientation.z, odom.pose.pose.orientation.w])        
        if yaw < 0: yaw = math.pi + yaw
        
        self.currentPosX = odom.pose.pose.position.x 
        self.currentPosY = odom.pose.pose.position.y 
        self.currentPosZ = odom.pose.pose.position.z 
        self.currentPosYaw = yaw

    # ---------------------------- State Machine ----------------------------------
    def rotinaNormal(self):
        if self.unic["SM"] == 1: # Se tiver funcionando
            # ---------------- Decidindo sua vida ---------------------
            if self.status == self.arrived:
                self.unic["idle"] = 0
                print(self.pos) # DEBUG

                # ---------------- Cabou ---------------------
                if abs(self.currentPosX - self.rotas["x"][-1]) < 0.3 and abs(self.currentPosY - self.rotas["y"][-1]) < 0.3 and abs(self.currentPosZ - self.rotas["z"][-1]) < 0.3:
                #if abs(self.currentPosX - self.rotas["x"][-1]) < 0.3 and abs(self.currentPosY - self.rotas["y"][-1]) < 0.3: 
                    print("Tempo de voo: " + str(time.time() - self.counts["total"]))

                    self.unic["SM"] = 0
                    rospy.signal_shutdown("Acabou a missao")
                    exit()
                    return

                #---------------- Flag Start/End ---------------------
                elif self.rotas["x"][self.pos] == self.land:
                    self.unic["print"] = logstatemachine("Landing", self.unic["print"])
                    self.tempo["wait"] = self.tempo["land"]
                    land()

                elif self.rotas["x"][self.pos] == self.takeoff:
                    self.unic["print"] = logStateMachine("Take off", self.unic["print"])
                    self.tempo["wait"] = self.tempo["takeoff"]
                    takeoff()

                # ---------------- Flag Tempo ---------------------
                elif self.rotas["x"][self.pos] == self.hover:
                    self.unic["print"], self.unic["hover"] = logStateMachine("Hover", self.unic["print"], self.unic["hover"])
                    self.tempo["wait"] = self.tempo["hover"]

                elif self.rotas["x"][self.pos] == self.sec:
                    self.unic["print"], self.unic["sec"] = logStateMachine("Wait a second", self.unic["print"], self.unic["sec"])
                    self.tempo["wait"] = self.tempo["sec"]

                # ---------------- Puedo Caminar ---------------------
                else:
                    print("Indo para")
                    print(str(self.rotas["x"][self.pos]) + " - " + str(self.rotas["y"][self.pos]) + " - " + str(self.rotas["z"][self.pos]))
                    self.unic["print"], self.unic["andar"] = logStateMachine("Walking", self.unic["print"], self.unic["andar"])
                    self.tempo["wait"] = andarGlobal(self.rotas["x"][self.pos], self.rotas["y"][self.pos], self.rotas["z"][self.pos], self.rotas["yaw"][self.pos], self.currentPosX, self.currentPosY, self.currentPosZ, self.currentPosYaw)

                if self.unic["SM"] == 1:
                    self.counts["tempo"] = timeRos()
                    self.status = self.busy
            
            # ---------------- UAV ocupado ---------------------
            if self.status == self.busy:
                self.unic["print"] = 0
                self.unic["busy"] = logStateMachine("I am busy", self.unic["busy"])
                if timeRos() - self.counts["tempo"] > self.tempo["wait"]: 
                    self.status = self.idle
                    self.counts["parar"] = timeRos()

            # ---------------- UAV mudando de estado ---------------------
            if self.status == self.idle:
                if self.unic["hover"] == 1: self.unic["hover"] = 0
                if self.unic["sec"] == 1: self.unic["sec"] = 0

                self.unic["busy"] = 0
                self.unic["idle"] = logStateMachine("Idle", self.unic["idle"])
                if timeRos() - self.counts["parar"] > self.tempo["parar"]: 
                    self.status = self.arrived
                    if(self.pos == len(self.rotas['x'])-1): # Gambiarra para parar de dar erro...
                        self.pos = len(self.rotas['x'])-1
                    else:
                        self.pos += 1            

def main():
    rospy.init_node("Planejador")
    globalPlanner()
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    # plt.show()

if __name__ == "__main__":
    main()
