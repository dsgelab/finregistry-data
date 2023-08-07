#include "../header.h"

/**
 * Processes the original kanta data files with 25 columns and creates
 * a file with all minimal necessary columns.
 * 
 * Input:
 *  - res_path: Path to results folder
 *  - file: File number
 *  - thl_sote_path: Path to THL SOTE organisations name map
 *  - thl_abbrv_path: Path to official abbreviations map
 * 
 * @details 
 * 
 * Expected columns:
 *  1. asiakirjaoid - Document OID
 *  2. hetu - Finregistry ID
 *  3. merkintaoid - Note OID
 *  4. entryoid - Entry OID
 *  5. rekisterinpitaja_organisaatio - Registry controller organisation ID
 *  6. rekisterinpitaja -  Registry organisation ID
 *  7. palveluntuottaja_organisaatio - Service provider organisation ID
 *  8. palveluisanta_organisaatio - Service host organisation ID
 *  9. laboratoriotutkimusoid - Laboratory test OID
 *  10. potilassyntymaaika_pvm - Patient birth date
 *  11. potilas_sukupuoli - Patient sex
 *  12. tutkimusaika - Test time
 *  13. tutkimuksennaytelaatu - Test sample quality
 *  14. tutkimuksentekotapa - Test method
 *  15. paikallinentutkimusnimike - Local test name
 *  16. paikallinentutkimusnimikeid - Local test name ID
 *  17. laboratoriotutkimusnimikeid - Laboratory test name ID
 *  18. tutkimuskoodistonjarjestelmaid - Test code system ID
 *  19. tutkimusvastauksentila - Test result status
 *  20. tutkimustulosarvo - Test result value
 *  21. tutkimustulosyksikkö - Test result unit
 *  22. tuloksenvalmistumisaika - Test result time
 *  23. tuloksenpoikkeavuus - Test result abnormality
 *  24. erikoisalalyhenne - Speciality abbreviation
 *  25. asiakirjaluontiaika - Document creation time
 * 
 * Duplicate lines are removed and written to separate file. A duplicate is defined if all of the following data is the same: 
 *  1. Finregistry ID
 *  2. Date and time
 *  3. Service provider organization
 *  3. Laboratory test name ID
 *  4. Laboratory test name abbreviation
 *  5. Test result value
 *  6. Test result unit
 * 
*/
int main(int argc, char *argv[]) {
    /// READING IN ARGUMENTS
    std::string res_path = argv[1]; // Path to results folder
    std::string file = argv[2]; // File number
    std::string thl_sote_path = argv[3]; // Path to THL SOTE organisations name map
    std::string thl_abbrv_path = argv[4]; // Path to official abbreviations map
    
    /// OUTPUT FILE PATHS   
    // Results file
    std::vector<std::string> full_res_path_vec = {res_path, "processed/data/minimal_file_", file, ".csv"};    
    std::string full_res_path = concat_string(full_res_path_vec, std::string(""));
    // Row counts file
    std::vector<std::string> report_path_vec = {res_path, "processed/reports/counts/row_counts/row_counts_file_", file, ".csv"};    
    std::string report_path = concat_string(report_path_vec, std::string(""));
    // Problem rows file
    std::vector<std::string> error_path_vec = {res_path, "processed/reports/problem_rows/problem_rows_file_", file, ".csv"};    
    std::string error_path = concat_string(error_path_vec, std::string(""));
    // Missing rows file
    std::vector<std::string> missing_path_vec = {res_path, "processed/reports/problem_rows/missing_data_rows_file_", file, ".csv"};
    std::string missing_path = concat_string(missing_path_vec, std::string(""));

    // Opening results and error files
    std::ofstream error_file;
    std::ofstream missing_file;
    std::ofstream res_file;
    res_file.open(full_res_path); error_file.open(error_path);  missing_file.open(missing_path);
    check_out_open(res_file, full_res_path); check_out_open(error_file, error_path); check_out_open(missing_file, missing_path);

    /// READING IN OTHER FILES
    // Duplicate line map, including counts for current file
    std::unordered_map<std::string, int> all_dup_lines;
    get_previous_dup_lines(all_dup_lines, file, res_path);

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
    unsigned long long skip_count = 0; // Skipped lines due to other reasons but duplication
    unsigned long long valid_line_count = 0; // Valid lines actually written to file
    unsigned long long total_line_count = 0; // All lines
    unsigned long long na_count = 0;
    // This code is used for wrongly split lines writing to error file
    int lines_valid_status = 0; // 0: line is valid 1: line is invalid 2: both line and new line are invalid 3: line is invalid, but newline is valid

    /// READING IN DATA
    std::string line;
    while(std::getline(std::cin, line)) {
        ++total_line_count;
        if(total_line_count % 10000000 == 0) {
            cout << total_line_count << "\n";
        }
        // Getting current line as vector
        std::vector<std::string> final_line_vec = read_correct_lines(line, total_line_count, skip_count, error_file, lines_valid_status);

        // Line or newline is valid
        if((lines_valid_status == 0) | (lines_valid_status == 3)) {
            if((valid_line_count == 0)) {
                // Writing header
                res_file << "FINREGISTRYID;LAB_DATE_TIME;LAB_SERVICE_PROVIDER;LAB_ID;LAB_ID_SOURCE;LAB_ABBREVIATION;LAB_VALUE;LAB_UNIT;LAB_ABNORMALITY\n"; 
                ++valid_line_count;
            } else {
                // Fixing the NA indicators to actual NAs
                fix_nas(final_line_vec);

                // Column values directly from line
                std::string finregistry_id = final_line_vec[1];
                std::string date_time = final_line_vec[11];
                std::string service_provider_oid = final_line_vec[6];
                std::string lab_value = final_line_vec[19];
                std::string lab_unit = final_line_vec[20];
                std::string lab_abnormality = final_line_vec[22];

                // Removing characters like " ", "_", etc from unit
                lab_unit = clean_units(lab_unit);

                // Column values needed for mapping and cleaning
                std::string lab_name = final_line_vec[14];
                std::string local_lab_id = final_line_vec[15];
                std::string thl_lab_id = final_line_vec[16];

                // Lab ID, and source depend on data
                std::string lab_id; 
                std::string lab_id_source;

                // Duplicate line
                std::vector<std::string> dup_vec = {finregistry_id, date_time, service_provider_oid, lab_id, lab_name, lab_value, lab_unit};
                std::string dup_line = concat_string(dup_vec, std::string("")); 
                // Only saving non-duplicated lines
                if(all_dup_lines.find(dup_line) == all_dup_lines.end()) {
                    // Now doing the rest
                    get_lab_id_and_source(local_lab_id, thl_lab_id, lab_id, lab_id_source); 

                    // Mapped column values
                    std::string service_provider_name = get_service_provider_name(thl_sote_map, service_provider_oid);
                    std::string lab_abbrv = get_lab_abbrv(thl_abbrv_map, lab_id, lab_id_source, lab_name);

                    // Only saving if we have either the value or at least the abnormality
                    // and an lab ID
                    if((!((lab_value == "NA") & (lab_abnormality == "NA"))) & (lab_id != "NA") ) { 
                            // Increasing line count for this file to one
                            all_dup_lines[dup_line] = 1;
                            // Writing line to file
                            res_file << finregistry_id << ";" <<  date_time << ";" << service_provider_name << ";" << lab_id << ";" << lab_id_source << ";" << lab_abbrv << ";" << lab_value << ";" << lab_unit << ";" <<  lab_abnormality << "\n";
                            // Increasing valid line count
                            ++valid_line_count;

                        // Duplicate line
                        } else {
                            ++dup_count;
                        }
                // Invalid line because of NAs in both value, and abnormality or NA in lab ID
                } else {
                    ++na_count;       
                    missing_file << concat_string(final_line_vec, ";") << "\n";
                }
            }  
        }
    }

    // Closing
    error_file.close();
    missing_file.close();
    res_file.close(); 

    // Writing final files
    write_row_count_report(report_path, total_line_count, valid_line_count,skip_count, dup_count, na_count);
    write_dup_lines_file(res_path, file, report_path, all_dup_lines);
}

std::string clean_units(std::string lab_unit) {
    lab_unit = remove_chars(lab_unit, ' ');
    lab_unit = remove_chars(lab_unit, '_');
    lab_unit = remove_chars(lab_unit, ',');
    lab_unit = remove_chars(lab_unit, '.');
    lab_unit = remove_chars(lab_unit, '-');
    lab_unit = remove_chars(lab_unit, ')');
    lab_unit = remove_chars(lab_unit, '(');
    lab_unit = remove_chars(lab_unit, '{');
    lab_unit = remove_chars(lab_unit, '}');

    return(lab_unit);
}