# Getting general informations about Netcdf file

The code here return informations about a netcdf file content.

One input file needed, netcdf format (*.nc).

Variables names, dimensions, and sizes are summarized in an output tabular file.

## Galaxy usage

This code is designed as part of the Galaxy tool "Netcdf Info"

https://github.com/65MO/Galaxy-E/blob/master/tools/read_netcdf

## Output structure

The variable.tabular output looks like :


| Variable1-Name  | Var1-Number-Of-Dim | Dim1 | Dim1-Size | DimN | DimN-Size |
------------------|--------------------|------|-----------|------|-----------|
| VariableX-Name  | VarX-Number-Of-Dim | DimX1 | DimX1-Size | DimXN | DimXN-Size |


## Prerequisites

The code use the c library NetCDF (>= 4.5.0)

See original source :
https://www.unidata.ucar.edu/software/netcdf/


## Usage

### Binary executable
The source code can be compiled like :

  $ gcc NC\_info.c -lnetcdf -o nc\_info

### Conda package
Working on it !
