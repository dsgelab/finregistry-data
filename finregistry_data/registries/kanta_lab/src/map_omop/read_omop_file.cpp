#include "../header.h"

void read_omop_file(std::string omop_group_id_map_path,
                    std::unordered_map<std::string, std::string> &omop_group_id_map,
                    std::unordered_map<std::string, std::string> &omop_lab_id_map,
                    std::unordered_map<std::string, std::string> &omop_units,
                    std::unordered_map<std::string, std::string> &omop_names) {
    std::ifstream omop_in;
    std::string line;

    omop_in.open(omop_group_id_map_path); check_in_open(omop_in, omop_group_id_map_path);
    while(std::getline(omop_in, line)) {
        std::vector<std::string> line_vec = split(line, "\t");
        std::string lab_id = line_vec[0];
        std::string source = line_vec[1];
        std::string abbreviation = line_vec[2];
        std::string unit = line_vec[3];
        std::string group_id = line_vec[4];
        std::string name = line_vec[5];
        // LAB_ID, SOURCE, ....., OMOP_ID
        omop_group_id_map[abbreviation] = group_id;
        omop_lab_id_map[abbreviation] = lab_id;
        omop_names[group_id] = name;
        omop_units[group_id] = unit;
    }

    omop_in.close();
}