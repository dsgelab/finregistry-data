#include "../header.h"

int main(int argc, char *argv[])
{
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

    std::string res_path = argv[1];

    // Reading in maps for new omop concepts
    std::unordered_map<std::string, int> lab_count_data;
    std::unordered_map<std::string, std::unordered_set<std::string>> lab_indv_data;
    std::unordered_map<std::string, std::string> omop_mapped_data;
    std::unordered_map<std::string, int> omop_mapped_count_data;


    // Reading
    std::string line;
    char in_delim = '\t';
    char out_delim = '\t';

    int first_line = 1; // Indicates header line
    int n_lines = 0;
    while (std::getline(std::cin, line)) {
        if (first_line == 1) {
            first_line = 0;
            continue;
        }

        std::vector<std::string> line_vec(split(line, &in_delim));
        std::string finregid = line_vec[0];
        std::string lab_date_time = line_vec[1];
        std::string service_provider_name = line_vec[2];
        std::string lab_id = remove_chars(line_vec[3], ' ');
        std::string lab_id_source = line_vec[4];
        std::string lab_abbrv = remove_chars(line_vec[5], ' ');
        std::string lab_value = remove_chars(line_vec[6], ' ');
        std::string lab_unit = remove_chars(line_vec[7], ' ');
        std::string omop_id = line_vec[8];
        std::string omop_name = line_vec[9];
        std::string lab_abnormality = remove_chars(line_vec[10], ' ');
        std::string measure_stat = remove_chars(line_vec[11], ' ');
        std::string ref_value_text = line_vec[12];
        std::string data_system = line_vec[13];
        std::string data_system_ver = line_vec[14];

        // Create identifiers for the data
        std::string lab_info = get_lab_info(lab_abbrv, lab_unit, out_delim);
        std::string omop_info = get_omop_info(omop_id, omop_name, out_delim);
        std::string lab_omop_info = concat_string(std::vector<std::string>({lab_info, omop_info}), std::string(std::string(1, out_delim)));
        std::string lab_id_omop_info = get_lab_id_omop_info(lab_id, lab_info, omop_info, out_delim);
        
        // Adding to all lab data
        lab_indv_data[lab_id_omop_info].insert(finregid);
        lab_count_data[lab_id_omop_info]++;

        // Looking at only already OMOP mapped data
        if(!(omop_id == "NA")) {
            omop_mapped_data[lab_info] = omop_info;
            omop_mapped_count_data[lab_omop_info]++;
        }

        n_lines++; write_line_update(n_lines, begin);
    }


    // Write to file all lab ID / abbreviations and their counts in the data
    std::ofstream res_file;
    std::string crnt_res_path = concat_string(std::vector<std::string>({res_path, "_lab_counts.csv"}));
    res_file.open(crnt_res_path);
    check_out_open(res_file, crnt_res_path);

    std::vector<std::string> lab_header({"LAB_ID", "LAB_ABBRV", "LAB_UNIT", "OMOP_ID", "OMOP_NAME", "LAB_COUNT", "INDV_COUNT"});
    res_file << concat_string(lab_header, std::string(1, out_delim)) << "\n";
    for (auto &lab : lab_count_data) {
        res_file << lab.first << out_delim << lab.second << out_delim << lab_indv_data[lab.first].size() << "\n";
    }    

    res_file.close();

    // Write to file the OMOP mapped lab abbreviations
    crnt_res_path = concat_string(std::vector<std::string>({res_path,"_omop_mapped_lababbrv_counts.csv"}));
    res_file.open(crnt_res_path);
    check_out_open(res_file, crnt_res_path);
    
    std::vector<std::string> omop_mapped_header({"LAB_ABBRV", "LAB_UNIT", "OMOP_ID", "OMOP_NAME", "COUNT"});
    res_file << concat_string(omop_mapped_header, std::string(1, out_delim)) << "\n";
    for (auto &omop_mapped : omop_mapped_count_data) {
        res_file << omop_mapped.first << out_delim << omop_mapped.second << "\n";
    }

    res_file.close();

    write_end_run_summary(begin);
}
