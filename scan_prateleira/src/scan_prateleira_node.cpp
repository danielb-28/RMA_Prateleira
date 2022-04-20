#include <ros/ros.h>
#include <string>
#include "./Vec4.h"

int main(int argc, char** argv){

	// Inicializacao
	float y = 0.0;
       	float z = 0.8;
	bool sentido = true;

	// Parametros de geometria das prateleiras
	const float h = 1.7;
	const float w = 40;
	const float dh = 0.3;
	const float dw = 1.2;

	ros::init(argc, argv, "scan_prateleira");
	ros::NodeHandle nodeHandle("~");
	ros::Rate freq(0.5);
	
	std::string SERVICO_GOTO = "/uav1/control_manager/goto_fcu"; // MOD - Adicionar ao arquivo de parametros
	ros::ServiceClient srv_goto = nodeHandle.serviceClient<mrs_msgs::Vec4>(SERVICO_GOTO);
	mrs_msgs::Vec4 comando_posicao;
		
	while(nodeHandle.ok()){
	
		if(!(y > w)){
			if(z>h && sentido==true){
				sentido = !sentido;
				y += dw;
				comando_posicao.request.goal[1] = -dw;
			}
			else if(z-dh<1 && sentido==false){
				sentido = !sentido;
				y+= dw;
				comando_posicao.request.goal[1] = -dw;
			}
			else comando_posicao.request.goal[1] = 0;

			if(sentido) {
				z += dh;
				comando_posicao.request.goal[2] = dh;
			}
			else {
				z -= dh;
				comando_posicao.request.goal[2] = -dh;
			}	
		
		}

		else continue; 

		freq.sleep();
	
		comando_posicao.request.goal[0] = 0.0;
		comando_posicao.request.goal[3] = 0.0;
		ROS_INFO_STREAM(comando_posicao.request);
		srv_goto.call(comando_posicao);
	
	}	
	
	return 0;
}
