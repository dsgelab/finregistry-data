library(data.table)
library(feather)
library(dplyr)
library(tibble)
# Open mpf file
mpf = fread('/data/projects/mpf/mpf_create/minimal_phenotype_main_032022.csv')

# Save important values for easy access
row_count = nrow(mpf)
colnames = colnames(mpf)
na_counts = colSums(is.na(mpf))

# Generate dictionary from column names and count NA values in each column
data_dict = tibble(column_name = colnames(mpf), missing_count = colSums(is.na(mpf)))

# Calculate percentage of NA values in each colun
data_dict = data_dict %>% mutate(missing_pct = 100 * missing_count / row_count)

# Select columns that are numeric for further calculations
mpf_numerics = mpf %>% select_if(is.numeric)

# Calculate min and max value in each column containing numerical values
mins = mpf_numerics %>% summarise_all(~ min(., na.rm = TRUE)) %>% unlist(.)
maxs = mpf_numerics %>% summarise_all(~ max(., na.rm = TRUE)) %>% unlist(.)

# Calculate unique values in each column
uniques = mpf %>% summarise_all(~ n_distinct(., na.rm = TRUE)) %>% unlist(.)
# Get type of values in each column
types = mpf %>% slice(1) %>% summarise_all(~ typeof(.)) %>% unlist(.)

# Transpose dictionary
data_dict = data_dict %>%
  left_join(rownames_to_column(data.frame(types)), by = c('column_name' = 'rowname')) %>%
  left_join(rownames_to_column(data.frame(uniques)), by = c('column_name' = 'rowname')) %>%
  left_join(rownames_to_column(data.frame(mins)), by = c('column_name' = 'rowname')) %>%
  left_join(rownames_to_column(data.frame(maxs)), by = c('column_name' = 'rowname')) %>%
  rename(min = mins, max = maxs, type = types)  

# Save data dictionary
fwrite(data_dict, file = '/data/projects/mpf/mpf_create/mpf_data_dict.csv')
