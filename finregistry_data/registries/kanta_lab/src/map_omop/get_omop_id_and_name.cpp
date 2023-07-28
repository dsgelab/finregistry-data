#include "../header.h"
/**
 * @brief Gets the OMOP concept ID, given the laboratory source, lab ID and lab abbreviation
 * 
 * @param omop_group_id_map The map of the lab IDs and abbreviations to OMOP concept IDs
 * @param omop_lab_source The laboratory source (LABfi, LABfi_HUS, LABfi_TMP, LABfi_TKU)
 * @param omop_identifier The laboratory ID and abbreviation
 * 
 * @return The OMOP concept ID
 * 
 * The laboratory source is easily determined, using the information on the 
 * lab ID source in the original data and the service provider with the function 
 * `get_omop_lab_source`.
*/
std::string get_omop_id(std::unordered_map<std::string, std::unordered_map<std::string, std::string>> &omop_group_id_map,
                        std::string omop_lab_source,
                        std::string omop_identifier){
    std::string omop_id;
    // Code source is known
    if(omop_lab_source != "LABfi_NA") {
        // Checking if we also know the actual Lab ID abbreviation pair
        if(omop_group_id_map[omop_lab_source].find(omop_identifier) != omop_group_id_map[omop_lab_source].end()) {
            omop_id = omop_group_id_map[omop_lab_source][omop_identifier];
        // Cannot map
        } else {
            omop_id = "NA";
        }
    } else {
        // Currently using a hierarchical approach to mapping for the local codes outside of the
        // major hospitals  HUS (Helsinki), TMP (Tampere), TKU (Turku) - in that order
        if(omop_group_id_map["LABfi_HUS"].find(omop_identifier) != omop_group_id_map["LABfi_HUS"].end()) {
            omop_id = omop_group_id_map["LABfi_HUS"][omop_identifier];
        } else if(omop_group_id_map["LABfi_TMP"].find(omop_identifier) != omop_group_id_map["LABfi_TMP"].end()) {
            omop_id = omop_group_id_map["LABfi_HUS"][omop_identifier];
        } else if(omop_group_id_map["LABfi_TKU"].find(omop_identifier) != omop_group_id_map["LABfi_TKU"].end()) {
            omop_id = omop_group_id_map["LABfi_HUS"][omop_identifier];
        // Cannot map
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
            