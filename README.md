# dgm2freecad
Create a pointcloud from digital elevation model for use in frecad  BIM Workbench

So far tested with geo-data from North Rhine-Westphalia, Germany

Geo-data can be downloade here:
https://www.opengeodata.nrw.de/produkte/geobasis/hm/dgm1_xyz/dgm1_xyz/

This tool uses geo-data in the file format .xyz.
Coordinate systems of the xyz - file is EPSG 25832 location, hights in EPSG 7837.

How to use:
1. Download xyz - file from link above
   If filename is unknown you can copy 2 points from google maps and paste it as a bounding box to the input fields 'Bounding Box Pkt 1'
   and 'Bounding Box Pkt2'. After use of button 'BB bestätigen' the name of the xyz - file is shown beside the field 'Name der Kachel'.
2. Browse to the xyz - file. After file is read, the first 5 rows of the file will be shown in field benaeth.
3. If not yet done under Point 1, insert the to Points of the bounding box of interest.
4. Use 'BB bestätigen' button and the transformed coordinates from google maps will be shown in the field benaeth.
5. Insert name for the Layer of the surface and the referenc hight and click export. Two files will be exportet in the .asc file format.
6. The shp - file tool can be used to read the coordinates from a building. The shp - file can be downloaded here:
   https://www.tim-online.nrw.de/tim-online2/ the layer name in 'tim-online' is ALKIS. Browse to the shp - file downloaded.
7. After shp - file is read, the  file will be shown in field benaeth.
8. Input the Number of the property from firste column to the field beside the 'ID Grundstück eingeben'.
9. After using of the button 'Export Gebäude' the coordinates of the building will be exportet to a file in asc - file format.
   The name of the exportet file is the name of the property choosen before.
