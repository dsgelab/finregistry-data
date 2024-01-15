# Data processing pipeline for Kanta lab data

# Change these paths to match your system
orig_data_dir = /data/original_data/kela_lab/
res_dir = /home/kdetrois/projects/kanta_lab_processing/
date = v2_2023-12-12

# These are provided in the data folder
thl_sote_map_path = data/thl_sote_map_named.tsv
thl_lab_map_path = data/thl_lab_id_abbrv_map.csv
omop_map_path = data/omop_concept_map.tsv
new_omop_map_path = data/new_omop_mappings.tsv

# For summary statistics
sumstats_res_path = $(res_dir)processed/sumstats/kanta_lab_$(date)
# For adding new OMOP mappings
min_count_for_new_omops = 1000

run_all:
	# Prepare directories
	mkdir -p $(res_dir)processed/data
	mkdir -p $(res_dir)processed/reports/problem_rows
	mkdir -p $(res_dir)processed/reports/counts/row_counts
	mkdir -p $(res_dir)processed/sumstats/

	# Initial file processing
	make create_minimal
	make concat_files
	make compress_files

	# OMOP mapping and fixing
	make map_omop
	make fix_units
	make final_fixing

	# Creating summary statistics, round 1
	make create_lab_omop_map_overview
	make learn_lab_omop_map
	make add_new_omop_concepts

	# Creating final summary statistics
	make omop_sumstats

# Selects relevant columns/info, removes duplicates and fully missing data rows
create_minimal: 
	for file_no in 1 2 3 4 5 6 7 8 9 10 ; do \
		echo "Processing file $$file_no" $(orig_data_dir)"finregistry_$$file_no.csv.finreg_IDs"; \
		cat $(orig_data_dir)"finregistry_$$file_no.csv.finreg_IDs" | exec/minimal $(res_dir) $$file_no $(date) $(thl_sote_map_path) $(thl_lab_map_path) False; \
	done 

# Gather data from the original files into a single file
concat_files:
	cat $(res_dir)processed/data/kanta_lab_file_1_$(date).tsv | awk -F "," -f exec/concat_files_head.awk > $(res_dir)processed/data/kanta_lab_$(date)_minimal.tsv ; \
	for file_no in 2 3 4 5 6 7 8 9 10 ; do \
		cat $(res_dir)"processed/data/kanta_lab_file_$$file_no"_$(date).tsv | awk -F "," -f exec/concat_files.awk >> $(res_dir)processed/data/kanta_lab_$(date)_minimal.tsv ; \
	done

# Adds mapping of OMOP concept IDs, based on the THL-SOTE mapping using lab ID and abbreviation
map_omop:
	cat $(res_dir)processed/data/kanta_lab_$(date)_minimal.tsv | exec/map_omop $(res_dir) $(omop_map_path) $(date)
	rm -f $(res_dir)processed/data/kanta_lab_$(date)_minimal.tsv

# Fixes units using regex
fix_units:
	python3.9 exec/unit_fixing.py $(res_dir) $(res_dir)processed/data/kanta_lab_$(date)_omop.tsv $(date)

# Fixes remaining issues
final_fixing:
	cat $(res_dir)processed/data/kanta_lab_$(date)_fixed_units.tsv | exec/final_fixing $(res_dir) $(date)
	rm -f $(res_dir)processed/data/kanta_lab_$(date)_fixed_units.tsv

# Creates overview of lab ID, abbreviation and unit mapped to each OMOP as well as those not yet mapped
create_lab_omop_map_overview:
	cat $(res_dir)processed/data/kanta_lab_$(date)_final_fix.tsv | exec/create_lab_omop_map_overview $(sumstats_res_path)

# Learns potential new OMOP mappings for lab IDs not yet mapped, but known abbreviation and unit
learn_lab_omop_map:
	exec/learn_lab_omop_map $(sumstats_res_path)

# Adds new OMOP mappings to the data
add_new_omop_concepts:
	cat $(res_dir)processed/data/kanta_lab_$(date)_final_fix.tsv | exec/add_omop_concepts $(sumstats_res_path)_new_omop_candidates.tsv $(res_dir) $(date) $(min_count_for_new_omops)
	
# Creates summary statistics for each OMOP concept and unit combinations
omop_sumstats:
	cat $(res_dir)processed/data/kanta_lab_$(date)_new_omop.tsv | exec/omop_sumstats $(res_dir) $(date)