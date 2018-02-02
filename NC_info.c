/*

General code to read and return information about Netcdf file.

Input : netcdf format file

Output is a summary tabular file with the general structure :

*****************************************************************************************
*Variable1    Var1_Number_of_Dim    Dim1    Dim1_size    ...    DimN    DimN_size       *
*VariableX    VarX_Number_of_Dim    DimX1    DimX1_size    ...    DimXN    DimXN_size   *
*...                                                                                    *
*****************************************************************************************


Dependencie : Netcdf 4.5 library, see : https://www.unidata.ucar.edu/software/netcdf/

General code can be compilated 	as follow : 
  $ gcc NC_info.c -lnetcdf -o NCinfo

Also available as conda package "netcdf_info", see https://github.com/Alanamosse/netcdf

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netcdf.h> 


#define CDI_MAX_NAME 300
typedef struct {
    int ncvarid;
    int dimtype;
    size_t len;
    char name[CDI_MAX_NAME];
}
ncdim_t;

//Global structure to store info
typedef struct {
    int ncid;
    int dims[NC_MAX_VAR_DIMS];
    int xtype;
    int ndims;
    int gmapid;
    int positive;
    int dimids[8];
    int dimtype[8];
    int chunks[8];
    int chunked;
    int chunktype;
    int natts;
    int deflate;
    int lunsigned;
    int lvalidrange;
    int *atts;
    size_t vctsize;
    double *vct;
    double missval;
    double fillval;
    double addoffset;
    double scalefactor;
    double validrange[2];
    char name[CDI_MAX_NAME];
    char longname[CDI_MAX_NAME];
    char stdname[CDI_MAX_NAME];
    char units[CDI_MAX_NAME];
    char extra[CDI_MAX_NAME];
 }
 ncvar_t;


/* Handle errors by printing an error message and exiting with a non-zero status. */
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); return 2;}

/* Handle error */
void handle_error(int status){
if (status!=NC_NOERR){
    fprintf(stderr,"%s\n",nc_strerror(status));
    exit(-1);}}


int
main(int argc, char *argv[])
{


    //Check parameter
    if(argc!=2){printf("One argument expected : Netcdf file path.\n");return 2;}


    #define FILE_NAME argv[1]
    int ncid;
    int maxdim=0;
    int id;

    /* We will learn about the data file and store results in thee program variables.  */
    int ndims_in, nvars_in, ngatts_in, unlimdimid_in;
   
    /* Error handling. */
    int retval;
   
    /* Var for nv_inq_dim*/
    int varid;
    size_t recs,len;
    char recname[NC_MAX_NAME+1];
    nc_type xtypep;
    int ndimsp,nattsp;

    /* Open the file. */
    if ((retval = nc_open(FILE_NAME, NC_NOWRITE, &ncid))){ERR(retval);}
   
    /* File details */
    if (retval = nc_inq(ncid, &ndims_in, &nvars_in, &ngatts_in,&unlimdimid_in)){ERR(retval);}
    //printf("dim number %d\nvar number: %d \nGlobal attributes number %d\n unlimited location : %d\n\n",ndims_in, nvars_in, ngatts_in, unlimdimid_in);


    char * name;
    int attnum;    
    ncvar_t var;
    char dim_name[NC_MAX_NAME+1];


    /* Open file */
    FILE * var_file;
    var_file=fopen("variables.tabular","w"); //TODO change name smthing like input_name.info ?

    if(var_file==NULL){printf("Error!");exit(1);}


    /* Print header - part 1 */
    fprintf(var_file,"VariableName	NumberOfDimensions");
    
    /* Find number max of dimensions */
    for(varid=0;varid<nvars_in;varid++){
        if(retval=(nc_inq_varndims(ncid,varid,&var.ndims))){ERR(retval);}
        if(var.ndims > maxdim){maxdim=var.ndims;}
        }


    /* Print header - part 2 */
    for(id=0;id<maxdim;id++){
        fprintf(var_file,"	Dim%dName	Dim%dSize",id,id);
        }
    fprintf(var_file,"\n");

    /* Print var informations */
    for(varid=0;varid<nvars_in;varid++){
        if(retval=(nc_inq_varndims(ncid,varid,&var.ndims))){ERR(retval);}
        if(retval=(nc_inq_var(ncid, varid, var.name, &xtypep, 0,var.dims, &var.natts))){ERR(retval);}
        fprintf(var_file,"%s\t%d",var.name,var.ndims);       
        for(id=0;id<ndims_in;id++){
            if(retval=(nc_inq_dim(ncid,var.dims[id],dim_name,&recs))){ERR(retval);}
            if(id<var.ndims){fprintf(var_file,"\t%s\t%lu",dim_name,recs);}
            else{fprintf(var_file,"\t \t ");}
        }
        fprintf(var_file,"\n");
    }

return 0;
}
