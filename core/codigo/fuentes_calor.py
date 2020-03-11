areas = []

def EncuentraPuntoDeGridMasCercanoACentroFuente(fuentes,divisiones,dx1,dx2,dz,num_puntos_por_renglon):

	punto_renglon_x = dist_x = 0
	while dist_x < fuentes['centro_x']:
		for i in range(divisiones['num_div_x1']):
			punto_renglon_x += 1
			dist_x += dx1
			#print(dx1,punto_renglon_x,dist_x,fuentes[0])
			if dist_x >= fuentes['centro_x']:
				break
		if dist_x >= fuentes['centro_x']:
			break
		for i in range(divisiones['num_div_x2']):
			punto_renglon_x += 1
			dist_x += dx2
			#print(dx2,punto_renglon_x,dist_x,fuentes[0])
			if dist_x >= fuentes['centro_x']:
				break
		if dist_x >= fuentes['centro_x']:
				break

	punto_columna_z = dist_z = 0
	while dist_z < fuentes['centro_z']:
		punto_columna_z += 1
		dist_z += dz
		#print(punto_columna_z,dist_z,dz)

	#print("Centro X: ", punto_renglon_x, "Centro Z: ", punto_columna_z)

	return punto_columna_z * num_puntos_por_renglon + punto_renglon_x, punto_renglon_x, punto_columna_z

def EncuentraPuntosConFuenteEnZ(fuentes,dz,punto_columna_z):

	puntos_en_z = {}

	dist_a_punto_centro = punto_columna_z * dz

	num_puntos_z_superior = (fuentes['centro_z'] + fuentes['profundo']/2 - dist_a_punto_centro) / dz
	num_puntos_z_inferior = ((dist_a_punto_centro - fuentes['centro_z']) + fuentes['profundo']/2 ) / dz

	if num_puntos_z_superior < 1:
		excedente_superior = num_puntos_z_superior
	else:
		excedente_superior = num_puntos_z_superior % int(num_puntos_z_superior)

	if num_puntos_z_inferior < 1:
		excedente_inferior = num_puntos_z_inferior
	else:
		excedente_inferior = num_puntos_z_inferior % int(num_puntos_z_inferior)

	if excedente_superior > 0.5:
		num_puntos_z_superior += 1
		excedente_superior = -(excedente_superior - 0.5)
	elif excedente_superior == 0.5:
		excedente_superior = 0
	elif excedente_superior == 0:
		excedente_superior = -0.5

	if excedente_inferior > 0.5:
		num_puntos_z_inferior += 1
		excedente_inferior = -(excedente_inferior - 0.5)
	elif excedente_inferior == 0.5:
		excedente_inferior = 0
	elif excedente_inferior == 0:
		excedente_inferior = -0.5

	dist_extra_superior = excedente_superior * dz
	dist_extra_inferior = excedente_inferior * dz

	puntos_en_z['superior'] = int(num_puntos_z_superior)
	puntos_en_z['inferior'] = int(num_puntos_z_inferior)
	puntos_en_z['extra_superior'] = dist_extra_superior
	puntos_en_z['extra_inferior'] = dist_extra_inferior

	return puntos_en_z

def EncuentraDistAPuntoX(div,punto_renglon_x,dx1,dx2):

	dist_a_punto_x = i = j = 0

	while i < punto_renglon_x:
		for j in range(div['num_div_x1']):
			dist_a_punto_x += dx1
			i += 1
			#print(dist_a_punto_centro_x,i,j,dx1)
			if i == punto_renglon_x:
				break
		if i == punto_renglon_x:
		 	break
		for j in range(div['num_div_x2']):
			dist_a_punto_x += dx2
			i += 1
			#print(dist_a_punto_centro_x,i,j,dx2)
			if i == punto_renglon_x:
				break
		if i == punto_renglon_x:
		 	break

	return dist_a_punto_x

def CreaVectoresConDistAIzqYDer(divisiones,dx1,dx2,punto_renglon_x, num_puntos_por_renglon):

	vector_a_izq = []
	vector_a_der = []
	i = 0

	while i < punto_renglon_x:
		for j in range(divisiones['num_div_x1']):
			i += 1
			vector_a_izq.append(dx1)
			if i == punto_renglon_x:
				break
		if i == punto_renglon_x:
			break
		for j in range(divisiones['num_div_x2']):
			i += 1
			vector_a_izq.append(dx2)
			if i == punto_renglon_x:
				break
		if i == punto_renglon_x:
			break

	i = num_puntos_por_renglon

	while i > punto_renglon_x:
		for j in range(divisiones['num_div_x1']):
			i -= 1
			vector_a_der.append(dx1)
			if i == (punto_renglon_x + 1):
				i = punto_renglon_x
				break
		if i == punto_renglon_x:
			break
		for j in range(divisiones['num_div_x2']):
			i -= 1
			vector_a_der.append(dx2)
			if i == (punto_renglon_x + 1):
				i = punto_renglon_x
				break
		if i == punto_renglon_x:
			break

	return vector_a_izq,vector_a_der

def EncuentraPuntosConFuenteEnX(fuentes,divisiones,dx1,dx2,punto_renglon_x,num_puntos_por_renglon):

	puntos_con_fuente_en_x = {}

	dist_a_punto_x = EncuentraDistAPuntoX(divisiones,punto_renglon_x,dx1,dx2)

	vector_izq, vector_der = CreaVectoresConDistAIzqYDer(divisiones,dx1,dx2,punto_renglon_x,num_puntos_por_renglon)

	dist_x_izq = fuentes['centro_x'] - (dist_a_punto_x - vector_izq[-1])
	dist_x_der = dist_a_punto_x - fuentes['centro_x']

	num_puntos_izq = 0
	num_puntos_der = -1 #-1 ya que si no contaríamos el punto central 2 veces.

	#Empezamos con el contador en -2 ya que el punto central es el -1 y ya se consideró
	contador_izq = -2
	while dist_x_izq < fuentes['ancho']/2:
		num_puntos_izq += 1
		dist_x_izq += vector_izq[contador_izq]
		if dist_x_izq < fuentes['ancho']/2:
			contador_izq -= 1

	contador_der = -1
	while dist_x_der < fuentes['ancho']/2:
		num_puntos_der += 1
		dist_x_der += vector_der[contador_der]
		if dist_x_der < fuentes['ancho']/2:
			contador_der -= 1

	porcentaje_sobrado_izq =  1 - ((dist_x_izq -  fuentes['ancho']/2) / vector_izq[contador_izq])
	porcentaje_sobrado_der =  1 - ((dist_x_der -  fuentes['ancho']/2) / vector_der[contador_der])

	if porcentaje_sobrado_izq > 0.5:
		num_puntos_izq += 1
		porcentaje_sobrado_izq = -(porcentaje_sobrado_izq - 0.5)
	elif porcentaje_sobrado_izq == 0.5:
		porcentaje_sobrado_izq = 0
	elif porcentaje_sobrado_izq == 0:
		porcentaje_sobrado_izq = -0.5

	if porcentaje_sobrado_der > 0.5:
		num_puntos_der+= 1
		porcentaje_sobrado_der =  -(porcentaje_sobrado_der - 0.5)
	elif porcentaje_sobrado_der == 0.5:
		porcentaje_sobrado_der = 0
	elif porcentaje_sobrado_der == 0:
		porcentaje_sobrado_der = -0.5

	dist_extra_izq = porcentaje_sobrado_izq * vector_izq[contador_izq]
	dist_extra_der = porcentaje_sobrado_der * vector_der[contador_der]

	puntos_con_fuente_en_x['puntos_izq'] = num_puntos_izq
	puntos_con_fuente_en_x['puntos_der'] = num_puntos_der
	puntos_con_fuente_en_x['sobrado_izq'] = dist_extra_izq
	puntos_con_fuente_en_x['sobrado_der'] = dist_extra_der

	return puntos_con_fuente_en_x

def EncuentraPuntosDeSuperficieCubiertosPorFuenteDeCalor(punto_centro_x,punto_centro_z,puntos_en_x,puntos_en_z,puntos_con_fuente_de_calor,num_puntos_por_renglon):

	punto_a_agregar = (punto_centro_z - puntos_en_z['inferior']) * num_puntos_por_renglon + (punto_centro_x - puntos_en_x['puntos_izq'])
	puntos_con_fuente_de_calor.append(punto_a_agregar)

	for i in range(puntos_en_z['superior'] + puntos_en_z['inferior'] + 1):
		for j in range(puntos_en_x['puntos_izq'] + puntos_en_x['puntos_der']):
			punto_a_agregar += 1
			if punto_a_agregar == puntos_con_fuente_de_calor[0]:
				continue
			else:
				puntos_con_fuente_de_calor.append(punto_a_agregar)
		punto_a_agregar += num_puntos_por_renglon - (puntos_en_x['puntos_izq'] + puntos_en_x['puntos_der'])
		if i == puntos_en_z['superior'] + puntos_en_z['inferior'] and j == puntos_en_x['puntos_izq'] + puntos_en_x['puntos_der'] - 1:
			continue
		else:
			puntos_con_fuente_de_calor.append(punto_a_agregar)

	return puntos_con_fuente_de_calor

def CreaListaPuntosTotalmenteCubiertos(puntos_despl_en_x,puntos_despl_en_z,puntos_con_calor):

	puntos_totalmente_cubiertos = puntos_con_calor.copy()
	limite = puntos_despl_en_x['puntos_izq'] + puntos_despl_en_x['puntos_der'] + 1

	puntos_superior_z = []
	puntos_inferior_z = []
	puntos_izq_x = []
	puntos_der_x = []

	if puntos_despl_en_z['extra_superior'] != 0:
		puntos_superior_z = puntos_con_calor[-limite:-1]
		puntos_superior_z.append(puntos_con_calor[-1])
	if puntos_despl_en_z['extra_inferior'] != 0:
		puntos_inferior_z = puntos_con_calor[0:limite]
	if puntos_despl_en_x['sobrado_izq'] != 0 or puntos_despl_en_x['sobrado_der'] != 0:
		contador_para_subir = 0
		for i in range(puntos_despl_en_z['superior'] + puntos_despl_en_z['inferior'] + 1):
			if puntos_despl_en_x['sobrado_izq'] != 0:
				puntos_izq_x.append(puntos_con_calor[contador_para_subir])
			if puntos_despl_en_x['sobrado_der'] != 0:
				puntos_der_x.append(puntos_con_calor[contador_para_subir + limite - 1])
			contador_para_subir += limite

	puntos_a_remover = sorted(list(set(puntos_superior_z + puntos_inferior_z + puntos_izq_x + puntos_der_x)))

	for i in puntos_a_remover:
		if i in puntos_totalmente_cubiertos: puntos_totalmente_cubiertos.remove(i)

	return puntos_totalmente_cubiertos,puntos_superior_z,puntos_inferior_z,puntos_izq_x,puntos_der_x

def CalculaPuntosInteriores(puntos_cubiertos,puntos_base,dx1,dx2,dz,k,q_prima,h,hr,T,C):

	for punto in puntos_cubiertos:
		if puntos_base[punto][2] == 'superficie_x2':
			area_calor = dz * dx2
			areas.append(['punto_interior_no_frontera',punto,area_calor/dz,dz,area_calor])
		elif puntos_base[punto][2] == 'superficie_x1':
			area_calor = dz * dx1
			areas.append(['punto_interior_no_frontera',punto,area_calor/dz,dz,area_calor])
		elif puntos_base[punto][2] == 'frontera_x_izq' or puntos_base[punto][2] == 'frontera_x_der':
			area_calor = dz * (dx1/2 + dx2/2)
			if puntos_base[punto][2] == 'frontera_x_izq':
				areas.append(['punto_interior_frontera_izq',punto,area_calor/dz,dz,area_calor])
			else:
				areas.append(['punto_interior_frontera_der',punto,area_calor/dz,dz,area_calor])

		C[puntos_base[punto][1]] = - (2 * q_prima * area_calor / k)
		T[puntos_base[punto][1]][puntos_base[punto][1]] += 2*(h+hr)/k*area_calor

	return

def CalculaBordes(direccion_puntos,sobrado,puntos_base,puntos_con_fuente_x,dx1,dx2):

	if puntos_base[direccion_puntos[0]][2] == 'superficie_x2':
		dist_x = dx2
	elif puntos_base[direccion_puntos[0]][2] == 'superficie_x1':
		dist_x = dx1
	elif puntos_base[direccion_puntos[0]][2] == 'frontera_x_izq' or puntos_base[direccion_puntos[0]][2] == 'frontera_x_der':
		if puntos_con_fuente_x['sobrado'] < 0:
			dist_x = dx2
		else:
			dist_x = dx1

	return dist_x

def CalculaBordeEnZ(puntos_z,puntos_con_fuente_z,superior_o_inferior,puntos_base,dz,dx1,dx2,k,q_prima,h,Tinf,hr,Tsur,T,C):

	for punto in puntos_z:

		if puntos_con_fuente_z[superior_o_inferior] < 0:
			dist_z = -puntos_con_fuente_z[superior_o_inferior]
		else:
			dist_z = dz/2 + puntos_con_fuente_z[superior_o_inferior]

		if puntos_base[punto][2] == 'superficie_x2':
			area_total = dx2 * dz
			area_calor = dist_z * dx2
			areas.append(['borde_z_no_frontera',punto,area_calor/dist_z,dist_z,area_calor])
		elif puntos_base[punto][2] == 'superficie_x1':
			area_total = dx1 * dz
			area_calor = dist_z * dx1
			areas.append(['borde_z_no_frontera',punto,area_calor/dist_z,dist_z,area_calor])
		elif puntos_base[punto][2] == 'frontera_x_izq' or puntos_base[punto][2] == 'frontera_x_der':
			area_total = (dx1/2 + dx2/2) * dz
			area_calor = dist_z * (dx1/2 + dx2/2)
			if puntos_base[punto][2] == 'frontera_x_izq':
				areas.append(['borde_z_frontera_izq',punto,area_calor/dist_z,dist_z,area_calor])
			else:
				areas.append(['borde_z_frontera_der',punto,area_calor/dist_z,dist_z,area_calor])

		C[puntos_base[punto][1]] += 2*(h*Tinf+hr*Tsur)/k*(area_calor) - (2*q_prima*area_calor/k)
		#C[puntos_base[punto][1]] = -2*(h*Tinf+hr*Tsur)/k*(area_total - area_calor) - (2 * q_prima * area_calor / k)
		T[puntos_base[punto][1]][puntos_base[punto][1]] += 2*(h+hr)/k*area_calor

	return

def ExtraeYEliminaEsquinasDuplicadas(puntos_base,puntos_superior_z,puntos_inferior_z,puntos_izq_x,puntos_der_x):

	puntos_esquina = []

	if len(puntos_superior_z) != 0 and len(puntos_izq_x) != 0: #Solo entrar a estas condiciones si existen sobrantes
		if puntos_superior_z[0] == puntos_izq_x[-1]:
			puntos_esquina.append([puntos_superior_z[0],'extra_superior','sobrado_izq',puntos_base[puntos_superior_z[0]][2]])
			del puntos_superior_z[0]
			del puntos_izq_x[-1]
	if len(puntos_inferior_z) != 0 and len(puntos_izq_x) != 0:
		if puntos_izq_x[0] == puntos_inferior_z[0]:
			puntos_esquina.append([puntos_izq_x[0],'extra_inferior','sobrado_izq',puntos_base[puntos_izq_x[0]][2]])
			del puntos_izq_x[0]
			del puntos_inferior_z[0]
	if len(puntos_inferior_z) != 0 and len(puntos_der_x) != 0:
		if puntos_inferior_z[-1] == puntos_der_x[0]:
			puntos_esquina.append([puntos_inferior_z[-1],'extra_inferior','sobrado_der',puntos_base[puntos_inferior_z[-1]][2]])
			del puntos_inferior_z[-1]
			del puntos_der_x[0]
	if len(puntos_superior_z) != 0 and len(puntos_der_x) != 0:
		if puntos_der_x[-1] == puntos_superior_z[-1]:
			puntos_esquina.append([puntos_der_x[-1],'extra_superior','sobrado_der',puntos_base[puntos_der_x[-1]][2]])
			del puntos_der_x[-1]
			del puntos_superior_z[-1]

	return puntos_esquina

def CalculaBordeZ(puntos_base,puntos_superior_z,puntos_inferior_z,puntos_con_fuente_z,dz,dx1,dx2,k,q_prima,h,Tinf,hr,Tsur,T,C):

	CalculaBordeEnZ(puntos_superior_z,puntos_con_fuente_z,'extra_superior',puntos_base,dz,dx1,dx2,k,q_prima,h,Tinf,hr,Tsur,T,C)
	CalculaBordeEnZ(puntos_inferior_z,puntos_con_fuente_z,'extra_inferior',puntos_base,dz,dx1,dx2,k,q_prima,h,Tinf,hr,Tsur,T,C)

	return

def CalculaBordeEnX(puntos_base,tipo_puntos,tipo_sobrado,puntos_con_fuente_x,dz,dx1,dx2,k,q_prima,h,Tinf,hr,Tsur,T,C):

	if puntos_base[tipo_puntos[0]][2] == 'superficie_x2':
		dist_x = dx2/2
		area_total = dz * dx2
	elif puntos_base[tipo_puntos[0]][2] == 'superficie_x1':
		dist_x = dx1/2
		area_total = dz * dx1
	elif puntos_base[tipo_puntos[0]][2] == 'frontera_x_izq':
		if tipo_sobrado == 'sobrado_izq':
			dist_x = dx2/2
		else:
			dist_x = dx1/2
		area_total = dz * (dx1/2+dx2/2)
	elif puntos_base[tipo_puntos[0]][2] == 'frontera_x_der':
		if tipo_sobrado == 'sobrado_izq':
			dist_x = dx1/2
		else:
			dist_x = dx2/2
		area_total = dz * (dx1/2+dx2/2)
	else:
		area_total = dz * dx1/2

	if puntos_con_fuente_x[tipo_sobrado] < 0:
		area_calor = -puntos_con_fuente_x[tipo_sobrado] * dz
	else:
		area_calor = (dist_x + puntos_con_fuente_x[tipo_sobrado]) * dz

	for punto in tipo_puntos:
		C[puntos_base[punto][1]] += 2*(h*Tinf+hr*Tsur)/k*(area_calor) - (2*q_prima*area_calor/k)
		#C[puntos_base[punto][1]] = -2*(h*Tinf+hr*Tsur)/k*(area_total - area_calor) - (2 * q_prima * area_calor / k)
		T[puntos_base[punto][1]][puntos_base[punto][1]] += 2*(h+hr)/k*area_calor
		areas.append(['borde_x',punto,area_calor/dz,dz,area_calor])

	return

def CalculaBordeX(puntos_base,puntos_izq_x,puntos_der_x,puntos_con_fuente_x,dz,dx1,dx2,k,q_prima,h,Tinf,hr,Tsur,T,C):

	CalculaBordeEnX(puntos_base,puntos_izq_x,'sobrado_izq',puntos_con_fuente_x,dz,dx1,dx2,k,q_prima,h,Tinf,hr,Tsur,T,C)
	CalculaBordeEnX(puntos_base,puntos_der_x,'sobrado_der',puntos_con_fuente_x,dz,dx1,dx2,k,q_prima,h,Tinf,hr,Tsur,T,C)

	return

def CalculaEsquinas(puntos_esquina,puntos_base,puntos_con_fuente_x,puntos_con_fuente_z,dz,dx1,dx2,k,q_prima,h,Tinf,hr,Tsur,T,C):

	for p in puntos_esquina:
		if p[3] == 'superficie_x2':
			area_total = dx2 * dz
			dist_x = dx2/2
		elif p[3] == 'superficie_x1':
			area_total = dx1 * dz
			dist_x = dx1/2
		elif p[3] == 'frontera_x_izq':
			area_total = dz * (dx1/2 + dx2/2)
			if p[2] == 'sobrado_izq':
				dist_x = dx2/2
			else:
				dist_x = dx1/2
		elif p[3] == 'frontera_x_der':
			area_total = dz * (dx1/2 + dx2/2)
			if p[2] == 'sobrado_der':
				dist_x = dx2/2
			else:
				dist_x = dx1/2
		else:
			area_total = dz/2 * dx1/2

		if puntos_con_fuente_z[p[1]] > 0 and puntos_con_fuente_x[p[2]] > 0:
			area_calor = (dz/2 + puntos_con_fuente_z[p[1]]) * (dist_x + puntos_con_fuente_x[p[2]])
		elif puntos_con_fuente_z[p[1]] < 0 and puntos_con_fuente_x[p[2]] > 0:
			area_calor = -puntos_con_fuente_z[p[1]] * (dist_x + puntos_con_fuente_x[p[2]])
		elif puntos_con_fuente_z[p[1]] > 0 and puntos_con_fuente_x[p[2]] < 0:
			area_calor = -puntos_con_fuente_x[p[2]] * (dz/2 + puntos_con_fuente_z[p[1]])
		elif puntos_con_fuente_z[p[1]] < 0 and puntos_con_fuente_x[p[2]] < 0:
			area_calor = puntos_con_fuente_z[p[1]] * puntos_con_fuente_x[p[2]]

		C[puntos_base[p[0]][1]] += 2*(h*Tinf+hr*Tsur)/k*(area_calor) - (2*q_prima*area_calor/k)
		#C[puntos_base[p[0]][1]] = -2*(h*Tinf+hr*Tsur)/k*(area_total - area_calor) - (2 * q_prima * area_calor / k)
		T[puntos_base[p[0]][1]][puntos_base[p[0]][1]] += 2*(h+hr)/k*area_calor
		areas.append(['esquina',p[0],area_calor/dz,dz,area_calor])

	return

def CalculaPuntosExternos(puntos_base,puntos_con_fuente_x,puntos_con_fuente_z,puntos_superior_z,puntos_inferior_z,puntos_izq_x,puntos_der_x,dx1,dx2,dz,k,q_prima,h,Tinf,hr,Tsur,T,C):

	puntos_esquina = ExtraeYEliminaEsquinasDuplicadas(puntos_base,puntos_superior_z,puntos_inferior_z,puntos_izq_x,puntos_der_x)

	#print(puntos_con_fuente_x)
	#print(puntos_con_fuente_z)

	CalculaBordeZ(puntos_base,puntos_superior_z,puntos_inferior_z,puntos_con_fuente_z,dz,dx1,dx2,k,q_prima,h,Tinf,hr,Tsur,T,C)
	CalculaBordeX(puntos_base,puntos_izq_x,puntos_der_x,puntos_con_fuente_x,dz,dx1,dx2,k,q_prima,h,Tinf,hr,Tsur,T,C)
	CalculaEsquinas(puntos_esquina,puntos_base,puntos_con_fuente_x,puntos_con_fuente_z,dz,dx1,dx2,k,q_prima,h,Tinf,hr,Tsur,T,C)

	return

def CalculaCoeficientesdeMatriz(puntos_cubiertos,puntos_con_fuente_x,puntos_con_fuente_z,puntos_superior_z,puntos_inferior_z,puntos_izq_x,puntos_der_x,puntos_base,k,q_prima,dx1,dx2,dz,h,Tinf,hr,Tsur,T,C):

	CalculaPuntosInteriores(puntos_cubiertos,puntos_base,dx1,dx2,dz,k,q_prima,h,hr,T,C)
	CalculaPuntosExternos(puntos_base,puntos_con_fuente_x,puntos_con_fuente_z,puntos_superior_z,puntos_inferior_z,puntos_izq_x,puntos_der_x,dx1,dx2,dz,k,q_prima,h,Tinf,hr,Tsur,T,C)

	return

def ColocaFuentesDeCalor(divisiones,dx1,dx2,dz,vector_fuentes,puntos_base,N,k,h,Tinf,hr,Tsur,T,C):

	for fuente in vector_fuentes:

		fuentes = {}
		fuentes['centro_x'] = fuente[0]
		fuentes['centro_z']= fuente[1]
		fuentes['ancho']= fuente[2]
		fuentes['profundo']= fuente[3]
		fuentes['calor'] = fuente[4]

		q_prima = fuentes['calor'] / ( fuentes['ancho'] * fuentes['profundo'] )

		puntos_con_fuente_de_calor = []

		num_puntos_por_renglon = divisiones['num_div_x1'] * N + divisiones['num_div_x2'] * (N-1) + 1

		punto_centro, punto_renglon_x, punto_columna_z = EncuentraPuntoDeGridMasCercanoACentroFuente(fuentes,divisiones,dx1,dx2,dz,num_puntos_por_renglon)
		puntos_con_fuente_de_calor.append(punto_centro)

		puntos_con_fuente_en_x = EncuentraPuntosConFuenteEnX(fuentes,divisiones,dx1,dx2,punto_renglon_x,num_puntos_por_renglon)
		puntos_con_fuente_en_z = EncuentraPuntosConFuenteEnZ(fuentes,dz,punto_columna_z)

		puntos_con_fuentes_de_calor = EncuentraPuntosDeSuperficieCubiertosPorFuenteDeCalor(punto_renglon_x,punto_columna_z,puntos_con_fuente_en_x,puntos_con_fuente_en_z,puntos_con_fuente_de_calor,num_puntos_por_renglon)

		puntos_cubiertos,puntos_superior_z,puntos_inferior_z,puntos_izq_x,puntos_der_x = CreaListaPuntosTotalmenteCubiertos(puntos_con_fuente_en_x,puntos_con_fuente_en_z,sorted(puntos_con_fuente_de_calor))

		CalculaCoeficientesdeMatriz(puntos_cubiertos,puntos_con_fuente_en_x,puntos_con_fuente_en_z,puntos_superior_z,puntos_inferior_z,puntos_izq_x,puntos_der_x,puntos_base,k,q_prima,dx1,dx2,dz,h,Tinf,hr,Tsur,T,C)

	return areas,punto_centro
