#include "../include/leitor_qr/LeitorQR.hpp"

namespace leitor_qr
{

	// Construtor
	LeitorQR::LeitorQR(ros::NodeHandle& nodeHandle) :
	 nodeHandle_(nodeHandle)
	{
		ROS_INFO("Leitor QR iniciado!"); // DEBUG 	

		arquivo_csv.open("/home/danielb/qr_encontrados.csv"); // MOD
		arquivo_csv.close();

		listener_tf = new tf2_ros::TransformListener(buffer_tf); // Inicializa o listener do tf

		// MOD - COLOCAR NO ARQUIVO DE PARAMETROS
		TOPICO_IMAGEM_RGB = "/uav1/rgbd/color/image_raw";
		TOPICO_IMAGEM_BW = "/image_mono"; 
		TOPICO_IMAGEM_RAW = "/image_raw";
		TOPICO_POINTCLOUD = "/camera/depth/points";
		TOPICO_MARCADOR = "/visualization_marker";
		//

		sub_imagem_sensor = nodeHandle_.subscribe(TOPICO_IMAGEM_RGB, 10, &LeitorQR::CallbackImagemSensor, this); // Subscriber imagem sensor	
		sub_imagem_qr  = nodeHandle_.subscribe(TOPICO_IMAGEM_BW, 10, &LeitorQR::CallbackImagem, this); // Subscriber imagem processada
		sub_pointcloud_camera = nodeHandle_.subscribe(TOPICO_POINTCLOUD, 10, &LeitorQR::CallbackPointcloud, this); // Subscriber pointcloud imagem

		pub_imagem_raw = nodeHandle_.advertise<sensor_msgs::Image>(TOPICO_IMAGEM_RAW, 10); // Publisher imagem para processar	
		pub_marcador = nodeHandle_.advertise<visualization_msgs::Marker>(TOPICO_MARCADOR, 10); // Publisher marcador	
		
		ROS_INFO("Aguardando imagem"); // DEBUG	
		
	}

	// Destrutor
	LeitorQR::~LeitorQR()
	{
		delete listener_tf;
	}

	// Callback Subscriber Imagem Sensor
	void LeitorQR::CallbackImagemSensor(const sensor_msgs::Image& msg){
		ROS_INFO("Imagem recebida do UAV"); // DEBUG
		
		sensor_msgs::Image img_proc(msg); // Imagem limitada 

		// Limita os valores de entrada 
		for(unsigned int i=0; i<msg.step*msg.height; i++){
			if (img_proc.data[i] > 150) img_proc.data[i] = 0;
		}	

		pub_imagem_raw.publish(img_proc); // Envia a imagem colorida para ser processada
		ROS_INFO("Imagem enviada para o processamento"); // DEBUG
		return;
	}	
	
	// Callback PointCloud RGBD
	void LeitorQR::CallbackPointcloud(const sensor_msgs::PointCloud2& msg){
		pointcloud_camera = sensor_msgs::PointCloud2(msg); // Copia e armazena a pointcloud recebida
		if(!flag_pointcloud_recebida) flag_pointcloud_recebida = true; // Flag para indicar o recebimento da primeira point cloud
		return;
	}

	// Callback Subscriber Imagem Processada
	void LeitorQR::CallbackImagem(const sensor_msgs::Image& msg)	
	{

		if(!flag_pointcloud_recebida) return; // Verifica se a primeira point cloud ja foi recebida

		uint32_t h = msg.height; // Altura da imagem
		uint32_t w = msg.width; // Largura da imagem
		uint32_t passo = msg.step; // Bytes por linha

		uint32_t x0 = w/2; // Centro x
		uint32_t y0 = h/2; // Centro y

		ROS_INFO_STREAM("Imagem Recebida:	" << h << "; " << w << " Passo: " << passo); // DEBUG
		
		// Criacao do decodificador
		struct quirc *qr; // Decodificador
		qr = quirc_new();
		if (!qr){
			ROS_INFO("Falha ao alocar memoria para o decodificador"); // DEBUG
			ros::requestShutdown();
		}
		
		// Definir tamanho da imagem para o decodificador
		if (quirc_resize(qr, w, h) < 0){
			ROS_INFO("Falha ao alocar memoria para a imagem"); // DEBUG
			ros::requestShutdown();
		}


		// Buscar por QR codes na imagem
		uint8_t *imagem; // buffer da imagem
		int pix_linha, linhas_buffer; // Quantidade de pixels por linha, quantidade de linhas no buffer
		
		imagem = quirc_begin(qr, &pix_linha, &linhas_buffer);
		
		ROS_INFO_STREAM("Buffer Alocado:	"	<< linhas_buffer << "; " << pix_linha); // DEBUG

		for(int i=0; i<linhas_buffer*pix_linha; i++){ // Copia a imagem para o buffer
			imagem[i] = msg.data[i]; 
		}
		
		quirc_end(qr);
			
		// QR codes encontrados
		int qr_detectados = quirc_count(qr);
		ROS_INFO_STREAM("QR Codes Detectados:	" << qr_detectados); // DEBUG

		uint32_t pos[2] = {0,0}; // Posicao do qr code

		// Processar os QR codes encontrados
		for(int i=0; i<qr_detectados; i++){
			struct quirc_code  codigo;
			struct quirc_data  dados;
			quirc_decode_error_t err;

			// Decodificacao
			quirc_extract(qr, i, &codigo);
			err = quirc_decode(&codigo, &dados);

			pos[0] = (codigo.corners[0].x + codigo.corners[1].x)/2.0; // Centro x do QR code
			pos[1] = (codigo.corners[0].y + codigo.corners[3].y)/2.0; // Centro y do QR code
			
			// Verifica se foi possivel decodificar
			if(err) ROS_INFO_STREAM("Erro no QR" << i); // DEBUG
			else {
								
				// Verifica se o conteudo do  QR Code ja foi detectado anteriormente
				bool qr_repetido = false;
				std::vector<uint8_t> conteudo_atual(dados.payload, dados.payload + dados.payload_len); // copia o conteudo
				
				for(unsigned long int j=0; j<qr_codes_encontrados.size(); j++){ // Busca por conteudos iguais
					if(qr_codes_encontrados[j].conteudo == conteudo_atual) qr_repetido = true;
				}
				
				// Caso o QR Code seja novo
				if(!qr_repetido){

					// Novo QR Code
					struct qr_code qr_atual;
					qr_atual.conteudo = conteudo_atual;
					qr_atual.pos_pixel[0] = pos[0];
				       	qr_atual.pos_pixel[1] = pos[1];

					// Conversao da pointcloud para xyz
					pcl::PointCloud<pcl::PointXYZ> *pointcloud_conversao = new pcl::PointCloud<pcl::PointXYZ>;
					pcl::fromROSMsg(pointcloud_camera, *pointcloud_conversao);

					// Indice do QR Code no vetor da pointcloud
					unsigned int indice_pointcloud = qr_atual.pos_pixel[0] + 1280 * qr_atual.pos_pixel[1]; 
					
					// Transformacao para o frame global
					geometry_msgs::PointStamped ponto_entrada;
					geometry_msgs::PointStamped ponto_saida;

					ponto_entrada.header.frame_id = pointcloud_conversao->header.frame_id;
					ponto_entrada.point.x = pointcloud_conversao->points[indice_pointcloud].x;
					ponto_entrada.point.y = pointcloud_conversao->points[indice_pointcloud].y;
					ponto_entrada.point.z = pointcloud_conversao->points[indice_pointcloud].z;
					
					try{
						buffer_tf.transform<geometry_msgs::PointStamped>(ponto_entrada, ponto_saida, "uav1/fixed_map_odom");	
  					}
					catch (tf2::TransformException &ex) {
  						ROS_WARN("%s",ex.what());
  						ros::Duration(1.0).sleep();
  						continue;
  					}


					// Armazena a posicao do QR Code no referencial global
					qr_atual.pos_mundo[0] = ponto_saida.point.x; 
					qr_atual.pos_mundo[1] = ponto_saida.point.y;
					qr_atual.pos_mundo[2] = ponto_saida.point.z;
					qr_atual.frame = "uav1/fixed_map_odom";

					// Salva o QR Code 
					qr_codes_encontrados.push_back(qr_atual);

					std::string str_conteudo(qr_atual.conteudo.begin(), qr_atual.conteudo.end());
					arquivo_csv.open("/home/danielb/qr_encontrados.csv", std::ios_base::app);
					arquivo_csv << str_conteudo << ", " << qr_atual.pos_mundo[0] << ", " << qr_atual.pos_mundo[1] << ", " << qr_atual.pos_mundo[2] << '\n';
					arquivo_csv.close();

					ROS_INFO_STREAM("Dados QR" << i << "	");	
					for(auto elem : qr_atual.conteudo){
						ROS_INFO_STREAM(elem);
					}	
					ROS_INFO_STREAM("Posicao Pixel QR" << i << "	" << qr_atual.pos_pixel[0] << ";" << qr_atual.pos_pixel[1] << "Centro da Imagem	" << x0 << ";"<< y0); // DEBUG
					ROS_INFO_STREAM("Tamanho Pontos	" << pointcloud_conversao->points.size()); // DEBUG
					ROS_INFO_STREAM("Indice Pontos	" << indice_pointcloud); // DEBUG
					ROS_INFO_STREAM("Posicao QR Mundo	" << qr_atual.pos_mundo[0] << ";" << qr_atual.pos_mundo[1] << ";"  << qr_atual.pos_mundo[2]); // DEBUG

					delete pointcloud_conversao; // Libera a memoria

				}
			}

			PlotMarcadores(); // Plota qr codes no rviz

		}

		// Fim
		quirc_destroy(qr); // libera o decodificador
		return;
	}

	void LeitorQR::PlotMarcadores(void){

		for(unsigned int i=0; i < qr_codes_encontrados.size(); i++){
					
			// Marcador RViz
			visualization_msgs::Marker ponto;
	
			ponto.header.frame_id = qr_codes_encontrados[i].frame;
			//ponto.header.stamp = ros::Time::now();
			ponto.id = i;
			ponto.type = visualization_msgs::Marker::SPHERE;
			ponto.action = visualization_msgs::Marker::ADD;
			ponto.pose.position.x = qr_codes_encontrados[i].pos_mundo[0];
			ponto.pose.position.y = qr_codes_encontrados[i].pos_mundo[1];
			ponto.pose.position.z = qr_codes_encontrados[i].pos_mundo[2];
			ponto.scale.x = 0.1;
			ponto.scale.y = 0.1;
			ponto.scale.z = 0.1;
			ponto.color.a = 0.6;
			ponto.color.r = 0.0;
			ponto.color.g = 1.0;
			ponto.color.b = 1.0;

			// Publica marcador
			pub_marcador.publish(ponto);
		}	
	}
} 
