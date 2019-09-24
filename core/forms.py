from django import forms

class HeatSinkForm(forms.Form):
    tipo_disipador = forms.ChoiceField(label="TipoDisipador",choices=(('7.6','7.6cm'),('8.7','8.7cm')))
    longitud = forms.FloatField(label="Longitud")
    temperatura = forms.DecimalField(label='Temperatura',decimal_places=1,max_digits=5)
