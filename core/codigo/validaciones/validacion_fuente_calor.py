def ValidaFuenteCalorEsteDentroDisipador(datos):

    fuentes = {}
    fuentes['centro_x'] = datos["centro_x_fuente"] * 1e-3
    fuentes['centro_z']= datos["centro_z_fuente"] * 1e-3
    fuentes['ancho']= datos["ancho_x_fuente"] * 1e-3
    fuentes['profundo']= datos["profundo_z_fuente"] * 1e-3

    longitud_disipador = datos["longitud"] * 1e-3
    ancho_disipador = float(datos['tipo_disipador']) * 1e-2

    if fuentes['centro_x'] + fuentes['ancho']/2 > ancho_disipador or fuentes['centro_x'] - fuentes['ancho']/2 < 0:
        return False
    elif fuentes['centro_z'] + fuentes['profundo']/2 > longitud_disipador or fuentes['centro_z'] - fuentes['profundo']/2 < 0:
        return False
    else:
        return True
