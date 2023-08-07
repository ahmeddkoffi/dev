import pandas as pd
import statistics




#On calcule les ecarts types mobiles sur les 6 derniers jours à partir d'un jour quelconque, cette fonction prend en input un dataframe
# contenant absolument les variables 'Date' et 'Prix' ; La fonction renvoie la même dataframe avec en plus la colonne 'Ecartype'
# correspondant à l'écart type mobile
def calculate_std(data):
    # Tri des données par date
    data = data.sort_values('Date')

    # Création d'une nouvelle colonne pour la disponibilité en herbe
    data['std'] = 0.0

    # Boucle pour calculer la disponibilité en herbe à partir des valeurs des 30 jours précédents
    for i, row in data.iterrows():
        current_date = row['Date']
        previous_dates = pd.date_range(end=current_date, periods=6)
        previous_data = data[data['Date'].isin(previous_dates)]
        if len(previous_data)>2:
            std_ = statistics.stdev(previous_data['Prix'])
            # Mise à jour de la valeur de disponibilité en herbe dans la dataframe
            data.at[i, 'std'] = std_
    #data = data.drop('Date',axis=1)
    return data


# On a un dataframe avec les variables 'Date','Prix' et 'Ecartype'; on voudrait transformer ce dataframe en un dataframe dont la ième 
#ligne est le (Prix aujourd'hui, Prix Hier, Prix avant hier, prix 3 jours avant, Ecart type aujourd'hui, ...hier,... avant hier, ... 3 jours avant)
def new_data(data):
    data['Prix aujourdhui'] = 0.0
    data['Prix jour-1'] = 0.0
    data['Prix jour-2'] = 0.0
    data['Prix jour-3'] = 0.0               
    data['std aujourdhui'] = 0
    data['std jour-1'] = 0
    data['std jour-2'] = 0
    data['std jour-3'] = 0

    for i, row in data.iterrows():
        if i > 3:
            data.at[i,'Prix aujourdhui'] = data.at[i,'Prix']
            data.at[i,'Prix jour-1'] = data.at[i-1,'Prix']
            data.at[i,'Prix jour-2'] = data.at[i-2,'Prix']
            data.at[i,'Prix jour-3'] = data.at[i-3,'Prix']
            data.at[i,'std aujourdhui'] = data.at[i,'std']
            data.at[i,'std jour-1'] = data.at[i-1,'std']
            data.at[i,'std jour-2'] = data.at[i-2,'std']
            data.at[i,'std jour-3'] = data.at[i-3,'std']
    data = data.drop(['Prix','std'],axis=1)
    return data
