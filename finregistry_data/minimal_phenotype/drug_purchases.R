library(data.table)

# Get file paths for all files in kela_purchases directory.
directory = '/data/processed_data/kela_purchase'
file_paths = list.files(directory, full.names = T)

# Read HETU column and combine years.
data = rbindlist(lapply(file_paths, function(path) fread(path, select = c('HETU'))))

# Count purchases for each HETU (FINREGISTRYID).
drug_purchases <- unique(data[, drug_purchases := .N, by = HETU])

# Save purchases as a .csv file.
fwrite(drug_purchases, '/data/projects/mpf/mpf_create/drug_purchases.csv')
