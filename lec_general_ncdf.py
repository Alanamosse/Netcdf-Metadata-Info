#a="b=f.variables['latitude'][:]"
#exec(a)
#b
#ncdump -h dataset-ibi-reanalysis-bio-005-003-monthly-regulargrid_1510914389133.nc | sed -n  '/dimensions:/,/variables:/p

from pylab import *
import netCDF4
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from scipy import spatial
from math import radians, cos, sin, asin, sqrt
 
def checklist(dim_list, dim_name, filtre, threshold):
    if not dim_list:
        error="Error "+str(dim_name)+" has no value "+str(filtre)+" "+str(threshold)
        sys.exit(error)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def is_strict_inf(filename, dim_name, threshold):
    list_dim=[]
    for i in range(0,filename.variables[dim_name].size):
        if filename.variables[dim_name][i] < threshold:
            list_dim.append(i)
    checklist(list_dim,dim_name,"<",threshold)
    return list_dim

def is_equal_inf(filename, dim_name, threshold):
    list_dim=[]
    for i in range(0,filename.variables[dim_name].size):
        if filename.variables[dim_name][i] <= threshold:
            list_dim.append(i)
    checklist(list_dim,dim_name,"<=",threshold)
    return list_dim

def is_equal_sup(filename, dim_name, threshold):
    list_dim=[]
    for i in range(0,filename.variables[dim_name].size):
        if filename.variables[dim_name][i] >= threshold:
            list_dim.append(i)
    checklist(list_dim,dim_name,">=",threshold)
    return list_dim

def is_strict_sup(filename, dim_name, threshold):
    list_dim=[]
    for i in range(0,filename.variables[dim_name].size):
        if filename.variables[dim_name][i] > threshold:
            list_dim.append(i)
    checklist(list_dim,dim_name,">",threshold)
    return list_dim

def find_nearest(array,value):
    index = (np.abs(array-value)).argmin()
    return index

def is_equal(filename, dim_name, value):
    try:
        index=filename.variables[dim_name][:].tolist().index(value)
    except:
        index=find_nearest(filename.variables[dim_name][:],value)
    return index


arg_n=len(sys.argv)-1

#A mettre en option ici
point_unique=True
zone_geo=False

#recup fichier nc
inputfile=Dataset(sys.argv[1])

#recup le fichier dim.tab
var_file=open(sys.argv[2],"r")
lines=var_file.readlines()
dim_names=[]
for line in lines:
    words=line.split()
    if (words[0]==sys.argv[3]):
        #print line
        varndim=words[1] #TODO ici faire une boucle for i<varndim{recup dim_i}
        for dim in xrange(2,len(words),2):
            #print words[dim]
            dim_names.append(words[dim])
        print ("Variable choisie : "+sys.argv[3]+". Nombre de dimensions : "+str(varndim)+". Dimensions : "+str(dim_names))
        



#Recup Lat et Lon
lat=np.ma.MaskedArray(inputfile.variables['latitude']) #TODO#a faire en try ou faire un if nom=latitude or nom=lat.
lon=np.ma.MaskedArray(inputfile.variables['longitude'])

if point_unique:
    var=sys.argv[3]
    #ndim=(arg_n-3)/3 
    #print ("nombre de dim :"+str(ndim))
    my_dic={} #lol #d["string{0}".format(x)]
    execu="vec=inputfile.variables['"+str(sys.argv[3])+"']["
    for i in xrange(4,arg_n,3):
        #print("Nom de la dim : "+sys.argv[i]+" action sur la dim : "+sys.argv[i+1]+" .Valeur de la dim choisie : "+sys.argv[i+2])
        my_dic["string{0}".format(i)]="list_index_dim"
        my_dic_index="list_index_dim"+str(i/3)
        if i!=4:
            execu=execu+","
        if (sys.argv[i+1]=="<"):
            my_dic[my_dic_index]=is_strict_inf(inputfile, sys.argv[i], int(sys.argv[i+2]))
            execu=execu+"my_dic[\""+str(my_dic_index)+"\"]"
            #print inputfile.variables[sys.argv[i]][my_dic[my_dic_index]]
            #print my_dic["list_index_dim1"]
        if (sys.argv[i+1]=="<="):
            my_dic[my_dic_index]=is_equal_inf(inputfile, sys.argv[i], float(sys.argv[i+2]))
            execu=execu+"my_dic[\""+str(my_dic_index)+"\"]"
        if (sys.argv[i+1]==">"):
            my_dic[my_dic_index]=is_strict_sup(inputfile, sys.argv[i], float(sys.argv[i+2]))
            execu=execu+"my_dic[\""+str(my_dic_index)+"\"]"
        if (sys.argv[i+1]==">="):
            my_dic[my_dic_index]=is_equal_sup(inputfile, sys.argv[i], float(sys.argv[i+2]))
            execu=execu+"my_dic[\""+str(my_dic_index)+"\"]"
        if (sys.argv[i+1]=="="):
            my_dic[my_dic_index]=is_equal(inputfile, sys.argv[i], float(sys.argv[i+2]))
            execu=execu+"my_dic[\""+str(my_dic_index)+"\"]"
        if (sys.argv[i+1]==":"):
            execu=execu+":"
    execu=execu+"]"
    #print execu
    exec(execu)
    print vec




    #Recup Lat et Lon
    lat=np.ma.MaskedArray(inputfile.variables['latitude'])
    lon=np.ma.MaskedArray(inputfile.variables['longitude'])
    all_coord=np.reshape(list,(lat.size*lon.size,2))


    noval=True
    
    while noval:

     tree=spatial.KDTree(all_coord)
     closest_coord=(tree.query([(latx,lonx)]))
     cc=closest_coord[1]
    
     a=float(all_coord[closest_coord[1]][0][0])
     b=float(all_coord[closest_coord[1]][0][1])
     id_latx=lat.tolist().index(a)
     id_lonx=lon.tolist().index(b)

     #Print des coords les plus proches retenues
     #print ("Lat cherchee : "+str(latx)+" - Lat la plus proche disponible : "+str(lat[id_latx])+"\nLon cherchee : "+str(lonx)+" - Lon la plus proche disponible : "+str(lon[id_lonx])+"\n")

     #Recup toutes les donnees dispo #Temporalitee choisie ici
     phy=(inputfile.variables[var][:,0,id_latx,id_lonx])


     #Check qu'il y au moins une donnee int de dispo
     i=0
     while True and i<len(phy):
         if isinstance(phy[i],(np.float32)):
             break
         i=i+1

     #Si vals dispo :
     if i<len(phy):
         #print ("Valeurs disponibles aux coordonnees : "+str(lat[id_latx])+" "+str(lon[id_lonx])+" : "+str(phy))
         plot(phy)
         plt.savefig('plot.png')
         noval=False
         print("impression de "+str(latx)+"_"+str(lonx))
         
         fout="%s_%s:%s"%(var,latx,lonx)
         fo=open(fout,'w')
         fo.write(str(latx)+"_"+str(lonx)+"\t"+str(lat[id_latx])+"_"+str(lon[id_lonx])+"\t"+str(haversine(lonx,latx,lon[id_lonx],lat[id_latx]))+"\t")
         phy.tofile(fo,sep="\t",format="%s")
         fo.close()


     else:
         #print ("Aucune donnee dispo aux coordonnees : "+str(lat[id_latx])+" "+str(lon[id_lonx])+".\nRecherche du deuxieme set de coord le plus proche")
         all_coord=np.delete(all_coord,cc,0)


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





   
 
