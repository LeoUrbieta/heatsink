from django import forms

class HeatSinkForm(forms.Form):
    tipo_disipador = forms.ChoiceField(label="TipoDisipador",choices=(('7.6','7.6cm'),('8.7','8.7cm')))
    longitud = forms.FloatField(label="Longitud")
    direccion_aletas = forms.ChoiceField(
                        label="Direccion de Aletas",
                        choices=(
                            ('aletas_apuntan_arriba','arriba'),
                            ('aletas_apuntan_abajo','abajo')
                            #('aletas_perpendicular_a_suelo','perpendicular')
                            )
                        )
    emisividad = forms.FloatField(label="Emisividad")
    centro_x_fuente = forms.FloatField(label="Centro X Fuente")
    centro_z_fuente = forms.FloatField(label="Centro Z Fuente")
    ancho_x_fuente = forms.FloatField(label="Ancho X Fuente")
    profundo_z_fuente = forms.FloatField(label="Largo Z Fuente")
    calor_fuente = forms.FloatField(label="Calor Fuente")
    temperatura = forms.FloatField(label='Temperatura Ambiente')
