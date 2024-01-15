#include "../header.h"


/**
 * @brief Learns new Lab IDs for lab abbreviations and units already mapped to an OMOP ID
 * 
 * @param new_omop_candidates The map to store the new OMOP candidates "lab_id;lab_abbrv;lab_unit;omop_id;omop_name" -> count
 * @param lab_data The map containing the lab data "lab_id;lab_abbrv;lab_unit;omop_id;omop_name" -> count
 * @param omop_mapped_data The map containing the OMOP mapped data "lab_abbrv;lab_unit" -> "omop_id;omop_name"
 * 
 * @return void
*/
void find_new_omop_candidates(std::unordered_map<std::string, int> &new_omop_candidates, 
                              std::unordered_map<std::string, int> &lab_data, 
                              std::unordered_map<std::string, std::string> &omop_mapped_data,
                              std::unordered_set<std::string> &duplicate_mappings,
                              char delim) {
        for(auto &lab : lab_data) {
            // take apart elements
            std::vector<std::string> lab_info_vec(split(lab.first, &delim));

            std::string lab_id = lab_info_vec[0];
            std::string lab_abbrv = lab_info_vec[1];
            std::string lab_unit = lab_info_vec[2];
            std::string omop_id = lab_info_vec[3];
            std::string omop_name = lab_info_vec[4];

            if(omop_id == "NA") {
                std::string lab_info = get_lab_info(lab_abbrv, lab_unit, delim);
                
                if((omop_mapped_data.find(lab_info) != omop_mapped_data.end()) &&
                    (duplicate_mappings.find(lab_info) == duplicate_mappings.end())) {
                    std::string omop_info = omop_mapped_data[lab_info];
                    std::string lab_id_omop_info = get_lab_id_omop_info(lab_id, lab_info, omop_info, delim);
                    new_omop_candidates[lab_id_omop_info] += lab.second;
                }
            }
    }
}

/**
 * @brief Writes the new candidate lab IDs for OMOP mapping to a file
 * 
 * @param res_path The path to the results file
 * @param new_omop_candidates The map containing the new OMOP candidates "lab_id;lab_abbrv;lab_unit;omop_id;omop_name" -> count
 * @param omop_mapped_count_data The map containing the OMOP mapped data "lab_abbrv;lab_unit;omop_id;omop_name" -> count
 * 
 * @return void
 * 
 * The file is written in the format:
 * LAB_ID;LAB_ABBRV;LAB_UNIT;OMOP_ID;OMOP_NAME;LAB_COUNT;OMOP_COUNT
*/
void write_new_omop_candidates_file(std::string res_path, 
                                    std::unordered_map<std::string, int> &new_omop_candidates, 
                                    std::unordered_map<std::string, int> &omop_mapped_count_data,
                                    char delim) {
    // Write the new omop candidates to a file
    std::ofstream res_file;
    std::string crnt_res_path = concat_string(std::vector<std::string>({res_path, "_new_omop_candidates.csv"}));
    res_file.open(crnt_res_path);
    check_out_open(res_file, crnt_res_path);
    
    // Write header
    std::vector<std::string> lab_header({"LAB_ID", "LAB_ABBRV", "LAB_UNIT", "OMOP_ID", "OMOP_NAME", "LAB_COUNT", "OMOP_COUNT"});
    res_file << concat_string(lab_header, std::string(1, delim)) << std::endl;
    for (auto &new_omop_candidate : new_omop_candidates) {
        res_file << new_omop_candidate.first << delim << new_omop_candidate.second;
        // get parts of new_omop_candidate.first
        std::vector<std::string> new_omop_candidate_vec(splitString(new_omop_candidate.first, delim));
        std::string lab_id = new_omop_candidate_vec[0];
        std::string lab_abbrv = new_omop_candidate_vec[1];  
        std::string lab_unit = new_omop_candidate_vec[2];
        std::string omop_id = new_omop_candidate_vec[3];
        std::string omop_name = new_omop_candidate_vec[4];

        // concate those in omop_mapped_data 
        std::string lab_info = get_lab_info(lab_abbrv, lab_unit, delim);
        std::string omop_info = get_omop_info(omop_id, omop_name, delim);
        std::string lab_omop_info = concat_string(std::vector<std::string>({lab_info, omop_info}), std::string(1, delim));
        res_file << delim << omop_mapped_count_data[lab_omop_info] << std::endl;
    }

    res_file.close();
}

/**
 * @brief Main function for learning new OMOP candidates for lab IDs
 * 
 * @param argc Number of arguments - expects one argument the path where the results are to be read from and stored. 
 * @param argv Arguments
 * 
 * @return int
 * 
 * The function reads in the following files:
 * - <res_path>_lab_counts.csv
 * - <res_path>_omop_mapped_lababbrv_counts.csv
 * They are created by the executable create_lab_omop_map_overview with the same res_path.
 * 
 * The function writes the following files:
 * - <res_path>_new_omop_candidates.csv
 * 
 * The function takes the following steps:
 * - Read in the lab data from <res_path>_lab_counts.csv
 * - Read in the OMOP mapped lab data from <res_path>_omop_mapped_lababbrv_counts.csv
 * - Find new OMOP candidates for lab IDs - i.e. lab IDs that are not yet mapped to an OMOP ID but have a lab 
 *   abbreviation and unit that is already mapped to an OMOP ID, excluding lab abbreviations 
 *   that have multiple OMOP IDs mapped to them. 
 * - Write the new OMOP candidates to <res_path>_new_omop_candidates.csv
*/
int main(int argc, char *argv[])
{
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

    std::string res_path = argv[1];

    // Reading in maps for new omop concepts
    std::unordered_map<std::string, int> lab_data;
    std::unordered_map<std::string, std::string> omop_mapped_data;
    std::unordered_map<std::string, int> omop_mapped_count_data;
    std::unordered_set<std::string> duplicate_mappings;

    // Write to file all lab ID / abbreviations and their counts in the data
    std::ifstream in_file;
    std::string crnt_in_path = concat_string(std::vector<std::string>({res_path, "_lab_counts.csv"}));

    // Reading
    char delim = find_delim(crnt_in_path);
    in_file.open(crnt_in_path);
    check_in_open(in_file, crnt_in_path);
    std::string line;
    int first_line = 1; // Indicates header line    
    while(std::getline(in_file, line)) {
        if(first_line == 1) {
            first_line = 0;
        } else {
            // Fill in lab_data map
            std::vector<std::string> line_vec(split(line, &delim));
            std::string lab_id = line_vec[0];
            std::string lab_abbrv = line_vec[1];
            std::string lab_unit = line_vec[2];
            std::string omop_id = line_vec[3];
            std::string omop_name = line_vec[4];
            int count = std::stoi(line_vec[5]);

            std::string lab_info = get_lab_info(lab_abbrv, lab_unit, delim);
            std::string omop_info = get_omop_info(omop_id, omop_name, delim);
            std::string lab_id_omop_info = get_lab_id_omop_info(lab_id, lab_info, omop_info, delim);

            lab_data[lab_id_omop_info] = count;
        }
    }
    in_file.close();

    // Do same for omop_mapped_data
    crnt_in_path = concat_string(std::vector<std::string>({res_path, "_omop_mapped_lababbrv_counts.csv"}));
    char delim_2 = find_delim(crnt_in_path);

    in_file.open(crnt_in_path);
    check_in_open(in_file, crnt_in_path);
    // Reading
    first_line = 1; // Indicates header line
    int count = 1;
    while(std::getline(in_file, line)) {
        if(first_line == 1) {
            first_line = 0;
        } else {
            cout << count << endl;
            count++;
            // Read omop_mapped_data
            std::vector<std::string> line_vec(splitString(line, delim_2));
            std::string lab_abbrv = line_vec[0];
            std::string lab_unit = line_vec[1];
            std::string omop_id = line_vec[2];
            std::string omop_name = line_vec[3];
            int count = std::stoi(line_vec[4]);

            std::string lab_info = get_lab_info(lab_abbrv, lab_unit, delim_2);
            std::string omop_info = get_omop_info(omop_id, omop_name, delim_2);
            std::string lab_omop_info = concat_string(std::vector<std::string>({lab_info, omop_info}), std::string("\t"));

            // Check for duplicate mappings
            if(omop_mapped_data.find(lab_info) != omop_mapped_data.end()) {
                duplicate_mappings.insert(lab_info);
            }
            omop_mapped_data[lab_info] = omop_info;
            omop_mapped_count_data[lab_omop_info] = count;
        }
    }
    in_file.close();
    std::unordered_map<std::string, int> new_omop_candidates;
    find_new_omop_candidates(new_omop_candidates, lab_data, omop_mapped_data, duplicate_mappings, delim);
    write_new_omop_candidates_file(res_path, new_omop_candidates, omop_mapped_count_data, delim);

    write_end_run_summary(begin);
}

