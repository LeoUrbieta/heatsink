import io
import matplotlib.pyplot as plt
import django_rq

from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg
from .codigo.disipador_completo import RealizaSimulacion
#from .codigo.validaciones.validacion_fuente_calor import ValidaFuenteCalorEsteDentroDisipador
from .forms import HeatSinkForm
from rq.job import Job

def home(request):

    if request.method == 'POST':
        form = HeatSinkForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            #fuente_esta_adentro = ValidaFuenteCalorEsteDentroDisipador(datos)
            mensaje_status = "Da click en el botón de abajo para ver el estatus de tu simulación"
            queue = django_rq.get_queue('high')
            fig = queue.enqueue(RealizaSimulacion,datos)
            if fig != None:
                request.session['figura'] = fig.id
                #fig = RealizaSimulacion(datos)
                return render(request, "core/home.html",{'form': form,'mensaje': mensaje_status})
            else:
                #Este else es para un doble chequeo dentro del código de ejecución de RealizaSimulacion, solo por si acaso
                mensaje_status = "Hubo un gran problema. Por favor, envíame un correo a leourbieta@pm.me"
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
        if job.result[1] == [0]:
            mensaje_status = "Tu simulación está lista"
        elif len(job.result[1]) == 1:
            fuente_fuera_disipador = job.result[1]
            mensaje_status = "La fuente " + str(fuente_fuera_disipador[0]) + " está fuera del disipador"
        else:
            fuentes_traslapadas = job.result[1]
            mensaje_status = "La fuente " + str(fuentes_traslapadas[0]) + " y " + str(fuentes_traslapadas[1]) + " se traslapan."
    else:
        mensaje_status = "Todavia no he terminado :(. Vuelve a dar click en 10 segundos. Gracias."
        info = "Sin informacion"

    return render(request, "core/home.html",{'form': form,'mensaje': mensaje_status})

def plot(request):

    fig_id = request.session.get('figura')
    redis_conn = django_rq.get_connection('high')
    job = Job.fetch(fig_id,connection = redis_conn)

    if job.get_status() == 'finished':
        # Como enviaremos la imagen en bytes la guardaremos en un buffer
        buf = io.BytesIO()
        canvas = FigureCanvasAgg(job.result[0])
        canvas.print_png(buf)

        # Creamos la respuesta enviando los bytes en tipo imagen png
        response = HttpResponse(buf.getvalue(), content_type='image/png')

        # Limpiamos la figura para liberar memoria
        plt.close(job.result[0])
        buf.close()

        # Añadimos la cabecera de longitud de fichero para más estabilidad
        response['Content-Length'] = str(len(response.content))
        # Devolvemos la response
        return response

    else:
        return HttpResponse('')

def drag(request):
    return render(request,"core/drag.html")
