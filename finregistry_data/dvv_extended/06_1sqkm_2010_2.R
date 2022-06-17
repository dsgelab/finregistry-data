# Load packages:
library(tidyr)
library(dplyr)
library(lubridate)
library(stringr)
library(forcats)
library(ggplot2)
library(data.table)


km_df <- fread("~/dvv_azip_1km_shp_2010.csv.gz")

km_df2 <- km_df %>% select(ident, ko_perus:pt_muut)
km_df2 <- km_df2 %>% select(-hr_tuy)


dvv <- fread("~/dvv_ext_core.csv")
dvv <- dvv %>% 
  left_join(km_df2 %>% dplyr::select(ident, hr_ktu, hr_mtu, pt_vakiy)) 

km_df2 <- km_df2 %>% select(-hr_ktu, -hr_mtu, -pt_vakiy)
colnames(km_df2)
fwrite(km_df2, "~/dvv_ext_1sqkm_2010.csv")

dvv <- dvv %>% dplyr::select(FINREGISTRYID:self_rated_health_moderate_or_poor_scaled_health_and_welfare_indicator, hr_ktu:pt_vakiy, ident)
colnames(dvv)
fwrite(dvv, "~/dvv_ext_core.csv")
