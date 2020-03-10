import numpy

air_properties={}

#Donde se obtuvieron los datos: https://www.engineersedge.com/physics/viscosity_of_air_dynamic_and_kinematic_14483.htm


#Dynamic viscosity,Kinematic Viscosity,Thermal Conductivity, Specific Heat
air_properties["-150"] = [8.636e-6,3.013e-6,0.01171,983]
air_properties["-100"] = [1.189e-6,5.837e-6,0.01582,966]
air_properties["-50"] = [1.474e-5,9.319e-6,0.01979,999]
air_properties["-40"] = [1.527e-5,1.008e-5,0.02057,1002]
air_properties["-30"] = [1.579e-5,1.087e-5,0.02134,1004]
air_properties["-20"] = [1.630e-5,1.169e-5,0.02211,1005]
air_properties["-10"] = [1.680e-5,1.252e-5,0.02288,1006]
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
air_properties["120"] = [2.264e-5,2.522e-5,0.03235,1011]
air_properties["140"] = [2.345e-5,2.745e-5,0.03374,1013]
air_properties["160"] = [2.420e-5,2.975e-5,0.03511,1016]
air_properties["180"] = [2.504e-5,3.212e-5,0.03646,1019]
air_properties["200"] = [2.577e-5,3.455e-5,0.03779,1023]
air_properties["250"] = [2.760e-5,4.091e-5,0.04104,1033]
air_properties["300"] = [2.934e-5,4.765e-5,0.04418,1044]
air_properties["350"] = [3.101e-5,5.475e-5,0.04721,1056]
air_properties["400"] = [3.261e-5,6.219e-5,0.05015,1069]
air_properties["450"] = [3.415e-5,6.997e-5,0.05298,1081]
air_properties["500"] = [3.563e-5,7.806e-5,0.05572,1093]
air_properties["600"] = [3.846e-5,9.515e-5,0.06093,1115]
air_properties["700"] = [4.111e-5,1.133e-4,0.06581,1135]
air_properties["800"] = [4.362e-5,1.326e-4,0.07037,1153]
air_properties["900"] = [4.600e-5,1.529e-4,0.07465,1169]
air_properties["1000"] = [4.826e-5,1.741e-4,0.07868,1184]
air_properties["1500"] = [5.817e-5,2.922e-4,0.09599,1234]
air_properties["2000"] = [6.630e-5,4.270e-4,0.11113,1264]

def ExtraeInfoAire(temperatura_aire):

	if temperatura_aire <= -125.0:
		return air_properties["-150"][0],air_properties["-150"][1],air_properties["-150"][2],air_properties["-150"][3]
	elif -125.0 < temperatura_aire <= -75.0:
		return air_properties["-100"][0],air_properties["-100"][1],air_properties["-100"][2],air_properties["-100"][3]
	elif -75.0 < temperatura_aire <= -45.0:
		return air_properties["-50"][0],air_properties["-50"][1],air_properties["-50"][2],air_properties["-50"][3]
	elif -45.0 < temperatura_aire <= -35.0:
		return air_properties["-40"][0],air_properties["-40"][1],air_properties["-40"][2],air_properties["-40"][3]
	elif -35.0 < temperatura_aire <= -25.0:
		return air_properties["-30"][0],air_properties["-30"][1],air_properties["-30"][2],air_properties["-30"][3]
	elif -25.0 < temperatura_aire <= -15.0:
		return air_properties["-20"][0],air_properties["-20"][1],air_properties["-20"][2],air_properties["-20"][3]
	elif -15.0 < temperatura_aire <= -5.0:
		return air_properties["-10"][0],air_properties["-10"][1],air_properties["-10"][2],air_properties["-10"][3]
	elif -5.0 < temperatura_aire <= 2.5:
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
	elif 95.0 < temperatura_aire <= 110.0:
		return air_properties["100"][0],air_properties["100"][1],air_properties["100"][2],air_properties["100"][3]
	elif 110.0 < temperatura_aire <= 130.0:
		return air_properties["120"][0],air_properties["120"][1],air_properties["120"][2],air_properties["120"][3]
	elif 130.0 < temperatura_aire <= 150.0:
		return air_properties["140"][0],air_properties["140"][1],air_properties["140"][2],air_properties["140"][3]
	elif 150.0 < temperatura_aire <= 170.0:
		return air_properties["160"][0],air_properties["160"][1],air_properties["160"][2],air_properties["160"][3]
	elif 170.0 < temperatura_aire <= 190.0:
		return air_properties["180"][0],air_properties["180"][1],air_properties["180"][2],air_properties["180"][3]
	elif 190.0 < temperatura_aire <= 225.0:
		return air_properties["200"][0],air_properties["200"][1],air_properties["200"][2],air_properties["200"][3]
	elif 225.0 < temperatura_aire <= 275.0:
		return air_properties["250"][0],air_properties["250"][1],air_properties["250"][2],air_properties["250"][3]
	elif 275.0 < temperatura_aire <= 325.0:
		return air_properties["300"][0],air_properties["300"][1],air_properties["300"][2],air_properties["300"][3]
	elif 325.0 < temperatura_aire <= 375.0:
		return air_properties["350"][0],air_properties["350"][1],air_properties["350"][2],air_properties["350"][3]
	elif 375.0 < temperatura_aire <= 425.0:
		return air_properties["400"][0],air_properties["400"][1],air_properties["400"][2],air_properties["400"][3]
	elif 425.0 < temperatura_aire <= 475.0:
		return air_properties["450"][0],air_properties["450"][1],air_properties["450"][2],air_properties["450"][3]
	elif 475.0 < temperatura_aire <= 550.0:
		return air_properties["500"][0],air_properties["500"][1],air_properties["500"][2],air_properties["500"][3]
	elif 550.0 < temperatura_aire <= 650.0:
		return air_properties["600"][0],air_properties["600"][1],air_properties["600"][2],air_properties["600"][3]
	elif 650.0 < temperatura_aire <= 750.0:
		return air_properties["700"][0],air_properties["700"][1],air_properties["700"][2],air_properties["700"][3]
	elif 750.0 < temperatura_aire <= 850.0:
		return air_properties["800"][0],air_properties["800"][1],air_properties["800"][2],air_properties["800"][3]
	elif 850.0 < temperatura_aire <= 950.0:
		return air_properties["900"][0],air_properties["900"][1],air_properties["900"][2],air_properties["900"][3]
	elif 950.0 < temperatura_aire <= 1250.0:
		return air_properties["1000"][0],air_properties["1000"][1],air_properties["1000"][2],air_properties["1000"][3]
	elif 1250.0 < temperatura_aire <= 1750.0:
		return air_properties["1500"][0],air_properties["1500"][1],air_properties["1500"][2],air_properties["1500"][3]
	elif 1750.0 < temperatura_aire:
		return air_properties["2000"][0],air_properties["2000"][1],air_properties["2000"][2],air_properties["2000"][3]
	else:
		return None

def ObtenLongitudCaracteristicaAletas(altura,grosor,longitud,orientacion,espacio_entre_aletas,ancho):

	#longitud_caracteristica = espacio_entre_aletas / (altura-grosor) * longitud
	#longitud_caracteristica = longitud
	longitud_caracteristica = altura-grosor

	if orientacion == "arriba" or orientacion == "abajo":
		return longitud_caracteristica
	else:
		return longitud

def CalculaGrashof(temp_ambiente,g,beta,kinematic_viscosity,temp_superficie,long_caracteristica_base,long_caracteristica_aletas):

	grashof_aletas = (g * long_caracteristica_aletas**3 * beta * (temp_superficie - temp_ambiente)) / (kinematic_viscosity**2)
	grashof_base = (g * long_caracteristica_base**3 * beta * (temp_superficie - temp_ambiente)) / (kinematic_viscosity**2)

	return grashof_aletas, grashof_base

def CalculaPrandtl(dynamic_viscosity,thermal_conductivity,cp):

	return (dynamic_viscosity * cp) / (thermal_conductivity)

def CalculaCoeficienteConveccionDeNusselt(thermal_conductivity,long_caracteristica_aletas,nusselt_aletas,nusselt_base,long_caracteristica_base):

	coef_aletas = (nusselt_aletas * thermal_conductivity) / long_caracteristica_aletas
	coef_base = (nusselt_base * thermal_conductivity) / long_caracteristica_base

	return coef_aletas, coef_base

def ObtenLongitudCaracteristicaBase(ancho, largo,area_total_fuentes,perimetro_total_fuentes):

	area = ancho * largo
	perimetro = 2 * ancho + 2 * largo

	long_caracteristica_efectiva_base = (area - area_total_fuentes) / (perimetro - perimetro_total_fuentes)

	return long_caracteristica_efectiva_base

def CalculaRayleigh(grashof_aletas,grashof_base,prandtl):

	rayleigh_aletas = grashof_aletas * prandtl
	rayleigh_base = grashof_base * prandtl

	return rayleigh_aletas, rayleigh_base

def CalculaNusselt(rayleigh_aletas,rayleigh_base,orientacion,espacio_entre_aletas,altura_disipador,grosor_aleta,grosor_base, ancho, longitud, beta, temp_superficie, temp_ambiente):

	if rayleigh_aletas < 1e9:
		if(orientacion == "arriba"):
			if ancho == 2.8e-2:
				nusselt_aletas = (ancho / longitud**0.005) * rayleigh_aletas**0.455 #2.8cm
			elif ancho == 7.6e-2:
				nusselt_aletas = ancho / (longitud**0.5) * rayleigh_aletas**0.277 #7.6cm
			elif ancho == 8.7e-2:
				nusselt_aletas = ancho / (longitud**0.25) * rayleigh_aletas**0.321 #8.7cm
			#nusselt_aletas = espacio_entre_aletas / (altura_disipador - grosor_base) * rayleigh_aletas**0.272 #13.7cm
		elif(orientacion == "abajo"):
			if ancho == 2.8e-2:
				nusselt_aletas = ancho / (longitud**0.175) * rayleigh_aletas**0.423 #2.8cm
			#nusselt_aletas =  espacio_entre_aletas / (altura_disipador - grosor_base) * rayleigh_aletas**0.223 #7.6cm
		else:
			nusselt_aletas = 0.59 * rayleigh_aletas**0.25
	else:
		nusselt_aletas = 0.14 * rayleigh_aletas**0.33

	if rayleigh_base < 1e9:
		if(orientacion == "arriba"):
			nusselt_base =  0.27 * rayleigh_base**0.25
		elif(orientacion == "abajo"):
			nusselt_base = 0.54 * rayleigh_base**0.25
		else:
			nusselt_base = 0.59 * rayleigh_base**0.25
	else:
		nusselt_base =  0.14 * rayleigh_base**0.33

	return nusselt_aletas, nusselt_base

def CalculaCoeficienteConveccion(ancho_disipador,altura_disipador,grosor_base,longitud_disipador,grosor_aleta,N,temp_ambiente,calor_fuente_en_watts,temp_superficie_posterior,orientacion,area_total_fuentes,perimetro_total_fuentes):

	g = 9.81
	beta = 1/(273 + temp_ambiente)
	espacio_entre_aletas = (ancho_disipador - N * grosor_aleta)/(N-1)

	dynamic_viscosity, kinematic_viscosity, thermal_conductivity, specific_heat = ExtraeInfoAire(temp_ambiente)
	long_caracteristica_aletas = ObtenLongitudCaracteristicaAletas(altura_disipador,grosor_base,longitud_disipador,orientacion,espacio_entre_aletas,ancho_disipador)
	long_caracteristica_base = ObtenLongitudCaracteristicaBase(ancho_disipador,longitud_disipador,area_total_fuentes,perimetro_total_fuentes)

	grashof_aletas, grashof_base = CalculaGrashof(temp_ambiente,g,beta,kinematic_viscosity,temp_superficie_posterior,long_caracteristica_base,long_caracteristica_aletas)
	prandtl = CalculaPrandtl(dynamic_viscosity,thermal_conductivity,specific_heat)
	rayleigh_aletas, rayleigh_base = CalculaRayleigh(grashof_aletas,grashof_base,prandtl)
	nusselt_aletas, nusselt_base = CalculaNusselt(rayleigh_aletas,rayleigh_base,orientacion,espacio_entre_aletas,altura_disipador,grosor_aleta,grosor_base, ancho_disipador, longitud_disipador, beta, temp_superficie_posterior, temp_ambiente)

	coeficiente_conveccion_aletas, coeficiente_conveccion_base = CalculaCoeficienteConveccionDeNusselt(thermal_conductivity,long_caracteristica_aletas,nusselt_aletas,nusselt_base,long_caracteristica_base)
	if temp_superficie_posterior == temp_ambiente:
		return 1.0, 1.0 #Se regresa un valor constante cuando la fuente de calor es 0W. Esto para que el sistema lineal no se vuelva homogeneo.
	else:
		return coeficiente_conveccion_aletas, coeficiente_conveccion_base
