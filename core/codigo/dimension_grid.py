import math

def ValidaFuenteEsteDentroDeDisipador(fuentes,ancho_x_disipador,profundo_z_disipador):

	fuente_problema = []

	for idx,fuente in enumerate(fuentes):
		if fuente[0] + fuente[2]/2 > ancho_x_disipador or fuente[0] - fuente[2]/2 < 0:
			fuente_problema.append(idx + 1)
			return False, fuente_problema
		if fuente[1] + fuente[3]/2 > profundo_z_disipador or fuente[1] - fuente[3]/2 < 0:
			fuente_problema.append(idx + 1)
			return False, fuente_problema
	return True, fuente_problema

def EncuentraAnchoYProfundoMinimos(fuentes):

	ancho = []
	profundo = []

	for fuente in fuentes:
		ancho.append(fuente[2])
		profundo.append(fuente[3])

	return min(ancho), min(profundo)

def ValidaFuentesNoSeTraslapen(fuentes):

	fuentes_problema = []

	for idx, fuente in enumerate(fuentes):

		i = len(fuentes)-1

		x_izq = round(fuente[0] - fuente[2]/2,6)
		y_izq = round(fuente[1] + fuente[3]/2,6)
		x_der = round(fuente[0] + fuente[2]/2,6)
		y_der = round(fuente[1] - fuente[3]/2,6)
		while i > idx:
			fuente_a_comparar = fuentes[i]
			x_izq_a_comparar = round(fuente_a_comparar[0] - fuente_a_comparar[2]/2,6)
			y_izq_a_comparar = round(fuente_a_comparar[1] + fuente_a_comparar[3]/2,6)
			x_der_a_comparar = round(fuente_a_comparar[0] + fuente_a_comparar[2]/2,6)
			y_der_a_comparar = round(fuente_a_comparar[1] - fuente_a_comparar[3]/2,6)

			if x_izq >= x_der_a_comparar or x_izq_a_comparar >= x_der:
				i -= 1
				continue
			if(y_izq <= y_der_a_comparar or y_izq_a_comparar <= y_der):
				i -= 1
				continue

			fuentes_problema.append(idx + 1)
			fuentes_problema.append(i + 1)
			return False, fuentes_problema
	return True, fuentes_problema

def EstableceDimensionesGrid(fuentes,ancho_x_disipador,profundo_z_disipador,grosor_aleta,N):

	divisiones = {}

	fuentes_dentro, fuente_fuera = ValidaFuenteEsteDentroDeDisipador(fuentes,ancho_x_disipador,profundo_z_disipador)
	if fuentes_dentro:

		fuentes_no_se_traslapan, fuentes_traslapadas = ValidaFuentesNoSeTraslapen(fuentes)

		if fuentes_no_se_traslapan:

			ancho_x, profundo_z = EncuentraAnchoYProfundoMinimos(fuentes)
			densidad_x1 = densidad_x2 = ancho_x / 4
			densidad_z = profundo_z / 4

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

			return divisiones, [0]
		else:
			return None, fuentes_traslapadas
	else:
		return None, fuente_fuera
