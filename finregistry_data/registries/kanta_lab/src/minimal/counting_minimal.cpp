void update_col_tabs_minimal(std::vector<std::string> line,
                               std::vector<std::string> &col_names,
                                std::unordered_map<std::string, std::unordered_map<std::string, unsigned long long>> &col_tables) {

    for(long unsigned int col_idx=0; col_idx < col_names.size(); col_idx++) {
        std::string col_name = col_names[col_idx];
        std::string col;
        switch(col_idx) {
            case 1: // ID, measure time, measurement
                {std::stringstream ss;
                ss << line[0] << "\t" << line[1] << "\t" << line[2];
                col = ss.str();}
                break;}
            case 4: // measurement, regional ID, lab ID
                {std::stringstream ss;
                ss << line[3] << "\t" << line[4] << "\t" << line[5];
                col = ss.str();}
            case  
            default:
                col = line[col_idx];
        }
        if(col_tables[col_name].count(col) != 1){
            col_tables[col_name][col] = 1;
        } else {
            col_tables[col_name][col]++;
        }
    }
}