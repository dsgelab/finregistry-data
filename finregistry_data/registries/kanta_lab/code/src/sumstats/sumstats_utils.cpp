#include "../header.h"

/**
 * @brief writes the omop sumstats to a file
 * 
 * @param omops unordered map of omop identifiers and their values
 * @param res_file file to write to
 * @return void
 * 
 * @details 
 * Writes the omop sumstats to a file. The omop identifiers are split into their components and written to the file. 
 * The omop values are sorted and the mean, median, standard deviation, first and third quantiles, min, max and number
 * of elements are calculated and written to the file.
**/
void write_omop_sumstats(std::unordered_map<std::string, std::vector<double>> &omops,
                         std::unordered_map<std::string, std::unordered_set<std::string>> &omop_indvs,
                         std::string res_path,
                         std::string date,
                         char out_delim) {

    // Opening results file
    std::vector<std::string> full_res_path_vec = {res_path, "kanta_lab_", date, "_omop_sumstats.tsv"};
    std::string full_res_path = concat_string(full_res_path_vec);
    std::ofstream res_file;
    res_file.open(full_res_path);
    check_out_open(res_file, full_res_path);

    // write header in all caps
    std::vector<std::string> header_vec = {"OMOP_ID", "OMOP_NAME", "LAB_UNIT", "MEAN", "MEDIAN", "SD", "FIRST_QUANTILE", "THIRD_QUANTILE", "MIN", "MAX", "N_ELEMS", "N_INDVS"};
    std::string header = concat_string(header_vec, std::string(1, out_delim));
    res_file << header << "\n";

    cout << "Starting summary statistics" << endl;
    for(auto omop: omops) {
        std::string omop_identifier = omop.first;
        std::vector<double> values = omop.second;
        std::sort(values.begin(), values.end());

        double mean = get_mean(values);
        double median = get_median(values);
        double sd = get_sd(values, mean);
        double first_quantile = get_quantile(values, double(0.25));
        double third_quantile = get_quantile(values, double(0.75));
        double min = values[0];
        double max = values[values.size()-1];
        int n_elems = values.size();
        int n_indvs = omop_indvs[omop_identifier].size();

        // write to file 
        std::vector<std::string> res_vec = {omop_identifier, std::to_string(mean), std::to_string(median), std::to_string(sd), std::to_string(first_quantile), std::to_string(third_quantile), std::to_string(min), std::to_string(max), std::to_string(n_elems), std::to_string(n_indvs)};
        res_file << concat_string(res_vec, std::string(1, out_delim)) << "\n";
    }

    res_file.close();
}

/**
 * @brief writes the individual omop sumstats to a file
 * 
 * @param indvs_omops_values unordered map of individual omop values
 * @param res_path path to write to
 * 
 * @return void
 * 
 * @details
 * Writes the individual omop sumstats to a file. The omop identifiers are split into their components and written to the file.
 * The omop values are sorted and the mean, median, standard deviation, first and third quantiles, min, max and number
 * of elements are calculated and written to the file.
*/
void write_indvs_omops_sumstats(std::unordered_map<std::string, std::unordered_map<std::string, std::vector<double>>> &indvs_omops_values,
                                std::string res_path) {    
    // Opening results file
    std::vector<std::string> full_res_path_vec = {res_path, "indv_omop_sumstats.csv"};
    std::string full_res_path = concat_string(full_res_path_vec);
    std::ofstream res_file;
    res_file.open(full_res_path);
    check_out_open(res_file, full_res_path);

    char out_delim = '\t';
    // Write header in all caps
    std::vector<std::string> header_vec = {"FINREGISTRYID", "OMOP_ID", "LAB_UNIT", "MEAN", "MEDIAN", "SD", "FIRST_QUANTILE", "THIRD_QUANTILE", "MIN", "MAX", "N_ELEMS"};
    res_file << concat_string(header_vec, std::string(1, out_delim)) << "\n";
    for(auto indv_data: indvs_omops_values) {
        std::string finregid = indv_data.first;
          for(auto omop:  indv_data.second) {
            std::string omop_identifier = omop.first;
            std::string omop_id = split(omop_identifier, "_")[0];
            std::string lab_unit = split(omop_identifier, "_")[1];

            // Getting all values for this omop
            std::vector<double> values = omop.second;
            std::sort(values.begin(), values.end());

            // Calculating summary statistics
            double mean = get_mean(values);
            double median = get_median(values);
            double sd = get_sd(values, mean);
            double first_quantile = get_quantile(values, double(0.25));
            double third_quantile = get_quantile(values, double(0.75));
            double min = values[0];
            double max = values[values.size()-1];
            int n_elems = values.size();

            // Writing to file
            std::vector<std::string> res_vec = {finregid, omop_id, lab_unit, std::to_string(mean), std::to_string(median), std::to_string(sd), std::to_string(first_quantile), std::to_string(third_quantile), std::to_string(min), std::to_string(max), std::to_string(n_elems)};

            res_file << concat_string(res_vec, std::string(1, out_delim)) << "\n";
        }
    }
}

/**
 * @brief calculates the quantile of a vector of values
 * 
 * @param values vector of values
 * @param quantile quantile to calculate
 * @return double quantile value
 * 
 * @details
 * Calculates the quantile of a vector of values. The vector is sorted and the quantile is calculated using linear interpolation.
*/
double get_quantile(std::vector<double> values, 
                    double quantile) {
    // Step 2: Calculate the position of the quantile
    int n = values.size();
    double position = (n - 1) * quantile; // Using quantile directly

    // Step 3: Find the value at the position with linear interpolation
    int lower_index = static_cast<int>(position);
    int upper_index = lower_index + 1;
    double lower_value = values[lower_index];
    double upper_value = values[upper_index];
    double index_diff = position - lower_index;
    double quantile_value = lower_value + index_diff * (upper_value - lower_value);

    return quantile_value;
}

/**
 * @brief calculates the mean of a vector of values
 * 
 * @param values vector of values
 * @return double mean
 * 
 * @details
 * Calculates the mean of a vector of values.
*/
double get_mean(std::vector<double> values) {
    double sum = std::accumulate(values.begin(), values.end(), 0.0);
    double mean = sum / values.size();
    return(mean);
}

/**
 * @brief calculates the median of a vector of values
 * 
 * @param values vector of values
 * @return double median
 * 
 * @details
 * Calculates the median of a vector of values. If the vector has an even number of elements, the median is calculated
 * as the mean of the two middle elements.
*/
double get_median(std::vector<double> values) {
    double median;
    if (values.size() % 2 == 0) {
        median = (values[values.size()/2 - 1] + values[values.size()/2]) / 2;
    } else {
        median = values[values.size()/2];
    }
    return(median);
}

/**
 * @brief calculates the standard deviation of a vector of values
 * 
 * @param values vector of values
 * @param mean mean of the vector of values
 * 
 * @return double standard deviation
 * 
 * @details
 * Calculates the standard deviation of a vector of values.
*/
double get_sd(std::vector<double> values,
              double mean) {
    double sum_of_squares = 0.0;

    for (const double& value : values) {
        double difference = value - mean;
        sum_of_squares += difference * difference;
    }

    double variance = sum_of_squares / (values.size()-1);
    double sd = std::sqrt(variance);
    return(sd);
}