
# FinRegisty: create minimal phenotype dataset  

# load R libraries
library(data.table)
library(dplyr)
library(tibble)
library(tidyr)
library(lubridate)
library(stringr)


## file paths and loading the initial data #####

dvv_dir <- "/data/processed_data/dvv/"
# list.files(dvv_dir, pattern="csv")
dvv_living_name <- "living_history_2023-06-14.csv"
dvv_marriage_name <- "marriages_2023-06-14.csv"
dvv_relative_name <- "relatives_2023-06-14.csv"

id_bd_path <- "/data/original_data/dvv/Finregistry_IDs_and_full_DOB_SEX.txt"

# list.files("/data/processed_data/thl_birth", pattern="csv")
# list.files("/data/processed_data/thl_vaccination", pattern="csv")
# list.files("/data/processed_data/thl_infectious_diseases", pattern="csv")
# list.files("/data/processed_data/thl_malformations", pattern="csv")
# list.files("/data/processed_data/thl_cancer", pattern="csv")
birth_path <- "/data/processed_data/thl_birth/birth_2023-06-26.csv"
vaccine_path <- "/data/processed_data/thl_vaccination/vaccination_2023-06-26.csv"
infect_path <- "/data/processed_data/thl_infectious_diseases/infectious_diseases_2023-06-26.csv"
malf_path <- "/data/processed_data/thl_malformations/malformations_anomaly_2023-06-26.csv"
cancer_path <- "/data/processed_data/thl_cancer/cancer_2023-06-26.csv"

# paths to the custom datafiles created for the minimal pheno
drug_purchases_path <- '/data/projects/mpf/mpf_create/drug_purchases.csv'
kanta_prescriptions_path <- '/data/projects/mpf/mpf_create/kanta_prescriptions.csv'
# kela purchases not joined

# function to replace missing values with 0s
replace.na.0 <- function(var) {
  ifelse(is.na(var), 0, var)
}


# load FinRegistry ####

# start with the id, dob, sex file
# sex: 0 = male, 1 = female
cat("Reading dvv id list", "\n")

id_bd <- fread(id_bd_path) %>% as_tibble %>%
  # rename variables
  rename(DATE_OF_BIRTH = `DOB(DD-MM-YYYY-format)`,
         SEX = `SEX(1=male,2=female)`) %>%
  # recode gender to match 0 = male, 1 = female
  mutate(SEX = SEX - 1) %>%
  # mutate date of birth to the standard R format.
  mutate(FORMATTED_DATE_OF_BIRTH = (as.Date(DATE_OF_BIRTH, format = "%d-%m-%Y"))) %>%
  # recode non-existing false leap year dates into actual dates
  mutate(DATE_OF_BIRTH = case_when(
    
    is.na(FORMATTED_DATE_OF_BIRTH)&
      substr(DATE_OF_BIRTH, 1, 5) == "29-02" ~ paste0("28", substr(DATE_OF_BIRTH, 3, 10)),
    
    TRUE ~ DATE_OF_BIRTH)) %>%
  # change the DOB into date format 
  mutate(DATE_OF_BIRTH = as.Date(DATE_OF_BIRTH, format = "%d-%m-%Y")) %>%
  select(-FORMATTED_DATE_OF_BIRTH) 


## check: no missingness ####
# id_bd %>% filter(is.na(SEX)|is.na(DATE_OF_BIRTH))


# load the registries ####
cat("Reading dvv_living", "\n")
dvv_living <- fread(paste0(dvv_dir, dvv_living_name)) %>% as_tibble
cat("Reading dvv_marriage", "\n")
dvv_marriage <- fread(paste0(dvv_dir, dvv_marriage_name)) %>% as_tibble
cat("Reading dvv_relative", "\n")
dvv_relative <- fread(paste0(dvv_dir, dvv_relative_name)) %>% as_tibble
cat("Reading thl_birth", "\n")
thl_birth <- fread(birth_path) %>% as_tibble

# get id numbers from each registries
id_living <- dvv_living %>% select(FINREGISTRYID)
id_mar <- dvv_marriage %>% select(FINREGISTRYID)
id_relative <- dvv_relative %>% select(FINREGISTRYID)
id_birth <- thl_birth %>%
  select(LAPSI_FINREGISTRYID) %>%
  rename(FINREGISTRYID = LAPSI_FINREGISTRYID) %>%
  filter(FINREGISTRYID != "")


# get IDs from DVV registries (also adding spouse ids and checking thl birth registry for extra ids) ####

all_ids_multi <- bind_rows(id_living, id_mar, id_relative)

all_ids <- unique(all_ids_multi)

all_relative_ids <- dvv_relative %>% select(RELATIVE_ID) %>% unique

# mpf is the minimum phenotype file
mpf <- all_ids %>%
  mutate(INDEX_PERSON = 1)

# get all relative id's
all_relative_ids <- all_relative_ids %>%
  rename(FINREGISTRYID = RELATIVE_ID)

# relatives not index persons
only_relatives <- setdiff(all_relative_ids, all_ids) 


# get all spouses' ids from marriage registry
all_spouse_ids <- dvv_marriage %>% 
  select(SPOUSE_ID) %>%
  filter(SPOUSE_ID != "") %>%
  rename(FINREGISTRYID = SPOUSE_ID) 

# identify unique spouses (not in index persons or in relatives!)
only_spouses <- setdiff(all_spouse_ids, all_relative_ids)

# join relatives and spouses to index persons
only_rels_and_spouses <- bind_rows(only_relatives, only_spouses) %>%
  mutate(INDEX_PERSON = 0)

mpf_all_ids <- bind_rows(mpf, only_rels_and_spouses)

# remove if ID is missing
mpf <- mpf_all_ids %>%
  filter(FINREGISTRYID != "")


# check if this list matches the data containing all ID's and birth dates

setdiff(mpf$FINREGISTRYID, id_bd$FINREGISTRYID) # empty vector
setdiff(id_birth$FINREGISTRYID, mpf$FINREGISTRYID) # empty vector - no extra IDs in the birth registry

# join birth dates and sex 
mpf <- mpf %>%
  left_join(id_bd, by = "FINREGISTRYID")


# dates of death and birth #####

# Kept only entries with existing death date.

## get birth and death dates from DVV relative registry

death_dates <- dvv_relative %>%
  select(RELATIVE_ID, RELATIVE_DEATH_DATE) %>%
  rename(FINREGISTRYID = RELATIVE_ID,
         DEATH_DATE = RELATIVE_DEATH_DATE) %>%
  distinct() 


## Death dates from causes of death registry 

# Causes of death dirs and names
sf_dir <- "/data/processed_data/sf_death/"
# list.files(sf_dir, pattern="csv")
cod_recent_name <- "death_2023-08-10.csv"

# load causes of death
cat("Reading sf_death", "\n")
cod <- fread(paste0(sf_dir, cod_recent_name)) %>% as_tibble

# select death date from both cause of death registries
cod_date <- cod %>% 
  select(FINREGISTRYID, KPV)

# bind the dates and select unique rows
all_cod_dates <- cod_date %>% distinct

mpf_death_date <- death_dates %>%
  select(FINREGISTRYID, DEATH_DATE)

# join two sources of death dates (KPV from cod, death_date from dvv_relatives)
compare_death_dates <- left_join(mpf_death_date, all_cod_dates, by = "FINREGISTRYID") 


## checks ##
# There's not full overlap between COD and DVV registries.

# check where neither is not null
# dim(compare_death_dates[!is.na(compare_death_dates$DEATH_DATE) & !is.na(compare_death_dates$KPV) & compare_death_dates$DEATH_DATE != compare_death_dates$KPV,])

compare_death_dates %>%
  filter(DEATH_DATE != KPV) %>%
  mutate(deathdiff = difftime(DEATH_DATE, KPV) %>% as.numeric) %>%
  pull(deathdiff) %>% quantile(., c(0, 0.01, (1:9)/10, 0.99, 1)) 

# identify those with discrepant death dates
not_identical_death_dates <- compare_death_dates %>%
  filter(DEATH_DATE != KPV) %>%
  mutate(deathdiff = difftime(DEATH_DATE, KPV) %>% as.numeric) %>%
  filter(deathdiff != 0)

# If there's discrepancy in death dates, we'll use the COD death date.
use_cod_for_these <- not_identical_death_dates %>%
  select(FINREGISTRYID, KPV) %>%
  rename(DEATH_DATE_COD = KPV)


# find missing death dates from both & combine

missing_relative_death_dates <- compare_death_dates %>%
  filter(!is.na(KPV)& is.na(DEATH_DATE)) %>%
  select(FINREGISTRYID, KPV) %>%
  rename(DEATH_DATE = KPV)

missing_cod_death_dates <- compare_death_dates %>%
  filter(is.na(KPV)& !is.na(DEATH_DATE)) %>%
  select(FINREGISTRYID, DEATH_DATE) 

missing_death_dates <- bind_rows(missing_cod_death_dates, missing_relative_death_dates) %>%
  distinct()

bd_dates_2 <- left_join(death_dates, missing_death_dates, by = "FINREGISTRYID") %>%
  mutate(DEATH_DATE = case_when(
    !is.na(DEATH_DATE.y) ~ DEATH_DATE.y,
    TRUE ~ DEATH_DATE.x
  )) %>%
  select(-c(DEATH_DATE.x, DEATH_DATE.y))

# replace death dates (from dvv_relatives) with COD dates for those with discrepancies
bd_dates_2 <- bd_dates_2 %>%
  left_join(use_cod_for_these, by = "FINREGISTRYID") %>% 
  mutate(DEATH_DATE = case_when(
    !is.na(DEATH_DATE_COD) ~ DEATH_DATE_COD,
    TRUE ~ DEATH_DATE
  )) %>%
  select(-DEATH_DATE_COD) 


## join relative- and causes_of_death -based death dates
mpf_temporary <- left_join(mpf, bd_dates_2, by = "FINREGISTRYID") 

mpf <- mpf_temporary

# remove temporary files to save memory
rm(death_dates, bd_dates_2, missing_cod_death_dates, missing_relative_death_dates,
   cod_date, cod, cod_vuosi)

gc()

# nrow(mpf)

# identify duplicate ids

dupl <- mpf %>%
  mutate(dupl = duplicated(FINREGISTRYID)) %>%
  filter(dupl == TRUE) %>%
  select(FINREGISTRYID)

dupl_id <- dupl$FINREGISTRYID

# remove id's completely that are duplicated, will be joined later

mpf_without_dupl <- mpf %>%
  filter(!(FINREGISTRYID %in% dupl_id))

# get duplicate cases and remove cases with missing death dates
actual_dupl_cases <- mpf %>%
  filter(FINREGISTRYID %in% dupl_id) %>%
  filter(!is.na(DEATH_DATE)) %>%
  distinct()

# join rows
mpf <- bind_rows(mpf_without_dupl, actual_dupl_cases)

if(sum(duplicated(mpf$FINREGISTRYID)) > 0) {
  stop("there are duplicate entries still")
}


# last place of residence ######

# the post codes are as double. This coding loses the first digits if they are 0.

change_post_codes <- dvv_living %>%
  mutate(POST_CODE_LENGTH = nchar(POST_CODE)) %>%
  mutate(POST_CODE = as.character(POST_CODE)) %>%
  mutate(POST_CODE = case_when(
    POST_CODE_LENGTH == 4 ~ paste0("0", POST_CODE),
    POST_CODE_LENGTH == 3 ~ paste0("00", POST_CODE),
    TRUE ~ POST_CODE)) %>%
  select(-POST_CODE_LENGTH)

# post codes still "0", exclude these.
dvv_living <- change_post_codes %>%
  filter(POST_CODE != "0")

# get the latest residence place. Checked a few dates, they match e.g. date of death

# arrange according to descending start of residence, and select the latest. 
residence <- dvv_living %>% 
  group_by(FINREGISTRYID) %>%
  arrange(desc(START_OF_RESIDENCE), .by_group = TRUE) %>%
  filter(row_number() == 1)

residence <- residence %>%
  select(FINREGISTRYID, RESIDENCE_TYPE, POST_CODE, LATITUDE, LONGITUDE,
         START_OF_RESIDENCE, END_OF_RESIDENCE)

test <- left_join(mpf, residence, by = "FINREGISTRYID", suffix = c("", "_LATEST"))


mpf <- test %>% rename(RESIDENCE_TYPE_LAST = RESIDENCE_TYPE,
                       POST_CODE_LAST = POST_CODE,
                       LATITUDE_LAST = LATITUDE,
                       LONGITUDE_LAST = LONGITUDE,
                       RESIDENCE_START_DATE_LAST = START_OF_RESIDENCE,
                       RESIDENCE_END_DATE_LAST = END_OF_RESIDENCE)


# first place of residence  #####
# note, there's low match  in DOB and first recorded place of residence

birth_dates <- mpf %>%
  select(FINREGISTRYID, DATE_OF_BIRTH)

# note: these take time!!

# first residences according to the end date
# - to be used at least in immigration
first_residence_by_end_date <- dvv_living %>%
  select(FINREGISTRYID, START_OF_RESIDENCE, END_OF_RESIDENCE,
         RESIDENCE_TYPE, POST_CODE, LATITUDE, LONGITUDE) %>%
  group_by(FINREGISTRYID) %>%
  arrange(END_OF_RESIDENCE, by.group = TRUE) %>%
  slice(1) %>%
  ungroup()

first_residence <- first_residence_by_end_date


# join with birth dates. The match of DOB and date of 
# first residence is very poor (only in 38,5%)
resi <- left_join(first_residence, birth_dates, by = "FINREGISTRYID")

firstresi <- resi %>%
  rename(POST_CODE_FIRST = POST_CODE,
         LATITUDE_FIRST = LATITUDE,
         LONGITUDE_FIRST = LONGITUDE,
         RESIDENCE_START_DATE_FIRST = START_OF_RESIDENCE,
         RESIDENCE_END_DATE_FIRST = END_OF_RESIDENCE,
         RESIDENCE_TYPE_FIRST = RESIDENCE_TYPE) %>%
  select(FINREGISTRYID, POST_CODE_FIRST, LATITUDE_FIRST, LONGITUDE_FIRST,
         RESIDENCE_START_DATE_FIRST, RESIDENCE_END_DATE_FIRST, RESIDENCE_TYPE_FIRST)

mpf_resi <- left_join(mpf, firstresi, by = "FINREGISTRYID")


# check that column number is correct before joining to the official data
if(ncol(mpf_resi) > 17) {
  stop("too many columns, have some joins failed?")
}

mpf <- mpf_resi

# erase temporary data
rm(test, mpf_resi, resi, birth_dates)

gc()


# mother tongue data #####

# take mother tongue variable from relatives registry
mo_to <- dvv_relative %>%
  select(RELATIVE_ID, MOTHER_TONGUE) %>%
  rename(FINREGISTRYID = RELATIVE_ID) %>%
  distinct()

# some duplicate relative ids. Find out which duplicate ids to keep

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
  mutate(MOTHER_TONGUE2 = case_when(
    MOTHER_TONGUE %in% c("fi", "sv", "ru") ~ MOTHER_TONGUE,
    MOTHER_TONGUE == "" ~ NA_character_,
    TRUE ~ "other")) %>%
  select(-MOTHER_TONGUE) %>%
  rename(MOTHER_TONGUE=MOTHER_TONGUE2)

mpf_mo_to <- left_join(mpf, mo_to, by = "FINREGISTRYID")

mpf <- mpf_mo_to 


# D V V   M A R R I A G E S ####

# ever married
dvv_marriage %>% glimpse
dvv_marriage$FINREGISTRYID %>% duplicated %>% sum()

dvv_mar_filt <- dvv_marriage %>%
  filter(CURRENT_MARITAL_STATUS %in% c(2:8)|!(is.na(ENDING_REASON)))

spouse_id <- dvv_mar_filt$SPOUSE_ID
marry_id <- dvv_mar_filt$FINREGISTRYID

all_married <- c(spouse_id, marry_id) %>% unique

ever_mar <- as_tibble(all_married) %>% mutate(EVER_MARRIED = 1) %>%
  rename(FINREGISTRYID = value) %>%
  filter(FINREGISTRYID != "")

# ever_divorced
# divorced index persons

divor_index <- dvv_marriage %>%
  filter((CURRENT_MARITAL_STATUS %in% c(4, 7) | ENDING_REASON %in% c(1, 5, 6, 8))) %>%
  pull(FINREGISTRYID)

# divorced spouses, filter only from ending reason. 
divor_spouse <- dvv_marriage %>%
  filter(ENDING_REASON %in% c(1, 5, 6, 8)) %>%
  pull(SPOUSE_ID)

ever_divor <- unique(c(divor_index, divor_spouse))

# create a df and a variable, remember to filter empty id's away
ever_divor <- as_tibble(ever_divor) %>%
  mutate(EVER_DIVORCED = 1) %>%
  rename(FINREGISTRYID = value) %>%
  filter(FINREGISTRYID != "")

mpf_mar <- left_join(mpf, ever_mar, by = "FINREGISTRYID")
mpf_mar <- left_join(mpf_mar, ever_divor, by = "FINREGISTRYID")

# mutate ever_married and ever_divorced 0s. Important to mutate them only for index persons,
# although we have marriage data on some of the relatives. Spouses with missing data are now missing (not 0)
# apparently some spouses have marriage information even if they're not index persons.

mpf_mar <- mpf_mar %>% 
  mutate(EVER_MARRIED = case_when(
    is.na(EVER_MARRIED) & INDEX_PERSON == 1 ~ 0,
    TRUE ~ EVER_MARRIED
  )) %>%
  mutate(EVER_DIVORCED = case_when(
    is.na(EVER_DIVORCED) & INDEX_PERSON == 1 ~ 0,
    TRUE ~ EVER_DIVORCED
  ))


mpf <- mpf_mar

rm(dvv_mar_filt, spouse_id, ever_mar, marry_id, 
   all_married, divor, divor_index, divor_spouse, ever_divor, mpf_mar, index, allspouses)
gc()


# immigration ####
# MARCH 2022: WE WON'T USE AN IMMIGRATION DEFINITION. LATER ON WOULD BE NICE TO CHECK IF 
# THERE ARE REGISTRY ENTRIES BEFORE SUSPECTED IMMIGRATION DATE. 

# EMIGRATION ####

# JANUARY 2023: in some individuals, emigration date was later than the death date. 
# this is clearly wrong, and demonstrates the inconsistency in some of the DVV dates related to living places.
# as a rule of thumb, death date is more likely to be correct.  

# MARCH 2022: WE WILL USE ONLY A SIMPLE DEFINITION OF EMIGRATION. 
# Take information only from DVV relatives' "emigration_date" variable.

# emigrants from relatives
emigrants_relatives <- dvv_relative %>%
  filter(HOME_TOWN == 200 | !is.na(EMIGRATION_DATE)) %>%
  select(RELATIVE_ID, COUNTRY_OF_RESIDENCE, 
         COUNTRY_NAME, EMIGRATION_DATE, HOME_TOWN, 
         MUNICIPALITY_NAME) %>%
  rename(FINREGISTRYID = RELATIVE_ID) %>%
  distinct()

probable_emigrants <- emigrants_relatives %>%
  select(FINREGISTRYID, EMIGRATION_DATE) %>%
  #rename(emigration_date = Emigration_date) %>%
  ungroup %>%
  mutate(EMIGRATED = 1)


# emigrated
mpf_emigr <- left_join(mpf, probable_emigrants, by = "FINREGISTRYID") %>%
  mutate(EMIGRATED = ifelse((is.na(EMIGRATED) & INDEX_PERSON == 1), 0, EMIGRATED))

## if death date < emigration date, emigration date will be removed
# 102 cases have death < emigration
mpf_emigr %>%
  filter(DEATH_DATE < EMIGRATION_DATE) %>%
  nrow

# recode emigration_date to missing 
mpf_emigr$EMIGRATION_DATE[mpf_emigr$DEATH_DATE < mpf_emigr$EMIGRATION_DATE] <- NA


# not run, immigration definition
# mpf_emigr <- left_join(mpf_emigr, probable_immigrants, by = "FINREGISTRYID")

# check
mpf_emigr %>%
  select(INDEX_PERSON, EMIGRATED) %>% table(., useNA = "ifany")

mpf <- mpf_emigr 


# assisted living ####

# load social hilmo
data_dir <- "/data/processed_data/thl_soshilmo/"
social_hilmo_name <- "soshilmo_2023-06-19.csv"

social_hilmo <- fread(paste0(data_dir, social_hilmo_name)) %>% as_tibble


# ever been in assisted living: 
# Select all unique id's in social hilmo registry and indicate them with 
# assisted_living = 1
in_social_hilmo <- social_hilmo %>%
  select(FINREGISTRYID) %>%
  #rename(FINREGISTRYID = TNRO) %>%
  distinct() %>%
  mutate(IN_SOCIAL_HILMO = 1)

# join to mpf
mpf <- left_join(mpf, in_social_hilmo, by = "FINREGISTRYID") %>%
  mutate(IN_SOCIAL_HILMO = ifelse(is.na(IN_SOCIAL_HILMO), 0, IN_SOCIAL_HILMO)) 


# remove original social_hilmo data
rm(social_hilmo)
gc()

# social assistance ####      
# Select those ids that are in the social assistance registry

social_assist_dir <- "/data/processed_data/thl_social_assistance/"
# list.files(social_assist_dir, pattern="csv")
social_assist_name <- "provision_2023-06-19.csv"
social_assist_spouse_name <- "spouse_provision_2023-06-19.csv"


social_assist <- fread(paste0(social_assist_dir, social_assist_name)) %>% as_tibble
social_assist_spouse <- fread(paste0(social_assist_dir, social_assist_spouse_name)) %>% as_tibble

s_a_ids <- social_assist %>%
  select(FINREGISTRYID)
s_a_sp_ids <- social_assist_spouse %>%
  select(FINREGISTRYID)

all_social_assist <- bind_rows(s_a_ids, s_a_sp_ids) %>% distinct() %>%
  mutate(IN_SOCIAL_ASSISTANCE_REGISTRIES = 1)

mpf <- left_join(mpf, all_social_assist, by = "FINREGISTRYID") %>%
  mutate(IN_SOCIAL_ASSISTANCE_REGISTRIES = ifelse(is.na(IN_SOCIAL_ASSISTANCE_REGISTRIES), 
                                                  0, 
                                                  IN_SOCIAL_ASSISTANCE_REGISTRIES))

# remove temporary files
rm(social_assist, social_assist_spouse, s_a_ids, s_a_sp_ids)
gc()

mpf <- mpf %>% distinct()


# mothers and fathers ids ####

# id_mother

mothers = dvv_relative %>%
  filter(RELATIONSHIP == "3a") %>%
  rename(ID_MOTHER = RELATIVE_ID) %>%
  select(FINREGISTRYID, ID_MOTHER)


dupl_mother_ids <- mothers %>%
  filter(duplicated(FINREGISTRYID) | duplicated(FINREGISTRYID, fromLast = TRUE)) %>%
  pull(FINREGISTRYID)

mothers <- mothers %>%
  filter(!(FINREGISTRYID %in% dupl_mother_ids))

# join filtered mother ids
mpf <- mpf %>% left_join(mothers)


# id_father ####

fathers = dvv_relative %>%
  filter(RELATIONSHIP == "3i") %>%
  rename(ID_FATHER = RELATIVE_ID) %>%
  select(FINREGISTRYID, ID_FATHER)


dupl_father_ids <- fathers %>%
  filter(duplicated(FINREGISTRYID) | duplicated(FINREGISTRYID, fromLast = TRUE)) %>%
  pull(FINREGISTRYID)

fathers <- fathers %>%
  filter(!(FINREGISTRYID %in% dupl_father_ids))

mpf <-  mpf %>% left_join(fathers)


# number_of_children ####
# Count n:o of children in DVV relatives. If no children, will appear as missing.

number_of_children = dvv_relative %>%
  filter(RELATIONSHIP == "2") %>%
  count(FINREGISTRYID, name = 'NUMBER_OF_CHILDREN')

mpf <-  mpf %>% left_join(number_of_children)

# set number of children to 0 if index person doesn't have any children.
mpf <- mpf %>%
  as_tibble() %>%
  mutate(NUMBER_OF_CHILDREN = ifelse(is.na(NUMBER_OF_CHILDREN) & INDEX_PERSON == 1, 0, NUMBER_OF_CHILDREN))


# add thl_birth ####
# Add a column for having records in THL Birth registry as a mother

mothers_birth <- thl_birth %>%
  distinct(AITI_FINREGISTRYID) %>%
  mutate(BIRTH_REGISTRY_MOTHER = 1)

mpf <- mpf %>%
  left_join(mothers_birth, by = c("FINREGISTRYID" = "AITI_FINREGISTRYID")) %>%
  mutate(BIRTH_REGISTRY_MOTHER = ifelse(is.na(BIRTH_REGISTRY_MOTHER), 0, 1)) 


# Add a column for having records in THL Birth registry as a child

children <- thl_birth %>%
  distinct(LAPSI_FINREGISTRYID) %>%
  mutate(BIRTH_REGISTRY_CHILD = 1)

mpf <- mpf %>%
  left_join(children, by = c("FINREGISTRYID" = "LAPSI_FINREGISTRYID")) %>%
  mutate(BIRTH_REGISTRY_CHILD = ifelse(is.na(BIRTH_REGISTRY_CHILD), 0, 1))


# In vaccination registry ####

vaccine <- fread(vaccine_path, select = c("FINREGISTRYID")) %>% as_tibble %>%
  mutate(IN_VACCINATION_REGISTRY = 1) %>%
  distinct()

mpf <- left_join(mpf, vaccine, by = "FINREGISTRYID") %>%
  mutate(IN_VACCINATION_REGISTRY = replace.na.0(IN_VACCINATION_REGISTRY))

# in infectious disease registry ####

infect <- fread(infect_path, select = c("FINREGISTRYID")) %>% as_tibble %>%
  distinct() %>%
  mutate(IN_INFECT_DIS_REGISTRY = 1)

mpf <- left_join(mpf, infect, by = "FINREGISTRYID") %>%
  mutate(IN_INFECT_DIS_REGISTRY = replace.na.0(IN_INFECT_DIS_REGISTRY))  


# in Malformations_registry ####

malf <- fread(malf_path, select = c("FINREGISTRYID")) %>% as_tibble %>%
  distinct() %>%
  mutate(IN_MALFORMATIONS_REGISTRY = 1)

mpf <- left_join(mpf, malf, by = "FINREGISTRYID") %>%
  mutate(IN_MALFORMATIONS_REGISTRY = replace.na.0(IN_MALFORMATIONS_REGISTRY)) 


# cancer ####

cancer <- fread(cancer_path, select = c("FINREGISTRYID")) %>% as_tibble %>%
  distinct() %>%
  mutate(IN_CANCER_REGISTRY = 1) 

mpf <- left_join(mpf, cancer, by = "FINREGISTRYID") %>%
  mutate(IN_CANCER_REGISTRY = replace.na.0(IN_CANCER_REGISTRY)) 

# duplicate check
nrow(mpf)


# identify duplicate ids 

dupl <- mpf %>%
  mutate(dupl = duplicated(FINREGISTRYID)) %>%
  filter(dupl) %>%
  pull(FINREGISTRYID)

if(length(dupl) > 0) {
  stop("duplicates identified!")
} # all clear


# add drug purchases ####

drug_purchases <- fread(drug_purchases_path) %>% as_tibble

mpf <- mpf %>%
  left_join(drug_purchases, by = c("FINREGISTRYID" = "HETU")) %>%
  rename(DRUG_PURCHASES = drug_purchases)

# add kanta prescriptions
kanta_prescriptions <- fread(kanta_prescriptions_path) %>% as_tibble

mpf <- mpf %>%
  left_join(kanta_prescriptions, by = c("FINREGISTRYID" = "PATIENT_ID")) %>%
  rename(KANTA_PRESCRIPTIONS = kanta_prescriptions)


# add automatic date
today <- Sys.Date()
filename <- paste0("minimal_phenotype_",today,".csv")

# save 
setwd("/data/processed_data/minimal_phenotype/")
write.csv(mpf, filename, 
          row.names = FALSE)

