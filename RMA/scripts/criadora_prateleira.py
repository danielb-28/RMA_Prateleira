exec(open('removedora_arquivos.py').read()) # Exclui arquivos anteriores
import random
import math
import qrcode as qr
import os
import shutil
import numpy as np
#-------------------CRIAÇÃO DO LAUNCH----------------------
launchInicio = "<launch>\n\
\n\
  <!-- these are the arguments you can pass this launch file, for example gui:=false -->\n\
  <arg name=\"paused\" default=\"false\" />\n\
  <arg name=\"use_sim_time\" default=\"true\" />\n\
  <arg name=\"extra_gazebo_args\" default=\"\" />\n\
  <arg name=\"gui\" default=\"true\" />\n\
  <arg name=\"headless\" default=\"false\" />\n\
  <arg name=\"debug\" default=\"false\" />\n\
  <arg name=\"physics\" default=\"ode\" />\n\
  <arg name=\"verbose\" default=\"true\" />\n\
\n\
    <!-- supply this argument to specify the world name within the worlds folder -->\n\
  <arg name=\"world_name\" default=\"fase1\" />\n\
\n\
    <!-- supply this argument to specity a world file -->\n\
  <arg name=\"world_file\" default=\"$(find robotica_movel)/worlds/$(arg world_name).world\" />\n\
\n\
  <!-- set use_sim_time flag -->\n\
  <group if=\"$(arg use_sim_time)\">\n\
    <param name=\"/use_sim_time\" value=\"true\" />\n\
  </group>\n\
\n\
  <!-- set command arguments -->\n\
  <arg unless=\"$(arg paused)\" name=\"command_arg1\" value=\"\" />\n\
  <arg     if=\"$(arg paused)\" name=\"command_arg1\" value=\"-u\" />\n\
  <arg unless=\"$(arg headless)\" name=\"command_arg2\" value=\"\" />\n\
  <arg     if=\"$(arg headless)\" name=\"command_arg2\" value=\"-r\" />\n\
  <arg unless=\"$(arg verbose)\" name=\"command_arg3\" value=\"\" />\n\
  <arg     if=\"$(arg verbose)\" name=\"command_arg3\" value=\"--verbose\" />\n\
  <arg unless=\"$(arg debug)\" name=\"script_type\" value=\"gzserver\" />\n\
  <arg     if=\"$(arg debug)\" name=\"script_type\" value=\"debug\" />\n\
\n\
	<include file=\"$(find mrs_simulation)/launch/mrs_drone_spawner.launch\" />\n\
    \n"

launchFim = "\n<!--<param name=\"robot_description\" command=\"$(find xacro)/xacro '$(find mybot_description)/urdf/mybot.xacro'\"/>\n\
<node name=\"mybot_spawn\" pkg=\"gazebo_ros\" type=\"spawn_model\" output=\"screen\"\n\
   args=\"-urdf -param robot_description -model mybot\" />-->\n\
\n\
    <!-- start gazebo server-->\n\
  <node name=\"gazebo\" pkg=\"gazebo_ros\" type=\"$(arg script_type)\" respawn=\"false\" output=\"screen\"\n\
    args=\"$(arg command_arg1) $(arg command_arg2) $(arg command_arg3) -e $(arg physics) $(arg extra_gazebo_args) $(arg world_file)\" />\n\
\n\
    <!-- start gazebo client -->\n\
  <group if=\"$(arg gui)\">\n\
    <node name=\"gazebo_gui\" pkg=\"gazebo_ros\" type=\"gzclient\" respawn=\"false\" output=\"screen\" />\n\
  </group>\n\
\n\
</launch>\n"

def launchTagsRFID(x,y,z, nome):
    return "\n\
<!-- Início da criação de tags-->\n\
<param name=\"tag_rfid\" command=\"$(find xacro)/xacro '$(find rfid_simulator_test)/urdf/tag/tag.urdf.xacro'\"/>\n\
    	<node name=\"spawn_gazebo_object" + str(nome) + "\" pkg=\"gazebo_ros\" type=\"spawn_model\"\n\
		args=\"-urdf -param tag_rfid -model tag" + str(nome) + " -x " + str(x) + " -y " + str(y) + " -z " + str(z) + "\" respawn=\"false\" output=\"screen\" />\n\
	<node pkg=\"tf\" type=\"static_transform_publisher\" name=\"tag" + str(nome) + "_to_map\" args=\"" + str(x) + " " + str(y) + " " + str(z) + " 0 0 0 1 map tag" + str(nome) + " 100\" />\n\
<!-- Até aqui (criação da tag " + str(nome) + ")-->\n\n"


#-------------------CRIAÇÃO DO MUNDO-----------------------
start = "<?xml version=\"1.0\" ?>\n\
<?xml-model href=\"http://sdformat.org/schemas/root.xsd\" schematypens=\"http://www.w3.org/2001/XMLSchema\"?>\n\
<sdf version=\"1.5\">\n\
  <world name=\"default\">\n"

pluginAttach = "<plugin name=\"mrs_gazebo_static_transform_republisher_plugin\" filename=\"libMRSGazeboStaticTransformRepublisher.so\"/>\n"

coordenadasSistema = "<spherical_coordinates> \n\
      <surface_model>EARTH_WGS84</surface_model>\n\
      <latitude_deg>47.397743</latitude_deg>\n\
      <longitude_deg>8.545594</longitude_deg>\n\
      <elevation>0.0</elevation>\n\
      <heading_deg>0</heading_deg>\n\
    </spherical_coordinates>\n"

physicsEngine = "<physics name=\"default_physics\" default=\"0\" type=\"ode\">\n\
      <gravity>0 0 -9.8066</gravity>\n\
      <ode>\n\
        <solver>\n\
          <type>quick</type>\n\
          <iters>10</iters>\n\
          <sor>1.3</sor>\n\
          <use_dynamic_moi_rescaling>0</use_dynamic_moi_rescaling>\n\
        </solver>\n\
        <constraints>z\n\
          <cfm>0</cfm>\n\
          <erp>0.2</erp>\n\
          <contact_max_correcting_vel>1000</contact_max_correcting_vel>\n\
          <contact_surface_layer>0.001</contact_surface_layer>\n\
        </constraints>\n\
      </ode>\n\
      <max_step_size>0.004</max_step_size>\n\
      <real_time_factor>1</real_time_factor>\n\
      <real_time_update_rate>250</real_time_update_rate>\n\
      <magnetic_field>6.0e-06 2.3e-05 -4.2e-05</magnetic_field>\n\
    </physics>\n"

shadown = "<scene>\n\
      <shadows>false</shadows>\n\
      <sky>\n\
        <clouds/>\n\
      </sky>\n\
    </scene>\n"

sol = "<light type=\"directional\" name=\"sun\">\n\
      <cast_shadows>true</cast_shadows>\n\
      <pose>250 250 600 0 0 0</pose>\n\
      <diffuse>0.8 0.8 0.8 1</diffuse>\n\
      <specular>0.2 0.2 0.2 1</specular>\n\
      <attenuation>\n\
        <range>1000</range>\n\
        <constant>0.9</constant>\n\
        <linear>0.01</linear>\n\
        <quadratic>0.001</quadratic>\n\
      </attenuation>\n\
      <direction>0 0 -1</direction>\n\
    </light>\n"

# groundPlane = "<model name=\"ground_plane\">\n\
#       <static>true</static>\n\
#       <link name=\"link\">\n\
#         <collision name=\"collision\">\n\
#           <pose>0 0 0 0 0 0</pose>\n\
#           <geometry>\n\
#             <plane>\n\
#           <pose>0 0 0 0 0 0</pose>\n\
#           <geometry>\n\
#             <plane>\n\
#               <normal>0 0 1</normal>\n\
#               <size>250 250</size>\n\
#             </plane>\n\
#           </geometry>\n\
#           <surface>\n\
#             <friction>\n\
#               <ode>\n\
#                 <mu>1</mu>\n\
#                 <mu2>1</mu2>\n\
#               </ode>\n\
#             </friction>\n\
#           </surface>\n\
#         </collision>\n\
#         <visual name=\"grass\">\n\
#           <pose>0 0 0 0 0 0</pose>\n\
#           <cast_shadows>false</cast_shadows>\n\
#           <geometry>\n\
#             <mesh>\n\
#               <uri>file://grass_plane/meshes/grass_plane.dae</uri>\n\
#             </mesh>\n\
#           </geometry>\n\
#         </visual>\n\
#       </link>\n\
#     </model>\n"

groundPlane = "<model name='chao_metalico'>\n\
           <scale>10 10 0.01</scale>\n\
            <include>\n\
      <pose>0 0 0 0 0 0</pose>\n\
      <uri>model://chaoMetal</uri>\n\
    </include>\n\
          </model>\n"

# groundPlane = "<include>\n\
#       <uri>model://ground_plane</uri>\n\
#     </include>\n\
#     <include>\n\
#       <uri>model://asphalt_plane</uri>\n\
#     </include>\n"

# groundPlane = "<model name='ground_plane'>\n\
#       <static>1</static>\n\
#       <link name='link'>\n\
#         <collision name='collision'>\n\
#           <geometry>\n\
#             <plane>\n\
#               <normal>0 0 1</normal>\n\
#               <size>100 100</size>\n\
#             </plane>\n\
#           </geometry>\n\
#           <surface>\n\
#             <friction>\n\
#               <ode>\n\
#                 <mu>100</mu>\n\
#                 <mu2>50</mu2>\n\
#               </ode>\n\
#               <torsional>\n\
#                 <ode/>\n\
#               </torsional>\n\
#             </friction>\n\
#             <contact>\n\
#               <ode/>\n\
#             </contact>\n\
#             <bounce/>\n\
#           </surface>\n\
#           <max_contacts>10</max_contacts>\n\
#         </collision>\n\
#         <visual name='visual'>\n\
#           <cast_shadows>0</cast_shadows>\n\
#           <geometry>\n\
#             <plane>\n\
#               <normal>0 0 1</normal>\n\
#               <size>100 100</size>\n\
#             </plane>\n\
#           </geometry>\n\
#           <material>\n\
#             <script>\n\
#               <uri>file://media/materials/scripts/gazebo.material</uri>\n\
#               <name>Gazebo/Pink</name>\n\
#             </script>\n\
#           </material>\n\
#         </visual>\n\
#         <self_collide>0</self_collide>\n\
#         <kinematic>0</kinematic>\n\
#         <gravity>1</gravity>\n\
#       </link>\n\
#     </model>\n"

# -----------------------------------------------------------------------------------
    
cameraSpawnObjects = "<model name='the_void'>\n\
      <static>1</static>\n\
      <link name='link'>\n\
        <pose frame=''>0 0 0.1 0 -0 0</pose>\n\
        <visual name='the_void'>\n\
          <pose frame=''>0 0 2 0 -0 0</pose>\n\
          <geometry>\n\
            <sphere>\n\
              <radius>0.25</radius>\n\
            </sphere>\n\
          </geometry>\n\
          <material>\n\
            <script>\n\
              <uri>file://media/materials/scripts/Gazebo.material</uri>\n\
              <name>Gazebo/Black</name>\n\
            </script>\n\
          </material>\n\
        </visual>\n\
        <self_collide>0</self_collide>\n\
        <enable_wind>0</enable_wind>\n\
        <kinematic>0</kinematic>\n\
      </link>\n\
      <pose frame=''>-1000 -1000 0 0 0 0</pose>\n\
    </model>\n"

userCameraCima = "<gui>\n\
      <camera name=\"camera\">\n\
        <pose>45 25 100 0 1.57 1.57</pose>\n\
      </camera>\n\
    </gui>\n"

userCameraFrente = "<gui>\n\
      <camera name=\"camera\">\n\
        <pose>8 -15 6 0 0.1 1.57</pose>\n\
      </camera>\n\
    </gui>\n"

guiFrameSinc = "<plugin name=\"mrs_gazebo_rviz_cam_synchronizer\" filename=\"libMRSGazeboRvizCameraSynchronizer.so\" >\n\
      <target_frame_id>gazebo_user_camera</target_frame_id>\n\
      <world_origin_frame_id>uav1/gps_origin</world_origin_frame_id>\n\
      <frame_to_follow>uav1::base_link</frame_to_follow>\n\
    </plugin>\n"

end = "</world>\n\
</sdf>\n"

# -----------------------------------------------------------------------------------

def qrcode(px, py, pz, nObjeto, pr=math.pi, pp=0, pyaw=0, sx=1.7, sy=1.7, sz=0.2):
#  if nObjeto == 1:
  pyaw = -math.pi/2 if pr == math.pi/2 else math.pi/2
  py += 0.015 if pr == math.pi/2 else -0.015
  return "<model name='qrcode" + str(nObjeto) + "'>\n\
           <scale>" + str(sx) + " " + str(sy) + " " + str(sz) + "</scale>\n\
            <include>\n\
      <pose>" + str(px) + " " + str(py) + " " + str(pz) +  " " + str(pr) +  " " + str(pp) +  " " + str(pyaw+math.pi) + "</pose>\n\
      <uri>model://qrcode" + str(nObjeto) + "</uri>\n\
    </include>\n\
          </model>\n"

# def qrcode(px, py, pz, n, nObjeto, pr=0, pp=0, pyaw=0, sx=1.7, sy=1.7, sz=0.2):
#     return "<model name='qrcode" + str(nObjeto) + "_" + str(n) +"'>\n\
#         <pose frame=''>" + str(px) + " " + str(py) + " " + str(pz) +  " " + str(pr) +  " " + str(pp) +  " " + str(pyaw) + "</pose>\n\
#         <link name='link_A_" + str(n) +"'>\n\
#         <visual name='visual'>\n\
#             <pose frame=''>0 0 0 0 0 0</pose>\n\
#             <geometry>\n\
#             <mesh>\n\
#                 <uri>model://qrcode" + str(nObjeto) + "/meshes/equipment_A.obj</uri>\n\
#                 <scale>" + str(sx) + " " + str(sy) + " " + str(sz) + "</scale>\n\
#             </mesh>\n\
#             </geometry>\n\
#             <transparency>0</transparency>\n\
#             <cast_shadows>1</cast_shadows>\n\
#         </visual>\n\
#         <collision name='collision'>\n\
#             <laser_retro>0</laser_retro>\n\
#             <max_contacts>10</max_contacts>\n\
#             <pose frame=''>0 0 0.05 0 -0 0</pose>\n\
#             <geometry>\n\
#             <box>\n\
#                 <size>0.1 0.1 0.1</size>\n\
#             </box>\n\
#             </geometry>\n\
#             </collision>\n\
#         </link>\n\
#         <static>1</static>\n\
#         <allow_auto_disable>1</allow_auto_disable>\n\
#     </model>\n"

def cardbox(px, py, pz, n, pr=0, pp=0, pyaw=0, sx=1.2, sy=1.0, sz=0.75):
    return "<model name='cardboard_box_" + str(n) +"'>\n\
        <pose>" + str(px) + " " + str(py) + " " + str(pz) +  " " + str(pr) +  " " + str(pp) +  " " + str(pyaw) + "</pose>\n\
        <link name='link_" + str(n) +"'>\n\
        <collision name='collision'>\n\
            <geometry>\n\
            <box>\n\
                <size>0.7 0.7 0.7</size>\n\
            </box>\n\
            </geometry>\n\
        </collision>\n\
        <visual name='visual'>\n\
            <pose>0 0 0 0 0 0</pose>\n\
            <geometry>\n\
            <mesh>\n\
                <uri>model://cardboard_box/meshes/cardboard_box.dae</uri>\n\
                <scale>" + str(sx) + " " + str(sy) + " " + str(sz) + "</scale>\n\
            </mesh>\n\
            </geometry>\n\
        </visual>\n\
        </link>\n\
        <static>1</static>\n\
    </model>\n"

def shelf(px, py, pz, n, p1, pr=0, pp=0, pyaw=0):
  if p1:
    return "<model name='wire_shelf_" + str(n) + "'>\n\
            <include>\n\
      <pose>" + str(px) + " " + str(py) + " " + str(pz) +  " " + str(pr) +  " " + str(pp) +  " " + str(pyaw) + "</pose>\n\
      <uri>model://bookshelf_large</uri>\n\
    </include>\n\
          </model>\n"
  else:
    return "<model name='wire_shelf_" + str(n) + "'>\n\
            <include>\n\
      <pose>" + str(px+0.12) + " " + str(py) + " " + str(pz) +  " " + str(pr) +  " " + str(pp) +  " " + str(pyaw+math.pi) + "</pose>\n\
      <uri>model://bookshelf_large</uri>\n\
    </include>\n\
          </model>\n"
#--------------------------------------------------------CRIAÇÃO DO MAPA------------------------------------------------------------
resolucao = 3
def mapaInicio(Xdim, Ydim):
  Xdim = math.ceil(Xdim)
  Ydim = math.ceil(Ydim)
  escrever = "P2 \n\
# Created by GIMP version 2.10.18 PNM plug-in\n\
" + str(Xdim) + " " + str(Ydim) + "\n255\n"
  return escrever

def retangulo(vetor, Xinicio, Yinicio):
    for j in range(1*resolucao+1):
        for i in range(4*resolucao):
            vetor[math.ceil(Xinicio*resolucao+i)][math.ceil(Yinicio*resolucao+j-1)] = 0
    return vetor
#-------------------------------------------------------------Main------------------------------------------------------------------
#def Alturas(quantidade_prateleiras, altura_inicial = 0.05, passo_altura = 0.45):
#  alturas = []
#  for i in range(quantidade_prateleiras):
#    alturas.append(altura_inicial + i*passo_altura)
#  return alturas

# o ideal seria fazer algumas restricoes nesse quantidade de blocos 
# pra evitar q as caixas se sobreponham
quantidade_blocos = 3        # Quantidade de blocos de fileiras
quantidade_fileiras = 8       # Quantidade de fileiras por bloco (Y)
comprimento_fileira = 5       # Comprimento em x*3.32 de cada fileira (X)
quantidade_prateleiras = 3    # Quantidade de prateleiras (empilhadas) em cada fileira, até 8
andar2 = True if quantidade_prateleiras > 4 else False  # prateleira em cima de prateleira
#alturas = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]     # Altura das caixas, da mais baixa até a mais alta, observe que deve haver alturas de acordo com a quantidade de prateleiras configuradas [0.3, 1.6, 2.8]
#alturas = Alturas(quantidade_prateleiras)         # Função que cria as alturas automaticamente de acordo com a quantidade de prateleiras, a altura inicial e a altura de cada prateleira


alturas = [0.1, 0.99, 1.86, 2.735, 3.69, 4.58, 5.45, 6.33]  
#caixas_fileira = 1           # Porcentagem de caixas ocupando a totalidade do depósito. Substituído por parâmetro aleatorizador

p1 = False                    # Primeira fileira virada para fora (True)
count = 1
tam_corredorHorizontal = 6    # Tamanho do corredor entre as fileiras de mesma orientação (Nesse corredor ainda existe uma fileira virada para o outro lado)
tam_corredorVertical = 4      # Tamanho do corredor entre os blocos de fileiras
Yinicial = 5 + 0.425          # Localização Y do centro da primeira prateleira (o ajuste de 0.425 se dá por conta do centro da prateleira)
Xinicial = 5 + 1.6            # Localização X do centro da primeira prateleira (o ajuste de 1.6 se dá por conta do centro da prateleira)

localizacaoProduto = []
localizacaoDrone = []
caixas_prateleira = 2         # Cada estante em uma fileira admite de uma a duas caixas em suas prateleiras
nCaixas = quantidade_blocos*quantidade_fileiras*comprimento_fileira*quantidade_prateleiras*caixas_prateleira

nomeLaunch = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/launch/simulation_arena")
arquivoLaunch = open(nomeLaunch + ".launch", "w")
arquivoLaunch.write(launchInicio)

nomeMundo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "worlds/prateleira")
arquivoMundo = open(nomeMundo + ".world", "w")
arquivoMundo.write(start)
arquivoMundo.write(pluginAttach)
arquivoMundo.write(coordenadasSistema)
arquivoMundo.write(physicsEngine)
arquivoMundo.write(shadown)
arquivoMundo.write(sol)
arquivoMundo.write(groundPlane)

arquivoMapa = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapa.pgm"), "w")
Xdim = math.ceil(Xinicial + (quantidade_blocos)*(comprimento_fileira*3 + tam_corredorVertical))*resolucao
Ydim = math.ceil(Yinicial + quantidade_fileiras*4)*resolucao
arquivoMapa.write(mapaInicio(Xdim, Ydim))
Mapa = np.zeros((Xdim, Ydim)) + 255

checkpoints = []
# inserir prateleiras aki

for qb in range(quantidade_blocos):     # Cria os blocos de fileiras, ganhando tamanho em x
  y = Yinicial                          # Reseta a localização y para que todos os blocos tenho começo igual

  for qf in range(quantidade_fileiras): # Cria cada fileira em um bloco, ganhando tamanho em y

      for cf in range(comprimento_fileira): # Cria cada prateleira em uma fileira, delimitando o comprimento em x de cada fileira

          arquivoMundo.write(shelf(Xinicial + cf*2.428+qb*(comprimento_fileira*3+tam_corredorVertical),y,0,count,p1))     # Escreve cada prateleira no arquivo do mundo
          Mapa = retangulo(Mapa, (Xinicial-1.6) + cf*2.4+qb*(comprimento_fileira*3+tam_corredorVertical), (y-0.425))      # Escreve os obstáculos no arquivo de mapa usado pelo A*
          if p1:                                                                                                          # Define a orientação das prateleiras
            if cf == 0:                                                                                                   # Pega a primeira prateleira para criar o checkpoint
              checkpoints.append([Xinicial + qb*(comprimento_fileira*3+tam_corredorVertical)-1.2, y-1.6, 1.5, math.pi/2])                  # Escreve o checkpoint no início (no sentido de x) do corredor entre as fileiras
              # arquivoMundo.write(qrcode(Xinicial + qb*(comprimento_fileira*3+tam_corredorVertical)-1.2, y-1.6, 1.5,nObjeto = count, pr=math.pi/2))   # Conferir localização dos checkpoints
          else:
            if cf == comprimento_fileira-1:                                                                             # Pega a última prateleira para criar o checkpoint
              checkpoints.append([Xinicial + cf*2.428+qb*(comprimento_fileira*3+tam_corredorVertical)+1.2, y+1.6, 1.5, -math.pi/2])                 # Escreve o checkpoint no fim (no sentido de x) do corredor entre as fileiras
              # arquivoMundo.write(qrcode(Xinicial + cf*2.428+qb*(comprimento_fileira*3+tam_corredorVertical)+1.2, y+1.6, 1.5,nObjeto = count, pr=-math.pi/2))   # Conferir localização dos checkpoints
          if andar2:                                                                                                      # Executa caso haja mais de 4 caixas a serem empilhadas
            arquivoMundo.write(shelf(Xinicial + cf*2.428+qb*(comprimento_fileira*3+tam_corredorVertical),y,3.59,count*-1,p1))   # escreve a prateleira acima no arquivo do mundo

          for qp in range(quantidade_prateleiras):                                                                        # Roda a altura da criação das caixas em uma fileira

              for nc in range(caixas_prateleira):                                                                         # Roda a posição x da criação das caixas em uma fileira
                ocupacao_caixas = random.uniform(0.3, 1)                                                                  # Aleatoriza a quantidade de caixas por fileira
                if random.random() < ocupacao_caixas:
                    aux_x = random.uniform(-0.25, 0.3)                                                                    # Define um espaço x onde a caixa pode ser gerada aleatoriamente
                    x_pos = Xinicial + (cf*2.428) + aux_x + qb*(comprimento_fileira*3+tam_corredorVertical) + (nc%2)*1.2 - 0.6    # Posição x de cada caixa e QrCode
                    arquivoMundo.write(cardbox(x_pos,y,alturas[qp],count, sx=1.6, sy=1.6, sz=1.6))                        # Escreve a caixa no arquivo do mundo
                    if p1:                                                                                                # Define a orientação do QrCode, e a posição do RFID
                        arquivoMundo.write(qrcode(x_pos, y-0.3, alturas[qp]+0.36, nObjeto= count, pr=-math.pi/2))         # Escreve o QrCode no arquivo do mundo
                        # arquivoLaunch.write(launchTagsRFID(x_pos, y-0.3, alturas[qp]+0.36, count))                      # Escreve o RFID no launch
                        localizacaoProduto.append([count, x_pos, y-0.3, alturas[qp]+0.36])                                # Escreve a localização de onde o drone deve estar para ler o QrCode
                        localizacaoDrone.append([count, x_pos, y-1.6, alturas[qp]+0.36, math.pi/2])                       # Escreve a localização de onde o drone deve estar para ler o QrCode
                    else:
                        arquivoMundo.write(qrcode(x_pos, y+0.3, alturas[qp]+0.36, nObjeto= count, pr=math.pi/2))          # Escreve o QrCode no arquivo do mundo
                        # arquivoLaunch.write(launchTagsRFID(x_pos, y+0.3, alturas[qp]+0.36, count))                      # Escreve o RFID no launch
                        localizacaoProduto.append([count, x_pos,y+0.3,alturas[qp]+0.36])                                  # Escreve a localização do QrCode
                        localizacaoDrone.append([count, x_pos,y+1.6,alturas[qp]+0.36, -math.pi/2])                        # Escreve a localização de onde o drone deve estar para ler o QrCode
                    count += 1                                                                                            # Conta qual produto (caixa-QrCode) foi criado
      if p1:                              # Troca orientação da próxima fileira e as caixas e QrCodes que ela contém
          y += 1                          # Distancia uma fileira de costas para outra
          p1 = False
      else:
          y += tam_corredorHorizontal     # Distancia uma fileira de frente para outra criando um corredor horizontal
          p1 = True 

Mapa = Mapa.T
for i in range(len(Mapa)):
    Mapa[-i-1][0] = 0
    Mapa[-i-1][Xdim-1] = 0
    for j in range(len(Mapa[0])):
      Mapa[Ydim-1][j] = 0
      # Mapa[0][j] = 0
      arquivoMapa.write(str(round(Mapa[-i-1][j])) + '\n')
arquivoMapa.close()

arquivoLaunch.write(launchFim)
arquivoLaunch.close()

arquivoMundo.write(cameraSpawnObjects)

arquivoMundo.write(userCameraCima)
# arquivoMundo.write(userCameraFrente)

arquivoMundo.write(guiFrameSinc)
arquivoMundo.write(end)
arquivoMundo.close()

arquivoProdutos = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "localizacao_produtos_gerados.csv"), "w")
for i in range(len(localizacaoProduto)):
  for j in range(len(localizacaoProduto[0])):
    if j == len(localizacaoProduto[0])-1:
      arquivoProdutos.write(str(localizacaoProduto[i][j]) + '\n')
    else:
      arquivoProdutos.write(str(localizacaoProduto[i][j]) + ',')
arquivoProdutos.close()

arquivoProdutos = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "localizacao_produtos.csv"), "w")
for i in range(len(localizacaoProduto)):
  for j in range(len(localizacaoProduto[0])-1):
    if j == len(localizacaoProduto[0])-2:
      arquivoProdutos.write(str(localizacaoProduto[i][j+1]) + '\n')
    else:
      arquivoProdutos.write(str(localizacaoProduto[i][j+1]) + ',')

arquivoProdutos.close()
arquivoCheckpoints = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "localizacao_checkpoints.csv"), "w")
#arquivoCheckpoints.write('X, Y, Z, Orientação\n')
for i in range(len(checkpoints)):
  arquivoCheckpoints.write(str(checkpoints[i][0]) + ',' + str(checkpoints[i][1]) + ',' + str(checkpoints[i][2]) + ',' + str(checkpoints[i][3]) + '\n')

arquivoDrone = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pontos.csv"), "w")
for i in range(len(localizacaoDrone)):
  for j in range(len(localizacaoDrone[0])-1):
    if j == len(localizacaoDrone[0])-2:
      arquivoDrone.write(str(localizacaoDrone[i][j+1]) + '\n')
    else:
      arquivoDrone.write(str(localizacaoDrone[i][j+1]) + ',')
arquivoDrone.close()

pastaCopia = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'qrcode1')
enderecoQR = os.path.join('meshes','materials','qr.png')
# imagem = qr.make('Salve o glorioso João Carlos Tonon Campi')
# imagem.save(os.path.join(pastaCopia, enderecoQR))
imagem = qr.make('1')
imagem.save(os.path.join(pastaCopia, enderecoQR))

for qb in range(nCaixas-1):
  pastaCola = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'qrcode' + str(qb+2))
  if os.path.isdir(pastaCola):
    shutil.rmtree(pastaCola)
    
for qb in range(nCaixas-1):
  pastaCola = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'qrcode' + str(qb+2))
  shutil.copytree(pastaCopia, pastaCola)
  # imagem = qr.make('produto ' + str(qb+2))
  imagem = qr.make(str(qb+2))
  imagem.save(os.path.join(pastaCola, enderecoQR))
  
  with open(pastaCola + '/model.sdf', 'r') as arquivo:
    linhas = arquivo.readlines() #cada linha é um elemento da lista linhas
  # editando a linha
  linhas[21] = '            <uri>model://qrcode' + str(qb+2) +'/meshes/t1.dae</uri>\n'
  # escrevendo de novo
  with open(pastaCola + '/model.sdf', 'w') as arquivo:
    arquivo.writelines(linhas)

print('\nPrateleiras criadas com sucesso, divirta-se! Mas se lembre que João Carlos Tonon Campi está de olho nas suas travessuras...')