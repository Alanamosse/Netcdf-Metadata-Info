from pylab import *
import netCDF4
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from scipy import spatial

#TODO
#A mettre en option ici
point_unique=True
zone_geo=False

#recup fichier
inputfile=Dataset(sys.argv[1])
#print sys.argv[1]

#print variable
print ("Details des variables dispo : "+str(inputfile.variables)+"\n")

#Recup Lat et Lon
lat=np.ma.MaskedArray(inputfile.variables['latitude'])
lon=np.ma.MaskedArray(inputfile.variables['longitude'])

if point_unique:
    #recup lat lon
    latx=sys.argv[2]
    lonx=sys.argv[3]
    var=sys.argv[4]

    noval=True
    while noval:
     #Recup id de point le + proche
     id_latx=(np.abs(lat-float(latx))).argmin() 
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


         if (abs(lon[id_lonx]-lon2[id_lonx2]) < abs(lat[id_latx]-lat2[id_latx2])):
             print "1"
             lon=np.delete(lon,id_lonx)
         else:
             lat=np.delete(lat,id_latx)
             print "2"

if zone_geo:
    #Coord
    lat_min=float(sys.argv[2])
    lat_max=float(sys.argv[3])
    lon_min=float(sys.argv[4])
    lon_max=float(sys.argv[5])
    #Var eg phy, chl ...
    var=sys.argv[6]
    
    lat2=[]
    lon2=[]
    
    #Recup les ids des coords dispo dans l'interval fourni
    for i in lat:
        if (i>=lat_min and i<=lat_max):
            lat2.append(lat.tolist().index(i))
            
    for i in lon:
        if (i>=lon_min and i<=lon_max):
            lon2.append(lon.tolist().index(i))
    
    phy=np.array(inputfile.variables[var][:,0,lat2,lon2])
    #print phy.shape
    phy=np.swapaxes(phy,0,2)
    

#Prints pour verif integritee data
    #print phy.shape
    print lat[lat2]
    print lon[lon2]
    #print inputfile.variables[var]
    #print inputfile.variables[var][:,0,lat2[2],lon2[0]] 
    #print phy 

    #Impression dans fichiers
    fout='saved_array'
    fo=open(fout,'w')
    phy.tofile(fo,sep="\t",format="%s")   
    fo.close()


    fout='coord_header'
    os.remove(fout)
    fo=open(fout,'a')
    for i in range(0,len(lon2)):
        for j in range(0,len(lat2)):
            fo.write (str(lat[lat2[j]])+":"+str(lon[lon2[i]])+"\t")
    fo.write("\n")
    fo.close()



#Manips a faire pour formater en tabular :

#cat saved_array |  xargs -n145 > saved_array2    ##xargs -n[taille variable temps)

#awk '               
#{ 
#    for (i=1; i<=NF; i++)  {
#        a[NR,i] = $i
#    }
#}
#NF>p { p = NF }
#END {    
#    for(j=1; j<=p; j++) {
#        str=a[1,j]
#        for(i=2; i<=NR; i++){
#            str=str" "a[i,j];
#        }
#        print str
#    }
#}' saved_array2 >saved_array3

#cat coord_header saved_array3 > super.tab
#cat super.tab | tr ' ' '\t' > super.tab2 
# mv super.tab2 super.tab  





   
 
