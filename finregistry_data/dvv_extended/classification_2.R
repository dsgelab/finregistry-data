library(tidyr)
library(dplyr)
library(lubridate)
library(stringr)
library(forcats)
library(ggplot2)
library(data.table)

shp_data <- fread("shapefiles/dvv_and_shp_5.csv")

# Create Unique Column Names
names(shp_data) <- make.names(names(shp_data), unique=TRUE)

shp_data <- shp_data %>% select(-Residence_type, -Municipality, -Municipality_name, -V1,
                                  -Building_ID, -Residence_code, -Post_code, -'Unnamed..0')  


shp_data <- shp_data %>% distinct(FINREGISTRYID, Start_of_residence, .keep_all = TRUE)



living_shp_2 <- shp_data %>% select(FINREGISTRYID : index_right_3, index_right_4, index_right_5)
colnames(living_shp_2)

# Checking how many Addresses are in more than one Area  
nrow(living_shp_2 %>% filter(!is.na(index_right_3) & !is.na(index_right_4)))  # 697      # Sparse Small House Area  &  Apartment building Area
nrow(living_shp_2 %>% filter(!is.na(index_right_3) & !is.na(index_right_5)))  # 11816    # Sparse Small House Area  &  Small house Area
nrow(living_shp_2 %>% filter(!is.na(index_right_4) & !is.na(index_right_5)))  # 29869    # Apartment building Area  &  Small house Area

# Renaming 
living_shp_2 <- living_shp_2 %>% dplyr::rename(sparse_small_house_area = index_right_3,
                        apartment_building_area = index_right_4,
                        small_house_area = index_right_5)
# For each value (!=NA) assign number 1, else (=NA) 0   
living_shp_2 <- living_shp_2 %>% mutate(sparse_small_house_area = ifelse(!is.na(sparse_small_house_area), 1, 0),
                                        apartment_building_area = ifelse(!is.na(apartment_building_area), 1, 0),
                                        small_house_area = ifelse(!is.na(small_house_area), 1, 0)
)

# Keep NAs for Addresses with missing geographical data (e.g. Latitude is NA)
living_shp_2$sparse_small_house_area[is.na(living_shp_2$Latitude)] <- NA
living_shp_2$apartment_building_area[is.na(living_shp_2$Latitude)] <- NA
living_shp_2$small_house_area[is.na(living_shp_2$Latitude)] <- NA

nrow(living_shp_2 %>% filter(is.na(sparse_small_house_area))) /35041489
living_shp_2


# How many Addresses have no Area assigned?
nrow(living_shp_2 %>% filter(sparse_small_house_area == 0 & apartment_building_area == 0 & small_house_area == 0))  # 4008584
# How many Addresses are in all three Areas?
nrow(living_shp_2 %>% filter(sparse_small_house_area == 1 & apartment_building_area == 1 & small_house_area == 1))  # 17
# What is the percentage of Addresses with no Area assigned? (basically all NA in raw data)
nrow(living_shp_2 %>% filter(sparse_small_house_area == 0 & apartment_building_area == 0 & small_house_area == 0))/35041489  # 0.2024187
# Are there still NAs? -> No because they were replaced with 0
nrow(living_shp_2 %>% filter(is.na(sparse_small_house_area)))  # 0  # no NAs because they were replaced with 0
nrow(is.na(living_shp_2$small_house_area))

## Urban_rural Shapefile
# Check unique values of Luokka (class) of Urban_rural Shapefile?
unique(living_shp_2$Luokka)  # "" (empty string) is a class
living_shp_2 %>% filter(Luokka == "")  # 3084602
# Replace empty string with NA
living_shp_2$Luokka[living_shp_2$Luokka==''] <- NA 
living_shp_2 %>% filter(is.na(Luokka))  #  3084602

## Dense_sparse Shapefile
unique(living_shp_2$TaajamaSel)  # "" (empty string) is a class
# Replace empty string with NA
living_shp_2$TaajamaSel[living_shp_2$TaajamaSel==''] <- NA 
nrow(living_shp_2 %>% filter(is.na(TaajamaSel))) /35041489  # 0.176443 
unique(na.omit(living_shp_2$TaajamaSel))


## Municipality Shapefile
living_shp_2 %>% filter(nimi == "")
living_shp_2$nimi[living_shp_2$nimi==''] <- NA
living_shp_2$namn[living_shp_2$namn==''] <- NA


living_shp_2 <- living_shp_2 %>% select(FINREGISTRYID:geometry, posti_alue:namn, kuntanro, pinta_ala, TaajamaLuo, TaajamaSel, Luokka, Nimi, sparse_small_house_area:small_house_area)
living_shp_2

fwrite(living_shp_2, "dvv_shapefiles_essential.csv")

