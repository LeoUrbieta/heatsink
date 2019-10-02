import io
import matplotlib.pyplot as plt
import django_rq

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.cache import add_never_cache_headers
from matplotlib.backends.backend_agg import FigureCanvasAgg
from .codigo.disipador_completo import RealizaSimulacion
from .forms import HeatSinkForm
from django.views.decorators.cache import never_cache
from rq.job import Job

fig = "Sin figura"
form = HeatSinkForm()
datos = "Sin datos"

@never_cache
def home(request):

    global form, datos

    if request.method == 'POST':
        fig = "Sin figura"
        form = HeatSinkForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            queue = django_rq.get_queue('high')
            fig = queue.enqueue(RealizaSimulacion,datos)
            request.session['figura'] = fig.id
            #fig = RealizaSimulacion(datos)
            return  render(request, "core/home.html",{'form': form,'datos': datos,'elemento': request.session.items()})
    else:
        form = HeatSinkForm()

    return render(request, "core/home.html",{'form': form})

@never_cache
def busqueda(request):

    global form, datos

    fig_id = request.session.get('figura')
    redis_conn = django_rq.get_connection('high')
    job = Job.fetch(fig_id,connection = redis_conn)

    status = job.get_status()

    return render(request, "core/home.html",{'form': form,'datos': datos,'elementos': request.session.get('figura'),'status': status})

@never_cache
def plot(request):

    fig_id = request.session.get('figura')
    redis_conn = django_rq.get_connection('high')
    job = Job.fetch(fig_id,connection = redis_conn)

    if job.get_status() == 'finished':
        # Como enviaremos la imagen en bytes la guardaremos en un buffer
        buf = io.BytesIO()
        canvas = FigureCanvasAgg(job.result)
        canvas.print_png(buf)

        # Creamos la respuesta enviando los bytes en tipo imagen png
        response = HttpResponse(buf.getvalue(), content_type='image/png')

        # Limpiamos la figura para liberar memoria
        plt.close(job.result)
        buf.close()

        # Añadimos la cabecera de longitud de fichero para más estabilidad
        response['Content-Length'] = str(len(response.content))
        add_never_cache_headers(response)
        # Devolvemos la response
        return response

    else:
        return HttpResponse('')
