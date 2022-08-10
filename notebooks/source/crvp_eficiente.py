import os
from time import time
import folium
import geopandas as gpd
import numpy as np
import pandas as pd
import polyline
import requests
from folium import Marker
from matplotlib import cm
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def get_data():
    # Data from S3
    url = 'https://test-manuelromero-0001.s3.amazonaws.com/UbicacionesVolumen.csv'
    # Creating the dataframe with the CEDIS
    df_ubicaciones = pd.read_csv(url)
    # CEDIS Azcapotzalco location
    df_ubicaciones=df_ubicaciones.append({"index":00000,"Latitud":19.4907364,"Longitud":-99.1620038,"Direccion":"CEDIS Azcapotzcalco","Vol":0},ignore_index=True)

    # Changing the m^3 to cm^3
    df_ubicaciones["Vol"]=round(df_ubicaciones["Vol"]*1000000)

    # Creating the Delivery Time col
    df_ubicaciones["TiempoEntrega"]=0

    # This is an estimate for the time it would take (in seconds), depending of the load
    df_ubicaciones.loc[df_ubicaciones['Vol']<=500000,"TiempoEntrega"]=5*60
    df_ubicaciones.loc[(df_ubicaciones['Vol']>500000)&(df_ubicaciones['Vol']<=1000000),"TiempoEntrega"]=10*60
    df_ubicaciones.loc[(df_ubicaciones['Vol']>1000000)&(df_ubicaciones['Vol']<=2000000),"TiempoEntrega"]=20*60
    df_ubicaciones.loc[(df_ubicaciones['Vol']>2000000)&(df_ubicaciones['Vol']<=3000000),"TiempoEntrega"]=25*60
    df_ubicaciones.loc[(df_ubicaciones['Vol']>3000000),"TiempoEntrega"]=30*60

    return df_ubicaciones


def get_cord():
    df_ubicaciones = get_data()
    coordenadas=""
    for i in range(len(df_ubicaciones)):
        fila=df_ubicaciones.iloc[i]
        long=fila["Longitud"]
        lat=fila["Latitud"]
        coordenadas=coordenadas+str(long)+","+str(lat)+";"
    coordenadas=coordenadas[:-1]
    return coordenadas

def get_time():
    coordenadas = get_cord()
    df_ubicaciones = get_data()
    df_tiempos = pd.DataFrame()
    for i in range(0,291,10):
        rangos= list(range(i,i+10))
        sources= ";".join(str(item) for item in rangos)
        url="http://router.project-osrm.org/table/v1/car/"+coordenadas+"?sources="+sources
        r = requests.get(url)
        res = r.json()
        df_tiempos=df_tiempos.append(res["durations"])
        print("Ubicaciones Completas:",i+10)
    url="http://router.project-osrm.org/table/v1/car/"+coordenadas+"?sources=300"
    r = requests.get(url)
    res = r.json()
    df_tiempos=df_tiempos.append(res["durations"])
    df_tiempos.columns=df_ubicaciones["index"]
    df_tiempos.index=df_ubicaciones["index"]    
    return df_tiempos

def main():
    data = get_time()
    print(data)

if __name__ == '__main__':
    inicio = time()
    main()
    fin = time() - inicio
    print(f"Tomo {fin} segundos")




