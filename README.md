# dgm2freecad
Create a pointcloud from digital elevation model for use in freecad BIM Workbench

So far tested with geo-data from North Rhine-Westphalia, Germany

Geo-data can be downloade here:
https://www.opengeodata.nrw.de/produkte/geobasis/hm/dgm1_xyz/dgm1_xyz/

This tool uses geo-data in the file format .xyz.
Coordinate systems of the xyz - file is EPSG 25832 location, hights in EPSG 7837.
![Gui_dgm2freecad](https://user-images.githubusercontent.com/18013240/170783270-cd5eca67-8b5c-4f21-8909-0809d6774b33.png)



How to use:
1. Download xyz - file from link above
   If filename is unknown you can copy 2 points from google maps and paste it as a bounding box to the input fields 'Bounding Box Pkt 1'
   and 'Bounding Box Pkt2'. After use of button 'BB bestätigen' the name of the xyz - file is shown beside the field 'Name der Kachel'.
2. Browse to the xyz - file. After file is read, the first 5 rows of the file will be shown in field beneath.
3. If not yet done under Point 1, insert the to Points of the bounding box of interest.
4. Use 'BB bestätigen' button and the transformed coordinates from google maps will be shown in the field beneath.
5. Insert name for the Layer of the surface and the reference height and click export. Two files will be exported in the .asc file format.
6. The shp - file tool can be used to read the coordinates from a building. The shp - file can be downloaded here:
   https://www.tim-online.nrw.de/tim-online2/ the layer name in 'tim-online' is ALKIS. Browse to the shp - file downloaded.
7. After shp - file is read, the  file will be shown in field beneath.
8. Input the Number of the property from firste column to the field beside the 'ID Grundstück eingeben'.
9. After using of the button 'Export Gebäude' the coordinates of the building will be exported to a file in asc - file format.
   The name of the export file is the name of the property chosen before.


Go on with freecad:
1. Open 'Points' Workbench (WB) in freecad and import the surface asc - file 
![freecad1](https://user-images.githubusercontent.com/18013240/170785617-fb1c9f5f-3245-4a42-b389-5ad099caf9c5.png)

3. Open 'Reverse Engineering' WB and use B-Spline - tool under Approximation
![freecad2](https://user-images.githubusercontent.com/18013240/170785865-e272f6aa-8bf9-40a8-a0ce-92fb4747d1fa.png)

5. Open 'Points' Workbench (WB) in freecad and import the reference height asc - file
![freecad3](https://user-images.githubusercontent.com/18013240/170786171-df005d82-6cc9-458c-8b9d-baa030f746af.png)

6. Connect points from reference hight with points from B-Spline with wire in 'Arch' WB
![freecad4](https://user-images.githubusercontent.com/18013240/170786438-295f6f5d-42de-4f6a-b221-998bc2535846.png)

7. Open 'Part' WB and build faces: Part-WB -> shape builder -> faces from edges
![freecad5](https://user-images.githubusercontent.com/18013240/170786896-3a2c89d4-714d-4733-b4d8-96d455eb96fa.png)

8. Create shell from faces: Part-WB -> shape builder -> shell from faces (include B-Spline)
9. Create solid from shell: Part-WB -> shape builder -> solid from shell 
![freecad6](https://user-images.githubusercontent.com/18013240/170787638-7da91d1a-633c-4f14-b224-de92f9fd5ed5.png)
10. Open 'Points' Workbench and import asc - file with the coordinates of the property. 
    Connect point in  'Arch' WB with wires, build faces in 'Part' WB and extrude
![freecad7](https://user-images.githubusercontent.com/18013240/170788869-c39df375-b4de-45e8-95c0-f5b0a928366f.png)


Dependencies:
pandas, geopandas, shapely, PySimpleGUI, numpy


