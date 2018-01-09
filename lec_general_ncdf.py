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


#recup fichier nc
inputfile=Dataset(sys.argv[1])

Coord_bool=False

#Check if coord is passed as parameter
arg_n=len(sys.argv)-1
if(((arg_n-3)%3)!=0):
    #print "il y a des coord a prendre en compte. Reduction de arg_n de 4."
    Coord_bool=True #Utile pour recup les coord les plus proche plus loins
    arg_n=arg_n-4
    name_dim_lat=str(sys.argv[-4])
    name_dim_lon=str(sys.argv[-2])
    value_dim_lat=float(sys.argv[-3])
    value_dim_lon=float(sys.argv[-1])

#Recup coord user
    try:
        lat=np.ma.MaskedArray(inputfile.variables[name_dim_lat])
        lon=np.ma.MaskedArray(inputfile.variables[name_dim_lon])
    except:
        sys.exit("Latitude & Longitude not found") 

#Recup all coord set available
    list_coord_dispo=[]
    for i in lat:
        for j in lon:
            list_coord_dispo.append(i);list_coord_dispo.append(j)


    all_coord=np.reshape(list_coord_dispo,(lat.size*lon.size,2))
    noval=True


#recup le fichier var.tab
var_file=open(sys.argv[2],"r") #read
lines=var_file.readlines() #line
dim_names=[]
for line in lines:
    words=line.split()
    if (words[0]==sys.argv[3]): #Quand ligne correspondante a la var passee en entree
        varndim=int(words[1])  #Nombre de dim pour la var
        for dim in range(2,varndim*2+2,2): #Recup des dim names
            dim_names.append(words[dim])
            if Coord_bool:
                if words[dim]==name_dim_lat: #Recup index de lat et lon dans la liste des dim 
                    dim_lat_index=dim/2 #WARNING useles
                    #print dim_lat_index
                if words[dim]==name_dim_lon:
                    dim_lon_index=dim/2 #WARNING useles
                    #print dim_lon_index
        #print ("Variable choisie : "+sys.argv[3]+". Nombre de dimensions : "+str(varndim)+". Dimensions : "+str(dim_names))
        

#TODO WARNING USELES, decrementer la suite
#A mettre en option ici
point_unique=True
zone_geo=False

if point_unique:
    var=sys.argv[3]
    my_dic={} ##d["string{0}".format(x)]
    for i in range(4,arg_n,3):
        #print("\nNom de la dim : "+sys.argv[i]+" action sur la dim : "+sys.argv[i+1]+" .Valeur de la dim choisie : "+sys.argv[i+2]+"\n")
        my_dic["string{0}".format(i)]="list_index_dim"
        my_dic_index="list_index_dim"+str(sys.argv[i])   #TODO Verif si il y a lon et lat
        if (sys.argv[i+1]=="l"):
            my_dic[my_dic_index]=is_strict_inf(inputfile, sys.argv[i], float(sys.argv[i+2]))
        if (sys.argv[i+1]=="le"):
            my_dic[my_dic_index]=is_equal_inf(inputfile, sys.argv[i], float(sys.argv[i+2]))
        if (sys.argv[i+1]=="g"):
            my_dic[my_dic_index]=is_strict_sup(inputfile, sys.argv[i], float(sys.argv[i+2]))
        if (sys.argv[i+1]=="ge"):
            my_dic[my_dic_index]=is_equal_sup(inputfile, sys.argv[i], float(sys.argv[i+2]))
        if (sys.argv[i+1]=="e"):
            my_dic[my_dic_index]=is_equal(inputfile, sys.argv[i], float(sys.argv[i+2]))
        if (sys.argv[i+1]==":"):
            my_dic[my_dic_index]=np.arange(inputfile.variables[sys.argv[i]].size)


    #Si on a des coord a retrouver
    if Coord_bool: 
     while noval:
        #print (all_coord.size)
        #Recherche coord dispo la plus proche
        tree=spatial.KDTree(all_coord)
        closest_coord=(tree.query([(value_dim_lat,value_dim_lon)]))
        cc_index=closest_coord[1]

        a=float(all_coord[closest_coord[1]][0][0])
        b=float(all_coord[closest_coord[1]][0][1])

        #Recup des index dans dic
        my_dic_index="list_index_dim"+str(name_dim_lat)
        my_dic[my_dic_index]=lat.tolist().index(a)

        my_dic_index="list_index_dim"+str(name_dim_lon)
        my_dic[my_dic_index]=lon.tolist().index(b)


        #Execution du string avec les dic pour recup des valeurs apres filtres
        exec2="vec2=inputfile.variables['"+str(sys.argv[3])+"']["
        first=True
        for i in dim_names: #Respect de l'ordre des dimensions
            if not first:
                exec2=exec2+","
            dimension_indexes="my_dic[\"list_index_dim"+i+"\"]"
            try:  #Si ca fonctionne pas on met tout ? c'est yolo mais evite erreur
                exec(dimension_indexes)
            except:
                dimension_indexes=":"
            exec2=exec2+dimension_indexes
            first=False
        exec2=exec2+"]"
        #print exec2 #Execution et recup dans vec2
        exec(exec2)
        #print vec2


        #Check qu'il y au moins une donnee int de dispo
        i=0 
        #print vec2.size
        #print vec2
        if vec2.size>1:
            while True and i<len(vec2):
                try:
                    float(vec2[i])
                    break
                except:
                    i=i+1
        else:
            if isinstance(vec2,(np.float32)):
                i=vec2.size+1 
                noval=False
                #print vec2
                break
        #print a
        #print b
        if i<vec2.size:
            #print lat.tolist().index(a)
            #print lon.tolist().index(b)
            noval=False
            #print vec2
        else:
            all_coord=np.delete(all_coord,cc_index,0)


#TODO check if i<len(vec2). si oui pop la coord de all_coord. Faire une fonction pour remplir my_dic_lat et _lon pour recup plus vite et plus proprement. faire un while dans un if Coord_bool pour trouver coord avec values
    else:
        #Execution du string avec les dic pour recup des valeurs apres filtres
        exec2="vec2=inputfile.variables['"+str(sys.argv[3])+"']["
        first=True
        for i in dim_names: #Respect de l'ordre des dimensions
            if not first:
                exec2=exec2+","
            dimension_indexes="my_dic[\"list_index_dim"+i+"\"]"
            try:  #Si ca fonctionne pas on met tout ? c'est yolo mais evite erreur
                exec(dimension_indexes)
            except:
                dimension_indexes=":"
            exec2=exec2+dimension_indexes
            first=False
        exec2=exec2+"]"
        #print exec2 #Execution et recup dans vec2
        exec(exec2)
   
#can be skiped AND MUST BE
    a=[]
    for i in dim_names:
        try: #If it doesn't work here its because my_dic= : so there is no size. Except will direcly take size of the dim.
            size_dim=inputfile[i][my_dic['list_index_dim'+i]].size
        except:
            size_dim=inputfile[i].size 
            my_dic['list_index_dim'+i]=range(size_dim)
        print (i,size_dim)
        b=[]
        if size_dim>1:
            for s in range(0,size_dim):
                b.append(inputfile[i][my_dic['list_index_dim'+i][s]])
                #print (i,inputfile[i][my_dic['list_index_dim'+i][s]])
        else:
            b.append(inputfile[i][my_dic['list_index_dim'+i]])
            #print (i,inputfile[i][my_dic['list_index_dim'+i]])
        a.append(b)
    #print (a)
    import itertools
    fo=open("header",'w')
    for combination in itertools.product(*a):
        fo.write(str(combination)+"\t")
    fo.write("\n")
    fo.close()
    #print exec2
    #print (vec2)
    #print vec2.shape

#test itertools combination
#    import itertools
 #   a=[]
  #  for i in dim_names:
   #     b=[]
    #    to_exe="b.append((inputfile['"+i+"'][my_dic['list_index_dim"+i+"']]))"
     #   exec(to_exe)
#
 #       print (to_exe,b)
  #      a.append(b)   
   # print (a)
    #print ("\n")   
    #for combination in itertools.product(*a):
    #    print (combination)


    fo=open("sortie.tabular",'w')
    try:
        vec2.tofile(fo,sep="\t",format="%s")
    except:
        vec3=np.ma.filled(vec2,np.nan)
        vec3.tofile(fo,sep="\t",format="%s")
    fo.close()




################################################################"""""" 
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





   
 
