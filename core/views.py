import io
import matplotlib.pyplot as plt

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg
from .codigo.disipador_completo import RealizaSimulacion
from .forms import HeatSinkForm

def home(request):

    global fig

    if request.method == 'POST':
        form = HeatSinkForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            fig = RealizaSimulacion(datos)
            return render(request, "core/home.html",{'form': form})
    else:
        form = HeatSinkForm()

    return render(request, "core/home.html",{'form': form})

def plot(request):

    global fig
    # Como enviaremos la imagen en bytes la guardaremos en un buffer
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)

    # Creamos la respuesta enviando los bytes en tipo imagen png
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    # Limpiamos la figura para liberar memoria
    fig.clear()

    # Añadimos la cabecera de longitud de fichero para más estabilidad
    response['Content-Length'] = str(len(response.content))

    # Devolvemos la response
    return response
