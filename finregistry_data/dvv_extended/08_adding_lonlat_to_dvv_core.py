# Load packages:
library(tidyr)
library(dplyr)
library(lubridate)
library(stringr)
library(forcats)
library(ggplot2)
library(data.table)

latlon <- fread('~/dvv_ext_ess_lat_lon.csv')
shp <- fread("~/dvv_ext_core.csv")
shp <- shp %>% left_join(latlon, by="ident")

shp <- shp %>% select(FINREGISTRYID:pinta_ala, lon, lat, TaajamaLuo:ident)
