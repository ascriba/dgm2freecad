#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 22:22:04 2022

@author: ascriba
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import PySimpleGUI as sg
import numpy as np
import pickle


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
    
def convert_google(pkt):
        pkt = pkt.replace(" ", "").split(',')
        return [float(pkt[1]), float(pkt[0])]
        

df = []
kachel=''

size_txt = (22,1)
font = ("Arial, 11")

sg.theme("DarkTeal2")
sg.set_options(font=font)
layout = [
    [sg.Text("Choose XYZ-File:", size=size_txt), sg.Input(key='-FILE-', visible=True, enable_events=True), sg.FileBrowse(file_types=(("Text Files", "*.xyz"),), target='-FILE-')], 
    [sg.T("Show first read coordinates")],
    [sg.Multiline(size=(40,8), enable_events=True, autoscroll=False, key='-ML_XYZ-')],
    [sg.T("copy -> paste coordinates from Google Maps ")],
    [sg.Text('Bounding Box Point 1:', size=size_txt), sg.Input(key='-BB_Pkt1-')],
    [sg.Text('Bounding Box Point 2:', size=size_txt), sg.Input(key='-BB_Pkt2-')],
    [sg.Button('confirm BB')],
    [sg.T("Bounding Box in EPSG 25832 coordinates")],
    [sg.Multiline(size=(40,5), enable_events=True, autoscroll=False, key='-ML_BB-')],
    [sg.Text('tile name:', size=size_txt), sg.Text(kachel, key='-Kachel_Name-', size=(25,1))],
    [sg.Text('Name elevation layer:', size=size_txt), sg.Input(key='-f_hoehe-')],
    [sg.Text('Name reference layer:', size=size_txt), sg.Input(key='-f_ebene-')],
    [sg.Button('Export')],
    [sg.Text("Choose shp-file:", size=size_txt), sg.Input(key='-FILE_shp-', visible=True, enable_events=True), sg.FileBrowse(file_types=(("Text Files", "*.shp"),), target='-FILE_shp-')],
    [sg.Multiline(size=(40,6), enable_events=True, autoscroll=False, key='-ML_shp-')],
    [sg.Text('Input ID of property:', size=size_txt), sg.Input(key='-ID_Grund-')],
    [sg.Text('Name shp layer:', size=size_txt), sg.Input(key='-f_shp-')],
    [sg.Button('Export shp-file')],
    [sg.Text("Save project file:", size=size_txt), sg.Input(key='-project-', visible=True), sg.Button("Save")],
    [sg.Text("Open project file:", size=size_txt), sg.Input(key='-FILE_Pro-', visible=True, enable_events=True), sg.FileBrowse(file_types=(("Text Files", "*.dgm2"),), target='-FILE_Pro-')]
    ]


###Building Window
window = sg.Window('dgm2freecad', layout, size=(800,850),resizable=True)

while True:
    event, values = window.read()
    print('event:\n',event, '\nvalues:\n', values)
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    
    elif event == "confirm BB":
        pkt1 = convert_google(values["-BB_Pkt1-"])
        pkt2 = convert_google(values["-BB_Pkt2-"])
        df_bb = bb_box(pkt1, pkt2)
        window['-ML_BB-'].print(df_bb, text_color='red', background_color='yellow')
        
        str1=str(df_bb.mean()[0])[0:3]
        str2=str(df_bb.mean()[1])[0:4]
        kachel='dgm1_32_'+str1+'_'+str2+'_1_nw.xyz'
        window['-Kachel_Name-'].update(kachel)
        
        if values['-FILE-'] =='':
            sg.popup('choose XYZ-file forst!')
        else:
            df_grund = slice_dgm(df, df_bb)
        
    elif event == '-FILE-':
        df = read_dgm(values['-FILE-'])
        window['-ML_XYZ-'].print(str(df.head()), text_color='red', background_color='yellow')
        
    elif event == 'Export':
        f_hoehe = values['-f_hoehe-']
        f_ebene = values['-f_ebene-']
        export(df_grund, f_hoehe, f_ebene)
        sg.popup('points exported!')
        
    elif event == '-FILE_shp-':
        df_gebaeude = gpd.read_file(values['-FILE_shp-'])
        window['-ML_shp-'].print(df_gebaeude.lagebeztxt, text_color='red', background_color='yellow')

    elif event == 'Export shp-file':
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
        export_haus=(df_haus-df_grund.min())*1000
        
        if values['-f_shp-'] == '':
            sg.popup('name shp empty!')
        else:
            export_haus.to_csv(values['-f_shp-']+'.asc', index=False, header=False, sep=' ')
                     
    elif event == 'Save':
        if values['-project-'] =='':
            sg.popup('no file name specified!')
        else:        
            pickle.dump( values, open( values['-project-']+".dgm2", "wb" ) )
            sg.popup('Project saved under '+values['-project-']+".dgm2")
        
    elif event == '-FILE_Pro-':
        import_val = pickle.load( open( values['-FILE_Pro-'], "rb" ) )
        print(import_val)
        window['-ML_XYZ-'].update(import_val['-ML_XYZ-'])
        window['-FILE-'].update(import_val['-FILE-'])
        window['-BB_Pkt1-'].update(import_val['-BB_Pkt1-'])
        window['-BB_Pkt2-'].update(import_val['-BB_Pkt2-'])
        window['-ML_BB-'].update(import_val['-ML_BB-'])
        window['-f_hoehe-'].update(import_val['-f_hoehe-'])
        window['-f_ebene-'].update(import_val['-f_ebene-'])
        window['-FILE_shp-'].update(import_val['-FILE_shp-'])
        window['-ID_Grund-'].update(import_val['-ID_Grund-'])
        window['-ML_shp-'].update(import_val['-ML_shp-'])
        window.refresh()  
        
        df = read_dgm(import_val['-FILE-'])
        df_gebaeude = gpd.read_file(import_val['-FILE_shp-'])
        df_bb = bb_box(convert_google(import_val['-BB_Pkt1-']), convert_google(import_val['-BB_Pkt2-']))
        df_grund=slice_dgm(df, df_bb)
        
window.close()