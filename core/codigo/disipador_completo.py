import numpy as np
import array
from . import dimension_grid
from . import fuentes_calor
from . import grafica
import math
from . import coeficiente_conveccion
from . import coeficiente_radiacion
from . import eficiencia_aleta

def EncuentraPuntosEsquinaExtEmpezandoPor(punto_inicio,lista_puntos,zeta):

	lista_puntos.append([punto_inicio,1,1,zeta,dy1])
	lista_puntos.append([lista_puntos[-1][0] + altura_disipador,1,-1,zeta,dy2])
	lista_puntos.append([lista_puntos[-1][0] + (altura_disipador + 1) * (num_divisiones_x1 - 1) + 1,-1,1,zeta,dy1])
	for i in range(N-1):
		lista_puntos.append([lista_puntos[-1][0] + altura_disipador + (num_divisiones_y2 + 1) * (num_divisiones_x2-1) + 1,1,1,zeta,dy1])
		lista_puntos.append([lista_puntos[-1][0] + (altura_disipador + 1) * num_divisiones_x1, -1,1,zeta,dy1])
	lista_puntos.append([lista_puntos[-1][0] + altura_disipador,-1,-1,zeta,dy2])

	return lista_puntos[-1][0]

def EncuentraPuntosEsquinaIntEmpezandoPor(punto_inicio,lista_puntos,zeta):

	lista_puntos.append([punto_inicio,'izq',zeta])

	for i in range(N-1):
		lista_puntos.append([lista_puntos[-1][0] + (num_divisiones_y2 + 1) * num_divisiones_x2 + num_divisiones_y1,'der',zeta])
		if N - 1 > 1 and i is not N - 2:
			lista_puntos.append([lista_puntos[-1][0] + (num_divisiones_y2 + num_divisiones_y1 + 1) * num_divisiones_x1,'izq',zeta])

	return lista_puntos[-1][0]

def PuntosEsquinaExteriores():

	punt_ext = []

	punto_final_iteracion_pasada = EncuentraPuntosEsquinaExtEmpezandoPor(0,punt_ext,1)
	punto_final = EncuentraPuntosEsquinaExtEmpezandoPor((punto_final_iteracion_pasada+1)*num_divisiones_z,punt_ext,-1)

	return punt_ext, punto_final_iteracion_pasada + 1, punto_final

def PuntosEsquinaInteriores(num_puntos_para_bajar_nivel_z):

	punt_int = []

	punto_inicio = (num_divisiones_y1 + num_divisiones_y2 + 1) * num_divisiones_x1 + num_divisiones_y1

	punto_final_iteracion_pasada = EncuentraPuntosEsquinaIntEmpezandoPor(punto_inicio,punt_int,1)
	EncuentraPuntosEsquinaIntEmpezandoPor((num_puntos_para_bajar_nivel_z)*num_divisiones_z + punto_inicio,punt_int,-1)

	return punt_int

def IncluyePuntosSuperficieYPuntaAleta(counter, lista_puntos, punto_inicio,valor_pared_frontal_o_trasera):

	for j in range(num_divisiones_x1 - 1):
		if counter == 0 and j == 0:
			lista_puntos.append([punto_inicio + altura_disipador + 1,'aleta',valor_pared_frontal_o_trasera])
			lista_puntos.append([lista_puntos[-1][0] + altura_disipador,'superficie_x1',valor_pared_frontal_o_trasera])
		elif j == 0:
			lista_puntos.append([lista_puntos[-1][0] + 1,'aleta',valor_pared_frontal_o_trasera])
			lista_puntos.append([lista_puntos[-1][0] + altura_disipador,'superficie_x1',valor_pared_frontal_o_trasera])
		else:
			lista_puntos.append([lista_puntos[-1][0] + 1,'aleta',valor_pared_frontal_o_trasera])
			lista_puntos.append([lista_puntos[-1][0] + altura_disipador,'superficie_x1',valor_pared_frontal_o_trasera])
	if counter != N - 1:
		lista_puntos.append([lista_puntos[-1][0] + 1 + altura_disipador,'frontera_x_izq',valor_pared_frontal_o_trasera])

	return lista_puntos

def IncluyePuntosSuperficieYEspacioEntreAletas(counter, lista_puntos,valor_pared_frontal_o_trasera):

	for k in range(num_divisiones_x2 - 1):
		if counter == N - 1:
			break
		elif k == 0:
			lista_puntos.append([lista_puntos[-1][0] + 1,'espacio',valor_pared_frontal_o_trasera,k])
			lista_puntos.append([lista_puntos[-1][0] + num_divisiones_y2,'superficie_x2',valor_pared_frontal_o_trasera,k])
		else:
			lista_puntos.append([lista_puntos[-1][0] + 1,'espacio',valor_pared_frontal_o_trasera,k])
			lista_puntos.append([lista_puntos[-1][0] + num_divisiones_y2,'superficie_x2',valor_pared_frontal_o_trasera,k])
	if counter != N - 1:
		lista_puntos.append([lista_puntos[-1][0] + 1 + altura_disipador,'frontera_x_der',valor_pared_frontal_o_trasera,k])

	return lista_puntos

def DefinePuntoInicialenZ(tipo_punto,puntos_para_bajar_z):

	if tipo_punto == 'frontal':
		#En este caso los valores de 1 y -1 nos ayudan a determinar en que cara estamos
		punto_inicio = [[0,1],[puntos_para_bajar_z * num_divisiones_z,-1]]
	else:
		punto_inicio = []
		for i in range(num_divisiones_z - 1):
			#En este caso el valor de 0 es solo para mantener congruencia en la presentación de datos
			punto_inicio.append([puntos_para_bajar_z * (i+1),'punto_no_frontal'])

	return punto_inicio

def BordesEjeX(puntos_para_bajar_z,tipo_de_punto):

	punt_borde_x = []

	punto_inicio = DefinePuntoInicialenZ(tipo_de_punto,puntos_para_bajar_z)

	for punto_inicio_z in punto_inicio:
		for i in range(N):
			punt_borde_x = IncluyePuntosSuperficieYPuntaAleta(i,punt_borde_x,punto_inicio_z[0],punto_inicio_z[1])
			punt_borde_x = IncluyePuntosSuperficieYEspacioEntreAletas(i,punt_borde_x,punto_inicio_z[1])

	return punt_borde_x

def IncluyePuntosAletasEnLosExtremos(i,lista_puntos,punto_para_inicio,valor_cara_frontal_o_trasera):

	for j in range(num_divisiones_y1 - 1):
		if i == 0 and j == 0:
			lista_puntos.append([punto_para_inicio + 1,'izq_y1',valor_cara_frontal_o_trasera])
		else:
			if i == 0:
				lista_puntos.append([lista_puntos[-1][0]+1,'izq_y1',valor_cara_frontal_o_trasera])
			elif j != 0 and num_divisiones_y1 - 1 >= 2:
				lista_puntos.append([lista_puntos[-1][0]+1,'der_y1',valor_cara_frontal_o_trasera])
	if i == 0:  #Punto frontera aleta izquierda
				lista_puntos.append([lista_puntos[-1][0]+1,'izq_frontera_y',valor_cara_frontal_o_trasera])
	else: 		#Punto frontera aleta derecha
				lista_puntos.append([lista_puntos[-1][0]+1,'der_frontera_y',valor_cara_frontal_o_trasera])
	for k in range(num_divisiones_y2 - 1):
		if i == 0:
			lista_puntos.append([lista_puntos[-1][0]+1,'izq_y2',valor_cara_frontal_o_trasera])
		else:
			lista_puntos.append([lista_puntos[-1][0]+1,'der_y2',valor_cara_frontal_o_trasera])

	return lista_puntos

def IncluyePuntosAletasInteriores(counter, lista_puntos,punto,valor_cara_frontal_o_trasera):

	if counter % 2 != 0:
		lado = 'der_y1'
		lado2 = 'izq_y1'
	else:
		lado = 'izq_y1'
		lado2 = 'der_y1'

	for m in range(num_divisiones_y1 - 1):
		if counter == 1 and m == 0:
			lista_puntos.append([lista_puntos[-1][0] + 2 + (altura_disipador + 1)*(num_divisiones_x1 - 1) + 1,'der_y1',valor_cara_frontal_o_trasera])
		elif m != 0:
			lista_puntos.append([lista_puntos[-1][0]+1,lado,valor_cara_frontal_o_trasera])
	if counter % 2 != 0:
		lista_puntos.append([lista_puntos[-1][0]+ 1 + num_divisiones_y2 + 1 + ((num_divisiones_x2 - 1) * (num_divisiones_y2 + 1)) + 1,lado2,valor_cara_frontal_o_trasera])
	else:
		lista_puntos.append([lista_puntos[-1][0] + 1 + num_divisiones_y2 + 1 + ((num_divisiones_x1 - 1) * (altura_disipador + 1)) + 1,lado2,valor_cara_frontal_o_trasera])

	return lista_puntos

def BordesEjeY(puntos_para_bajar_z,tipo_de_punto):

	punt_borde_y = []

	punto_inicio = DefinePuntoInicialenZ(tipo_de_punto,puntos_para_bajar_z)

	for punto_inicio_z in punto_inicio:
		for i in range(2*N):
			if i == 0 or i == 2*N - 1:
				punt_borde_y = IncluyePuntosAletasEnLosExtremos(i,punt_borde_y,punto_inicio_z[0],punto_inicio_z[1])
			else:
				punt_borde_y = IncluyePuntosAletasInteriores(i,punt_borde_y,punto_inicio_z[0],punto_inicio_z[1])

	return(punt_borde_y)


def BordesEjeZ(puntos_para_bajar_z):

	punt_borde_z = []
	punto_inicio = []

	for i in range(num_divisiones_z - 1):
		punto_inicio.append((i+1) * puntos_para_bajar_z)

	for punto_inicio_z in punto_inicio:
		punt_borde_z.append([punto_inicio_z,'externo',1,1])
		punt_borde_z.append([punt_borde_z[-1][0] + altura_disipador,'externo_sup',1,-1])
		for i in range(N - 1):
			if i == 0:
				punt_borde_z.append([punt_borde_z[-1][0] + 1 + (altura_disipador + 1) * (num_divisiones_x1 - 1),'externo',-1,1])
			else:
				punt_borde_z.append([punt_borde_z[-1][0] + num_divisiones_y2 + 1 + (altura_disipador + 1) * (num_divisiones_x1 - 1),'externo',-1,1])
			punt_borde_z.append([punt_borde_z[-1][0] + num_divisiones_y1,'frontera_z_der',0,0])
			punt_borde_z.append([punt_borde_z[-1][0] + (num_divisiones_y2 + 1) * num_divisiones_x2,'externo',1,1])
			punt_borde_z.append([punt_borde_z[-1][0] + num_divisiones_y1,'frontera_z_izq',0,0])
		punt_borde_z.append([punt_borde_z[-1][0] + num_divisiones_y2 + 1 + (altura_disipador + 1) * (num_divisiones_x1 - 1),'externo',-1,1])
		punt_borde_z.append([punt_borde_z[-1][0] + altura_disipador,'externo_sup',-1,-1])

	return punt_borde_z

def PuntosInterioresCaraFrontalYCuerpo(puntos_para_bajar_z,tipo_de_punto):

	puntos_paredes = []

	punto_inicio = DefinePuntoInicialenZ(tipo_de_punto,puntos_para_bajar_z)

	for punto_inicio_z in punto_inicio:

		puntos_paredes.append([punto_inicio_z[0] + altura_disipador + 2,'x1_y1',punto_inicio_z[1]])

		for num_aleta in range(N):
			for j in range(num_divisiones_x1 - 1):
				if num_divisiones_y1 > 2:
					for k in range(num_divisiones_y1-2):
						puntos_paredes.append([puntos_paredes[-1][0] + 1,'x1_y1',punto_inicio_z[1]])
				puntos_paredes.append([puntos_paredes[-1][0] + 1,'frontera_y',punto_inicio_z[1]])
				puntos_paredes.append([puntos_paredes[-1][0] + 1,'x1_y2',punto_inicio_z[1]])
				if num_divisiones_y2 > 2:
					for k in range(num_divisiones_y2-2):
						puntos_paredes.append([puntos_paredes[-1][0] + 1,'x1_y2',punto_inicio_z[1]])
				if j < num_divisiones_x1 - 2 and num_divisiones_x1 > 2:
					puntos_paredes.append([puntos_paredes[-1][0] + 3,'x1_y1',punto_inicio_z[1]])

			if num_aleta != N - 1:
				puntos_paredes.append([puntos_paredes[-1][0] + 2 + num_divisiones_y1 + 1,'frontera_x_der',punto_inicio_z[1]])

				for j in range(num_divisiones_x2):
					if num_divisiones_y2 > 2:
						for k in range(num_divisiones_y2-2):
							if j == 0:
								puntos_paredes.append([puntos_paredes[-1][0] + 1,'frontera_x_der',punto_inicio_z[1]])
							else:
								puntos_paredes.append([puntos_paredes[-1][0] + 1,'x2_y2',punto_inicio_z[1],j-1])
					if j < num_divisiones_x2 - 1:
						puntos_paredes.append([puntos_paredes[-1][0] + 3,'x2_y2',punto_inicio_z[1],j])

				puntos_paredes.append([puntos_paredes[-1][0] + 2 + num_divisiones_y1 + 1,'frontera_x_izq',punto_inicio_z[1]])
				for h_conv_aletas in range(num_divisiones_y2 - 2):
					puntos_paredes.append([puntos_paredes[-1][0] + 1,'frontera_x_izq',punto_inicio_z[1]])

				puntos_paredes.append([puntos_paredes[-1][0] + 3,'x1_y1',punto_inicio_z[1]])

	return puntos_paredes


def PuntosParedesExcluidosFrontales(puntos_para_bajar_z):

	puntos_paredes = []

	puntos_paredes.append(BordesEjeX(puntos_para_bajar_z,'cara_no_frontal'))
	puntos_paredes.append(BordesEjeY(puntos_para_bajar_z,'cara_no_frontal'))

	return puntos_paredes

def CreaListadePuntos():

	#En esta función, todas las variables que empiezan con 'puntos_' son variables globales
	global puntos_esquina_exteriores, puntos_esquina_interiores,puntos_borde_x,puntos_borde_y,puntos_borde_z,puntos_paredes_frontales,puntos_paredes_no_frontales,puntos_interiores

	puntos_esquina_exteriores, num_puntos_para_bajar_nivel_z, punto_final = PuntosEsquinaExteriores()
	puntos_esquina_interiores = PuntosEsquinaInteriores(num_puntos_para_bajar_nivel_z)
	puntos_borde_x = BordesEjeX(num_puntos_para_bajar_nivel_z,'frontal')
	puntos_borde_y = BordesEjeY(num_puntos_para_bajar_nivel_z,'frontal')
	puntos_borde_z = BordesEjeZ(num_puntos_para_bajar_nivel_z)
	puntos_paredes_frontales = PuntosInterioresCaraFrontalYCuerpo(num_puntos_para_bajar_nivel_z,'frontal')
	puntos_paredes_no_frontales = PuntosParedesExcluidosFrontales(num_puntos_para_bajar_nivel_z)
	puntos_interiores = PuntosInterioresCaraFrontalYCuerpo(num_puntos_para_bajar_nivel_z,"interiores")

	return punto_final, num_puntos_para_bajar_nivel_z

def EligeCoeficienteConveccionYRadiacion(punto,puntos_base_sin_info_adicional):

	if punto[0] not in puntos_base_sin_info_adicional:
		h_conv = h_conv_aletas
		h_rad = hr_aletas
	else:
		h_conv = h_conv_base
		h_rad = hr_base

	return h_conv,h_rad

def GeneraEcuacionesParaPuntosEsquinaExteriores(T,C,puntos_sig_z):

	#print('Esquina Exteriores')

	for punto in puntos_esquina_exteriores:

		dir_x = punto[1]
		dir_y = punto[2]
		dir_z = punto[3]
		tam_y = punto[4]

		h_conv,h_rad = EligeCoeficienteConveccionYRadiacion(punto,puntos_base_sin_info_adicional)

		T[punto[0]][punto[0]] = -(tam_y*dz/dx1 + dz*dx1/tam_y + tam_y*dx1/dz + (h_conv+h_rad)*(dx1*tam_y + tam_y*dz + dx1*dz)/k)
		T[punto[0]][punto[0] + dir_x * (altura_disipador + 1)] = tam_y*dz/dx1
		T[punto[0]][punto[0] + dir_y] = dz*dx1/tam_y
		T[punto[0]][punto[0] + dir_z * puntos_sig_z] = tam_y*dx1/dz
		C[punto[0]] = - (h_conv * Tinf + h_rad * Tsur) * (tam_y*dx1 + tam_y*dz + dx1*dz)/k

		#print(punto[0],punto[0] + dir_x * (altura_disipador + 1),punto[0] + dir_y,punto[0] + dir_z * puntos_sig_z,punto[4])

def GeneraEcuacionesParaPuntosEsquinaInteriores(T,C,puntos_sig_z):


	#print('Esquina Interiores')
	valor_x1 = (dy1 + dy2)*dz/dx1
	valor_x2 = dy2*dz/dx2

	for punto in puntos_esquina_interiores:

		dir_z = punto[2]

		despl_x_der = despl_x_izq = altura_disipador + 1

		T[punto[0]][punto[0]] = -(dx1*dz/dy1 + (dy1 + dy2)*dz/dx1 + (dx1 + dx2)*dz/dy2 + dy2*dz/dx2 + 1/dz*(dx1*(dy1+dy2) + dx2*dy2) + 1/k*(h_conv_aletas+hr_aletas)*(dx1*(dy1 + dy2) + dx2*dy2))

		if punto[1] == 'izq':
			despl_x_der = num_divisiones_y2 + 1
			T[punto[0]][punto[0] - despl_x_izq] = valor_x1
			T[punto[0]][punto[0] + despl_x_der] = valor_x2
		else:
			T[punto[0]][punto[0] + despl_x_der] = valor_x1
			T[punto[0]][punto[0] - despl_x_izq] = valor_x2

		T[punto[0]][punto[0] - 1] = dx1*dz/dy1
		T[punto[0]][punto[0] + 1] = (dx1 + dx2)/dy2*dz
		T[punto[0]][punto[0] + dir_z * (puntos_sig_z)] = 1/dz*(dx1*(dy1+dy2) + dx2*dy2)
		C[punto[0]] = - 1/k * (h_conv_aletas*Tinf + hr_aletas*Tsur)*(dx1*(dy1 + dy2) + dx2*dy2)

		#print(punto[0],punto[0] - despl_x_izq,punto[0] + despl_x_der,punto[0] - 1,punto[0] + 1,punto[0] + dir_z * (puntos_sig_z))

def EcuacionParaPuntoFronteraBorde(T,C,punto_frontera,dir_z,puntos_sig_z):

	if punto_frontera[1] == 'frontera_x_izq' or punto_frontera[1] == 'frontera_x_der':

		#print('Frontera X Frontal Borde')

		if punto_frontera[1] == 'frontera_x_izq':
			despl_x_izq = altura_disipador + 1
			despl_x_der = num_divisiones_y2 + 1
			interv_x_izq = dx1
			interv_x_der = dx2
		else:
			despl_x_der = despl_x_izq = altura_disipador + 1
			interv_x_izq = dx2
			interv_x_der = dx1

		T[punto_frontera[0]][punto_frontera[0]] = - (dz/dy2*(dx1 + dx2) + dy2*dz/dx1 + dy2*dz/dx2 + dy2/dz*(dx1 + dx2) + 1/k*(hr_base+h_conv_base)*((dy2+dz)*(dx1+dx2)))
		T[punto_frontera[0]][punto_frontera[0] - despl_x_izq] = dy2*dz/interv_x_izq
		T[punto_frontera[0]][punto_frontera[0] + despl_x_der] = dy2*dz/interv_x_der
		T[punto_frontera[0]][punto_frontera[0] - 1] = dz/dy2*(dx1 + dx2)
		T[punto_frontera[0]][punto_frontera[0] + dir_z * puntos_sig_z] = dy2/dz*(dx1 + dx2)
		C[punto_frontera[0]] = - 1/k * (h_conv_base*Tinf + hr_base*Tsur)*((dy2 + dz)*(dx1 + dx2))

		#print(punto_frontera[0],punto_frontera[0] - despl_x_izq,punto_frontera[0] + despl_x_der,punto_frontera[0] - 1,punto_frontera[0] + dir_z * puntos_sig_z)

	elif punto_frontera[1] == 'izq_frontera_y' or punto_frontera[1] == 'der_frontera_y':

		#print('Frontera Y Frontal Borde')
		if punto_frontera[1] == 'izq_frontera_y':
			despl_x = 1
		else:
			despl_x = -1

		T[punto_frontera[0]][punto_frontera[0]] = - (dz/dx1*(dy1+dy2) + dx1*dz/dy1 + dx1*dz/dy2 + dx1/dz*(dy1+dy2) + 1/k*(hr_aletas+h_conv_aletas)*((dx1+dz)*(dy1+dy2)))
		T[punto_frontera[0]][punto_frontera[0] + despl_x * (altura_disipador + 1)] = dz/dx1*(dy1+dy2)
		T[punto_frontera[0]][punto_frontera[0] - 1] = dx1*dz/dy1
		T[punto_frontera[0]][punto_frontera[0] + 1] = dx1*dz/dy2
		T[punto_frontera[0]][punto_frontera[0] + dir_z * puntos_sig_z] = dx1/dz*(dy1+dy2)
		C[punto_frontera[0]] = - 1/k * (h_conv_aletas*Tinf + hr_aletas*Tsur)*((dx1 + dz)*(dy1+dy2))

		#print(punto_frontera[0],punto_frontera[0] + despl_x * (altura_disipador + 1),punto_frontera[0] - 1,punto_frontera[0] + 1,punto_frontera[0] + dir_z * puntos_sig_z)

	else:

		#print('Borde Z interior')

		if punto_frontera[1] == 'frontera_z_der':
			despl_x_izq = - (altura_disipador + 1)
			despl_x_der = num_divisiones_y2 + 1
			valor_x_izq = dz*(dy1+dy2)/dx1
			valor_x_der = dy2*dz/dx2
		else:
			despl_x_izq = - (altura_disipador + 1)
			despl_x_der = altura_disipador + 1
			valor_x_izq = dy2*dz/dx2
			valor_x_der = dz*(dy1+dy2)/dx1

		T[punto_frontera[0]][punto_frontera[0]] = - (dz/dx1*(dy1+dy2) + dy2*dz/dx2 + dz*dx1/dy1 + dz/dy2*(dx1+dx2) + 1/dz*(dx1*(dy1+dy2)+dx2*dy2) + dz/k*(h_conv_aletas+hr_aletas)*(dy1+dx2))
		T[punto_frontera[0]][punto_frontera[0] + despl_x_izq] = valor_x_izq
		T[punto_frontera[0]][punto_frontera[0] + despl_x_der] = valor_x_der
		T[punto_frontera[0]][punto_frontera[0] - 1] = dz*dx1/dy1
		T[punto_frontera[0]][punto_frontera[0] + 1] = dz*(dx1+dx2)/dy2
		T[punto_frontera[0]][punto_frontera[0] + puntos_sig_z] = 1/2*1/dz*(dx1*(dy1+dy2)+dx2*dy2)
		T[punto_frontera[0]][punto_frontera[0] - puntos_sig_z] = 1/2*1/dz*(dx1*(dy1+dy2)+dx2*dy2)
		C[punto_frontera[0]] = - dz/k *(dy1 + dx2)*(h_conv_aletas*Tinf + hr_aletas*Tsur)

		#print(punto_frontera[0],punto_frontera[0] + despl_x_izq,punto_frontera[0] + despl_x_der,punto_frontera[0] - 1,punto_frontera[0] + 1,punto_frontera[0] + puntos_sig_z,punto_frontera[0] - puntos_sig_z)

def GeneraEcuacionesX(T,C,puntos_sig_z):

	for punto in puntos_borde_x:

		#print('BordesX')
		h_conv, h_rad = EligeCoeficienteConveccionYRadiacion(punto,puntos_base_sin_info_adicional)

		dir_z = punto[2]

		if punto[1] == 'aleta':
			tam_x = dx1
			tam_y = dy1
			avance_x_der = avance_x_izq = altura_disipador + 1
			avance_y = 1
		elif punto[1] == 'superficie_x1':
			tam_x = dx1
			tam_y = dy2
			avance_x_der = avance_x_izq = altura_disipador + 1
			avance_y = -1
		elif punto[1] == 'superficie_x2' or punto[1] == 'espacio':
			tam_x = dx2
			tam_y = dy2
			avance_x_der = avance_x_izq = num_divisiones_y2 + 1
			if punto[3] == num_divisiones_x2 - 2:
				avance_x_der = altura_disipador + 1
			if punto[1] == 'espacio':
				avance_y = 1
			else:
				avance_y = -1
		else:
			EcuacionParaPuntoFronteraBorde(T,C,punto,dir_z,puntos_sig_z)
			continue

		T[punto[0]][punto[0]] = -2*(tam_y*dz/tam_x + dz*tam_x/tam_y + tam_y*tam_x/dz + (h_conv+h_rad)*(tam_x*tam_y+tam_x*dz)/k)
		T[punto[0]][punto[0] - avance_x_izq] = dz*tam_y/tam_x
		T[punto[0]][punto[0] + avance_x_der] = dz*tam_y/tam_x
		T[punto[0]][punto[0] + avance_y] = 2*tam_x*dz/tam_y
		T[punto[0]][punto[0] + dir_z * (puntos_sig_z)] = 2*tam_x*tam_y/dz
		C[punto[0]] = - 2*(h_conv*Tinf+h_rad*Tsur)*(tam_y*tam_x+tam_x*dz)/k

		#print(punto[0],punto[0] - avance_x_izq,punto[0] + avance_x_der,punto[0] + avance_y,punto[0] + dir_z * (puntos_sig_z),tam_x,tam_y)

def GeneraEcuacionesY(T,C,puntos_sig_z):

	for punto in puntos_borde_y:

		#print('BordesY')

		dir_z = punto[2]

		if punto[1] == 'izq_y1' or punto[1] == 'der_y1':
			tam_y = dy1
			if punto[1] == 'izq_y1':
				avance_x = 1
			else:
				avance_x = -1
		elif punto[1] == 'izq_y2' or punto[1] == 'der_y2':
			tam_y = dy2
			if punto[1] == 'izq_y2':
				avance_x = 1
			else:
				avance_x = -1
		else:
			EcuacionParaPuntoFronteraBorde(T,C,punto,dir_z,puntos_sig_z)
			continue

		T[punto[0]][punto[0]] = -2*(tam_y*dz/dx1 + dz*dx1/tam_y + tam_y*dx1/dz + (h_conv_aletas+hr_base)*(dx1*tam_y+tam_y*dz)/k)
		T[punto[0]][punto[0] + avance_x * (altura_disipador + 1)] = 2*dz*tam_y/dx1
		T[punto[0]][punto[0] - 1] = dz*dx1/tam_y
		T[punto[0]][punto[0] + 1] = dz*dx1/tam_y
		T[punto[0]][punto[0] + dir_z * puntos_sig_z] = 2*dx1*tam_y/dz
		C[punto[0]] = - 2*(h_conv_aletas*Tinf+hr_aletas*Tsur)*(tam_y*dx1 + tam_y*dz)/k

		#print(punto[0],punto[0] + avance_x * (altura_disipador + 1),punto[0] - 1,punto[0] + 1,punto[0] + dir_z * puntos_sig_z,tam_y)

def GeneraEcuacionesZ(T,C,puntos_sig_z):

	for punto in puntos_borde_z:

		#print('BordesZ')
		h_conv, h_rad = EligeCoeficienteConveccionYRadiacion(punto,puntos_base_sin_info_adicional)

		dir_x = punto[2]
		dir_y = punto[3]

		if punto[1] == 'externo':
			tam_y = dy1
		elif punto[1] == 'externo_sup':
			tam_y = dy2
		else:
			EcuacionParaPuntoFronteraBorde(T,C,punto,1,puntos_sig_z)
			continue

		T[punto[0]][punto[0]] = -2*(tam_y*dz/dx1 + dz*dx1/tam_y + tam_y*dx1/dz + (h_conv+h_rad)*(dx1*dz+tam_y*dz)/k)
		T[punto[0]][punto[0] + dir_x * (altura_disipador + 1)] = 2*tam_y*dz/dx1
		T[punto[0]][punto[0] + dir_y] = 2*dx1*dz/tam_y
		T[punto[0]][punto[0] + puntos_sig_z] = dx1*tam_y/dz
		T[punto[0]][punto[0] - puntos_sig_z] = dx1*tam_y/dz
		C[punto[0]] = -2*(h_conv*Tinf+h_rad*Tsur)*(dx1*dz + tam_y*dz)/k

		#print(punto[0],punto[0] + dir_x * (altura_disipador + 1),punto[0] + dir_y,punto[0] + puntos_sig_z,punto[0] - puntos_sig_z,tam_y)

def GeneraEcuacionesParaBordes(T,C,puntos_sig_z):

	GeneraEcuacionesX(T,C,puntos_sig_z)
	GeneraEcuacionesY(T,C,puntos_sig_z) #Esta funcion no tiene puntos en la base del disipador
	GeneraEcuacionesZ(T,C,puntos_sig_z)

def EcuacionParaPuntoFronteraCara(T,C,p,dir_z,puntos_sig_z,h_c,h_r):

	if p[2] != 'punto_no_frontal':

		if p[1] == 'frontera_y':

			#print('Punto frontal frontera y')

			T[p[0]][p[0]] = - (dz/dx1*(dy1+dy2) + dz*dx1/dy1 + dz*dx1/dy2 + dx1/dz*(dy1 + dy2) + dx1/k * (h_c + h_r)*(dy1+dy2))
			T[p[0]][p[0] - altura_disipador - 1] = 1/2 * dz/dx1*(dy1 + dy2)
			T[p[0]][p[0] + altura_disipador + 1] = 1/2 * dz/dx1*(dy1 + dy2)
			T[p[0]][p[0] - 1] = dz*dx1/dy1
			T[p[0]][p[0] + 1] = dz*dx1/dy2
			T[p[0]][p[0] + dir_z * puntos_sig_z] = dx1/dz*(dy1 + dy2)
			C[p[0]] = - dx1/k * (dy1 + dy2) * (h_c*Tinf+h_r*Tsur)

			#print(p[0],p[0] - altura_disipador - 1,p[0] + altura_disipador + 1,p[0] - 1,p[0] + 1,p[0] + dir_z * puntos_sig_z)

		elif p[1] == 'frontera_x_izq' or p[1] == 'frontera_x_der':

			#print('Punto frontal frontera X')

			if p[1] == 'frontera_x_der':
				despl_x_izq = - altura_disipador - 1
				despl_x_der = num_divisiones_y2 + 1
				interv_x_izq = dx1
				interv_x_der = dx2
			elif p[1] == 'frontera_x_izq':
				despl_x_izq = - altura_disipador - 1
				despl_x_der = altura_disipador + 1
				interv_x_izq = dx2
				interv_x_der = dx1

			T[p[0]][p[0]] = - (dz/dy2*(dx1+dx2) + dz*dy2/dx1 + dz*dy2/dx2 + dy2/dz*(dx1 + dx2) + dy2/k * (h_c + h_r)*(dx1+dx2))
			T[p[0]][p[0] + despl_x_izq] = dz*dy2/interv_x_izq
			T[p[0]][p[0] + despl_x_der] = dz*dy2/interv_x_der
			T[p[0]][p[0] - 1] = 1/2 * dz/dy2*(dx1 + dx2)
			T[p[0]][p[0] + 1] = 1/2 * dz/dy2*(dx1 + dx2)
			T[p[0]][p[0] + dir_z * puntos_sig_z] = dy2*(dx1+dx2)/dz
			C[p[0]] = - 1/k * dy2*(dx1+dx2)*(h_c*Tinf+h_r*Tsur)

			#print(p[0],p[0] + despl_x_izq,p[0] + despl_x_der,p[0] - 1,p[0] + 1,p[0] + dir_z * puntos_sig_z)

	else:

		#Puntos frontera en cara disipador

		if p[1] == 'frontera_x_izq' or p[1] == 'frontera_x_der':

			#print('Punto frontera no frontal X')

			if p[1] == 'frontera_x_izq':
				despl_x_izq = altura_disipador + 1
				despl_x_der = num_divisiones_y2 + 1
				interv_x_izq = dx1
				interv_x_der = dx2
			else:
				despl_x_izq = despl_x_der = altura_disipador + 1
				interv_x_izq = dx2
				interv_x_der = dx1

			T[p[0]][p[0]] = - (dy2*dz/dx1 + dy2*dz/dx2 + dy2/dz * (dx1 + dx2) + dz/dy2 * (dx1 + dx2) + 1/k * dz * (h_c + h_r) * (dx1 + dx2))
			T[p[0]][p[0] - despl_x_izq] = dy2*dz/interv_x_izq
			T[p[0]][p[0] + despl_x_der] = dy2*dz/interv_x_der
			T[p[0]][p[0] - 1] = dz*(dx1+dx2)/dy2
			T[p[0]][p[0] - puntos_sig_z] = 1/2*dy2/dz*(dx1+dx2)
			T[p[0]][p[0] + puntos_sig_z] = 1/2*dy2/dz*(dx1+dx2)
			C[p[0]] = - 1/k * (h_c*Tinf + h_r*Tsur) * dz * (dx1 + dx2)

			#print(p[0],p[0] - despl_x_izq,p[0] + despl_x_der,p[0] - 1,p[0] - puntos_sig_z,p[0] + puntos_sig_z)

		else:

			#print('Punto Frontera No Frontal Y')

			if p[1] == 'izq_frontera_y':
				dir_x = 1
			else:
				dir_x = -1

			T[p[0]][p[0]] = - (dz*(dy1+dy2)/dx1 + dx1*dz/dy1 + dx1*dz/dy2 + dx1/dz*(dy1 + dy2) + 1/k * dz * (dy1 + dy2) * (h_c + h_r))
			T[p[0]][p[0] + dir_x * (altura_disipador + 1)] = dz*(dy1+dy2)/dx1
			T[p[0]][p[0] - 1] = dx1*dz/dy1
			T[p[0]][p[0] + 1] = dx1*dz/dy2
			T[p[0]][p[0] - puntos_sig_z] = 1/2 * dx1/dz*(dy1 + dy2)
			T[p[0]][p[0] + puntos_sig_z] = 1/2 * dx1/dz*(dy1 + dy2)
			C[p[0]] = - 1/k * dz * (dy1 + dy2) * (h_c*Tinf + h_r*Tsur)

			#print(p[0],p[0] + dir_x * (altura_disipador + 1),p[0] - 1,p[0] + 1,p[0] - puntos_sig_z,p[0] + puntos_sig_z)


def GeneraEcuacionesParedFrontal(T,C,puntos_sig_z):

	for p in puntos_paredes_frontales:

		#print('Punto Pared Frontal')

		dir_z = p[2]

		despl_x_der = despl_x_izq = altura_disipador + 1

		if p[1] == 'x1_y1':
			tam_x = dx1
			tam_y = dy1
		elif p[1] == 'x1_y2':
			tam_x = dx1
			tam_y = dy2
		elif p[1] == 'x2_y2':
			tam_x = dx2
			tam_y = dy2
			despl_x_izq = despl_x_der = num_divisiones_y2 + 1
			if p[3] == num_divisiones_x2 - 2:
				despl_x_der = altura_disipador + 1
		else:
			EcuacionParaPuntoFronteraCara(T,C,p,dir_z,puntos_sig_z,h_conv_aletas,hr_aletas)
			continue

		T[p[0]][p[0]] = -2*(tam_x*tam_y/dz + tam_y*dz/tam_x + tam_x*dz/tam_y + (h_conv_aletas+hr_aletas)/k*tam_x*tam_y)
		T[p[0]][p[0] - despl_x_izq] = tam_y*dz/tam_x
		T[p[0]][p[0] + despl_x_der] = tam_y*dz/tam_x
		T[p[0]][p[0] - 1] = tam_x*dz/tam_y
		T[p[0]][p[0] + 1] = tam_x*dz/tam_y
		T[p[0]][p[0] + dir_z * puntos_sig_z] = 2*tam_x*tam_y/dz
		C[p[0]] = -2*(h_conv_aletas*Tinf+hr_aletas*Tsur)/k*tam_x*tam_y

		#print(p[0],p[0] - despl_x_izq,p[0] + despl_x_der,p[0] - 1,p[0] + 1,p[0] + dir_z * puntos_sig_z,tam_x,tam_y)

def GeneraEcuacionesParedLateralySuperior(T,C,puntos_sig_z):

	#puntos sobre X
	for p in puntos_paredes_no_frontales[0]:

		#print('Punto Pared No Frontal X')
		h_conv, h_rad = EligeCoeficienteConveccionYRadiacion(p,puntos_base_sin_info_adicional)

		if p[1] == 'aleta':
			tam_x = dx1
			tam_y = dy1
			despl_x_izq = despl_x_der = altura_disipador + 1
			dir_y = 1
		elif p[1] == 'superficie_x1':
			tam_x = dx1
			tam_y = dy2
			despl_x_izq = despl_x_der = altura_disipador + 1
			dir_y = -1
		elif p[1] == 'espacio':
			tam_x = dx2
			tam_y = dy2
			despl_x_izq = despl_x_der = num_divisiones_y2 + 1
			if p[3] == num_divisiones_x2 - 2:
				despl_x_der = altura_disipador + 1
			dir_y = 1
		elif p[1] == 'superficie_x2':
			tam_x = dx2
			tam_y = dy2
			despl_x_izq = despl_x_der = num_divisiones_y2 + 1
			if p[3] == num_divisiones_x2 - 2:
				despl_x_der = altura_disipador + 1
			dir_y = -1
		else:
			EcuacionParaPuntoFronteraCara(T,C,p,1,puntos_sig_z,h_conv,h_rad)
			continue

		T[p[0]][p[0]] = -2*(tam_x*dz/tam_y + tam_y*dz/tam_x + tam_x*tam_y/dz + (h_conv+h_rad)/k*tam_x*dz)
		T[p[0]][p[0] - despl_x_izq] = tam_y*dz/tam_x
		T[p[0]][p[0] + despl_x_der] = tam_y*dz/tam_x
		T[p[0]][p[0] + dir_y] = 2*dz*tam_x/tam_y
		T[p[0]][p[0] + puntos_sig_z] = tam_x*tam_y/dz
		T[p[0]][p[0] - puntos_sig_z] = tam_x*tam_y/dz
		C[p[0]] = -2*(h_conv*Tinf+h_rad)/k*tam_x*dz

		#print(p[0],p[0] - despl_x_izq,p[0] + despl_x_der,p[0] + dir_y,p[0] + puntos_sig_z,p[0] - puntos_sig_z,tam_x,tam_y)

	#puntos sobre Y
	for p in puntos_paredes_no_frontales[1]:

		#print('Punto Pared No Frontal Y')

		tam_x = dx1

		if p[1] == 'izq_y1':
			tam_y = dy1
			dir_x = 1
		elif p[1] == 'izq_y2':
			tam_y = dy2
			dir_x = 1
		elif p[1] == 'der_y1':
			tam_y = dy1
			dir_x = -1
		elif p[1] == 'der_y2':
			tam_y = dy2
			dir_x = -1
		else:
			EcuacionParaPuntoFronteraCara(T,C,p,1,puntos_sig_z,h_conv_aletas,hr_aletas)
			continue

		T[p[0]][p[0]] = -2*(tam_y*dz/tam_x + tam_y*tam_x/dz + tam_x*dz/tam_y + (h_conv_aletas+hr_aletas)/k*tam_y*dz)
		T[p[0]][p[0] + dir_x * (altura_disipador + 1)] = 2*tam_y*dz/tam_x
		T[p[0]][p[0] - 1] = tam_x*dz/tam_y
		T[p[0]][p[0] + 1] = tam_x*dz/tam_y
		T[p[0]][p[0] + puntos_sig_z] = tam_y*tam_x/dz
		T[p[0]][p[0] - puntos_sig_z] = tam_y*tam_x/dz
		C[p[0]] = -2*(h_conv_aletas*Tinf+hr_aletas*Tsur)/k*tam_y*dz

		#print(p[0],p[0] + dir_x * (altura_disipador + 1),p[0] - 1,p[0] + 1,p[0] + puntos_sig_z,p[0] - puntos_sig_z,tam_x,tam_y)

def GeneraEcuacionesPuntosParedes(T,C,puntos_sig_z):

	GeneraEcuacionesParedFrontal(T,C,puntos_sig_z) #Esta funcion no contiene puntos en la base
	GeneraEcuacionesParedLateralySuperior(T,C,puntos_sig_z)

def GeneraEcuacionParaPuntoFronteraInteriorCuerpo(T,C,p,puntos_sig_z):

	if p[1] == 'frontera_x_izq' or p[1] == 'frontera_x_der':

		#print('Punto Frontera Interior Cuerpo X')
		despl_x_izq = altura_disipador + 1
		despl_x_der = num_divisiones_y2 + 1
		interv_x_izq = dx1
		interv_x_der = dx2

		if p[1] == 'frontera_x_izq':
			despl_x_izq = despl_x_der = altura_disipador + 1
			interv_x_izq = dx2
			interv_x_der = dx1

		T[p[0]][p[0]] = - (dz*dy2/dx1 + dz*dy2/dx2 + dz/dy2 * (dx1 + dx2) + dy2/dz * (dx1 + dx2))
		T[p[0]][p[0] - despl_x_izq] = dz*dy2/interv_x_izq
		T[p[0]][p[0] + despl_x_der] = dz*dy2/interv_x_der
		T[p[0]][p[0] - 1] = 1/2 * dz/dy2 * (dx1 + dx2)
		T[p[0]][p[0] + 1] = 1/2 * dz/dy2 * (dx1 + dx2)
		T[p[0]][p[0] - puntos_sig_z] = 1/2 * dy2/dz * (dx1 + dx2)
		T[p[0]][p[0] + puntos_sig_z] = 1/2 * dy2/dz * (dx1 + dx2)
		C[p[0]] = 0

		#print(p[0],p[0] - despl_x_izq,p[0] + despl_x_der,p[0] - 1,p[0] + 1,p[0] - puntos_sig_z,p[0] + puntos_sig_z)

	if p[1] == 'frontera_y':

		#print('Punto Frontera Interior Cuerpo Y')
		despl_x_der = despl_x_izq = altura_disipador + 1

		T[p[0]][p[0]] = - (dz*dx1/dy1 + dz*dx1/dy2 + dz/dx1*(dy1 + dy2) + dx1/dz*(dy1 + dy2))
		T[p[0]][p[0] - despl_x_izq] = 1/2 * dz*(dy1 + dy2)/dx1
		T[p[0]][p[0] + despl_x_der] = 1/2 * dz*(dy1 + dy2)/dx1
		T[p[0]][p[0] - 1] = dx1*dz/dy1
		T[p[0]][p[0] + 1] = dx1*dz/dy2
		T[p[0]][p[0] - puntos_sig_z] = 1/2*dx1*(dy1 + dy2)/dz
		T[p[0]][p[0] + puntos_sig_z] = 1/2*dx1*(dy1 + dy2)/dz
		C[p[0]] = 0

		#print(p[0],p[0] - despl_x_izq,p[0] + despl_x_der,p[0] - 1,p[0] + 1,p[0] - puntos_sig_z,p[0] + puntos_sig_z)

def GeneraEcuacionesPuntosInteriores(T,C,puntos_sig_z):

	for p in puntos_interiores:

		#print('Punto Interior')

		despl_x_izq = despl_x_der = altura_disipador + 1

		if p[1] == 'x1_y1':
			dim_x = dx1
			dim_y = dy1
		elif p[1] == 'x1_y2':
			dim_x = dx1
			dim_y = dy2
		elif p[1] == 'x2_y2':
			dim_x = dx2
			dim_y = dy2
			despl_x_izq = despl_x_der = num_divisiones_y2 + 1
			if p[3] == num_divisiones_x2 - 2:
				despl_x_der = altura_disipador + 1
		else:
			GeneraEcuacionParaPuntoFronteraInteriorCuerpo(T,C,p,puntos_sig_z)
			continue

		T[p[0]][p[0]] = -2*(dim_y*dz/dim_x + dim_x*dz/dim_y + dim_x*dim_y/dz)
		T[p[0]][p[0] - despl_x_izq] = dim_y*dz/dim_x
		T[p[0]][p[0] + despl_x_der] = dim_y*dz/dim_x
		T[p[0]][p[0] - 1] = dim_x*dz/dim_y
		T[p[0]][p[0] + 1] = dim_x*dz/dim_y
		T[p[0]][p[0] - puntos_sig_z] = dim_x*dim_y/dz
		T[p[0]][p[0] + puntos_sig_z] = dim_x*dim_y/dz
		C[p[0]] = 0

		#print(p[0],p[0] - despl_x_izq,p[0] + despl_x_der,p[0] - 1,p[0] + 1,p[0] - puntos_sig_z,p[0] + puntos_sig_z,dim_x,dim_y)

def GeneraMatriz(total_de_puntos,puntos_sig_nivel_z):

	T = np.zeros([total_de_puntos + 1,total_de_puntos + 1])
	Const = np.zeros(total_de_puntos + 1)

	GeneraEcuacionesParaPuntosEsquinaExteriores(T,Const,puntos_sig_nivel_z)
	GeneraEcuacionesParaPuntosEsquinaInteriores(T,Const,puntos_sig_nivel_z) #Esta funcion no tiene puntos en la base del disipador
	GeneraEcuacionesParaBordes(T,Const,puntos_sig_nivel_z)
	GeneraEcuacionesPuntosParedes(T,Const,puntos_sig_nivel_z)
	GeneraEcuacionesPuntosInteriores(T,Const,puntos_sig_nivel_z) # Esta funcion no tiene puntos en la base del disipador

	return T, Const

def ObtenPuntosBase():

	puntos_base = []

	for punto_esquina in puntos_esquina_exteriores:
		if punto_esquina[2] == -1:
			puntos_base.append([punto_esquina[0],'esquina'])
		else:
			continue

	for punto_borde_x in puntos_borde_x:
		if punto_borde_x[1] not in ['aleta','espacio']:
			puntos_base.append([punto_borde_x[0],punto_borde_x[1]])
		else:
			continue

	for punto_borde_z in puntos_borde_z:
		if punto_borde_z[1] == 'externo_sup':
			puntos_base.append([punto_borde_z[0],'borde_z_superficie'])
		else:
			continue

	for punto_superficie_x in puntos_paredes_no_frontales[0]:
		if punto_superficie_x[1] not in ['aleta','espacio']:
			puntos_base.append([punto_superficie_x[0],punto_superficie_x[1]])
		else:
			continue

	return puntos_base

def ObtenPuntosYTemperaturaExterior(Temperatura):

	lista_puntos=[puntos_esquina_exteriores,puntos_esquina_interiores,puntos_borde_x,puntos_borde_y,puntos_borde_z,puntos_paredes_frontales]

	#print(puntos_paredes_no_frontales)

	puntos_exteriores = []
	temperatura_exterior = []

	for puntos in lista_puntos:
		for punto in puntos:
			puntos_exteriores.append(punto[0])

	for puntos_no_frontales in puntos_paredes_no_frontales:
		for punto in puntos_no_frontales:
			puntos_exteriores.append(punto[0])

	for punto in puntos_exteriores:
		temperatura_exterior.append(Temperatura[punto])

	promedio_temp_exterior = np.mean(temperatura_exterior)

	return promedio_temp_exterior

def TomaPrimerElemento(lista_doble):

	return lista_doble[0]

def EnumeraPuntosBase(puntos_de_base):

	for idx,punto in enumerate(puntos_de_base):
		punto.insert(0,idx)

	return

def CalculaAreaCanalesAletasYBase(ancho,alto,grueso_base,largo,grueso_aleta,N,area_fuentes):

	area_canales = (ancho - (N * grueso_aleta)) * largo

	area_aletas = 2*N * ((alto - grueso_base) * largo) + (N * grueso_aleta * largo) + (2 * N * (alto - grueso_base) * grueso_aleta) + 2 * grueso_base * ancho

	area_base = (ancho * largo) - area_fuentes

	return area_canales, area_aletas, area_base

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

def RealizaSimulacion(datos):

	global num_divisiones_x1, num_divisiones_x2, num_divisiones_z, num_divisiones_y1, num_divisiones_y2, dx1, dx2, dy1, dy2, dz, altura_disipador,N, puntos_base_sin_info_adicional, h_conv_aletas, hr_aletas, k, Tinf, Tsur, h_conv_base, hr_base

	disipadores={"7.6": {"ancho": 7.6e-2,"alto": 2.2e-2,"grosor_aleta":1.3e-3,"grosor_base":2e-3,"num_aletas":10}}
	ancho_x = disipadores[datos['tipo_disipador']]['ancho']
	alto_y = disipadores[datos['tipo_disipador']]['alto']
	profundo_z = datos["longitud"]
	grosor_aleta = disipadores[datos['tipo_disipador']]['grosor_aleta']
	grosor_base = disipadores[datos['tipo_disipador']]['grosor_base']

	#mínimo valor de N es N = 2
	N = disipadores[datos['tipo_disipador']]['num_aletas']

	#-----------------------------------

	#Datos fuente de calor

	fuentes = {}
	fuentes['centro_x'] = 3.8e-2
	fuentes['centro_z']= 2.5e-2
	fuentes['ancho']= 5.08e-2
	fuentes['profundo']= 1.27e-2

	area_fuentes = fuentes['ancho'] * fuentes['profundo']
	#Datos orientacion disipador

	tipos_de_orientacion = {}
	tipos_de_orientacion['aletas_apuntan_arriba'] = "arriba"
	tipos_de_orientacion['aletas_apuntan_abajo'] = "abajo"
	tipos_de_orientacion['aletas_perpendicular_a_suelo'] = "perpendicular"

	orientacion = "aletas_apuntan_arriba"

	calor_fuente_en_watts = 8.24
	Tinf = 24.3
	# 0.6 emision dorado
	# 0.8 emision negro
	# 0.05 emision natural

	k = 209
	Tsur = Tinf
	emisividad = 0.8
	# 100 y 105 son números arbitrarios para comenzar a buscar los coeficientes de convección y radiación
	temp_superficie_previo = 100
	temp_superficie_posterior = 105

	area_canales, area_aletas, area_base = CalculaAreaCanalesAletasYBase(ancho_x,alto_y,grosor_base,profundo_z,grosor_aleta,N,area_fuentes)

	contador_iteraciones = 0
	while(abs(temp_superficie_posterior - temp_superficie_previo) > 0.01):
		temp_superficie_previo = temp_superficie_posterior
		h_conv_aletas, h_conv_base = coeficiente_conveccion.CalculaCoeficienteConveccion(ancho_x,alto_y,grosor_base,profundo_z,grosor_aleta,N,Tinf,calor_fuente_en_watts,temp_superficie_posterior,tipos_de_orientacion[orientacion])
		hr_aletas, hr_base = coeficiente_radiacion.CalculaCoeficienteRadiacion(ancho_x,alto_y,grosor_base,profundo_z,grosor_aleta,N,Tinf,calor_fuente_en_watts,temp_superficie_posterior,area_canales,area_aletas,emisividad,area_base)
		h_tot_aletas = h_conv_aletas + hr_aletas
		h_tot_base = h_conv_base + hr_base
		eficiencia = eficiencia_aleta.CalculaEficienciaAleta(ancho_x,alto_y,grosor_base,profundo_z,grosor_aleta,h_tot_aletas,k)
		temp_superficie_posterior = (calor_fuente_en_watts / (h_tot_aletas * (area_canales + eficiencia * area_aletas) + h_tot_base * area_base)) + Tinf
		contador_iteraciones += 1
		if(contador_iteraciones == 10):
			break

	biot = h_tot_aletas * grosor_aleta / k

	#print("Conveccion_aletas: " , h_conv_aletas , "Radiacion_aletas: ", hr_aletas,"Conveccion_base: " , h_conv_base , "Radiacion_base: ", hr_base, "Eficiencia: ", eficiencia, "Biot: ", biot)

	q_prima = calor_fuente_en_watts / ( fuentes['ancho'] * fuentes['profundo'] )
	#print("El calor generado por area es: ",q_prima,"W/m^2")

	divisiones_xz = dimension_grid.EstableceDimensionesGrid(fuentes,ancho_x,profundo_z,grosor_aleta,N)

	num_divisiones_x1 = divisiones_xz['num_div_x1']
	num_divisiones_x2 = divisiones_xz['num_div_x2']
	num_divisiones_z = divisiones_xz['num_div_z']
	num_divisiones_y1 = divisiones_xz['num_div_y1']
	num_divisiones_y2 = divisiones_xz['num_div_y2']

	#-----------------------------------

	dx1 = grosor_aleta/num_divisiones_x1
	dx2 = ((ancho_x - N * grosor_aleta) / (N - 1)) / num_divisiones_x2
	dy1 = (alto_y-grosor_base)/num_divisiones_y1
	dy2 = grosor_base / num_divisiones_y2
	dz = profundo_z / num_divisiones_z

	#-----------------------------------

	altura_disipador = num_divisiones_y1 + num_divisiones_y2

	#-----------------------------------

	#Crea el grid que llenará el disipador
	num_total_de_puntos, puntos_para_bajar_z = CreaListadePuntos()

	puntos_de_base = sorted(ObtenPuntosBase(), key=TomaPrimerElemento )
	EnumeraPuntosBase(puntos_de_base)
	puntos_base_sin_info_adicional = []
	for p in puntos_de_base:
		puntos_base_sin_info_adicional.append(p[1])

	T, C = GeneraMatriz(num_total_de_puntos, puntos_para_bajar_z)

	areas,punto_centro = fuentes_calor.ColocaFuentesDeCalor(divisiones_xz,dx1,dx2,dz,fuentes,puntos_de_base,N,k,q_prima,h_conv_base,Tinf,hr_base,Tsur,T,C)

	Temps_inversa = np.linalg.solve(T,C)
	#······························#······························#······························#
	#print("El numero de divisiones por aleta es: ", num_divisiones_x1,"y la distancia por division es: ", dx1)
	#print("El numero de divisiones por espacio es: ", num_divisiones_x2,"y la distancia por division es: ", dx2)
	#print("El numero de divisiones en Z es: ", num_divisiones_z,"y la distancia por division es: ", dz)
	fig = grafica.dibujaElementos(ancho_x,profundo_z,fuentes,dz,dx1,dx2,num_divisiones_x1,num_divisiones_x2,num_divisiones_z,N,areas,punto_centro,Temps_inversa[puntos_base_sin_info_adicional])

	return fig

#if __name__ == '__main__':
#	RealizaSimulacion()
