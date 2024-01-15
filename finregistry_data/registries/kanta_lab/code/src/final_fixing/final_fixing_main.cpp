#include "../header.h"

/**
 * @brief Performs final fixes to the data
 * 
 * @param argc The number of arguments
 * @param argv The arguments. The first argument is the path to the results folder.
 * 
 * @return int
 * 
 * This program performs final fixes to the data. It is run after the data has 
 * been processed. For detailed steps performed see the README.
 */
int main(int argc, char *argv[])
{
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    
    std::string res_path = argv[1];
    std::string date = argv[2];
    std::string ph_list_file_path = argv[3];
    std::string title_list_file_path = argv[4];
    
    // Opening results file
    std::vector<std::string> full_res_path_vec = {res_path, "processed/data/kanta_lab_", date, "_final_fix.tsv"};
    std::string full_res_path = concat_string(full_res_path_vec);
    std::ofstream res_file;
    res_file.open(full_res_path);
    check_out_open(res_file, full_res_path);
    
    // Problem rows file
    std::vector<std::string> error_path_vec = {res_path, "processed/reports/problem_rows/removed_final_rows_", date, ".tsv"};
    std::string error_path = concat_string(error_path_vec, std::string(""));
    std::ofstream error_file;
    error_file.open(error_path);
    check_out_open(error_file, error_path);
    
    // Open phs and titles list of IDs and abbreviation
    std::map<std::string, std::unordered_set<std::string>> phs;
    read_lab_id_abbrv_map(ph_list_file_path, phs);
 
    std::map<std::string, std::unordered_set<std::string>> titles;
    read_lab_id_abbrv_map(title_list_file_path, titles);

    // Reading
    char out_delim = '\t';
    char in_delim = '\t';
    int first_line = 1; // Indicates header line
    int n_lines = 0;
    std::string line;
    while (std::getline(std::cin, line)) {
            if(first_line == 1) {
                // Column headers
                res_file << get_header_final(out_delim) << "\n";
                error_file << get_header_final(out_delim) << "\n";
                
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
            std::string measure_status = line_vec[11];
            std::string ref_value_text = line_vec[12];
            
            // Fixing values and units
            fix_abnorms(lab_abnormality);
            // unit_conversion(lab_value, lab_unit); - Current bug needs to be done in future versions
            remove_illegal_units(lab_unit);
            fix_phs(lab_id, lab_abbrv, lab_unit, phs);  // Phs often have no units
            fix_inrs(lab_id, lab_abbrv, lab_unit); // INRs often have no units
            fix_titles(lab_id, lab_abbrv, lab_unit, lab_value, titles); // Titles often have random units and values even though they are not measurements
            
            // Seeing if there are lines to be fully removed from the data
            int keep = 1;
            keep = remove_illegal_measure_year(lab_date_time, keep);
            keep = fix_percentages(lab_value, lab_unit, lab_abnormality, keep);
            keep = remove_illegal_values(lab_value, lab_abnormality, lab_abbrv, keep);
            keep = remove_bad_measure_status(measure_status, keep);
            
            shuffle_lab_abnorm_info(lab_value, lab_abnormality, lab_unit);
            
            // Writing line to file
            std::vector<std::string> final_line_vec = {finregid, lab_date_time, service_provider_name, lab_id, lab_id_source, lab_abbrv, lab_value, lab_unit, omop_id, omop_name, lab_abnormality, ref_value_text};
            // Making sure that all columns with the delimiter in the text are in quotation marks
            if(out_delim != '\t') for(unsigned int i = 0; i < final_line_vec.size(); ++i) add_quotation(final_line_vec[i], out_delim);
            if(keep)
                res_file << concat_string(final_line_vec, std::string(1, out_delim)) << "\n";
            else
                error_file << concat_string(final_line_vec, std::string(1, out_delim)) << "\n";
            
            // Write every 10000000 lines
            n_lines++; write_line_update(n_lines, begin);
    }
    error_file.close();
    res_file.close();
    
    write_end_run_summary(begin);
}

