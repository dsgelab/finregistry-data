#include "../header.h"

/**
 * @brief Maps OMOP Concept IDs and names to the minimal data
 * 
 * @param argc The number of arguments
 * @param argv The arguments
 * 
 * @return void
 * 
 * Maps the OMOP concetps IDs when both the lab ID and abbreviation map. 
 * We can map about 60% of the local lab codes this way
 * 
 * Reads in the minimal data from stdin. The delimiter is expected to be ";"
 * Expects the columns to be:
 * - FINREGISTRYID
 * - DATE_TIME
 * - SERVICE_PROVIDER
 * - LAB_ID
 * - LAB_ID_SOURCE
 * - LAB_ABBREVIATION
 * - LAB_VALUE
 * - LAB_UNIT
 * - LAB_ABNORMALITY
 * The column names are irrelevant but they need to be in the correct order.
 * 
 * The lab ID and abbreviations are mapped to the correct source table, if possible and 
 * otherwise hierarchical to the best matching source table. The four tables are
 * LABfi the nation wide table, LABfi_HUS the HUS table, LABfi_TMP the Tampere table, and
 * LABfi_TKU the Turku table. The hierarchy for local lab IDs from non-major hospitals is 
 * HUS, TMP, TKU.
 * 
 * Expects the following commandline arguments:
 *  - res_path: The path to the results directory
 *  - omop_group_id_map_path: The path to the OMOP group ID map. 
 *      Mapping from lab IDs and abbreviations to OMOP group IDs. The delimiter is expected
 *      to be "\t". Expects columns: LAB_ID, LAB_SOURCE, LAB_ABBREVIATION, UNIT, OMOP_ID, NAME. 
 *      The columns names are irrelevant but they need to be in the correct order. 
 *      LAB_SOURCE is either LABfi, LABfi_HUS, LABfi_TMP, LABfi_TKU.
**/
int main(int argc, char *argv[]) {
    // Arguments
    std::string res_path = argv[1];
    std::string omop_group_id_map_path = argv[2];

    // Results File
    std::vector<std::string> full_res_path_vec = {res_path, "processed/data/kanta_lab_minimal_omop.csv"};    
    std::string full_res_path = concat_string(full_res_path_vec, std::string(""));
    std::ofstream res_file;
    res_file.open(full_res_path); check_out_open(res_file, full_res_path); 

    // OMOP Maps
    // The OMOP group ID has separate maps for each lab source
    // LABfi, LABfi_HUS, LABfi_TMP, LABfi_TKU
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> omop_group_id_map;
    // The mapping to the OMOP name is unique for each group ID
    std::unordered_map<std::string, std::string> omop_names;
    // Reading in OMOP map from file
    read_omop_file(omop_group_id_map_path, omop_group_id_map, omop_names);

    // Flag for first line
    int first_line = 1;

    // Reading
    std::string line;
    while(std::getline(std::cin, line)) {
        if(first_line == 1) {
            // Column headers
            res_file << "FINREGISTRYID;DATE_TIME;SERVICE_PROVIDER;LAB_ID;LAB_ID_SOURCE;LAB_ABBREVIATION;LAB_VALUE;LAB_UNIT;LAB_ABNORMALITY;OMOP_ID;OMOP_NAME" << "\n";
            first_line = 0;
            continue;
        }

        // Splitting line
        std::vector<std::string> line_vec = split(line, ";");
        std::string finregistryid = line_vec[0];
        std::string date_time = line_vec[1];
        std::string service_provider = line_vec[2];
        std::string lab_id = line_vec[3];
        std::string lab_id_source = line_vec[4];
        std::string lab_abbreviation = line_vec[5];
        std::string lab_value = line_vec[6];
        std::string lab_unit = line_vec[7];
        std::string lab_abnormality = line_vec[8];  

        // Getting current lab source (LABfi, LABfi_HUS, LABfi_TMP, LABfi_TKU)
        std::string omop_lab_source = get_omop_lab_source(lab_id_source, service_provider);
  
        // Finding OMOP mapping
        // Currently identifying the OMOP concept by the lab ID and abbreviation.
        // We can map about 60% of the local lab codes this way
        std::string omop_identifier = concat_string({lab_id, lab_abbreviation}, " ");
        std::string omop_id = get_omop_id(omop_group_id_map, omop_lab_source, omop_identifier);
        std::string omop_name = get_omop_name(omop_id, omop_names);

        // Writing to results file
        res_file << finregistryid  << ";" <<  date_time << ";" << service_provider << ";" << lab_id << ";" << lab_id_source << ";" << lab_abbreviation << ";" << lab_value << ";" << lab_unit << ";" <<  lab_abnormality << ";" << omop_id << ";" << omop_name << "\n";
    }

    res_file.close(); 
}

              
