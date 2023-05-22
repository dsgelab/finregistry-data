#include "../header.h"

/**
 * @brief Reads the OMOP ID map file and adds the information to the maps
 * 
 * @param omop_group_id_map_path The path to the OMOP ID map file
 * @param omop_group_id_map The map of the lab IDs and abbreviations to OMOP concept IDs
 * @param omop_names The map of OMOP group IDs to the concept names
 * 
 * @return void
 * 
 * Reads the OMOP group ID map file. The delimiter is expected to be "\t". 
 * Expects columns: LAB_ID, LAB_SOURCE, LAB_ABBREVIATION, OMOP_UNIT, OMOP_ID, OMOP_NAME.
*/
void read_omop_file(std::string omop_group_id_map_path,
                    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> &omop_group_id_map,
                    std::unordered_map<std::string, std::string> &omop_names) {
    // Opening file
    std::ifstream omop_in;
    omop_in.open(omop_group_id_map_path); check_in_open(omop_in, omop_group_id_map_path);
    
    // Reading
    std::string line;
    while(std::getline(omop_in, line)) {
        // Splitting line
        
        std::vector<std::string> line_vec = split(line, "\t");
        std::string lab_id = line_vec[0];
        std::string source = line_vec[1];
        std::string abbreviation = line_vec[2];
        std::string unit = line_vec[3];
        std::string group_id = line_vec[4];
        std::string name = line_vec[5];

        // OMOP identifier is mape up of the lab ID and abbreviation
        std::string omop_identifier = concat_string({lab_id, abbreviation}, " ");

        // The OMOP group ID has separate maps for each lab source
        // LABfi, LABfi_HUS, LABfi_TMP, LABfi_TKU
        omop_group_id_map[source][omop_identifier] = group_id;
        // The mapping to the OMOP name is unique for each group ID
        omop_names[group_id] = name;
    }

    omop_in.close();
}