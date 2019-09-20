air_properties={}

#Donde se obtuvieron los datos: https://www.engineersedge.com/physics/viscosity_of_air_dynamic_and_kinematic_14483.htm


#Dynamic viscosity,Kinematic Viscosity,Thermal Conductivity, Specific Heat
air_properties["0"] = [1.729e-5,1.338e-5,0.02364,1006]
air_properties["5"] = [1.754e-5,1.382e-5,0.02401,1006]
air_properties["10"] = [1.778e-5,1.426e-5,0.02439,1006]
air_properties["15"] = [1.802e-5,1.470e-5,0.02476,1007]
air_properties["20"] = [1.825e-5,1.516e-5,0.02514,1007]
air_properties["25"] = [1.849e-5,1.562e-5,0.02551,1007]
air_properties["30"] = [1.872e-5,1.608e-5,0.02588,1007]
air_properties["35"] = [1.895e-5,1.655e-5,0.02625,1007]
air_properties["40"] = [1.918e-5,1.702e-5,0.02662,1007]
air_properties["45"] = [1.941e-5,1.750e-5,0.02699,1007]
air_properties["50"] = [1.963e-5,1.798e-5,0.02735,1007]
air_properties["60"] = [2.008e-5,1.896e-5,0.02808,1007]
air_properties["70"] = [2.052e-5,1.995e-5,0.02881,1007]
air_properties["80"] = [2.096e-5,2.097e-5,0.02953,1008]
air_properties["90"] = [2.139e-5,2.201e-5,0.03024,1008]
air_properties["100"] = [2.181e-5,2.306e-5,0.03095,1009]

def ExtraeInfoAire(temperatura_aire):

	if 0 < temperatura_aire <= 2.5:
		return air_properties["0"][0],air_properties["0"][1],air_properties["0"][2],air_properties["0"][3]
	elif 2.5 < temperatura_aire <= 7.5:
		return air_properties["5"][0],air_properties["5"][1],air_properties["5"][2],air_properties["5"][3]
	elif 7.5 < temperatura_aire <= 12.5:
		return air_properties["10"][0],air_properties["10"][1],air_properties["10"][2],air_properties["10"][3]
	elif 12.5 < temperatura_aire <= 17.5:
		return air_properties["15"][0],air_properties["15"][1],air_properties["15"][2],air_properties["15"][3]
	elif 17.5 < temperatura_aire <= 22.5:
		return air_properties["20"][0],air_properties["20"][1],air_properties["20"][2],air_properties["20"][3]
	elif 22.5 < temperatura_aire <= 27.5:
		return air_properties["25"][0],air_properties["25"][1],air_properties["25"][2],air_properties["25"][3]
	elif 27.5 < temperatura_aire <= 32.5:
		return air_properties["30"][0],air_properties["30"][1],air_properties["30"][2],air_properties["30"][3]
	elif 32.5 < temperatura_aire <= 37.5:
		return air_properties["35"][0],air_properties["35"][1],air_properties["35"][2],air_properties["35"][3]
	elif 37.5 < temperatura_aire <= 42.5:
		return air_properties["40"][0],air_properties["40"][1],air_properties["40"][2],air_properties["40"][3]
	elif 42.5 < temperatura_aire <= 47.5:
		return air_properties["45"][0],air_properties["45"][1],air_properties["45"][2],air_properties["45"][3]
	elif 47.5 < temperatura_aire <= 55.0:
		return air_properties["50"][0],air_properties["50"][1],air_properties["50"][2],air_properties["50"][3]
	elif 55.0 < temperatura_aire <= 65.0:
		return air_properties["60"][0],air_properties["60"][1],air_properties["60"][2],air_properties["60"][3]
	elif 65.0 < temperatura_aire <= 75.0:
		return air_properties["70"][0],air_properties["70"][1],air_properties["70"][2],air_properties["70"][3]
	elif 75.0 < temperatura_aire <= 85.0:
		return air_properties["80"][0],air_properties["80"][1],air_properties["80"][2],air_properties["80"][3]
	elif 85.0 < temperatura_aire <= 95.0:
		return air_properties["90"][0],air_properties["90"][1],air_properties["90"][2],air_properties["90"][3]
	elif 95.0 < temperatura_aire <= 105.0:
		return air_properties["100"][0],air_properties["100"][1],air_properties["100"][2],air_properties["100"][3]
	else:
		return None

def ObtenLongitudCaracteristicaAletas(altura,grosor,longitud):

	if (altura - grosor) > longitud:
		return altura - grosor
	else:
		return longitud

def CalculaGrashof(temp_ambiente,g,beta,long_caracteristica_aletas,kinematic_viscosity,temp_superficie,long_caracteristica_base):

	grashof_aletas = (g * long_caracteristica_aletas**3 * beta * (temp_superficie - temp_ambiente)) / (kinematic_viscosity**2)
	grashof_base = (g * long_caracteristica_base**3 * beta * (temp_superficie - temp_ambiente)) / (kinematic_viscosity**2)

	return grashof_aletas, grashof_base

def CalculaPrandtl(dynamic_viscosity,thermal_conductivity,cp):

	return (dynamic_viscosity * cp) / (thermal_conductivity)

def CalculaCoeficienteConveccionDeNusselt(thermal_conductivity,long_caracteristica_aletas,nusselt_aletas,nusselt_base,long_caracteristica_base):

	coef_aletas = (nusselt_aletas * thermal_conductivity) / long_caracteristica_aletas
	coef_base = (nusselt_base * thermal_conductivity) / long_caracteristica_base

	return coef_aletas, coef_base

def ObtenLongitudCaracteristicaBase(ancho, largo):

	if ancho > largo:
		return ancho
	else:
		return largo

def CalculaRayleigh(grashof_aletas,grashof_base,prandtl):

	rayleigh_aletas = grashof_aletas * prandtl
	rayleigh_base = grashof_base * prandtl

	return rayleigh_aletas, rayleigh_base

def CalculaNusselt(rayleigh_aletas,rayleigh_base,orientacion):

	if rayleigh_aletas < 1e9:
		if(orientacion == "arriba"):
			nusselt_aletas = 0.54 * rayleigh_aletas**0.243
			#nusselt_aletas = 0.54 * rayleigh_aletas**0.232
		elif(orientacion == "abajo"):
			nusselt_aletas = 0.27 * rayleigh_aletas**0.265
		else:
			nusselt_aletas = 0.1 * rayleigh_aletas**0.232
	else:
		nusselt_aletas = 0.14 * rayleigh_aletas**0.33

	if rayleigh_base < 1e9:
		if(orientacion == "arriba"):
			nusselt_base = 0.27 * rayleigh_base**0.243
			#nusselt_base = 0.27 * rayleigh_base**0.2645
		elif(orientacion == "abajo"):
			nusselt_base = 0.54 * rayleigh_base**0.27
		else:
			nusselt_base = 0.1 * rayleigh_base**0.232
	else:
		nusselt_base =  0.14 * rayleigh_base**0.33

	return nusselt_aletas, nusselt_base

def CalculaCoeficienteConveccion(ancho_disipador,altura_disipador,grosor_base,longitud_disipador,grosor_aleta,N,temp_ambiente,calor_fuente_en_watts,temp_superficie_posterior,orientacion):

	g = 9.81
	beta = 1/(273 + temp_ambiente)

	dynamic_viscosity, kinematic_viscosity, thermal_conductivity, specific_heat = ExtraeInfoAire(temp_ambiente)
	long_caracteristica_aletas = ObtenLongitudCaracteristicaAletas(altura_disipador,grosor_base,longitud_disipador)
	long_caracteristica_base = ObtenLongitudCaracteristicaBase(ancho_disipador,longitud_disipador)

	grashof_aletas, grashof_base = CalculaGrashof(temp_ambiente,g,beta,long_caracteristica_aletas,kinematic_viscosity,temp_superficie_posterior,long_caracteristica_base)
	prandtl = CalculaPrandtl(dynamic_viscosity,thermal_conductivity,specific_heat)
	rayleigh_aletas, rayleigh_base = CalculaRayleigh(grashof_aletas,grashof_base,prandtl)
	nusselt_aletas, nusselt_base = CalculaNusselt(rayleigh_aletas,rayleigh_base,orientacion)

	coeficiente_conveccion_aletas, coeficiente_conveccion_base = CalculaCoeficienteConveccionDeNusselt(thermal_conductivity,long_caracteristica_aletas,nusselt_aletas,nusselt_base,long_caracteristica_base)

	return coeficiente_conveccion_aletas, coeficiente_conveccion_base