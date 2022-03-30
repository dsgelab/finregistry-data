# minimal phenotype creation

# libraries
library(data.table)
library(feather)
library(dplyr)
library(tibble)
library(tidyr)
library(lubridate)
library(stringr)


## file paths and loading the initial data #####
# note, put the to the beginning of each path

dvv_dir <- "/data/processed_data/dvv/"

dvv_living_name <- "Tulokset_1900-2010_tutkhenk_asuinhist.txt.finreg_IDsp"
dvv_marriage_name <- "Tulokset_1900-2010_tutkhenk_aviohist.txt.finreg_IDsp"
dvv_relative_name <- "Tulokset_1900-2010_tutkhenk_ja_sukulaiset.txt.finreg_IDsp"
id_bd_path <- "/data/processed_data/dvv/Finregistry_IDs_and_full_DOB.txt"
birth_path <- "/data/processed_data/thl_birth/THL2019_1776_synre.csv.finreg_IDsp"

vaccine_path <- "/data/processed_data/thl_vaccination/vaccination_2022-01-14.csv"
infect_path <- "/data/processed_data/thl_infectious_diseases/infectious_diseases_2022-01-19.csv"
malf_path <- "/data/processed_data/thl_malformations/malformations_anomaly_2022-01-26.csv"
cancer_path <- "/data/processed_data/thl_cancer/fcr_data.txt.finreg_IDsp"

# paths to the custom datafiles created for the minimal pheno 
ses_path <- "/data/projects/mpf/mpf_create/mpf_ses_variables_22032022.csv" 
drug_purchases_path <- '/data/projects/mpf/mpf_create/drug_purchases.csv'
kanta_prescriptions_path <- '/data/projects/mpf/mpf_create/kanta_prescriptions.csv'
# kela purchases not joined


# load the registries
dvv_living <- fread(paste0(dvv_dir, dvv_living_name)) %>% as_tibble

dvv_marriage <- fread(paste0(dvv_dir, dvv_marriage_name)) %>% as_tibble

dvv_relative <- fread(paste0(dvv_dir, dvv_relative_name)) %>% as_tibble

id_bd <- fread(id_bd_path) %>% as_tibble %>%
  rename(date_of_birth = 'DOB(YYYY-MM-DD)')

thl_birth <- fread(birth_path) %>% as_tibble

# get id numbers from each registries
id_living <- dvv_living %>% select(FINREGISTRYID)
id_mar <- dvv_marriage %>% select(FINREGISTRYID)
id_relative <- dvv_relative %>% select(FINREGISTRYID)
id_birth <- thl_birth %>%
  select(LAPSI_TNRO) %>%
  rename(FINREGISTRYID = LAPSI_TNRO) %>%
  filter(FINREGISTRYID != "")



# function to replace missing values with 0s
replace.na.0 <- function(var) {
    ifelse(is.na(var), 0, var)
}


# get IDs from DVV registries (also adding spouse ids and checking thl birth registry for extra ids) ####

# this gives 77 247 698 rows
all_ids_multi <- bind_rows(id_living, id_mar, id_relative)

# 5 339 800 unique IDs in DVV registries
all_ids <- unique(all_ids_multi)

# 7 070 389 unique relative id's
all_relative_ids <- dvv_relative %>% select(Relative_ID) %>% unique

# mpf is the minimum phenotype file
mpf <- all_ids %>%
  mutate(index_person = 1)

# get all relative id's
all_relative_ids <- all_relative_ids %>%
  rename(FINREGISTRYID = Relative_ID)

# 1,7 million relatives not in IDs
only_relatives <- setdiff(all_relative_ids, all_ids) 


# get all spouses' ids from marriage registry
all_spouse_ids <- dvv_marriage %>% 
  select(Spouse_personal_ID) %>%
  filter(Spouse_personal_ID != "") %>%
  rename(FINREGISTRYID = Spouse_personal_ID) 

# identify unique spouses (not in index persons or in relatives!)
# n = 96028
only_spouses <- setdiff(all_spouse_ids, all_relative_ids)

# join relatives and spouses to index persons
only_rels_and_spouses <- bind_rows(only_relatives, only_spouses) %>%
  mutate(index_person = 0)

mpf_all_ids <- bind_rows(mpf, only_rels_and_spouses)

# remove id ID is missing
mpf <- mpf_all_ids %>%
  filter(FINREGISTRYID != "")


# check if this list matches the data containing all ID's and birth dates
id_bd <- fread(id_bd_path) %>% as_tibble %>%
  rename(date_of_birth = 'DOB(YYYY-MM-DD)')

setdiff(mpf$FINREGISTRYID, id_bd$FINREGISTRYID) # empty vector
setdiff(id_birth$FINREGISTRYID, mpf$FINREGISTRYID) # empty vector - no extra IDs in the birth registry




# dates of death and birth #####

# 11 birth dates missing (fixed in the data amendment)
# There are 257 unique duplicate ids. All of the duplicated had identical birth dates
# and second pair had non-NA death date.
# Kept only entries with existing death date.
# All of the death dates are in 2020.


# get birth and death dates from DVV relative registry

death_dates <- dvv_relative %>%
  select(Relative_ID, Relative_death_date) %>%
  rename(FINREGISTRYID = Relative_ID,
         death_date = Relative_death_date) %>%
  distinct() 

# use id_bd for birth dates, read in the last section (death date here is from DVV relatives)
bd_dates <- left_join(id_bd, death_dates, by = "FINREGISTRYID")


## 106 additional death dates from causes of death registry 

# Causes of death dirs and names
sf_dir <- "/data/processed_data/sf_death/"
cod_name <- "thl2019_1776_ksyy_tutkimus.csv.finreg_IDsp"
cod_name_vuosi <- "thl2019_1776_ksyy_vuosi.csv.finreg_IDsp"

# load causes of death
cod <- fread(paste0(sf_dir, cod_name)) %>% as_tibble
cod_vuosi <- fread(paste0(sf_dir, cod_name_vuosi)) %>% as_tibble

# select death date from both cause of death registries
cod_date <- cod %>% 
  select(TNRO, KPV) %>%
  rename(FINREGISTRYID = TNRO)

cod_date_vuosi <- cod_vuosi %>% 
  select(TNRO, KPV) %>%
  rename(FINREGISTRYID = TNRO)

# bind the dates and select unique rows (n = 1558314)
all_cod_dates <- bind_rows(cod_date, cod_date_vuosi) %>% distinct

# select dvv relative based death dates
mpf_death_date <- bd_dates %>%
  select(FINREGISTRYID, death_date)


# join two sources of death dates (KPV from cod, death_date from dvv_relatives)
compare_death_dates <- left_join(mpf_death_date, all_cod_dates, by = "FINREGISTRYID") 



## checks ##
# There's not full overlap between COD and DVV registries.

# 46078 death dates that are not in dvv relatives.
# 54560 death dates that are not in causes of death registry

# in 1786 cases, death dates are not identical.

#
#
 compare_death_dates %>%
  filter(death_date != KPV) %>%
  mutate(deathdiff = difftime(death_date, KPV) %>% as.numeric) %>%
  pull(deathdiff) %>% quantile(., c(0, 0.01, (1:9)/10, 0.99, 1)) 
# 
#      Min.   1st Qu.    Median      Mean   3rd Qu.      Max. 
#   <-7000    -1.000     1.000     1.349     2.000 12414.000 
#
# percentiles of differences

#       0%       1%      10%      20%      30%      40%      50%      60% 
#   <-7000   -365.00    -5.00    -1.00    -1.00    -1.00     1.00     1.00 
#
#      70%      80%      90%      99%     100% 
#     1.00     3.00    10.00   304.15   >12 000 
#
#
#
# No one has negatife lifespan.

# identify those with discrebant death dates
not_identical_death_dates <- compare_death_dates %>%
  filter(death_date != KPV) %>%
  mutate(deathdiff = difftime(death_date, KPV) %>% as.numeric) %>%
  filter(deathdiff != 0)

# Those with difference in death dates < 10 days, we'll use COD death date.
use_cod_for_these <- not_identical_death_dates %>%
  filter(abs(deathdiff) < 10) %>%
  select(FINREGISTRYID, KPV) %>%
  rename(death_date_cod = KPV)




# find missing death dates from both & combine

missing_relative_death_dates <- compare_death_dates %>%
  filter(!is.na(KPV)& is.na(death_date)) %>%
  select(FINREGISTRYID, KPV) %>%
  rename(death_date = KPV)

missing_cod_death_dates <- compare_death_dates %>%
  filter(is.na(KPV)& !is.na(death_date)) %>%
  select(FINREGISTRYID, death_date) 

missing_death_dates <- bind_rows(missing_cod_death_dates, missing_relative_death_dates) %>%
  distinct()

bd_dates_2 <- left_join(bd_dates, missing_death_dates, by = "FINREGISTRYID") %>%
  mutate(death_date = case_when(
    !is.na(death_date.y) ~ death_date.y,
    TRUE ~ death_date.x
  )) %>%
  select(-c(death_date.x, death_date.y))

# replace death dates (from dvv_relatives) with COD dates for those with discrebancies
bd_dates_2 <- bd_dates_2 %>%
  left_join(use_cod_for_these, by = "FINREGISTRYID") %>% 
  mutate(death_date = case_when(
    !is.na(death_date_cod) ~ death_date_cod,
    TRUE ~ death_date
  )) %>%
  select(-death_date_cod) 


## join relative- and causes_of_death -based death and birth dates

mpf <- left_join(mpf, bd_dates_2, by = "FINREGISTRYID") 

rm(bd_dates, bd_dates_2, missing_cod_death_dates, missing_relative_death_dates,
   cod_date, cod, cod_vuosi, cod_name, cod_name_vuosi)
gc()

# Now 'mpf' has 7,166,673 rows.






# identify duplicate ids (n = 257)

dupl <- mpf %>%
  mutate(dupl = duplicated(FINREGISTRYID)) %>%
  filter(dupl == TRUE) %>%
  select(FINREGISTRYID)

dupl_id <- dupl$FINREGISTRYID

# remove id's completely that are duplicated, will be joined later
# 7,166,159 rows

mpf_without_dupl <- mpf %>%
  filter(!(FINREGISTRYID %in% dupl_id))

# get duplicate cases and remove cases with missing death dates. n = 257
actual_dupl_cases <- mpf %>%
  filter(FINREGISTRYID %in% dupl_id) %>%
  filter(!is.na(death_date)) %>%
  distinct()

# join rows. Produces data with 257 cases less. 
# n = 7 166 416
mpf <- bind_rows(mpf_without_dupl, actual_dupl_cases)


if(sum(duplicated(mpf$FINREGISTRYID)) > 0) {
  stop("there are duplicate entries still")
}




# Join sex from DVV relatives registry #######
# sex exists in 7,070,389 / 7,166,416

dvv_sex <- dvv_relative %>% 
  select(Relative_ID, Sex) %>%
  rename(FINREGISTRYID = Relative_ID,
        sex = Sex) %>%
  distinct() %>%
  mutate(sex = sex - 1)

mpf <- left_join(mpf, dvv_sex, by = "FINREGISTRYID")

# 96 028 ids without sex information, most likely the spouses from DVV marriages
# mpf %>% filter(is.na(sex))


# last place of residence ######

# the post codes are as double. This coding loses the first digits if they are 0.
# Let's add 1 or two zeros to the start of too short post codes.


change_post_codes <- dvv_living %>%
  mutate(post_code_length = nchar(Post_code)) %>%
  mutate(Post_code = as.character(Post_code)) %>%
  mutate(Post_code = case_when(
    post_code_length == 4 ~ paste0("0", Post_code),
    post_code_length == 3 ~ paste0("00", Post_code),
    TRUE ~ Post_code)) %>%
  select(-post_code_length)


# 80 post codes still "0", exclude these.
dvv_living <- change_post_codes %>%
  filter(Post_code != "0")

# get the latest residence place. Checked a few dates, they match e.g. date of death

# arrange according to descing start of residence, and select the latest. 
residence <- dvv_living %>% 
  group_by(FINREGISTRYID) %>%
  arrange(desc(Start_of_residence), .by_group = TRUE) %>%
  filter(row_number() == 1)

residence <- residence %>%
  select(FINREGISTRYID, Residence_type, Post_code, Latitude, Longitude,
         Start_of_residence, End_of_residence)

test <- left_join(mpf, residence, by = "FINREGISTRYID", suffix = c("", "_latest"))



mpf <- test %>% rename(residence_type_last = Residence_type,
                post_code_last = Post_code,
                latitude_last = Latitude,
                longitude_last = Longitude,
                residence_start_date_last = Start_of_residence,
                residence_end_date_last = End_of_residence)




# first place of residence  #####
# note, there's low match  in DOB and first recorded place of residence

birth_dates <- mpf %>%
  select(FINREGISTRYID, date_of_birth)

# note: these take time!!
#
# first residences according to the start date
# first_residence_by_start_date <- dvv_living %>%
#   select(FINREGISTRYID, Start_of_residence, End_of_residence,
#          Residence_type, Post_code, Latitude, Longitude) %>%
#   group_by(FINREGISTRYID) %>%
#   arrange(Start_of_residence, .by_group = TRUE) %>%
#   filter(row_number() == 1) %>% 
#   ungroup()

# first residences according to the end date
# - to be used at least in immigration
first_residence_by_end_date <- dvv_living %>%
    select(FINREGISTRYID, Start_of_residence, End_of_residence,
         Residence_type, Post_code, Latitude, Longitude) %>%
    group_by(FINREGISTRYID) %>%
    arrange(End_of_residence, by.group = TRUE) %>%
    slice(1) %>%
    ungroup()
  
first_residence <- first_residence_by_end_date

# the following scripts compare whether we should use the definition of first residency 
# arranged by the end date or the start date. 
#
#
# Conclusion: we should use the end date. There are 61 individuals where this definition 
# (sorted according to end date) produces entries that have start date later than if sorted by 
# any of the dates 
# 
# 
#
# # compare the first residence period definitions 
# # combine the two definitions by bind_rows
# starttest <- first_residence_by_start_date 
# endtest <- first_residence_by_end_date 
# test <- bind_rows(starttest, endtest)
#
# # find the smallest date in the start/end date, and select the entry where the minimum date is smallest
# test_first_residence <- test %>%
#   mutate(min_date = pmin(Start_of_residence, End_of_residence, na.rm = TRUE)) %>%
#   group_by(FINREGISTRYID) %>%
#   arrange(min_date, by.group = TRUE) %>%
#   slice(1) %>%
#   ungroup()
#
# first_residence <- test_first_residence %>%
#   select(-min_date)
#
# # join together based by FINREGISTRYID
# whattest <- left_join((first_residence %>%
#             select(FINREGISTRYID, Start_of_residence, End_of_residence)), 
#           (first_residence_by_end_date %>%
#             select(FINREGISTRYID, Start_of_residence, End_of_residence)),
#             by = "FINREGISTRYID", suffix = c("_any", "_end"))
#
# whattest %>%
#   filter(Start_of_residence_any < Start_of_residence_end) %>%
#   glimpse


# join with birth dates. The match of DOB and date of 
# first residence is very poor (only in 38,5%)
resi <- left_join(first_residence, birth_dates, by = "FINREGISTRYID")

firstresi <- resi %>%
  rename(post_code_first = Post_code,
         latitude_first = Latitude,
         longitude_first = Longitude,
         residence_start_date_first = Start_of_residence,
         residence_end_date_first = End_of_residence,
         residence_type_first = Residence_type) %>%
  select(FINREGISTRYID, post_code_first, latitude_first, longitude_first,
         residence_start_date_first, residence_end_date_first, residence_type_first)

mpf_resi <- left_join(mpf, firstresi, by = "FINREGISTRYID")


# check that colum number is correct before joining to the official data
if(ncol(mpf_resi) > 17) {
  stop("too many columns, have some joins failed?")
}

mpf <- mpf_resi

# erase temporary data
rm(test, mpf_resi, resi, birth_dates)

gc()






# mother tongue data #########

# take mother tongue variable from relatives registry
mo_to <- dvv_relative %>%
  select(Relative_ID, Mother_tongue) %>%
  rename(FINREGISTRYID = Relative_ID) %>%
  distinct()

# 1055 duplicate relative ids. Find out which duplicate ids to keep

# get duplicate ids
mo_to_dupl <- mo_to %>%
  filter(duplicated(FINREGISTRYID)) %>%
  select(FINREGISTRYID)

mo_to_dupl_id <- mo_to_dupl$FINREGISTRYID

# select only unique ids 
mo_to_unique <- mo_to %>% filter(!(FINREGISTRYID %in% mo_to_dupl_id)) %>% ungroup()

# df of only duplicates
mo_to_dupl <- mo_to %>% filter(FINREGISTRYID %in% mo_to_dupl_id)

# select rows with fewer nas
# count n_of_na and paste as new variable
n_of_na <- mo_to_dupl %>%
  is.na %>% rowSums()

mo_to_dupl$n_of_na <- n_of_na

emigr_singled <- mo_to_dupl %>% 
  group_by(FINREGISTRYID) %>%
  slice_min(n_of_na, with_ties = FALSE) %>%
  select(-n_of_na) %>%
  ungroup()

# bind singled-out cases with earlier duplicates to those with no duplicates
mo_to <- bind_rows(mo_to_unique, emigr_singled) %>% 
  mutate(mother_tongue = case_when(
  Mother_tongue %in% c("fi", "sv", "ru") ~ Mother_tongue,
  Mother_tongue == "" ~ NA_character_,
  TRUE ~ "other")) %>%
  select(-Mother_tongue)

mpf_mo_to <- left_join(mpf, mo_to, by = "FINREGISTRYID")

mpf <- mpf_mo_to 



# D V V   M A R R I A G E S #

# ever married
dvv_marriage %>% glimpse
dvv_marriage$FINREGISTRYID %>% duplicated %>% sum()

dvv_mar_filt <- dvv_marriage %>%
  filter(Current_marital_status %in% c(2:8)|!(is.na(Ending_reason))) # n = 3,685,050

spouse_id <- dvv_mar_filt$Spouse_personal_ID
marry_id <- dvv_mar_filt$FINREGISTRYID

all_married <- c(spouse_id, marry_id) %>% unique

ever_mar <- as_tibble(all_married) %>% mutate(ever_married = 1) %>%
  rename(FINREGISTRYID = value) %>%
  filter(FINREGISTRYID != "")

# ever_divorced
# divorced index persons

divor_index <- dvv_marriage %>%
  filter((Current_marital_status %in% c(4, 7) | Ending_reason %in% c(1, 5, 6, 8))) %>%
  pull(FINREGISTRYID)

# divorced spouses, filter only from ending reason. 
divor_spouse <- dvv_marriage %>%
  filter(Ending_reason %in% c(1, 5, 6, 8)) %>%
  pull(Spouse_personal_ID)

ever_divor <- unique(c(divor_index, divor_spouse))

# create a df and a variable, remember to filter empty id's away
ever_divor <- as_tibble(ever_divor) %>%
  mutate(ever_divorced = 1) %>%
  rename(FINREGISTRYID = value) %>%
  filter(FINREGISTRYID != "")

mpf_mar <- left_join(mpf, ever_mar, by = "FINREGISTRYID")
mpf_mar <- left_join(mpf_mar, ever_divor, by = "FINREGISTRYID")

# mutate ever_married and ever_divorced 0s. Important to mutate them only for index persons,
# although we have marriage data on some of the relatives. Spouses with missing data are now missing (not 0)
# 
# we have 
# - 5,789,026 non-missing ever_married variables and 
# - 5,461,058 non-missing ever_divorced variables
# 
# apparently some spouses have marriage information even if they're not index persons.

 mpf_mar <- mpf_mar %>% 
  mutate(ever_married = case_when(
    is.na(ever_married) & index_person == 1 ~ 0,
    TRUE ~ ever_married
  )) %>%
  mutate(ever_divorced = case_when(
    is.na(ever_divorced) & index_person == 1 ~ 0,
    TRUE ~ ever_divorced
  ))


mpf <- mpf_mar

rm(dvv_mar_filt, spouse_id, ever_mar, marry_id, 
  all_married, divor, divor_index, divor_spouse, ever_divor, mpf_mar, index, allspouses)
gc()



# immigration ######
# MARCH 2022: WE WON'T USE AN IMMIGRATION DEFINITION. LATER ON WOULD BE NICE TO CHECK IF 
# THERE ARE REGISTRY ENTRIES BEFORE SUSPECTED IMMIGRATION DATE. 


# use slice to select first living entries
# first_residence

# # from first living entries, extract those with foreign residence 
# # type and missing start date
# probable_immigrants <- first_residence %>%
#   filter(is.na(Start_of_residence) & Residence_type == 3) %>% 
#   mutate(immigrated = 1) %>%
#   select(FINREGISTRYID, End_of_residence, immigrated) %>%
#   rename(immigration_date = End_of_residence)


# mother tongue check
# motocheck <- left_join(mo_to, probable_immigrants, by = "FINREGISTRYID")
#
# motocheck %>% 
#   filter(immigrated == 1) %>%
#     select(mother_tongue) %>% table


# Emigration ######

# MARCH 2022: WE WILL USE ONLY A SIMPLE DEFINITION OF EMIGRATION. 
# Take information only from DVV relatives' "emigration_date" variable.

# We have 208,907 according to this definition.

#             emigrated
# index_person       0       1    <NA>
#            0       0  147518 1679094
#            1 5278416   61389       0


# emigrants from relatives
emigrants_relatives <- dvv_relative %>%
  filter(Home_town == 200 | !is.na(Emigration_date)) %>%
  select(Relative_ID, Country_of_residence, 
         Country_name, Emigration_date, Home_town, 
         Municipality_name) %>%
  rename(FINREGISTRYID = Relative_ID) %>%
  distinct()

probable_emigrants <- emigrants_relatives %>%
  select(FINREGISTRYID, Emigration_date) %>%
  rename(emigration_date = Emigration_date) %>%
  ungroup %>%
  mutate(emigrated = 1)


# emigrated
mpf_emigr <- left_join(mpf, probable_emigrants, by = "FINREGISTRYID") %>%
  mutate(emigrated = ifelse((is.na(emigrated) & index_person == 1), 0, emigrated))


# not run, immigration definition
# mpf_emigr <- left_join(mpf_emigr, probable_immigrants, by = "FINREGISTRYID")

# check
mpf_emigr %>%
  select(index_person, emigrated) %>% table(., useNA = "ifany")
#
#
# Most of the emigrated are non-index persons.
# 
#             emigrated
# index_person       0       1    <NA>
#            0       0  147518 1679094
#            1 5278416   61389       0
#
#


mpf <- mpf_emigr 

# # from dvv_living, filter those with foreign period > 10 years or end date missing
# emigrants_living <- dvv_living %>%
#   filter(Residence_type == 3) %>%
#   mutate(foreign_years = interval(Start_of_residence, End_of_residence) / years(1)) %>%
#   filter(is.na(End_of_residence) | foreign_years > 10)

# # select the first emigration entry for each id to avoid dublicates. 
# first_emigration_in_living <- emigrants_living %>%
#   group_by(FINREGISTRYID) %>%
#   arrange(Start_of_residence, .by_group = TRUE) %>%
#   slice(1)

# # select start_of_residence as the emigration date
# emig_dates_living <- first_emigration_in_living %>%
#   select(FINREGISTRYID, Start_of_residence) %>%
#   ungroup

# combine emigrants from dvv_living and dvv_relatives.
# If there are mismatching dates (n = 60 843), keep the first date. 
# create an indicator variable (probable_emigrants).

# probable_emigrants <- full_join(emig_dates_living, emig_dates_relative, 
#                                 by = "FINREGISTRYID") %>%
#   # keep the first date
#   mutate(emigr_date = pmin(Emigration_date, Start_of_residence, na.rm = TRUE)) %>%
#   select(FINREGISTRYID, emigr_date) %>%
#   rename(emigration_date = emigr_date) %>%
#   mutate(emigrated = 1)


# immigrated (we decided against having immigration because of definition problems)

# mpf <- left_join(mpf, probable_immigrants, by = "FINREGISTRYID") %>% 
#   mutate(probably_immigrated = replace.na.0(probably_immigrated)) %>%
#   rename(immigration_date = End_of_residence) 






# # complete followup
# mpf <- mpf %>%
#   # complete follow-up
#   mutate(complete_followup = case_when(
    
#     emigrated == 1,
#     TRUE ~ 0
    
#   )) %>%
#   # end of fu date
#   mutate(end_of_followup = case_when(
    
#     !is.na(emigration_date) ~ emigration_date,
#     !is.na(death_date) & is.na(emigration_date) ~ death_date
    
#   ))






# assisted living ######

# load social hilmo
data_dir <- "/data/processed_data/thl_soshilmo/"
social_hilmo_name <- "thl2019_1776_soshilmo.csv.finreg_IDsp"

social_hilmo <- fread(paste0(data_dir, social_hilmo_name)) %>% as_tibble


# ever been in assisted living: 
# Select all unique id's in social hilmo registry and indicate them with 
# assisted_living = 1
in_social_hilmo <- social_hilmo %>%
  select(TNRO) %>%
  rename(FINREGISTRYID = TNRO) %>%
  distinct() %>%
  mutate(in_social_hilmo = 1)

# join to mpf
mpf <- left_join(mpf, in_social_hilmo, by = "FINREGISTRYID") %>%
  mutate(in_social_hilmo = ifelse(is.na(in_social_hilmo), 0, in_social_hilmo)) 


# check against index person status
# 
# mpf %>%
#   select(index_person, in_social_hilmo) %>% table(., useNA = "ifany")
#
#
#             in_social_hilmo
# index_person       0       1
#            0 1681089  145523
#            1 4904906  434899


#remove original social_hilmo data
rm(social_hilmo)
gc()

# social assistance ######
#           
# Select those ids that are in the social assistance registry
# 

social_assist_dir <- "/data/processed_data/thl_social_assistance/"
social_assist_name <- "3214_FinRegistry_toitu_MattssonHannele07122020.csv.finreg_IDsp"
social_assist_spouse_name <- "3214_FinRegistry_puolisontoitu_MattssonHannele07122020.csv.finreg_IDsp"


social_assist <- fread(paste0(social_assist_dir, social_assist_name)) %>% as_tibble
social_assist_spouse <- fread(paste0(social_assist_dir, social_assist_spouse_name)) %>% as_tibble

s_a_ids <- social_assist %>%
  select(TNRO)
s_a_sp_ids <- social_assist_spouse %>%
  select(TNRO)

all_social_assist <- bind_rows(s_a_ids, s_a_sp_ids) %>% distinct() %>%
  mutate(in_social_assistance_registries = 1) %>%
  rename(FINREGISTRYID = TNRO)

mpf <- left_join(mpf, all_social_assist, by = "FINREGISTRYID") %>%
  mutate(in_social_assistance_registries = ifelse(is.na(in_social_assistance_registries), 
                                             0, 
                                             in_social_assistance_registries))

# check
# mpf %>%
#   select(index_person, in_social_assistance_registries) %>% table(., useNA = "ifany")
#
#               in_social_assistance_registries
# index_person       0       1
#            0 1623599  203013
#            1 3745030 1594775


# remove temporary files
rm(social_assist, social_assist_spouse, s_a_ids, s_a_sp_ids)
gc()










# checks
#
# No missing ids
# setdiff(mpf$FINREGISTRYID, id_bd$FINREGISTRYID)
#
# there is 1 completely identical duplicate id that is removed with 'distinct'
#
# duplicates <- mpf %>%
#   filter(duplicated(FINREGISTRYID)) %>%
#   pull(FINREGISTRYID)
#
# mpf %>%
#   filter(FINREGISTRYID %in% duplicates)

mpf <- mpf %>% distinct()






mpf_intermediate_backup <- mpf

 
# mothers and fathers ids

# id_mother

mothers = dvv_relative %>%
  filter(Relationship == "3a") %>%
  rename(id_mother = Relative_ID) %>%
  select(FINREGISTRYID, id_mother)
#
#
# checks
#
# mothers %>%
#   mutate(dupl_mothers = duplicated(FINREGISTRYID)) %>%
#   pull(dupl_mothers) %>% sum
#
# 66 ids have more than 1 id_mother. They will all be coded as missing

dupl_mother_ids <- mothers %>%
  filter(duplicated(FINREGISTRYID) | duplicated(FINREGISTRYID, fromLast = TRUE)) %>%
  pull(FINREGISTRYID)

mothers <- mothers %>%
  filter(!(FINREGISTRYID %in% dupl_mother_ids))

# join filtered mother ids
mpf <- mpf %>% left_join(mothers)





#id_father

fathers = dvv_relative %>%
  filter(Relationship == "3i") %>%
  rename(id_father = Relative_ID) %>%
  select(FINREGISTRYID, id_father)
#
# check
# 
# 63 ids have duplicate fathers. Will be coded as missing.
#
# fathers %>%
#   mutate(dupl_fathers = duplicated(FINREGISTRYID)) %>%
#   pull(dupl_fathers) %>% sum


dupl_father_ids <- fathers %>%
  filter(duplicated(FINREGISTRYID) | duplicated(FINREGISTRYID, fromLast = TRUE)) %>%
  pull(FINREGISTRYID)

fathers <- fathers %>%
  filter(!(FINREGISTRYID %in% dupl_father_ids))


mpf <-  mpf %>% left_join(fathers)


#number_of_children
# 
# Count n:o of children in DVV relatives. If no children, will appear as missing.
# 
# no duplicates here!
number_of_children = dvv_relative %>%
  filter(Relationship == "2") %>%
  count(FINREGISTRYID, name = 'number_of_children')



mpf <-  mpf %>% left_join(number_of_children)

# set number of children to 0 if index person doesn't have any children.
mpf <- mpf %>%
  as_tibble() %>%
  mutate(number_of_children = ifelse(is.na(number_of_children) & index_person == 1, 0, number_of_children))



# mpf = mpf %>% left_join(dobs)
# mpf = mpf %>% mutate(date_of_birth = `DOB(YYYY-MM-DD)`)
# mpf = mpf %>% select(-`DOB(YYYY-MM-DD)`)

thl_birth # read in the beginning



# If death date 01-01-2020 or later set it as NA
# 
mpf <- mpf %>%
  mutate(death_date = as.IDate(ifelse(death_date < as.IDate('2020-01-01'), death_date, NA))) 



# Add a column for having records in THL Birth registry as a mother
#
# no duplicates
mothers_birth <- thl_birth %>%
  distinct(AITI_TNRO) %>%
  mutate(birth_registry_mother = 1)



mpf <- mpf %>%
  left_join(mothers_birth, by = c("FINREGISTRYID" = "AITI_TNRO")) %>%
  mutate(birth_registry_mother = ifelse(is.na(birth_registry_mother), 0, 1)) 


# Add a column for having records in THL Birth registry as a child
#
# no duplicates
children <- thl_birth %>%
  distinct(LAPSI_TNRO) %>%
  mutate(birth_registry_child = 1)


mpf <- mpf %>%
  left_join(children, by = c("FINREGISTRYID" = "LAPSI_TNRO")) %>%
  mutate(birth_registry_child = ifelse(is.na(birth_registry_child), 0, 1))


# In vaccination registrer


vaccine <- fread(vaccine_path, select = c("TNRO")) %>% as_tibble %>%
  mutate(in_vaccination_registry = 1) %>%
  distinct() %>%
  rename(FINREGISTRYID = TNRO)

mpf <- left_join(mpf, vaccine, by = "FINREGISTRYID") %>%
  mutate(in_vaccination_registry = replace.na.0(in_vaccination_registry))


# table for index persons and in_vaccination_registry
# mpf %>%
# select(in_vaccination_registry, index_person) %>% table(., useNA = "ifany")
#
#
#                        index_person
# in_vaccination_registry       0       1
#                       0 1227603  724258
#                       1  599009 4615546

# in infectious disease registry

infect <- fread(infect_path, select = c("TNRO")) %>% as_tibble %>%
  distinct() %>%
  mutate(in_infect_dis_registry = 1) %>%
  rename(FINREGISTRYID = TNRO)

mpf <- left_join(mpf, infect, by = "FINREGISTRYID") %>%
  mutate(in_infect_dis_registry = replace.na.0(in_infect_dis_registry))  


# check against index_person (this table includes individual duplicates)

# mpf %>%
# select(in_infect_dis_registry, index_person) %>% table(., useNA = "ifany")
#
# 
#                       index_person
# in_infect_dis_registry       0       1
#                      0 1719659 4411818
#                      1  106953  927986






# in Malformations_registry

malf <- fread(malf_path, select = c("TNRO")) %>% as_tibble %>%
  distinct() %>%
  mutate(in_malformations_registry = 1) %>%
  rename(FINREGISTRYID = TNRO)

mpf <- left_join(mpf, malf, by = "FINREGISTRYID") %>%
  mutate(in_malformations_registry = replace.na.0(in_malformations_registry)) 
#
# check against index_person 
#
# mpf %>%
# select(in_malformations_registry, index_person) %>% table(., useNA = "ifany")
#
#

#                          index_person
# in_malformations_registry       0       1
#                         0 1799269 5293809
#                         1   27343   45995

# cancer

cancer <- fread(cancer_path, select = c("FINREGISTRYID")) %>% as_tibble %>%
  distinct() %>%
  mutate(in_cancer_registry = 1) 

mpf <- left_join(mpf, cancer, by = "FINREGISTRYID") %>%
  mutate(in_cancer_registry = replace.na.0(in_cancer_registry)) 
#
#
# check against index person
#
# mpf %>%
# select(in_cancer_registry, index_person) %>% table(., useNA = "ifany")
#
#                   index_person
# in_cancer_registry       0       1
#                  0 1505208 4878723
#                  1  321404  461081




# duplicate check
nrow(mpf) #  7166416



# identify duplicate ids - 133 unique IDs
# no duplicates!
dupl <- mpf %>%
  mutate(dupl = duplicated(FINREGISTRYID)) %>%
  filter(dupl) %>%
  pull(FINREGISTRYID)

if(length(dupl) > 0) {
  stop("duplicates identified!")
} # all clear



# add SES variables
ses <- fread(ses_path) %>% as_tibble

# rename to lower case
mpf_ses <- left_join(mpf, ses, by = "FINREGISTRYID") %>%
  rename(ses = SES,
        occupation = OCCUPATION,
        edulevel = EDULEVEL,
        edufield = EDUFIELD)

mpf <- mpf_ses

# add drug purchases
drug_purchases <- fread(drug_purchases_path) %>% as_tibble

mpf <- mpf %>%
  left_join(drug_purchases, by = c("FINREGISTRYID" = "HETU"))

# add kanta prescriptions
kanta_prescriptions <- fread(kanta_prescriptions_path) %>% as_tibble

mpf <- mpf %>%
  left_join(kanta_prescriptions, by = c("FINREGISTRYID" = "PATIENT_ID"))



# save 
setwd("/data/projects/mpf/mpf_create/")
write.csv(mpf, "minimal_phenotype_main_032022.csv", 
    row.names = FALSE)

