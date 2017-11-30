from pylab import *
import netCDF4
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import sys

#recup fichier
inputfile=Dataset(sys.argv[1])
#print sys.argv[1]

#recup lat lon
latx=sys.argv[2]
lonx=sys.argv[3]
var=sys.argv[4]

#print variable
print ("Details des variables dispo : "+str(inputfile.variables)+"\n")


 
#Trouve le point de prelev dispo le plus proche
lat=np.ma.MaskedArray(inputfile.variables['latitude'])
lon=np.ma.MaskedArray(inputfile.variables['longitude'])


noval=True
while noval:
 #Recup l'id de ce point
 id_latx=(np.abs(lat-float(latx))).argmin() #voir avec sort
 id_lonx=(np.abs(lon-float(lonx))).argmin()

 #Print des coords les plus proches retenues
 print ("Lat cherchee : "+str(latx)+" - Lat la plus proche disponible : "+str(lat[id_latx])+"\nLon cherchee : "+str(lonx)+" - Lon la plus proche disponible : "+str(lon[id_lonx]))

 #Recup toutes les donnees dispo #Temporalitee choisie ici
 phy=(inputfile.variables[var][:,0,id_latx,id_lonx])

 #print phy

 #Check qu'il y au moins une donnee int de dispo
 i=0
 while True and i<len(phy):
     if isinstance(phy[i],(np.float32)):
         break
     i=i+1

 #Si vals dispo :
 if i<len(phy):
     print ("Valeurs disponibles aux coordonnees : "+str(lat[id_latx])+" "+str(lon[id_lonx])+" : "+str(phy))
     plot(phy)
     plt.savefig('plot.png')
     noval=False
 else:
     print ("Aucune donnee dispo aux coordonnees : "+str(lat[id_latx])+" "+str(lon[id_lonx])+".\nRecherche du deuxieme set de coord le plus proche")
     lon2=np.delete(lon,id_lonx)
     lat2=np.delete(lat,id_latx) 
     
     id_latx2=(np.abs(lat2-float(latx))).argmin()
     id_lonx2=(np.abs(lon2-float(lonx))).argmin()

     print(str(abs(lon[id_lonx]-lon2[id_lonx2]))+","+str(abs(lat[id_latx]-lat2[id_latx2])))


     if (abs(lon[id_lonx]-lon2[id_lonx2]) < abs(lat[id_latx]-lat2[id_latx2])): #A faire de maniere absolue
         print "1"
         lon=np.delete(lon,id_lonx)
     else:
         lat=np.delete(lat,id_latx)
         print "2"



    
