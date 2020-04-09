
import math

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

eps = 1
sigma = 5.67e-8

def CalculaViewFactor(ancho,alto,grueso_base,largo,grueso_aleta,N,ancho_canal,alto_aleta):

	h_p = alto_aleta / ancho_canal
	l_p = largo / ancho_canal

	return 1 - ((2 * h_p * ((1+l_p**2)**0.5 - 1))/(2 * h_p * l_p + (1+l_p**2)**0.5 - 1))

def CalculaCalorCanal(ancho,alto,grueso_base,largo,grueso_aleta,N,Tinf,temp_superficie_posterior):

	alto_aleta = alto - grueso_base
	ancho_canal = (ancho - (N * grueso_aleta)) / (N-1)

	view_factor = CalculaViewFactor(ancho,alto,grueso_base,largo,grueso_aleta,N,ancho_canal,alto_aleta)

	return (sigma * (ancho_canal + 2 * alto_aleta)*((temp_superficie_posterior+273)**4 - (Tinf+273)**4) * largo)/(((1-eps)/eps) + (1 / view_factor))

def CalculaAreaNoAfectadaPorReboteRadiacion(ancho,alto,grueso_base,largo,grueso_aleta,N,area_base):

	alto_aleta = alto - grueso_base

	return N * (largo * grueso_aleta + 2 * alto_aleta * grueso_aleta) + 2 * alto_aleta * largo + 2 * grueso_aleta * (largo + ancho) + area_base


def CalcularCalorRadiacionAletas(ancho,alto,grueso_base,largo,grueso_aleta,N,Tinf,temp_superficie_posterior,area_base):

	calor_canal = CalculaCalorCanal(ancho,alto,grueso_base,largo,grueso_aleta,N,Tinf,temp_superficie_posterior)
	area_no_afectada_por_rebote_radiacion = CalculaAreaNoAfectadaPorReboteRadiacion(ancho,alto,grueso_base,largo,grueso_aleta,N,area_base)

	return (N - 1) * calor_canal + area_no_afectada_por_rebote_radiacion * sigma * eps * ((temp_superficie_posterior+273)**4 - (Tinf+273)**4)

def CalculaCoeficienteRadiacion(ancho,alto,grueso_base,largo,grueso_aleta,N,Tinf,temp_superficie_posterior,area_canales,area_aletas,emisividad,area_base):

	global eps

	eps = emisividad

	calor_radiacion_aletas = CalcularCalorRadiacionAletas(ancho,alto,grueso_base,largo,grueso_aleta,N,Tinf,temp_superficie_posterior,area_base)

	if temp_superficie_posterior == Tinf:
		return 1.0, 1.0 #Se regresa un valor constante cuando la fuente de calor es 0W. Esto para que el sistema lineal no se vuelva homogeneo.
	else:
		return (calor_radiacion_aletas)/((area_canales + area_aletas + area_base)*(temp_superficie_posterior - Tinf)) , 0.0
		#return (calor_radiacion_aletas)/((area_canales + area_aletas + area_base)*(temp_superficie_posterior - Tinf)) , (calor_radiacion_aletas)/((area_canales + area_aletas + area_base)*(temp_superficie_posterior - Tinf))
