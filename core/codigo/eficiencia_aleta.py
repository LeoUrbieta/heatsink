
import numpy as np

def CalculaEficienciaAleta(ancho,alto,grosor_base,largo,grosor_aleta,h_tot,k):

	altura_aleta = alto - grosor_base

	perimetro_punta_aleta = 2 * largo + 2 * grosor_aleta

	area_punta_aleta = grosor_aleta * largo

	m = ((h_tot * perimetro_punta_aleta)/(k * area_punta_aleta))**0.5

	l_c = altura_aleta + (grosor_aleta / 2)

	return (np.tanh(m * l_c)) / (m * l_c)
