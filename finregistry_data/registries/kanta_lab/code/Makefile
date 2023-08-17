orig_data_dir = "data/kanta_lab_20233001/"
res_dir = "detrokir/"

# These are provided in the data folder
thl_sote_map_path = "data/thl_sote_map_named.tsv"
thl_lab_map_path = "data/thl_lab_id_abbrv_map.csv"
omop_map_path = "data/omop_concept_map.tsv"

run_all:
	mkdir -p $(res_dir)processed/data
	mkdir -p $(res_dir)processed/reports/problem_rows
	mkdir -p $(res_dir)processed/counts/row_counts

	make create_minimal
	make concat_files
	make compress_files
	make map_omop
	zstd -v -T24 --ultra -22 --rm $(res_dir)processed/data/kanta_lab_minimal_omop.csv
	python3.9 code/exec/unit_fixing.py $(res_dir)
	make final_fixing
	cat $(res_dir)processed/data/kanta_lab_final.csv | awk '{FS=";", OFS=""}{if(NR>1){print $1, ",", $2, ",", $3, ",", "\"", $4, "\",", $5, ",", "\"", $6, "\",", $7, ",", $8, ",", $9, "," $10, "," $11} else {print "FINREGISTRYID,LAB_DATE_TIME,LAB_SERVICE_PROVIDER,LAB_ID,LAB_ID_SOURCE,LAB_ABBREVIATION,LAB_VALUE,LAB_UNIT,LAB_ABNORMALITY,OMOP_ID,OMO_NAME"}}' > $(res_dir)processed/data/kanta_lab_2023-08-14.csv
	rm $(res_dir)processed/data/kanta_lab_2023-08-14.csv.zst
	rm  $(res_dir)processed/data/kanta_lab_final.csv 
	zstd -v -T24 --ultra -22 $(res_dir)processed/data/kanta_lab_2023-08-14.csv.zst

create_minimal: 
	for file_no in 1 2 3 4 5 6 7 8 9 10 ; do \
		echo "Reading file $$file_no" ; \
		zstdcat $(orig_data_dir)"finregistry_$$file_no.csv.finreg_IDs.zst" code/exec/minimal $(res_dir) $$file_no $(thl_sote_map_path) $(thl_lab_map_path) ; \
	done 

concat_files:
	cat $(res_dir)processed/data/minimal_file_1.csv | awk -F ";" -f code/exec/concat_files_head.awk > $(res_dir)processed/data/kanta_lab_minimal.csv ; \
	for file_no in 2 3 4 5 6 7 8 9 10 ; do \
		cat $(res_dir)"processed/data/minimal_file_$$file_no.csv" | awk -F ";" -f code/exec/concat_files.awk >> $(res_dir)processed/data/kanta_lab_minimal.csv ; \
	done

compress_files:
	for file_no in 1 2 3 4 5 6 7 8 9 10 ; do \
		rm -f $(res_dir)"processed/data/minimal_file_$$file_no.csv.zst" ; \
		zstd -v -T24 --ultra -22 --rm $(res_dir)"processed/data/minimal_file_$$file_no.csv" ; \
		rm -f $(res_dir)"processed/reports/problem_rows/duplines_$$file_no.csv.zst" ; \
		zstd -v -T24 --ultra -22 --rm $(res_dir)"processed/reports/problem_rows/duplines_$$file_no.csv" ; \
		rm -f $(res_dir)"processed/reports/problem_rows/problem_rows_file_$$file_no.csv.zst" ; \
		zstd -v -T24 --ultra -22 --rm $(res_dir)"processed/reports/problem_rows/problem_rows_file_$$file_no.csv" ; \
	done
	rm -f $(res_dir)processed/data/kanta_lab_minimal.csv.zst

map_omop:
	cat $(res_dir)processed/data/kanta_lab_minimal.csv | code/exec/map_omop $(res_dir) $(omop_map_path) 
	rm -f $(res_dir)processed/data/kanta_lab_minimal.csv

final_fixing:
	cat $(res_dir)processed/data/kanta_lab_minimal_fixed_units.csv | code/exec/final_fixing $(res_dir)
	rm -f $(res_dir)processed/data/kanta_lab_minimal_fixed_units.csv
