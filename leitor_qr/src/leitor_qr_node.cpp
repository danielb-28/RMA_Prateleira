#include <ros/ros.h>
#include "../include/leitor_qr/LeitorQR.hpp"

int main(int argc, char** argv) {
	ros::init(argc, argv, "leitor_qr");
	ros::NodeHandle nodeHandle("~");

	leitor_qr::LeitorQR leitor_qr(nodeHandle);

	ros::spin();
	return 0;
}
