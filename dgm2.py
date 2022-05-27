#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 15:06:04 2022

@author: ascriba
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import PySimpleGUI as sg
import sys
import numpy as np

#'dgm1_32_451_5668_1_nw.xyz'

def read_dgm(filename):
    #Kachel aus dgm einlesen
    df = pd.read_csv(filename, delim_whitespace=True, header=None)
    return df

def bb_box(pkt1, pkt2):
    #BOUNDING BOX Koordinaten aus Google Maps
    points1 = [Point(pkt1[0], pkt1[1]), Point(pkt2[0], pkt2[1])]
    gdf1 = gpd.GeoDataFrame([1, 2], geometry=points1, crs=4326)
    gdf=gdf1.to_crs('epsg:25832')
    df_bb = pd.DataFrame({'lon':gdf['geometry'].x, 'lat':gdf['geometry'].y})
    return df_bb

def slice_dgm(df, df_bb):
    #Gebiet eingrenzen mit Bounding Box
    df_grund = df[(df[0]>df_bb.lon.values.min()) & (df[0]<df_bb.lon.values.max())]
    df_grund = df_grund[(df_grund[1]>df_bb.lat.values.min()) & (df_grund[1]<df_bb.lat.values.max())]
    return df_grund

def export(df_grund, f_hoehe, f_ebene,  z_offset=1000):
    #export für Points WB
    export = (df_grund-df_grund.min())*1000
    export[2] = export[2]+z_offset

    minx = export[0].min()
    maxx =export[0].max()
    miny = export[1].min()
    maxy =export[1].max()
    
    df_ebene = pd.DataFrame({'x':[minx, maxx, minx, maxx], 'y':[miny, miny, maxy, maxy], 'z':[0,0,0,0]})
    
    export.to_csv(f_hoehe+'.asc', index=False, header=False, sep=' ')
    df_ebene.to_csv(f_ebene+'.asc', index=False, header=False, sep=' ')

df = []
kachel=''

sg.theme("DarkTeal2")
layout = [
     
    [sg.Text("XYZ-File wählen:  "), sg.Input(key='-FILE-', visible=True, enable_events=True), sg.FileBrowse(file_types=(("Text Files", "*.xyz"),))],
    [sg.T("Anzeigen der ersten eingelesenen Koordinaten")],
    [sg.Multiline(size=(40,6), enable_events=True, autoscroll=True, key='-ML_XYZ-')],
    [sg.T("copy -> paste Koordinaten von Google Maps ")],
    [sg.Text('Bounding Box Pkt 1'), sg.Input(key='-BB_Pkt1-')],
    [sg.Text('Bounding Box Pkt 2'), sg.Input(key='-BB_Pkt2-')],
    [sg.Button('BB bestätigen')],
    [sg.Multiline(size=(40,3), enable_events=True, autoscroll=True, key='-ML_BB-')],
    [sg.Text('Name der Kachel:  '), sg.Text(kachel, key='-Kachel_Name-', size=(25,1))],
    [sg.Text('Name Höhenlayer   '), sg.Input(key='-f_hoehe-')],
    [sg.Text('Name Groundlayer  '), sg.Input(key='-f_ebene-')],
    [sg.Button('Export')],
    [sg.T("shp - File laden")], 
    [sg.Text("shp-File wählen:  "), sg.Input(key='-FILE_shp-', visible=True, enable_events=True), sg.FileBrowse(file_types=(("Text Files", "*.shp"),))],
    [sg.Multiline(size=(40,6), enable_events=True, autoscroll=True, key='-ML_shp-')],
    [sg.Text('ID Grundstück eingeben'), sg.Input(key='-ID_Grund-')],
    [sg.Button('Export Gebäude')]
    ]

#key='-FILE-', visible=True, enable_events=True

###Building Window
window = sg.Window('dgm2freecad', layout, size=(600,600))

while True:
    event, values = window.read()
    print('event:\n',event, '\nvalues:\n', values)
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    
    elif event == "BB bestätigen":
        bb1 = values["-BB_Pkt1-"]
        bb1 = bb1.replace(" ", "").split(',')
        bb2= values["-BB_Pkt2-"]
        bb2 = bb2.replace(" ", "").split(',')
        print(bb1[0], bb2[1])
        pkt1 = [float(bb1[1]), float(bb1[0])]
        pkt2 = [float(bb2[1]), float(bb2[0])]
        df_bb = bb_box(pkt1, pkt2)
        window['-ML_BB-'].print(df_bb, text_color='red', background_color='yellow')
        
        str1=str(df_bb.mean()[0])[0:3]
        str2=str(df_bb.mean()[1])[0:4]
        kachel='dgm1_32_'+str1+'_'+str2+'_1_nw.xyz'
        window['-Kachel_Name-'].update(kachel)
        
        if values['-FILE-'] =='':
            sg.popup('Zuerst XYZ-File auswählen!')
        else:
            df_grund = slice_dgm(df, df_bb)
        
    elif event == '-FILE-':
        print('OK!\n', values['-FILE-'])
        df = read_dgm(values['-FILE-'])
        window['-ML_XYZ-'].print(str(df.head()), text_color='red', background_color='yellow')
        
    elif event == 'Export':
        f_hoehe = values['-f_hoehe-']
        f_ebene = values['-f_ebene-']
        export(df_grund, f_hoehe, f_ebene)
        sg.popup('Exportiert!')
        
    elif event == '-FILE_shp-':
        df_gebaeude = gpd.read_file(values['-FILE_shp-'])
        window['-ML_shp-'].print(df_gebaeude.lagebeztxt, text_color='red', background_color='yellow')

    elif event == 'Export Gebäude':
        gebäude_id = int(values['-ID_Grund-'])
        g = df_gebaeude.geometry[gebäude_id]
        x,y = g.exterior.coords.xy
        all_coords = np.dstack((x,y)  ).tolist()
        
        x_haus=[]
        y_haus=[]
        for i in range(len(all_coords[0])-1):
            x_haus.append(all_coords[0][i][0])
            y_haus.append(all_coords[0][i][1])
        
        df_haus = pd.DataFrame(list(zip(x_haus, y_haus)) )
        df_haus[2]=df_grund[2].min()
        name_exprt=df_gebaeude.lagebeztxt[gebäude_id]
        export_haus=(df_haus-df_grund.min())*1000
        export_haus.to_csv(name_exprt+'.asc', index=False, header=False, sep=' ')
        #print(x_haus, y_haus)              

        
        
window.close()