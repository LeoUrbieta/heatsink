import io
import matplotlib.pyplot as plt
import django_rq

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.cache import add_never_cache_headers
from matplotlib.backends.backend_agg import FigureCanvasAgg
from .codigo.disipador_completo import RealizaSimulacion
from .forms import HeatSinkForm
from django.views.decorators.cache import never_cache

fig = "Sin figura"
form = HeatSinkForm()

def home(request):

    global fig, form, datos

    if request.method == 'POST':
        form = HeatSinkForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            queue = django_rq.get_queue('high')
            fig = queue.enqueue(RealizaSimulacion,datos)
            #fig = RealizaSimulacion(datos)
            return  render(request, "core/home.html",{'form': form,'datos': datos})
    else:
        form = HeatSinkForm()

    return render(request, "core/home.html",{'form': form})

@never_cache
def busqueda(request):

    global fig,form, datos

    status = "Sin status"

    if fig != "Sin figura":
        status = fig.get_status()

    return render(request, "core/home.html",{'form': form,'status': status,'datos': datos})

def plot(request):

    global fig
    # Como enviaremos la imagen en bytes la guardaremos en un buffer
    if fig != "Sin figura" and fig.get_status() == 'finished':

        buf = io.BytesIO()
        canvas = FigureCanvasAgg(fig.result)
        canvas.print_png(buf)

        # Creamos la respuesta enviando los bytes en tipo imagen png
        response = HttpResponse(buf.getvalue(), content_type='image/png')

        # Limpiamos la figura para liberar memoria
        plt.close(fig.result)
        buf.close()

        # Añadimos la cabecera de longitud de fichero para más estabilidad
        response['Content-Length'] = str(len(response.content))
        add_never_cache_headers(response)
        # Devolvemos la response
        return response

    else:

        return HttpResponse('')
