#include <ros/ros.h>
#include <string>
#include "./Vec4.h"
#include <nav_msgs/Odometry.h>

void CallbackOdometria(const nav_msgs::Odometry &msg);

int main(int argc, char** argv){
/*	
	bool sentido = true;

	// Parametros de geometria das prateleiras
	const float h = 1.7;
	const float w = 10;
	const float dh = 1;
	const float dw = 2;

	// Inicializa o no
	ros::init(argc, argv, "scan_prateleira");
	ros::NodeHandle nodeHandle("~");
	ros::Rate freq(0.5);

	std::string TOPICO_ODOM = "/uav1/control_manager/cmd_odom"; // MOD - Adicionar ao arquivo de parametros
	ros::Subscriber sub_odom = nodeHandle.subscribe<nav_msgs::Odometry>(TOPICO_ODOM, 10, &CallbackOdometria);
	
	// Servico para movimentar o uav
	std::string SERVICO_GOTO = "/uav1/control_manager/goto_fcu"; // MOD - Adicionar ao arquivo de parametros
	ros::ServiceClient srv_goto = nodeHandle.serviceClient<mrs_msgs::Vec4>(SERVICO_GOTO);
	mrs_msgs::Vec4 comando_posicao;
		
	// Loop
	while(nodeHandle.ok()){
	
		// Verifica se o uav ainda esta na area da prateleira (largura)
		if(!(y > w)){
			// Verifica se o uav saiu da area da prateleira (altura) e define a movimentacao horizontal
			if(z>h && sentido==true){
				sentido = !sentido; // Inverte o sentido vertical
				y += dw; // Incrementa a posicao horizontal
				comando_posicao.request.goal[1] = -dw; // Movimenta o uav na horizontal
			}
			else if(z-dh<0.1 && sentido==false){ // Verifica se o uav esta proximo ao solo
				sentido = !sentido; // Inverte o sentido vertical
				y+= dw; // Incrementa a posicao horizontal
				comando_posicao.request.goal[1] = -dw; // Movimenta o uav na horizontal
			}
			else comando_posicao.request.goal[1] = 0; // Mantem a movimentacao vertical

			// Define a movimentacao vertical
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
		srv_goto.call(comando_posicao);
		ROS_INFO_STREAM(comando_posicao.request); // DEBUG
	
	}	
*/	
	return 0;
}

void CallbackOdometria(const nav_msgs::Odometry &msg){
/*
	// Inicializacao
	float y = msg.pose.pose.position.y;
       	float z = msg.pose.pose.position.z;

*/

}
