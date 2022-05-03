import sys
from std_srvs.srv import Trigger, SetBool, SetBoolRequest
from mrs_msgs.srv import ReferenceStampedSrv, ReferenceStampedSrvResponse, ReferenceStampedSrvRequest, StringRequest, String, Float64Srv, Float64SrvRequest
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest
import rospy
import math
from dynamic_reconfigure.srv import ReconfigureRequest, Reconfigure
from dynamic_reconfigure.parameter_generator import *

from gazebo_msgs.srv import GetModelState
from utils import rotacionar

from os import environ

def decolagemInicial():
    rospy.wait_for_service("/uav1/mavros/cmd/arming")
    try:
        ola = rospy.ServiceProxy("/uav1/mavros/cmd/arming", CommandBool)
        req = CommandBoolRequest()
        req.value = 1
        resp = ola(req)
        # rospy.loginfo(resp)
    except rospy.ServiceException as e:
        print("Falha na chamada de servico: %s"%e)
    
    rospy.wait_for_service("/uav1/mavros/set_mode")
    try:
        ola = rospy.ServiceProxy("/uav1/mavros/set_mode", SetMode)
        req = SetModeRequest()
        req.base_mode = 0
        req.custom_mode = "offboard"
        resp = ola(req)
        # rospy.loginfo(resp)
    except rospy.ServiceException as e:
        print("Falha na chamada de servico: %s"%e)

    rospy.wait_for_service("/uav1/control_manager/use_safety_area")
    try:
        ola = rospy.ServiceProxy("/uav1/control_manager/use_safety_area", SetBool)
        req = SetBoolRequest()
        req.data = False
        resp = ola(req)
        # rospy.loginfo(resp)
    except rospy.ServiceException as e:
        print("Falha na chamada de servico: %s"%e)

    rospy.wait_for_service("/uav1/control_manager/set_min_height")
    try:
        ola = rospy.ServiceProxy("/uav1/control_manager/set_min_height", Float64Srv)
        req = Float64SrvRequest()
        req.value = 0
        resp = ola(req)
        rospy.loginfo(resp)
    except rospy.ServiceException as e:
        print("Falha na chamada de servico: %s"%e)

def set_vio(estimador="BARO"):
    rospy.wait_for_service("/uav1/odometry/change_alt_estimator_type_string")
    try:
        ola = rospy.ServiceProxy("/uav1/odometry/change_alt_estimator_type_string", String)
        req = StringRequest()
        req.value = estimador
        resp = ola(req)
        # rospy.loginfo(resp)
    except rospy.ServiceException as e:
        print("Falha na chamada de servico: %s"%e)

def euclidiana(x, y, z=0, currentPosX=0, currentPosY=0, currentPosZ=0, currentPosYaw=0, yaw=0):
    vel = math.sqrt(math.pow(currentPosX - x, 2) + math.pow(currentPosY - y, 2) + math.pow(currentPosZ - z, 2))
    return vel

class parametroDouble: 
    def __init__(self, name, value):
        self.name = name
        self.value = value

def setDoubleParameter(option=["kiwxy"], value=[0.1]):
    # option can be kiwxy, kibxy, km
    rospy.wait_for_service("/uav1/control_manager/mpc_controller/set_parameters")
    try:
        ola = rospy.ServiceProxy("/uav1/control_manager/mpc_controller/set_parameters", Reconfigure)
        req = ReconfigureRequest()
        req.config.doubles = []
        for a, b in zip(option, value):
            parameter = parametroDouble(a, b)
            req.config.doubles.append(parameter)
        resp = ola(req)
        # rospy.loginfo(resp)
    except rospy.ServiceException as e:
        print("Falha na chamada de servico: %s"%e)

def addRotaPonto(ponto, vx, vy, rotax, rotay, rotaz, rotayaw, vz=3.2, vyaw=0):
    rotax.insert(ponto, vx)
    rotay.insert(ponto, vy)
    rotaz.insert(ponto, vz)
    rotayaw.insert(ponto, vyaw)
    return rotax, rotay, rotaz, rotayaw

def dist_euclidiana(v1, v2):
	dim, soma = len(v1), 0
	for i in range(dim):
		soma += math.pow(v1[i] - v2[i], 2)
	return math.sqrt(soma)

def addRota(vx, vy, rotax, rotay, rotaz, rotayaw, vz=3.2, vyaw=0):
    rotax.append(vx)
    rotay.append(vy)
    rotaz.append(vz)
    rotayaw.append(vyaw)
    return rotax, rotay, rotaz, rotayaw

def addTag(tag, rotax, rotay, rotaz, rotayaw):
    rotax.append(tag)
    rotay.append(500)
    rotaz.append(500)
    rotayaw.append(500)
    return rotax, rotay, rotaz, rotayaw

def logStateMachine(frase, condicao, extra=None):
    if condicao == 0 and len(frase) > 0: print(frase)
    return 1 if extra == None else 1, 1
    
def melhorRota(x, y, posX, posY):
    camFinalX = [posX]
    camFinalY = [posY]
    distancias = []

    while len(x) >= 1:
        d = float("inf")
        coord, index = [], 0
        for i in range(len(x)):
            dist = dist_euclidiana([camFinalX[-1], camFinalY[-1]], [x[i], y[i]])
            if dist < d:
                index = i
                coord = [x[i], y[i]]
                d = dist
        del x[index]
        del y[index]

        distancias.append(d)
        camFinalX.append(coord[0])
        camFinalY.append(coord[1])

    return camFinalX[1:], camFinalY[1:]

def takeoff():
    rospy.wait_for_service("/uav1/uav_manager/takeoff")
    try:
        ola = rospy.ServiceProxy("/uav1/uav_manager/takeoff", Trigger)
        ola()
    except rospy.ServiceException as e:
        print("Falha na chamada de servico: %s"%e)

def land():
    rospy.wait_for_service("/uav1/uav_manager/land")
    try:
        ola = rospy.ServiceProxy("/uav1/uav_manager/land", Trigger)
        ola()
    except rospy.ServiceException as e:
        print("Falha na chamada de servico: %s"%e)

def andarGlobal(x, y, z, rand, currentPosX, currentPosY, currentPosZ, currentPosYaw):
    rospy.wait_for_service("/uav1/control_manager/reference")
    #rand = rotacionar(currentPosX, currentPosY, x, y)
    
    try:
        ola = rospy.ServiceProxy("/uav1/control_manager/reference", ReferenceStampedSrv)
        req = ReferenceStampedSrvRequest()
        req.reference.position.x = x 
        req.reference.position.y = y 
        req.reference.position.z = z
        req.reference.heading = rand
        resp = ola(req)
        # rospy.loginfo(resp)
    except rospy.ServiceException as e:
        print("Falha na chamada de servico: %s"%e)

    return euclidiana(x, y, z, currentPosX, currentPosY, currentPosZ, currentPosYaw) 

def andarLocal(x, y, z, rand, currentPosX, currentPosY, currentPosZ, currentPosYaw):
    rospy.wait_for_service("/uav1/control_manager/reference")
    try:
        ola = rospy.ServiceProxy("/uav1/control_manager/reference", ReferenceStampedSrv)
        req = ReferenceStampedSrvRequest()
        req.reference.position.x = currentPosX - x
        req.reference.position.y = y + currentPosY
        req.reference.position.z = z + currentPosZ
        req.reference.heading = rand + currentPosYaw
        resp = ola(req)
        # rospy.loginfo(resp)
    except rospy.ServiceException as e:
        print("Falha na chamada de servico: %s"%e)
    
    return euclidiana(x, y, z, currentPosX, currentPosY, currentPosZ, currentPosYaw) 

def zerarTwist(valorTwist):
    valorTwist.angular.x = 0
    valorTwist.angular.y = 0
    valorTwist.angular.z = 0
    valorTwist.linear.x = 0
    valorTwist.linear.y = 0
    valorTwist.linear.z = 0

    return valorTwist

def criar_reta(x1, y1, x2, y2):
    delta_y = y2 - y1
    delta_x = x2 - x1
    
    if delta_x == 0:
        m = 0
    else:
        m = delta_y / delta_x # equivalente a a
        
    angulo = math.atan2(delta_x, delta_y)
    n = y2 - (m * x2)     # equivalente a c
    # b sempre vai ser -1

    return m, n, angulo

def sleeping(t=5):
    rospy.sleep(t)

def timeRos():
    return rospy.get_rostime().secs + (rospy.get_rostime().nsecs/1e9)
