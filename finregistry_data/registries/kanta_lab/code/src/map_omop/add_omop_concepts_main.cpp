
#include "../header.h"


/**
 * @brief Main function for adding OMOP concepts to lab data
 * 
 * @param argc Number of command line arguments
 * @param argv Command line arguments
 * 
 * @return int
 * 
 * Command line arguments:
 * 1. Path to file containing new OMOP mappings
 * 2. Path to results directory
 * 3. Date to distinguish between different runs
 * 4. Minimum count for new OMOP mappings - so how often this lab ID appears together with the abbreviation and unit that are mapped to the OMOP concept
 * 
 * Reads in lab data from stdin and adds OMOP concepts to it.
*/
int main(int argc, char *argv[]) {
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

    std::string new_omops_path = argv[1];
    std::string res_path = argv[2];
    std::string date = argv[3];
    // Read min counts input from command line
    int min_count = std::stoi(argv[4]);

    // Opening results file
    std::vector<std::string> full_res_path_vec_csv = {res_path, "processed/data/kanta_lab_", date, ".csv"};
    std::string full_res_path_csv = concat_string(full_res_path_vec_csv);
    std::ofstream res_file_csv;
    res_file_csv.open(full_res_path_csv);
    check_out_open(res_file_csv, full_res_path_csv);

    std::vector<std::string> full_res_path_vec_tsv = {res_path, "processed/data/kanta_lab_", date, "_new_omop.tsv"};
    std::string full_res_path_tsv = concat_string(full_res_path_vec_tsv);
    std::ofstream res_file_tsv;
    res_file_tsv.open(full_res_path_tsv);
    check_out_open(res_file_tsv, full_res_path_tsv);

    // Reading in maps for new omop concepts
    std::unordered_map<std::string, std::string> new_omops;
    std::unordered_map<std::string, std::string> omop_names;
    get_new_omop_concepts(new_omops, omop_names, new_omops_path, min_count);


    // Reading
    char in_delim = '\t';
    char out_delim_tsv = '\t';
    char out_delim_csv = ',';
    std::string line;
    int first_line = 1; // Indicates header line
    int n_lines = 0;
    while(std::getline(std::cin, line)) {
        if (first_line == 1) {
            res_file_tsv << get_header_final(out_delim_tsv) << "\n";
            res_file_csv << get_header_final(out_delim_csv) << "\n";
            first_line = 0;
            continue;
        }

        std::vector<std::string> line_vec(split(line, &in_delim));
        std::string finregid = line_vec[0];
        std::string lab_date_time = line_vec[1];
        std::string service_provider_name = line_vec[2];
        std::string lab_id = line_vec[3];
        std::string lab_id_source = line_vec[4];
        std::string lab_abbrv = line_vec[5];
        std::string lab_value = line_vec[6];
        std::string lab_unit = line_vec[7];
        std::string omop_id = line_vec[8];
        std::string omop_name = line_vec[9];
        std::string lab_abnormality = line_vec[10];
        std::string measure_stat = line_vec[11];
        std::string ref_value_text = line_vec[12];

        std::string omop_identifier = get_lab_id_omop_identifier(lab_id, lab_abbrv, lab_unit, out_delim_tsv);
        if(new_omops.find(omop_identifier) != new_omops.end()) {
            omop_id = new_omops[omop_identifier];
            omop_name = omop_names[omop_id];
        }
        
        // Writing line to file
        std::vector<std::string> final_line_vec = {finregid, lab_date_time, service_provider_name, lab_id, lab_id_source, lab_abbrv, lab_value, lab_unit, omop_id, omop_name, lab_abnormality, measure_stat, ref_value_text};
        // Making sure that all columns with the delimiter in the text are in quotation marks
        res_file_tsv << concat_string(final_line_vec, std::string(1, out_delim_tsv)) << "\n";
        for(unsigned int i = 0; i < final_line_vec.size(); ++i) add_quotation(final_line_vec[i], out_delim_csv);
        res_file_csv << concat_string(final_line_vec, std::string(1, out_delim_csv)) << "\n";

        // Write every 10000000 lines
        n_lines++; write_line_update(n_lines, begin);
    }
    res_file_tsv.close();
    res_file_csv.close();

    write_end_run_summary(begin);
}


