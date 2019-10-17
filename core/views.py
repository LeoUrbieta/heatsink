import io
import matplotlib.pyplot as plt
import django_rq

from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg
from .codigo.disipador_completo import RealizaSimulacion
from .forms import HeatSinkForm
from rq.job import Job

def home(request):

    if request.method == 'POST':
        form = HeatSinkForm(request.POST)
        if form.is_valid():
            mensaje_status = "Después de unos segundos, da click en el botón de abajo para obtener tu simulación"
            datos = form.cleaned_data
            queue = django_rq.get_queue('high')
            fig = queue.enqueue(RealizaSimulacion,datos)
            request.session['figura'] = fig.id
            #fig = RealizaSimulacion(datos)
            return render(request, "core/home.html",{'form': form,'mensaje': mensaje_status})
    else:
        form = HeatSinkForm()

    return render(request, "core/home.html",{'form': form})


def busqueda(request):

    form = HeatSinkForm()
    fig_id = request.session.get('figura')
    redis_conn = django_rq.get_connection('high')
    job = Job.fetch(fig_id,connection = redis_conn)

    if job.get_status() == 'finished':
        mensaje_status = "Tu simulación está lista"
    else:
        mensaje_status = "Todavia no he terminado :(. Vuelve a intentar en 10 segundos. Gracias."

    return render(request, "core/home.html",{'form': form,'mensaje': mensaje_status})

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
        # Devolvemos la response
        return response

    else:
        return HttpResponse('')
