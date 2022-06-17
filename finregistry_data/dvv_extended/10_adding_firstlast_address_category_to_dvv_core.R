# For the better compatibility of DVV Living extended with minimal phenotype, a column indicating if it's the first, last or only address was created

# Load packages:
library(tidyr)
library(dplyr)
library(lubridate)
library(stringr)
library(forcats)
library(ggplot2)
library(data.table)

core <- fread("dvv_ext_core.csv")
head(core)

mp <- fread("/data/processed_data/minimal_phenotype/minimal_phenotype_2022-03-28.csv")
mp <- as_tibble(mp)
colnames(mp)
mp <- mp %>% select(FINREGISTRYID, latitude_last, residence_start_date_last, 
                    latitude_first, residence_start_date_first)
                    

mpcore <- core %>% left_join(mp)

mpcore2 <- mpcore %>% select(FINREGISTRYID, Latitude, Start_of_residence, latitude_first, residence_start_date_first, latitude_last, residence_start_date_last)
head(mpcore2)

mpcore2$Start_of_residence[is.na(mpcore2$Start_of_residence)] <- as.Date("1500/01/01")
mpcore2$residence_start_date_first[is.na(mpcore2$residence_start_date_first)] <- as.Date("1500/01/01")
mpcore2$residence_start_date_last[is.na(mpcore2$residence_start_date_last)] <- as.Date("1500/01/01")
mpcore2$latitude_last[is.na(mpcore2$latitude_last)] <- 0
mpcore2$latitude_first[is.na(mpcore2$latitude_first)] <- 0
mpcore2$Latitude[is.na(mpcore2$Latitude)] <- 0

mpcore2 %>% filter(FINREGISTRYID == "FR0000003")

mpcore2 <- mpcore2 %>% 
  mutate(
    first_last_address = case_when(
      latitude_first == Latitude & residence_start_date_first == Start_of_residence & latitude_last != Latitude & residence_start_date_last != Start_of_residence ~ 1,
      latitude_last == Latitude & residence_start_date_last == Start_of_residence & latitude_first != Latitude & residence_start_date_first != Start_of_residence ~ 2,
      latitude_first == Latitude & residence_start_date_first == Start_of_residence & latitude_last == Latitude & residence_start_date_last == Start_of_residence ~ 3,
      latitude_first != Latitude & residence_start_date_first != Start_of_residence & latitude_last != Latitude & residence_start_date_last != Start_of_residence ~ 0
    )
  )

# bind the column to the dvv core file
core2 <- cbind(core, mpcore2$first_last_address)

#rename column V2 to first_last_address:
names(core2)[names(core2) == "V2"] <- "first_last_address"

# sort dvv core and save to csv
core2 <- core2 %>% select(FINREGISTRYID:pt_vakiy, first_last_address, ident)
glimpse(core2)
fwrite(core2, "dvv_ext_core.csv")
