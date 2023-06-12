#include "../header.h"

/**
 * @brief Gets the OMOP lab source based on the lab ID source and the service provider
 * 
 * @param lab_id_source The lab ID source from the original data. `0` means that the
 *                      lab ID is a local code, `1` that the lab ID is a national code.
 * @param service_provider The service provider name from the original data.
 * 
 * @return The OMOP lab source
 * 
 * The OMOP lab source is determined based on the lab ID source and the service provider.
 * It can be either LABfi, LABfi_HUS, LABfi_TMP, LABfi_TKU, or LABfi_NA. LABfi is the
 * national table, and LABfi_NA means the lab ID is a local code from a non-major hospital.
*/
std::string get_omop_lab_source(std::string lab_id_source,
                                std::string service_provider) {
    std::string lab_source;
    if(lab_id_source == "0") {
        lab_source = "LABfi";
    } else {
        if(service_provider.find("Helsinki") != std::string::npos) {
            lab_source = "LABfi_HUS";
        } else if(service_provider.find("Tampere") != std::string::npos) {
            lab_source = "LABfi_TMP";
        } else if(service_provider.find("Turku") != std::string::npos) {
            lab_source = "LABfi_TKU";
        } else {
            lab_source = "LABfi_NA";
        }
    }
    return(lab_source);
}