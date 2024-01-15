FLAGS = -std=c++17 -static -Wall

## Minimal
minimal: bin/minimal_main.o bin/file_helpers.o bin/string_helpers.o  bin/minimal_utils.o
	g++ $(FLAGS) bin/minimal_main.o bin/file_helpers.o bin/string_helpers.o bin/minimal_utils.o -o ../upload/exec/minimal

bin/minimal_main.o: src/minimal/minimal_main.cpp
	$(info Buildung Main minimal...)  g++ -c $(FLAGS) -o bin/minimal_main.o src/minimal/minimal_main.cpp

bin/minimal_utils.o: src/minimal/minimal_utils.cpp
	$(info Buildung Main minimal...)  g++ -c $(FLAGS) -o bin/minimal_utils.o src/minimal/minimal_utils.cpp

## Mapping OMOP
map_omop: bin/main_map_omop.o bin/file_helpers.o bin/string_helpers.o bin/map_omop_utils.o 
	g++ $(FLAGS) bin/main_map_omop.o bin/file_helpers.o bin/string_helpers.o bin/map_omop_utils.o -o ../upload/exec/map_omop

bin/main_map_omop.o: src/map_omop/map_omop_main.cpp
	$(info Buildung Main map_omop...)  g++ -c $(FLAGS) -o bin/main_map_omop.o src/map_omop/map_omop_main.cpp 

bin/map_omop_utils.o: src/map_omop/map_omop_utils.cpp
	$(info Buildung map_omop_utils...)  g++ -c $(FLAGS) -o bin/map_omop_utils.o src/map_omop/map_omop_utils.cpp

## HELPERS
bin/string_helpers.o: src/string_helpers.cpp
	$(info Buildung String Helpers...)  g++ -c $(FLAGS) -o bin/string_helpers.o src/string_helpers.cpp

bin/file_helpers.o: src/file_helpers.cpp
	$(info Buildung File Helpers...)  g++ -c $(FLAGS) -o bin/file_helpers.o src/file_helpers.cpp

# Add OMOP Map
run_map_omop: ../upload/exec/map_omop
	cat /home/kira/duni/helsinki/DSGE/Code/kanta_lab/code/tests/processed/data/all_minimal.csv | ../upload/exec/map_omop tests/ /home/kira/duni/helsinki/DSGE/Code/kanta_lab/code/tests/test_data/omop_group_id_map.csv /home/kira/duni/helsinki/DSGE/Code/kanta_lab/code/tests/test_data/omop_names.csv

# Final Fixing
final_fixing: bin/final_fixing_main.o bin/file_helpers.o bin/string_helpers.o  bin/final_fixing_utils.o
	g++ $(FLAGS) bin/final_fixing_main.o bin/file_helpers.o bin/string_helpers.o bin/final_fixing_utils.o -o ../upload/exec/final_fixing

bin/final_fixing_main.o: src/final_fixing/final_fixing_main.cpp
	$(info Buildung Main final_fixing_main...)  g++ -c $(FLAGS) -o bin/final_fixing_main.o src/final_fixing/final_fixing_main.cpp

bin/final_fixing_utils.o: src/final_fixing/final_fixing_utils.cpp
	$(info Buildung Main final_fixing_utils...)  g++ -c $(FLAGS) -o bin/final_fixing_utils.o src/final_fixing/final_fixing_utils.cpp

## Create lab OMOP maps
create_lab_omop_map_overview: bin/create_lab_omop_map_overview_main.o bin/file_helpers.o bin/string_helpers.o
	g++ $(FLAGS) bin/create_lab_omop_map_overview_main.o bin/file_helpers.o bin/string_helpers.o -o  ../upload/exec/create_lab_omop_map_overview

bin/create_lab_omop_map_overview_main.o: src/sumstats/create_lab_omop_map_overview_main.cpp
	$(info Buildung Main omop_sumstats...)  g++ -c $(FLAGS) -o bin/create_lab_omop_map_overview_main.o src/sumstats/create_lab_omop_map_overview_main.cpp

## All Labs Main
learn_lab_omop_map: bin/learn_lab_omop_map_main.o bin/file_helpers.o bin/string_helpers.o
	g++ $(FLAGS) bin/learn_lab_omop_map_main.o bin/file_helpers.o bin/string_helpers.o -o  ../upload/exec/learn_lab_omop_map

bin/learn_lab_omop_map_main.o: src/sumstats/learn_lab_omop_map_main.cpp
	$(info Buildung Main omop_sumstats...)  g++ -c $(FLAGS) -o bin/learn_lab_omop_map_main.o src/sumstats/learn_lab_omop_map_main.cpp

## Adding new omop concepts
add_omop_concepts: bin/add_omop_concepts_main.o bin/file_helpers.o bin/string_helpers.o bin/map_omop_utils.o 
	g++ $(FLAGS) bin/add_omop_concepts_main.o bin/file_helpers.o bin/string_helpers.o bin/map_omop_utils.o -o ../upload/exec/add_omop_concepts

bin/add_omop_concepts_main.o: src/map_omop/add_omop_concepts_main.cpp 
	$(info Buildung Main add_omop_concepts...)  g++ -c $(FLAGS) -o bin/add_omop_concepts_main.o src/map_omop/add_omop_concepts_main.cpp

## OMOP Sumstats
omop_sumstats: bin/omop_sumstats_main.o bin/file_helpers.o bin/string_helpers.o bin/sumstats_utils.o
	g++ $(FLAGS) bin/omop_sumstats_main.o bin/file_helpers.o bin/string_helpers.o bin/sumstats_utils.o -o ../upload/exec/omop_sumstats

bin/omop_sumstats_main.o: src/sumstats/omop_sumstats_main.cpp
	$(info Buildung Main omop_sumstats...)  g++ -c $(FLAGS) -o bin/omop_sumstats_main.o src/sumstats/omop_sumstats_main.cpp

bin/sumstats_utils.o: src/sumstats/sumstats_utils.cpp
	$(info Buildung Main omop_sumstats...)  g++ -c $(FLAGS) -o bin/sumstats_utils.o src/sumstats/sumstats_utils.cpp