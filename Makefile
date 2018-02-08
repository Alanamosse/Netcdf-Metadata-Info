CC=gcc
CFLAGS=-lnetcdf
EXEC=netcdf-metadata-info

all:$(EXEC)

netcdf-metadata-info: NC_info.c
	$(CC) NC_info.c -o netcdf-metadata-info $(CFLAGS)
