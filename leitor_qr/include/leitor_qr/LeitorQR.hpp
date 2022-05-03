#pragma once

#include <ros/ros.h>
#include <vector>
#include <sensor_msgs/Image.h>
#include <quirc.h>
#include <inttypes.h>
#include <sensor_msgs/PointCloud2.h>
#include <sensor_msgs/PointCloud.h>
#include <sensor_msgs/point_cloud_conversion.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/PCLPointCloud2.h>
#include <visualization_msgs/Marker.h>
#include <tf2_ros/transform_listener.h>
#include <geometry_msgs/TransformStamped.h>
#include <geometry_msgs/PointStamped.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>
#include <iostream>
#include <fstream>

namespace leitor_qr{

	class LeitorQR{
		public:
			/*!
			 * Constructor.
			 */
			LeitorQR(ros::NodeHandle& nodeHandle);

			/*!
			 * Destructor.
			 */
			virtual ~LeitorQR();

		private:

			// Atributos
			ros::NodeHandle nodeHandle_;
			
			struct qr_code {
				uint32_t pos_pixel[2]; // Posicao do centro na imagem xy
				std::vector<uint8_t> conteudo; // Conteudo em ascii
				float pos_mundo[3]; // Posicao do qr code no referencial global xyz 
				std::string frame;
			};

			std::vector<qr_code> qr_codes_encontrados;

			sensor_msgs::PointCloud2 pointcloud_camera;

			tf2_ros::Buffer buffer_tf;
			tf2_ros::TransformListener *listener_tf;
			
			// Subscribers
			ros::Subscriber sub_imagem_qr; 
			ros::Subscriber sub_imagem_sensor; // Recebe a imagem da camera
			ros::Subscriber sub_pointcloud_camera;

			// Publishers
			ros::Publisher pub_imagem_raw; 
			ros::Publisher pub_marcador;

			// Parametros
			std::string TOPICO_IMAGEM_BW;
			std::string TOPICO_IMAGEM_RGB;
			std::string TOPICO_IMAGEM_RAW;
			std::string TOPICO_POINTCLOUD;
			std::string TOPICO_MARCADOR;

			// Flags
			bool flag_pointcloud_recebida = false;
			
			// Callbacks
			void CallbackImagemSensor(const sensor_msgs::Image& msg);
			void CallbackImagem(const sensor_msgs::Image& msg);
			void CallbackPointcloud(const sensor_msgs::PointCloud2& msg);
			
			// Metodos
			void PlotMarcadores(void);

			// Arquivos
			std::ofstream arquivo_csv;

	};

} /* namespace */
