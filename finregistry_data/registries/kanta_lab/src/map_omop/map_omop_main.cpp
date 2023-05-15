#include "../header.h"

int main(int argc, char *argv[]) {
    std::string res_path = argv[1];
    std::string omop_group_id_map_path = argv[2];
    // Out File
    std::vector<std::string> full_res_path_vec = {res_path, "processed/data/", "all_minimal_omop.csv"};    
    std::string full_res_path = concat_string(full_res_path_vec, std::string(""));


    // OMOP Maps
    std::unordered_map<std::string, std::string> omop_group_id_map;
    std::unordered_map<std::string, std::string> omop_lab_id_map;
    std::unordered_map<std::string, std::string> omop_units;
    std::unordered_map<std::string, std::string> omop_names;
    read_omop_file(omop_group_id_map_path, omop_group_id_map, omop_lab_id_map, omop_units, omop_names);

    std::ofstream res_file;
    res_file.open(full_res_path); check_out_open(res_file, full_res_path); 
    // Counts
    int first_line = 1;


    // Lines
    std::string line;

    // In
    while(std::getline(std::cin, line)) {
        if(first_line == 1) {
            res_file << "FINREGISTRYID;DATE_TIME;SERVICE_PROVIDER;LAB_ID;LAB_ID_SOURCE;LAB_ABBREVIATION;LAB_VALUE;LAB_UNIT;LAB_ABNORMALITY;OMOP_ID;OMOP_NAME;OMOP_UNIT" << "\n";
            first_line = 0;
            continue;
        }
        // 0: FINREGISTRYID, 1: DATE, 2: LAB_NAME, 3: ID, 4: ID_SOURCE, 5: NAME, 6: ABBREVIATION, 7: VALUE, 8: UNIT, 9: ABNORMALITY
        std::vector<std::string> line_vec = split(line, ";");

        // Finding OMOP mapping
        std::string omop_group_id;
        std::string omop_name;
        std::string omop_unit;
        std::string lab_abbreviation;
        if(line_vec[4] == "0") {
            lab_abbreviation = line_vec[5];
        } else {
            lab_abbreviation = line_vec[6];
        }
        std::cout << lab_abbreviation << "\n";
        if(omop_group_id_map.find(lab_abbreviation) != omop_group_id_map.end()) {
            omop_group_id = omop_group_id_map[lab_abbreviation];
            if(omop_group_id != "NA") {
                omop_name = omop_names[omop_group_id];
                omop_unit = omop_units[omop_group_id];
            } else {
                omop_name = "NA";
                omop_unit = "NA";
            }
        } else {
            omop_group_id = "NA";
            omop_name = "NA";
            omop_unit = "NA";
        }



        // Writing to file
        res_file << line_vec[0] << ";" << line_vec[1] << ";" << line_vec[2] << ";" << line_vec[3] << ";" << lab_abbreviation << ";" << line_vec[4] << ";" << line_vec[7] << ";" << line_vec[8] << ";" << line_vec[9] << ";" << omop_group_id << ";" << omop_name << ";" << omop_unit << "\n";
    }

    res_file.close(); 
}