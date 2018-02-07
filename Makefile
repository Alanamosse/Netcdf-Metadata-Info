CC=gcc
CFLAGS=-lnetcdf
EXEC=nc_info

all:$(EXEC)

nc_info: NC_info.c
	$(CC) NC_info.c -o netcdf-metadata-info $(CFLAGS)
