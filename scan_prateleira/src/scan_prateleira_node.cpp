#include <ros/ros.h>
#include <string>
#include "./Vec4.h"
#include <mrs_msgs/ControlManagerDiagnostics.h>
#include <mrs_msgs/Vec1.h>

void CallbackDiagnostico(const mrs_msgs::ControlManagerDiagnostics& msg);
void UpdateEstado();

bool flag_mov_completo = false;

int estado_atual = 0;
int prateleira_atual = 0;

ros::ServiceClient srv_goto_altitude;
ros::ServiceClient srv_goto_fcu;
mrs_msgs::Vec4 comando_posicao;
mrs_msgs::Vec1 comando_altitude;

ros::Subscriber sub_diag;

// Inicializacao
bool sentido = false;

// Parametros de geometria das prateleiras
const float w = 13;
const float alturas[4] = {2.0, 1.1, 2.8};

int main(int argc, char** argv){

	ros::init(argc, argv, "scan_prateleira");
	ros::NodeHandle nodeHandle("~");
	ros::Rate freq(0.5);
	
	std::string SERVICO_GOTO_ALTITUDE = "/uav1/control_manager/goto_altitude"; // MOD - Adicionar ao arquivo de parametros
	std::string SERVICO_GOTO_FCU = "/uav1/control_manager/goto_fcu"; // MOD - Adicionar ao arquivo de parametros
	srv_goto_altitude = nodeHandle.serviceClient<mrs_msgs::Vec1>(SERVICO_GOTO_ALTITUDE);
	srv_goto_fcu = nodeHandle.serviceClient<mrs_msgs::Vec4>(SERVICO_GOTO_FCU);


	std::string TOPICO_DIAGNOSTICO = "/uav1/control_manager/diagnostics"; 
	sub_diag = nodeHandle.subscribe(TOPICO_DIAGNOSTICO, 10, CallbackDiagnostico);
		
	ros::spin();

	return 0;
}

void CallbackDiagnostico(const mrs_msgs::ControlManagerDiagnostics &msg){
	flag_mov_completo = !msg.tracker_status.have_goal;
	if(flag_mov_completo) UpdateEstado();
	return;
}

void UpdateEstado(){
		
	int mov = 0;
	if(!(estado_atual%2)){
		mov = 0;
		sentido = !sentido;
	}
	else{
		if(estado_atual <= 6){
		mov = 1;
		}

		else{
			mov = 2;
		}
	}
	
	switch(mov){
		case 0:
			if(sentido) comando_posicao.request.goal[1] = -w;
			else comando_posicao.request.goal[1] = w;
  			
			comando_posicao.request.goal[2] = 0;
			
			srv_goto_fcu.call(comando_posicao);

			break;

		case 1:
			prateleira_atual++;

			//comando_posicao.request.goal[1] = 0.0;
  			//comando_posicao.request.goal[2] = dh;
			comando_altitude.request.goal = alturas[prateleira_atual];

			//srv_goto_fcu.call(comando_posicao);
			srv_goto_altitude.call(comando_altitude);

			break;

		case 2:

			//comando_altitude.request.goal = 0.6;
			prateleira_atual = 0;
			comando_altitude.request.goal = alturas[0];
			srv_goto_altitude.call(comando_altitude);
			
			break;
		
	}

	ROS_INFO_STREAM("ESTADO/MOVIMENTO:	" << estado_atual << "/" << mov);


	if(estado_atual <= 6) estado_atual++;
	//else estado_atual = 0;
	else ros::shutdown();
	
}
