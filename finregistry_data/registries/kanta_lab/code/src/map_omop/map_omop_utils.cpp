#include "../header.h"

/**
 * @brief Gets the OMOP concept ID, given the laboratory source, lab ID and lab abbreviation
 * 
 * @param omop_concept_map The map of the lab IDs and abbreviations to OMOP concept IDs
 * @param omop_lab_source The laboratory source (LABfi, LABfi_HUS, LABfi_TMP, LABfi_TKU)
 * @param omop_identifier The laboratory ID and abbreviation
 * 
 * @return The OMOP concept ID
 * 
 * The laboratory source is easily determined, using the information on the 
 * lab ID source in the original data and the service provider with the function 
 * `get_omop_lab_source`.
*/
std::string get_omop_id(std::unordered_map<std::string, std::unordered_map<std::string, std::string>> &omop_concept_map,
                        std::string omop_lab_source,
                        std::string omop_identifier){
    std::string omop_id = "NA";

    // Code source is known
    if(omop_lab_source != "LABfi_NA") {
        // Checking if we also know the actual Lab ID abbreviation pair
        if(omop_concept_map[omop_lab_source].find(omop_identifier) != omop_concept_map[omop_lab_source].end()) {
            omop_id = omop_concept_map[omop_lab_source][omop_identifier];
        } else {
            omop_id = "NA";
        }
    } 
    if(omop_id == "NA") {
        // Currently using a hierarchical approach to mapping for the local codes outside of the
        // major hospitals  HUS (Helsinki), TMP (Tampere), TKU (Turku) - in that order
        if(omop_concept_map["LABfi"].find(omop_identifier) != omop_concept_map["LABfi"].end()) {
            omop_id = omop_concept_map["LABfi"][omop_identifier];
        } else if(omop_concept_map["LABfi_HUS"].find(omop_identifier) != omop_concept_map["LABfi_HUS"].end()) {
            omop_id = omop_concept_map["LABfi_HUS"][omop_identifier];
        } else if(omop_concept_map["LABfi_TMP"].find(omop_identifier) != omop_concept_map["LABfi_TMP"].end()) {
            omop_id = omop_concept_map["LABfi_TMP"][omop_identifier];
        } else if(omop_concept_map["LABfi_TKU"].find(omop_identifier) != omop_concept_map["LABfi_TKU"].end()) {
            omop_id = omop_concept_map["LABfi_TKU"][omop_identifier];
        } else {
            omop_id = "NA";
        }
    }
    return(omop_id);
}

/**
 * @brief Gets the OMOP concept name, given the OMOP concept ID
 * 
 * @param omop_id The OMOP concept ID
 * @param omop_names The map of the OMOP concept IDs to names
 * 
 * @return The OMOP concept name
*/
std::string get_omop_name(std::string omop_id,
                          std::unordered_map<std::string, std::string> &omop_names){
    std::string omop_name;
    if(omop_id == "NA") {
        omop_name = "NA";
    } else {
        if(omop_names.find(omop_id) != omop_names.end()) {
            omop_name = omop_names[omop_id];
        } else {
            omop_name = "NA";
        }
    }
    return(omop_name);
}
            
/**
 * @brief Gets the OMOP lab source based on the lab ID source and the service provider
 * 
 * @param lab_id_source The lab ID source from the original data. `0` means that the
 *                      lab ID is a local code, `1` that the lab ID is a national code.
 * @param service_provider The service provider name from the original data.
 * 
 * @return The OMOP lab source
 * 
 * The OMOP lab source is determined based on the lab ID source and the service provider.
 * It can be either LABfi, LABfi_HUS, LABfi_TMP, LABfi_TKU, or LABfi_NA. LABfi is the
 * national table, and LABfi_NA means the lab ID is a local code from a non-major hospital.
*/
std::string get_omop_lab_source(std::string lab_id_source,
                                std::string service_provider) {
    std::string lab_source;
    if(lab_id_source == "0") {
        lab_source = "LABfi";
    } else {
        if(service_provider.find("Helsinki") != std::string::npos) {
            lab_source = "LABfi_HUS";
        } else if(service_provider.find("Tampere") != std::string::npos) {
            lab_source = "LABfi_TMP";
        } else if(service_provider.find("Turku") != std::string::npos) {
            lab_source = "LABfi_TKU";
        } else {
            lab_source = "LABfi_NA";
        }
    }
    return(lab_source);
}

/**
 * @brief Reads the OMOP ID map file and adds the information to the maps
 * 
 * @param omop_concept_map_path The path to the OMOP ID map file
 * @param omop_concept_map The map of the lab IDs and abbreviations to OMOP concept IDs
 * @param omop_names The map of OMOP concept IDs to the concept names
 * 
 * @return void
 * 
 * Reads the OMOP concept ID map file. The delimiter is expected to be "\t". 
 * Expects columns: LAB_ID, LAB_SOURCE, LAB_ABBREVIATION, OMOP_UNIT, OMOP_ID, OMOP_NAME.
*/
void read_omop_file(std::string omop_concept_map_path,
                    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> &omop_concept_map,
                    std::unordered_map<std::string, std::string> &omop_names) {
    // Opening file
    std::ifstream omop_in;
    omop_in.open(omop_concept_map_path); check_in_open(omop_in, omop_concept_map_path);

    char delim = find_delim(omop_concept_map_path);

    // Reading
    std::string line;
    while(std::getline(omop_in, line)) {
        // Splitting line
        std::vector<std::string> line_vec = splitString(line, delim);
        std::string lab_id = remove_chars(line_vec[0], ' ');
        std::string source = remove_chars(line_vec[1], ' ');
        std::string abbreviation = remove_chars(line_vec[2], ' ');
        std::string unit = line_vec[3];
        std::string omop_id = remove_chars(line_vec[4], ' ');
        std::string omop_name = line_vec[5];

        // OMOP identifier is mape up of the lab ID and abbreviation
        std::string lab_id_abbrv = get_lab_id_abbrv(lab_id, abbreviation);

        // The OMOP concept ID map has separate maps for each lab source
        // LABfi, LABfi_HUS, LABfi_TMP, LABfi_TKU
        if((omop_id == "\"\"") | (omop_id == "")) omop_id = "NA";
        omop_concept_map[source][lab_id_abbrv] = omop_id;
        // The mapping to the OMOP name is unique for each group ID
        omop_names[omop_id] = omop_name;
    }

    omop_in.close();
}


/**
 * @brief Gets new OMOP mappings from file
 * 
 * @param new_omops The map from lab ID, abbreviation, and lab unit to OMOP ID
 * @param omop_names The map from OMOP ID to OMOP names
 * @param file_path The path to the file containing the new OMOP mappings
 * @param min_count The minimum number of occurrences of a lab ID, abbreviation, and unit
 * 
 * @return void
 * 
 * These mappings are based on the lab ID, abbreviation, and unit. Detects new lab IDs
 * that appear at least x times mapped to a given OMOP ID. The file is expected to have
 * the following columns: LAB_ID, LAB_ABBREVIATION, UNIT, OMOP_ID, OMOP_NAME, LAB_COUNT, OMOP_COUNT.
*/
void get_new_omop_concepts(std::unordered_map<std::string, std::string> &new_omops,
                           std::unordered_map<std::string, std::string> &omop_names,   
                           std::string file_path,
                           int min_count) {
    // Opening file
    std::ifstream in_file;
    in_file.open(file_path); check_in_open(in_file, file_path); 
    char delim = find_delim(file_path);
    
    // Reading
    std::string line;
    int first_line = 1; // Indicates header line
    while(std::getline(in_file, line)) {
        if(first_line == 1) {
            first_line = 0;
            continue;
        }
        std::vector<std::string> line_vec = splitString(line, delim);

        std::string lab_id = line_vec[0];
        std::string lab_abbrv = line_vec[1];
        std::string lab_unit = line_vec[2];
        std::string omop_id = line_vec[3];
        std::string omop_name = line_vec[4];
        int lab_count = std::stoi(line_vec[5]);
        int omop_count = std::stoi(line_vec[6]);
        // This actually needs to be fixed to lab_count, but represents the current data 
        if(omop_count >= min_count) {
            std::string omop_identifier = get_lab_id_omop_identifier(lab_id, lab_abbrv, lab_unit, delim);
            new_omops[omop_identifier] = omop_id;
            omop_names[omop_id] = omop_name;
        }
    }   

    in_file.close(); 
}