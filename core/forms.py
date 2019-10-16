from django import forms

class HeatSinkForm(forms.Form):
    tipo_disipador = forms.ChoiceField(label="TipoDisipador",choices=(('7.6','7.6cm'),('8.7','8.7cm')))
    longitud = forms.FloatField(label="Longitud",help_text='mm')
    direccion_aletas = forms.ChoiceField(
                        label="Direccion de Aletas",
                        choices=(
                            ('aletas_apuntan_arriba','arriba'),
                            ('aletas_apuntan_abajo','abajo')
                            #('aletas_perpendicular_a_suelo','perpendicular')
                            )
                        )
    centro_x_fuente = forms.FloatField(label="Centro X Fuente",help_text='mm')
    centro_z_fuente = forms.FloatField(label="Centro Z Fuente",help_text='mm')
    ancho_x_fuente = forms.FloatField(label="Ancho X Fuente",help_text='mm')
    profundo_z_fuente = forms.FloatField(label="Largo Z Fuente",help_text='mm')
    calor_fuente = forms.FloatField(label="Calor Fuente",help_text='W')
    temperatura = forms.FloatField(label='Temperatura Ambiente',help_text='C')
