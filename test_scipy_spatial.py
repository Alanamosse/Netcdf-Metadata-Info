from pylab import *
import netCDF4
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from scipy import spatial

inputfile=Dataset(sys.argv[1])
latx=float(sys.argv[2])
lonx=float(sys.argv[3])
lat=np.ma.MaskedArray(inputfile.variables['latitude'])
lon=np.ma.MaskedArray(inputfile.variables['longitude'])

#print lat.size; print lon.size

list=[]
for i in inputfile.variables['latitude']:
 for j in inputfile.variables['longitude']:
  list.append(i);list.append(j)


all_coord=np.reshape(list,(lat.size*lon.size,2))
noval=True

while noval:
 print all_coord.shape
 tree=spatial.KDTree(all_coord)

 closest_coord=(tree.query([(latx,lonx)]))
 cc=closest_coord[1]

 print all_coord[cc]
 
 a=float(all_coord[closest_coord[1]][0][0])
 b=float(all_coord[closest_coord[1]][0][1])
 
 id_latx=lat.tolist().index(a)
 id_lonx=lon.tolist().index(b)
 #print id_latx;print lat[id_latx]

 phy=inputfile.variables['phy'][:,0,id_latx,id_lonx]

 i=0
 while True and i<len(phy):
  if isinstance(phy[i],(np.float32)):
   break
  i=i+1
 
 if i<len(phy):
     print ("Valeurs disponibles aux coordonnees : "+str(lat[id_latx])+" "+str(lon[id_lonx]))
     noval=False
 else:
     #print ("Aucune donnee dispo aux coordonnees : "+str(lat[id_latx])+" "+str(lon[id_lonx])+".\nRecherche du deuxieme set de coord le plus proche")
     all_coord=np.delete(all_coord,cc,0)



