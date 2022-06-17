# Load packages:
library(tidyr)
library(dplyr)
library(lubridate)
library(stringr)
library(forcats)
library(ggplot2)
library(data.table)
library(R.utils)

# Reading the DVV file
geo_data <- fread("~/dvv_ext_core.csv")

# Reading the Postal Codes Metadata (locally processed; find source in Documentation)
paavo_2013 <- fread("sotka_paavo/paavo_2013.csv") 

# Joining Postal Codes Metadata with DVV based on Postal Codes
geo_paavo <- geo_data %>% left_join(paavo_2013, by = c("posti_alue" = "postal_code_area"))

# Keep only columns with missing values < 20%
geo_paavo <- select(geo_paavo, which(colMeans(is.na(geo_paavo))< 0.2))

geo_paavo <- geo_paavo %>% select("ko_perus":"ident")
geo_paavo <- geo_paavo %>% select(ident, everything())


# Write dvv_ext_postal_codes.csv
fwrite(geo_paavo, "dvv_ext_postal_codes.csv")



