import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from random import sample
import scipy.interpolate as si

matriz_z = []
matriz_y = []
matriz_x = []

def fmt(x, y):
    z = np.take(si.interp2d(matriz_x, matriz_y, matriz_z)(x, y), 0)
    return 'x={x:.5f}  y={y:.5f}  z={z:.5f}'.format(x=x, y=y, z=z)

def dibujaElementos(ancho_x,profundo_z,fuentes,dz,dx1,dx2,num_divisiones_x1,num_divisiones_x2,num_divisiones_z,N,areas,punto_centro,Temps_base):

	fig= plt.figure()
	ax = fig.add_axes([0.1,0.1,0.9,0.8])

	rect = patches.Rectangle((fuentes['centro_x']-fuentes['ancho']/2,fuentes['centro_z']-fuentes['profundo']/2),fuentes['ancho'],fuentes['profundo'],linewidth=1,edgecolor='r',facecolor='none')

	# Add the patch to the Axes
	ax.add_patch(rect)

	lista_scatter_x=[]
	lista_scatter_y=[]
	renglon_z = []
	#matriz_z = []
	#matriz_x = []
	#matriz_y = []
	dist_recorrida = 0

	contador_z = 0
	contador_temp = 0
	for punto_z in range(num_divisiones_z+1):
		for aleta in range(N-1):
			for punto_x in range(num_divisiones_x1):
				lista_scatter_x.append(dist_recorrida)
				lista_scatter_y.append(punto_z * dz)
				renglon_z.append(Temps_base[contador_temp])
				contador_temp +=1
				#print(dist_recorrida,dx1,contador_z)
				if punto_z == 0:
					matriz_x.append(dist_recorrida)
				dist_recorrida += dx1

			for punto_x in range(num_divisiones_x2):
				lista_scatter_x.append(dist_recorrida)
				lista_scatter_y.append(punto_z * dz)
				renglon_z.append(Temps_base[contador_temp])
				contador_temp +=1
				if punto_z == 0:
					matriz_x.append(dist_recorrida)
				#print(dist_recorrida,dx2,contador_z)
				dist_recorrida += dx2
		for punto_x in range(num_divisiones_x1+1):
			lista_scatter_x.append(dist_recorrida)
			lista_scatter_y.append(punto_z * dz)
			renglon_z.append(Temps_base[contador_temp])
			contador_temp +=1
			if punto_z == 0:
					matriz_x.append(dist_recorrida)
			#print(dist_recorrida,dx1,contador_z)
			dist_recorrida += dx1
		matriz_z.append(renglon_z)
		matriz_y.append(punto_z*dz)
		renglon_z = []
		dist_recorrida = 0
		contador_z += 1

	suma = 0

	# for punto in areas:
	# 	if punto[0] == 'punto_interior_no_frontera':
	# 		rect1 = patches.Rectangle((lista_scatter_x[punto[1]]-punto[2]/2,lista_scatter_y[punto[1]]-punto[3]/2),punto[2],punto[3],linewidth=1,edgecolor='b',facecolor='none')
	# 		ax.add_patch(rect1)
	# 	elif punto[0] == 'punto_interior_frontera_izq':
	# 		rect1 = patches.Rectangle((lista_scatter_x[punto[1]]-dx1/2,lista_scatter_y[punto[1]]-punto[3]/2),punto[2],punto[3],linewidth=1,edgecolor='b',facecolor='none')
	# 		ax.add_patch(rect1)
	# 	elif punto[0] == 'punto_interior_frontera_der':
	# 		rect1 = patches.Rectangle((lista_scatter_x[punto[1]]-dx2/2,lista_scatter_y[punto[1]]-punto[3]/2),punto[2],punto[3],linewidth=1,edgecolor='b',facecolor='none')
	# 		ax.add_patch(rect1)
	# 	elif punto[0] == 'borde_z_no_frontera':
	# 		if punto[1] < punto_centro:
	# 			rect1 = patches.Rectangle((lista_scatter_x[punto[1]]-punto[2]/2,lista_scatter_y[punto[1]]-punto[3]+dz/2),punto[2],punto[3],linewidth=1,edgecolor='b',facecolor='none')
	# 			ax.add_patch(rect1)
	# 		else:
	# 			rect1 = patches.Rectangle((lista_scatter_x[punto[1]]-punto[2]/2,lista_scatter_y[punto[1]]-dz/2),punto[2],punto[3],linewidth=1,edgecolor='b',facecolor='none')
	# 			ax.add_patch(rect1)
	# 	elif punto[0] == 'borde_z_frontera_izq':
	# 		if punto[1] < punto_centro:
	# 			rect1 = patches.Rectangle((lista_scatter_x[punto[1]]-dx1/2,lista_scatter_y[punto[1]]-punto[3]+dz/2),punto[2],punto[3],linewidth=1,edgecolor='b',facecolor='none')
	# 			ax.add_patch(rect1)
	# 		else:
	# 			rect1 = patches.Rectangle((lista_scatter_x[punto[1]]-dx1/2,lista_scatter_y[punto[1]]-dz/2),punto[2],punto[3],linewidth=1,edgecolor='b',facecolor='none')
	# 			ax.add_patch(rect1)
	# 	elif punto[0] == 'borde_z_frontera_der':
	# 		if punto[1] < punto_centro:
	# 			rect1 = patches.Rectangle((lista_scatter_x[punto[1]]-dx2/2,lista_scatter_y[punto[1]]-punto[3]+dz/2),punto[2],punto[3],linewidth=1,edgecolor='b',facecolor='none')
	# 			ax.add_patch(rect1)
	# 		else:
	# 			rect1 = patches.Rectangle((lista_scatter_x[punto[1]]-dx2/2,lista_scatter_y[punto[1]]-dz/2),punto[2],punto[3],linewidth=1,edgecolor='b',facecolor='none')
	# 			ax.add_patch(rect1)
	# 	else:
	# 		rect1 = patches.Rectangle((lista_scatter_x[punto[1]]-punto[2]/2,lista_scatter_y[punto[1]]-punto[3]/2),punto[2],punto[3],linewidth=1,edgecolor='b',facecolor='none')
	# 		ax.add_patch(rect1)
	# 	suma += punto[4]

	# print(suma)

	CS = ax.contourf(matriz_x,matriz_y,matriz_z,40)
	#ax.clabel(CS, inline=1, fontsize=10)
	cbar = fig.colorbar(CS)
	cbar.ax.set_ylabel('Temperatura')

	plt.scatter(lista_scatter_x,lista_scatter_y,5)
	plt.axis('equal')
	plt.gca().format_coord = fmt
	plt.show()

	return
