from django.shortcuts import render
from django.http import JsonResponse 
from myapp.models import Events 
import pandas as pd
from datatransform.transformfonct import calculate_std, new_data
import pickle
import plotly.express as px
from myapp.forms import DateForm
from django.conf import settings

MODEL_FILE_PATH = settings.MODEL_FILE_PATH

# Create your views here.
def index(request): 
    all_events = Events.objects.all()
    context = {
    "events":all_events,
        
}
    return render(request,'index.html',context)




# views.py
from .forms import DateForm
import pandas as pd
import plotly.express as px
from django.shortcuts import render
from .models import Events
import pickle

def prediction(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    events = Events.objects.all()
    if start:
        events = events.filter(start_date__gte=start)
    if end:
        events = events.filter(start_date__lte=end)

    data = []
    for event in events:
        # Convertir la date de début en chaîne de caractères
        date_str = event.start_date.strftime("%Y-%m-%d")
        price = event.price
        data.append([date_str, price])

    df = pd.DataFrame(data, columns=['Date', 'Prix'])
    df = new_data(calculate_std(df))
    model_file_path = MODEL_FILE_PATH
    with open(model_file_path, 'rb') as file:
        loaded_model = pickle.load(file)
    df.drop('Date',axis=1, inplace=True)
    y_pred = loaded_model.predict(df.iloc[[-1]])
        
    fig = px.line(
        x=[c.start_date for c in events],
        y=[c.price for c in events],
        title="realized price plot",
        labels={'x': 'Date', 'y': 'observed price'}
    )

    fig.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
        }
    )
    chart = fig.to_html()
    context = {'chart': chart, 'form': DateForm(),'y_pred':y_pred}

    return render(request, 'chart.html', context)




def all_events(request):
    all_events = Events.objects.all()
    out = []
    for event in all_events:
        out.append({
            'id': event.id,
            'start': event.start_date.strftime("%Y-%m-%d"),
            'title': 'price observed today : '+ "\n" + str(event.price),  # Ajout du texte "prix observé ce jour"
        })
    return JsonResponse(out, safe=False)




def add_event(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        price = request.GET.get('title')  # Récupérer le prix saisi depuis la requête GET

        # Créer un nouvel événement dans la base de données avec le prix et la date
        
        event = Events.objects.create(start_date=start_date, price=price)
        event.save()
        # Pour l'instant, nous allons simplement renvoyer une réponse JSON avec le prix observé.
        observed_price = "price observed today : " + "\n" + str(price)
        response_data = {'status': 'success', 'observed_price': observed_price}
        return JsonResponse(response_data)
    else:
        # La vue ne gère que les requêtes GET, si la méthode est différente, renvoyer une réponse d'erreur.
        response_data = {'status': 'error', 'message': 'Méthode non autorisée'}
        return JsonResponse(response_data, status=405)



def update(request):
    start = request.GET.get("start_date", None)
    price = request.GET.get("price", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start_date = start
    event.price = price
    event.save()
    data = {}
    return JsonResponse(data)

def remove_event(request):
    if request.method == 'GET':
        event_id = request.GET.get('id')

        try:
            event = Events.objects.get(id=event_id)
            event.delete()

            response_data = {'status': 'success', 'message': 'Event removed'}
            return JsonResponse(response_data)
        except Events.DoesNotExist:
            response_data = {'status': 'error', 'message': 'Event not found'}
            return JsonResponse(response_data, status=404)
    else:
        response_data = {'status': 'error', 'message': 'Method not allowed'}
        return JsonResponse(response_data, status=405)
