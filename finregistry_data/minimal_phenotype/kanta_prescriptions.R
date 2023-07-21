library(data.table)

# Get file paths for all kanta prescription files in kela_kanta directory.
directory = '/data/processed_data/kela_kanta'
file_paths = list.files(directory, full.names = T, pattern = 'prescriptions*')

# Read PATIENT_ID column and combine years.
data = rbindlist(lapply(file_paths, function(path) fread(path, select = c('PATIENT_ID'))))

# Count prescriptions for each PATIENT_ID (FINREGISTRYID).
kanta_prescriptions <- unique(data[, kanta_prescriptions := .N, by = PATIENT_ID])

# Save prescriptions as a .csv file.
fwrite(kanta_prescriptions, '/data/projects/mpf/mpf_create/kanta_prescriptions.csv')
