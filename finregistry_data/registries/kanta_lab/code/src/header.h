#include <fstream>
#include <sstream>
#include <iostream>
#include <string>
#include <vector>
#include <regex>
#include <unordered_map>
#include <unordered_set>
#include <map>
#include <numeric>
#include <cmath>
#include <algorithm>
#include <chrono>

using namespace std;

// Helper functions
void write_line_update(int n_lines, std::chrono::steady_clock::time_point &begin, int line_limit = 10000000);
void write_end_run_summary(std::chrono::steady_clock::time_point &begin);

char find_delim(std::string file_path);
std::vector<std::string> splitString(const std::string &input, 
                                     char delimiter);
std::vector<std::string> split(const std::string &s, const char *delim);

std::string concat_string(const std::vector<std::string> &elems, std::string delim = std::string(""));
std::string concat_string(const std::unordered_set<std::string> &elems, std::string delim = std::string(""));

void check_out_open(std::ofstream &file_stream, std::string file_path);
int check_in_open(std::ifstream &file_stream, std::string file_path, int stop_if_not_open = 1); 

std::string to_lower(std::string str);
void add_quotation(std::string &str,
                   char delim);
std::string get_header(char delim);
std::string get_no_omop_header(char delim);
std::string get_header_final(char delim);

std::string remove_chars(std::string str, char remove_char);
std::string clean_units(std::string lab_unit);

std::string get_omop_info(std::string omop_id, std::string omop_name, char delim);
std::string get_lab_info(std::string lab_abbrv, std::string lab_unit, char delim);
std::string get_lab_id_omop_info(std::string lab_id, 
                                 std::string lab_info,
                                 std::string omop_info,
                                 char delim);
std::string get_lab_id_abbrv(std::string lab_id, 
                             std::string lab_abbrv);
std::string get_lab_id_omop_identifier(std::string lab_id,
                                       std::string lab_abbrv,
                                       std::string lab_unit,
                                       char = ' ');
std::string get_omop_identifier(std::string omop_id,
                                std::string omop_name,
                                std::string lab_unit,
                                char = ' ');
// Helper functions for minimal file creation
void fix_nas(std::vector<std::string> &final_line_vec);
std::string get_service_provider_name(std::unordered_map<std::string, std::string> &thl_sote_map,
                               std::string &service_provider_oid);
void get_lab_id_and_source(std::string &local_lab_id,
                           std::string &thl_lab_id,
                           std::string &lab_id,
                           std::string &lab_id_source);
std::string get_lab_abbrv(std::unordered_map<std::string, std::string> &thl_abbrv_map,
                          std::string &lab_id,
                          std::string &lab_id_source,
                          std::string &lab_name);
void write_row_count_report(std::string &report_path,
                            std::string &date,
                            unsigned long long &total_line_count,
                            unsigned long long &valid_line_count,
                            unsigned long long &dup_count,
                            unsigned long long &na_count,
                            unsigned long long &hetu_count,
                            unsigned long long &stat_count);
void write_dup_lines_file(std::string &res_path,
                          std::string &file,
                          std::string &date,
                          std::string &report_path,
                          std::unordered_map<std::string, int> &all_dup_lines);

// Writing functions
void write_omop_sumstats(std::unordered_map<std::string, std::vector<double>> &omops,
                         std::unordered_map<std::string, std::unordered_set<std::string>> &omop_indvs,
                         std::string res_path,
                         std::string date,
                         char out_delim);
void write_indvs_omops_sumstats( std::unordered_map<std::string, std::unordered_map<std::string, std::vector<double>>> &indvs_omops_values,
                                std::string res_path);

// Reading files function
void get_previous_dup_lines(std::unordered_map<std::string, int> &all_dup_lines, 
                            std::string file,
                            std::string date,
                            std::string res_path);
void read_thl_sote_map(std::unordered_map<std::string, std::string> &thl_sote_map,
                       std::string thl_sote_path);
void read_thl_lab_id_abbrv_map(std::unordered_map<std::string, std::string> &thl_abbrv_map,
                               std::string thl_abbrv_path);
std::vector<std::string> read_correct_lines(std::string &line,
                                            unsigned long long &total_line_count,
                                            unsigned long long &skip_count,
                                            std::ofstream &error_file,
                                            int &lines_valid_status,
                                            std::string write_reports="True");
void read_omop_file(std::string omop_concept_map_path,
                    std::unordered_map<std::string, std::unordered_map<std::string, std::string>>  &omop_concept_map,
                    std::unordered_map<std::string, std::string> &omop_names);
void get_new_omop_concepts(std::unordered_map<std::string, std::string> &new_omops,
                           std::unordered_map<std::string, std::string> &omop_names,   
                           std::string file_path,
                           int min_count);

// Helper functions for OMOP mapping
std::string get_omop_lab_source(std::string lab_id_source,
                                std::string service_provider);
std::string get_omop_id(std::unordered_map<std::string, std::unordered_map<std::string, std::string>> &omop_concept_map,
                        std::string omop_lab_source,
                        std::string omop_identifier);
std::string get_omop_name(std::string omop_id,
                          std::unordered_map<std::string, std::string> &omop_names);

// Helpfer functions final fixing
void unit_conversion(std::string lab_value,
                     std::string lab_unit);
void read_lab_id_abbrv_map(std::string file_path,
                           std::map<std::string, std::unordered_set<std::string>> &elems);
int fix_percentages(std::string &lab_value, 
                    std::string &lab_unit,
                    std::string &lab_abnorm,
                    int keep);
void fix_abnorms(std::string &lab_abnorm);
void shuffle_lab_abnorm_info(std::string &lab_value, 
                             std::string &lab_abnorm, 
                             std::string &lab_unit);
int remove_illegal_values(std::string &lab_value, 
                          std::string &lab_abnorm, 
                          std::string &lab_abbrv,
                          int keep);
int remove_bad_measure_status(std::string measure_status,
                              int keep);
void remove_illegal_units(std::string &lab_unit);
void fix_phs(std::string &lab_id,
             std::string &lab_abbrv,
             std::string &lab_unit,
             std::map<std::string, std::unordered_set<std::string>> &phs);
void fix_inrs(std::string &lab_id,
              std::string &lab_abbrv,
              std::string &lab_unit);
void remove_illegal_units(std::string &lab_unit);   
int remove_illegal_measure_year(std::string &date_time,
                                int keep);
void fix_titles(std::string &lab_id,
                  std::string &lab_abbrv,
                  std::string &lab_unit,
                  std::string &lab_value,
                  std::map<std::string, std::unordered_set<std::string>> &titles);

// Math helper function
double get_mean(std::vector<double> values_vec);
double get_median(std::vector<double> values_vec);
double get_sd(std::vector<double> values_vec, double mean);
double get_quantile(std::vector<double> values, double quantile);




