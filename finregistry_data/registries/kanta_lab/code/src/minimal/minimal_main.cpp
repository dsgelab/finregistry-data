#include "../header.h"

/**
 * Processes the original kanta data files with 46 columns and creates
 * files with only the minimal necessary columns. See README.md for more
 * information.
 * 
 * The input arguments need be appended in the correct order
 *  - `res_path`: Path to results directory
 *  - `file`: File number
 *  - `date`: Date of file
 *  - `thl_sote_path`: Path to THL SOTE organisations name map `data/thl_sote_organisations.tsv`
* `thl_abbrv_path`: Path to official abbreviations map `data/thl_lab_id_abbrv_map.tsv`
* `write_reports`: Wheter to write report or not, either "True" or "False"
*/
int main(int argc, char *argv[]) {
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

    /// READING IN ARGUMENTS
    std::string res_path = argv[1]; // Path to results folder
    std::string file = argv[2]; // File number
    std::string date = argv[3]; // Date of file
    std::string thl_sote_path = argv[4]; // Path to THL SOTE organisations name map
    std::string thl_abbrv_path = argv[5]; // Path to official abbreviations map
    std::string write_reports = argv[6];  // Write reports or not
    
    /// OUTPUT FILE PATHS   
    // Results file
    std::vector<std::string> full_res_path_vec = {res_path, "processed/data/kanta_lab_file_", file, "_", date, ".zsv"};    
    std::string full_res_path = concat_string(full_res_path_vec, std::string(""));
    // Row counts file
    std::vector<std::string> report_path_vec = {res_path, "processed/reports/counts/row_counts/row_counts_file_", file, "_", date, ".tsv"};    
    std::string report_path = concat_string(report_path_vec, std::string(""));
    // Problem rows file
    std::vector<std::string> error_path_vec = {res_path, "processed/reports/problem_rows/problem_rows_file_", file, "_", date, ".tsv"};    
    std::string error_path = concat_string(error_path_vec, std::string(""));
    // Missing rows file
    std::vector<std::string> missing_path_vec = {res_path, "processed/reports/problem_rows/missing_data_rows_file_", file, "_", date, ".tsv"};
    std::string missing_path = concat_string(missing_path_vec, std::string(""));

    std::ofstream error_file; std::ofstream missing_file;
    if (write_reports == "True") {
        error_file.open(error_path);
        missing_file.open(missing_path);
        check_out_open(error_file, error_path);
        check_out_open(missing_file, missing_path);
    }
    // Opening results and error files
    std::ofstream res_file; res_file.open(full_res_path); check_out_open(res_file, full_res_path); 

    /// READING IN OTHER FILES
    // Duplicate line map, including counts for current file
    std::unordered_map<std::string, int> all_dup_lines;
    get_previous_dup_lines(all_dup_lines, file, date, res_path);

    // Getting THL SOTE organisations name map. 
    // See: https://thl.fi/fi/web/tiedonhallinta-sosiaali-ja-terveysalalla/ohjeet-ja-soveltaminen/koodistopalvelun-ohjeet/sote-organisaatio-rekisteri
    std::unordered_map<std::string, std::string> thl_sote_map;
    read_thl_sote_map(thl_sote_map, thl_sote_path);

    // Getting official THL abbreviations map 
    // See: https://koodistopalvelu.kanta.fi/codeserver/pages/classification-view-page.xhtml?classificationKey=88&versionKey=120
    std::unordered_map<std::string, std::string> thl_abbrv_map;
    read_thl_lab_id_abbrv_map(thl_abbrv_map, thl_abbrv_path);

    /// INITIALIZING COUNTS
    unsigned long long dup_count = 0; // Duplicate lines
    unsigned long long valid_line_count = 0; // Valid lines actually written to file
    unsigned long long total_line_count = 0; // All lines
    unsigned long long na_count = 0;
    unsigned long long hetu_count = 0;
    unsigned long long stat_count = 0;

    /// READING IN DATA
    char out_delim = '\t';
    char in_delim = '\t';
    std::string line;
    cout << "Starting reading file " << file << endl;
    while(std::getline(std::cin, line)) {
        ++total_line_count;
        // Getting current line as vector
        std::vector<std::string> line_vec = split(line, &in_delim);

        // Line or newline is valid
        if((valid_line_count == 0)) {
            // Writing header
            res_file << get_no_omop_header(out_delim) << "\n";
            if (write_reports == "True") {
                error_file << line << "\n";
                missing_file << line << "\n";
            }
            ++valid_line_count;
            cout << "Header written, check if delimiter correct first element on line 1 is: " << line_vec[0] << endl;
        }
        else {
            // Fixing the NA indicators to actual NAs
            fix_nas(line_vec);

            // Column values directly from line
            std::string finregid = remove_chars(line_vec[4], ' ');
            std::string lab_date_time = remove_chars(line_vec[11], ' ');
            std::string service_provider_oid = remove_chars(line_vec[28], ' ');
            std::string measure_stat = remove_chars(line_vec[34], ' ');
            std::string lab_value = remove_chars(line_vec[35], ' ');
            std::string lab_unit = remove_chars(line_vec[36], ' ');
            std::string lab_abnormality = remove_chars(line_vec[37], ' ');
            std::string ref_value_text = remove_chars(line_vec[44], ' ');
            std::string data_system = remove_chars(line_vec[18], ' ');
            std::string data_system_ver = remove_chars(line_vec[20], ' ');

            // Skipping lines with not official hetu root, doing this here to avoid keeping hetu_root in later files
            std::string hetu_root = line_vec[30];
            if ((hetu_root != "1.2.246.21")) {
                error_file << line << "\n";
                ++hetu_count;
                continue;
            }
            // Skipping lines with measurement status = unfinished, W = wrong, X = no result, I = sample in the lab waiting for result
            if ((measure_stat == "K") | (measure_stat == "W") | (measure_stat == "X") | (measure_stat == "I")) {
                error_file << line << "\n";
                ++stat_count;
                continue;
            }

            // Removing characters like " ", "_", etc from unit
            lab_unit = clean_units(lab_unit);

            // Column values needed for mapping and cleaning
            std::string local_lab_abbrv = remove_chars(line_vec[31], ' ');
            std::string local_lab_id = remove_chars(line_vec[32], ' ');
            std::string thl_lab_id = remove_chars(line_vec[0], ' ');

            // Lab ID, and source depend on data
            std::string lab_id;
            std::string lab_id_source;

            // Duplicate line
            std::vector<std::string> dup_vec = {finregid, lab_date_time, service_provider_oid, lab_id, local_lab_abbrv, lab_value, lab_unit};
            std::string dup_line = concat_string(dup_vec, std::string(""));
            // Only saving non-duplicated lines
            if (all_dup_lines.find(dup_line) == all_dup_lines.end()) {
                // Merging the two lab IDs and getting the lab abbreviation
                get_lab_id_and_source(local_lab_id, thl_lab_id, lab_id, lab_id_source);
                std::string lab_abbrv = get_lab_abbrv(thl_abbrv_map, lab_id, lab_id_source, local_lab_abbrv);

                // Mapped column values
                std::string service_provider_name = get_service_provider_name(thl_sote_map, service_provider_oid);
                // Cleaning potential "" in lab-abbreviation
                lab_abbrv = remove_chars(lab_abbrv, '\"');

                // Only saving if we have either the value or at least the abnormality and a lab id
                if ((!((lab_value == "NA") & (lab_abnormality == "NA"))) & (lab_id != "NA")) {
                    // Increasing line count for duplicate lines in this file to one (meaning that this line is not actually duplicated)
                    all_dup_lines[dup_line] = 1;
                    // Writing line to file
                    std::vector<std::string> final_line_vec = {finregid, lab_date_time, service_provider_name, lab_id, lab_id_source, lab_abbrv, lab_value, lab_unit, lab_abnormality, measure_stat, ref_value_text, data_system, data_system_ver};
                    // Making sure that all columns with the delimiter in the text are in quotation marks if not tab separated
                    if (out_delim != '\t') for (unsigned int i = 0; i < final_line_vec.size(); ++i) add_quotation(final_line_vec[i], out_delim);
                    res_file << concat_string(final_line_vec, std::string(1, out_delim)) << "\n";
                    // Increasing valid line count
                    ++valid_line_count;
                // Line is missing all interesting data
                } else {
                    ++na_count; if (write_reports == "True") missing_file << line << "\n";
                }
            // Duplicate line
            } else {
                ++dup_count; all_dup_lines[dup_line]++;
            }
        }

        // Write every 10000000 lines
        write_line_update(total_line_count, begin);
    }

    // Closing
    if(write_reports == "True") {
        error_file.close();
        missing_file.close();
    }
    res_file.close(); 

    // Writing final files
    write_row_count_report(report_path, date, total_line_count, valid_line_count, dup_count, na_count, hetu_count, stat_count);
    write_dup_lines_file(res_path, file, date, report_path, all_dup_lines);

    write_end_run_summary(begin);
}