import sys
import math

def ValidaFuenteEsteDentroDeDisipador(centro_x,centro_z,ancho_x,profundo_z,ancho_x_disipador,profundo_z_disipador):

	if centro_x + ancho_x/2 > ancho_x_disipador or centro_x - ancho_x/2 < 0:
		return False
	elif centro_z + profundo_z/2 > profundo_z_disipador or centro_z - profundo_z/2 < 0:
		return False
	else:
		return True

def EstableceDimensionesGrid(fuentes,ancho_x_disipador,profundo_z_disipador,grosor_aleta,N):

	centro_x = fuentes['centro_x']
	centro_z = fuentes['centro_z']
	ancho_x = fuentes['ancho']
	profundo_z = fuentes['profundo']

	divisiones = {}

	fuente_dentro = ValidaFuenteEsteDentroDeDisipador(centro_x,centro_z,ancho_x,profundo_z,ancho_x_disipador,profundo_z_disipador)

	if fuente_dentro:
		densidad_x1 = densidad_x2 = ancho_x / 2
		densidad_z = profundo_z / 2

		divisiones['num_div_x1'] = math.ceil(grosor_aleta / densidad_x1)
		divisiones['num_div_x2'] = math.ceil(((ancho_x_disipador - N * grosor_aleta) / (N-1)) / densidad_x2)
		divisiones['num_div_z'] = math.ceil(profundo_z_disipador / densidad_z)

		if densidad_x1 > grosor_aleta:
			divisiones['num_div_x1'] = 2
		if densidad_x2 > (ancho_x_disipador - N * grosor_aleta)/(N-1):
			divisiones['num_div_x2'] = 2

		#El mínimo valor para cualquiera de los valores que empiezan con 'num' es num_ = 2

		#divisiones['num_div_x2']=15
		#divisiones['num_div_x1']=4
		#divisiones['num_div_z']=20

		divisiones['num_div_y1'] = 2
		divisiones['num_div_y2'] = 4

		return divisiones
	else:
		return None
