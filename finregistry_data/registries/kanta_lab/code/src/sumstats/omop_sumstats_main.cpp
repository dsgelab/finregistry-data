#include "../header.h"

int main(int argc, char *argv[]) {
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

    std::string res_path = argv[1];
    std::string date = argv[2];

    // Reading in maps for new omop concepts
    std::unordered_map<std::string, std::vector<double>> omops;
    std::unordered_map<std::string, std::unordered_set<std::string>> omop_indvs;

    // Reading
    char in_delim = '\t';
    char out_delim = '\t';
    std::string line;
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

        if (!(omop_id == "NA" || lab_value == "NA")) {
            std::string omop_identifier = get_omop_identifier(omop_id, omop_name, lab_unit, out_delim);
            omops[omop_identifier].push_back(std::stod(lab_value));
            omop_indvs[omop_identifier].insert(finregid);
        }
        n_lines++; write_line_update(n_lines, begin);
    }

    write_omop_sumstats(omops, omop_indvs, res_path, date, out_delim);
    write_end_run_summary(begin);
}
