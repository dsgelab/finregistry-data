#include "../header.h"

/***
 * @brief Reads in all previous duplines files into a map
 * 
 * @param all_dup_lines Map of all duplicate lines
 * @param file Current file number
 * @param res_path Path to results directory
 * 
 * @return void 
*/
void get_previous_dup_lines(std::unordered_map<std::string, int> &all_dup_lines, 
                            std::string file,
                            std::string res_path) {
    // For first file, nothing to read in yet
    if(file != "1") {
        int crnt_file_no = std::stoi(file);
        // Read in all previous duplines files
        for(int file_no=1; file_no < crnt_file_no; file_no++) {
            // File path
            std::vector<std::string> duplines_path_vec = {res_path, "processed/reports/problem_rows/duplines_", std::to_string(file_no), ".csv"};    
            std::string duplines_path = concat_string(duplines_path_vec, std::string(""));
            cout << duplines_path << endl;

            // Opening file
            std::ifstream duplines_file; duplines_file.open(duplines_path); check_in_open(duplines_file, duplines_path);

            // Reading in lines
            std::string line;
            while(std::getline(duplines_file, line)) {
                std::vector<std::string> line_vec = split(line, "\t");
                // Adding file specific counts
                all_dup_lines[line_vec[0]] = 0;
            }
            duplines_file.close();
        }
    }
}

/**
 * @brief Reads in THL SOTE file
 * 
 * @param thl_sote_map Reference to the map with THL SOTE service provider OIDs to the service provider names
 * @param thl_sote_path Path to THL SOTE organisations map file. First column needs to be the service provider OID and the second column the service provider name.
 * 
 * @return void
 * 
 * @details The THL SOTE map has the official organisations (service providers) OIDs as keys and readable service provider names as values. The readable service provider names are i.e. Helsinki_1301 for HUS. For what the THL SOTE organisation register is see: https://thl.fi/fi/web/tiedonhallinta-sosiaali-ja-terveysalalla/ohjeet-ja-soveltaminen/koodistopalvelun-ohjeet/sote-organisaatio-rekisteri and https://koodistopalvelu.kanta.fi/codeserver/pages/classification-view-page.xhtml?classificationKey=421&versionKey=501
*/
void read_thl_sote_map(std::unordered_map<std::string, std::string> &thl_sote_map,
                   std::string thl_sote_path) {
    // Opening file
    std::ifstream lab_file; lab_file.open(thl_sote_path); check_in_open(lab_file, thl_sote_path);

    // Reading in lines
    std::string line;
    while(std::getline(lab_file, line)) {
        std::vector<std::string> line_vec = split(line, "\t");

        std::string service_provider_name_oid = line_vec[0];
        std::string service_provider_name_name = line_vec[1];

        thl_sote_map[service_provider_name_oid] = service_provider_name_name;
    }
    lab_file.close();
}


/**
* @brief Reads in THL lab ID to THL lab value abbreviation map for the regional lab codes
* 
* @param thl_abbrv_map Reference to the map with THL lab ID to THL lab value abbreviation map
* @param thl_abbrv_path Path to THL lab ID to THL lab value abbreviation map file. First column needs to be the lab ID and the second column the lab value abbreviation.
*
* @return void
* 
* @details The THL lab ID to THL lab value abbreviation map has the lab IDs as keys and the lab value abbreviations as values. The lab IDs are i.e. 1301 for p-Krea (this is a fake example).For more information see: https://koodistopalvelu.kanta.fi/codeserver/pages/classification-view-page.xhtml?classificationKey=88&versionKey=120

**/
void read_thl_lab_id_abbrv_map(std::unordered_map<std::string, std::string> &thl_abbrv_map,
                      std::string thl_abbrv_path) {
    // Opening file
    std::ifstream abbrv_file; abbrv_file.open(thl_abbrv_path); check_in_open(abbrv_file, thl_abbrv_path);

    // Reading in lines
    std::string line;
    while(std::getline(abbrv_file, line)) {
        std::vector<std::string> line_vec = split(line, "\t");

        std::string lab_id = line_vec[0];
        std::string lab_abbrv = line_vec[1];

        thl_abbrv_map[lab_id] = lab_abbrv;
    }
    abbrv_file.close();
}


std::vector<std::string> read_correct_lines(std::string &line,
                                            unsigned long long &total_line_count,
                                            unsigned long long &skip_count,
                                            std::ofstream &error_file) {
    int n_cols(25);
    const char *delim = ";";
    int lines_valid_status;
    std::vector<std::string> new_line_vec;

    /// LINE VECTORS
    std::vector<std::string> final_line_vec(25);
    // Split values and copy into line vector
    std::vector<std::string> line_vec(split(line, delim));   

    // Seemingly correctly defined line
    if(int(line_vec.size()) == n_cols) {
        // Can savely copy into the final line vector
        std::copy(line_vec.begin(), line_vec.end(), final_line_vec.begin());
        // Line is valid
        lines_valid_status = 0;

    // TOO MANY COLUMNS, can't fix at the moment. Line invalid.
    } else if(int(line_vec.size()) > n_cols) {
        lines_valid_status = 1;
        
    // TOO FEW COLUMNS, fixing if early line break i.e. "B-Lym\nf"
    } else if(int(line_vec.size()) < n_cols)  {
        // Getting next line
        std::string new_line;
        std::getline(std::cin, new_line); 
        ++total_line_count;
        new_line_vec = split(new_line, delim);
    // Checking that new line has too few columns also -> likely a continuation of the previous line
    if(int(new_line_vec.size()) < n_cols) {
        // Concatinating back last element of previous line with first of new line
        std::string new_name = concat_string(std::vector<std::string> {line_vec[line_vec.size()-1], new_line_vec[0]});
        line_vec.at(line_vec.size()-1) =  new_name;

        // Concatinating the two line vectors
        line_vec.insert(line_vec.end(), next(new_line_vec.begin()), new_line_vec.end());

        // Concatination gives reasonable line. Line is valid, using it.
        if(int(line_vec.size()) == n_cols) {
            std::copy(line_vec.begin(), line_vec.end(), final_line_vec.begin());
            // Line(s) is valid
            lines_valid_status = 0;
        
        // Concatination does not give us a valid line. Both are invalid. 
        } else {
            lines_valid_status = 2;
        }
        // New line is actually a full line. Line is invalid. Newline is valid, using it. 
        } else if(int(new_line_vec.size()) == n_cols) { 
            // Copping new line into the final line vector
            std::copy(new_line_vec.begin(), new_line_vec.end(), final_line_vec.begin());
            // Line invalid, new line valid
            lines_valid_status = 3;
        // Both lines are invalid.
        } else {
            lines_valid_status = 2;
        }
    } 


    /// Writing lines to error files
    // Line is invalid
    if((lines_valid_status == 1) | (lines_valid_status == 3)) {
        error_file << concat_string(line_vec, ";") << "\n";
        ++skip_count;
    }  
    // Newline is also invalid
    if(lines_valid_status == 2) {
        error_file <<  concat_string(new_line_vec, ";") << "\n";
    }
    return final_line_vec;
}

/**
 * @brief Fixes the NA indicators in the line vector with NAs
 * 
 * @param final_line_vec Reference to the line vector with the line as vector elements
 * 
 * @return void
 * 
 * @details Different NA indicators are Puuttuu, "", TYHJÄ, _, -1 (except in value column)
*/
void fix_nas(std::vector<std::string> &final_line_vec) {
    int n_cols(25);
    // Replacing different NA indicators with NA
    for(int elem_idx=0; elem_idx < n_cols; elem_idx++) {
        // Replacing NAs
        if((final_line_vec[elem_idx] == "Puuttuu") |
            (final_line_vec[elem_idx] == "\"\"") | 
            (final_line_vec[elem_idx] == "TYHJÄ") | 
            (final_line_vec[elem_idx] == "_") |
            ((final_line_vec[elem_idx] == "-1") & (elem_idx != 19))) { // -1 in value not considered NA
            final_line_vec[elem_idx] = "NA";
            }
    }
}

/**
 * @brief Returns the service provider name for the service provider OID
 * 
 * @param thl_sote_map Reference to the unordered map with service provider OIDs as keys and service provider names as values
 * @param service_provider_oid Reference to the service provider OID
 * 
 * @return std::string The service provider name
*/
std::string get_service_provider_name(std::unordered_map<std::string, std::string> &thl_sote_map,
                               std::string &service_provider_oid) {
    std::string service_provider_name;
    // Mapping laboratory IDs to laboratory names
    if(thl_sote_map.find(service_provider_oid) != thl_sote_map.end()) {
        service_provider_name = thl_sote_map[service_provider_oid];
    } else {
        service_provider_name = "NA";
    }
    return(service_provider_name);
}

/**
 * @brief Sets the laboratory ID and laboratory ID source, depending on the data
 * 
 * @param local_lab_id Reference to the local laboratory value ID
 * @param thl_lab_id Reference to the finland wide THL laboratory value ID
 * @param lab_id Reference to the final unified laboratory value ID
 * @param lab_id_source Reference to the source of the final unified laboratory value ID. 0 = local, 1 = THL.
 * 
 * @return void
 * 
 * @details The data contains both local laboratory value IDs used by the service providers and finland wide THL IDs. This merges the two into one laboratory value ID. Denotes the source of the laboratory value ID with the lab_id_source variable.
*/
void get_lab_id_and_source(std::string &local_lab_id,
                           std::string &thl_lab_id,
                           std::string &lab_id,
                           std::string &lab_id_source) {
    // We would prefer the finland wide THL ID
    if(thl_lab_id == "NA") {
        lab_id = local_lab_id;
        lab_id_source = "0";
    } else {
        lab_id = thl_lab_id;
        lab_id_source = "1";
    }
}

/**
 * @brief Returns the laboratory abbreviation for the laboratory ID
 * 
 * @param thl_abbrv_map Reference to the unordered map with THL laboratory IDs as keys and laboratory abbreviations as values
 * @param lab_id Reference to the laboratory ID
 * @param lab_id_source Reference to the source of the laboratory ID. 0 = local, 1 = THL.
 * @param lab_name Reference to the laboratory name in the data
 * 
 * @return std::string The laboratory abbreviation
 * 
 * @details If the laboratory ID is the local code, returns the abbreviation from the data. If the labroatory ID is a regional THL code, returns the abbreviation from the THL abbreviation map. If the laboratory ID is not found in the THL abbreviation map, returns "NA".
*/
std::string get_lab_abbrv(std::unordered_map<std::string, std::string> thl_abbrv_map,
                          std::string &lab_id,
                          std::string &lab_id_source,
                          std::string &lab_name) {
    std::string lab_abbrv;
    if(lab_id_source == "0") {
        lab_abbrv = lab_name;
    } else {
        // Mapping lab IDs to abbreviations
        if(thl_abbrv_map.find(lab_id) != thl_abbrv_map.end()) {
            lab_abbrv = thl_abbrv_map[lab_id];
        } else {
            lab_abbrv = "NA";
        }    
    return(lab_abbrv);
}

void write_row_count_report(std::string &report_path,
                            unsigned long long &total_line_count,
                            unsigned long long &valid_line_count,
                            unsigned long long &skip_count,
                            unsigned long long &dup_count,
                            unsigned long long &na_count) {
    // Opening 
    std::ofstream report_file;
    report_file.open(report_path); check_out_open(report_file, report_path);

    // Writing 
    report_file << "All rows: " << total_line_count << "\n";
    report_file << "Usable rows: " << valid_line_count << "\n";
    report_file << "Skipped rows: " << skip_count << "\n";
    report_file << "Duplicate rows: " << dup_count << "\n";
    report_file << "Missing value rows: " << na_count << "\n";
    report_file << endl;

    // Closing
    report_file.close();  
}

void write_dup_lines_file(std::string &res_path,
                          std::string &file,
                          std::string &report_path,
                          std::ofstream &report_file,
                          std::unordered_map<std::string, int> &all_dup_lines) {
    // File paths
    std::vector<std::string> duplines_path_vec = {res_path, "processed/reports/problem_rows/", "duplines_", file, ".csv"};    
    std::string duplines_path = concat_string(duplines_path_vec, std::string(""));

    // Opening
    std::ofstream duplines_file;
    duplines_file.open(duplines_path); check_out_open(duplines_file, duplines_path); 

    // Writing
    for(const std::pair<const std::string, int>& elem: all_dup_lines) {
        if(elem.second != 0) {
            duplines_file << elem.first << "\t" << elem.second << "\n";
        }
    }

    // Closing
    duplines_file.close();
}