geo_data <- fread("~/dvv_shapefiles_essential.csv")
sotka <- fread("sotka_wide.csv")  # Municipality Metadata
as_data_frame(geo_data)
as_data_frame(sotka)

geo_data %>% select(FINREGISTRYID, kuntanro)
geo_sotka <- geo_data %>% left_join(sotka, by = c("kuntanro" = "m_code"))
geo_sotka <- geo_sotka %>% select(-municipality)

#fwrite(geo_sotka_combo, "geo_sotka_combo.csv")


sotka <- sotka %>% select(-index_right, -objectid, -vuosi, -kunta)

# Creating Uniqeu Identifier "Ident"
sotka1 <- sotka %>% arrange(FINREGISTRYID, Start_of_residence)
sotka1$ident <- seq.int(nrow(sotka1))

tail(sotka1 %>% select(FINREGISTRYID, Start_of_residence, ident))
head(sotka1 %>% select(FINREGISTRYID, Start_of_residence, ident))

sotka2 <- sotka1 %>% select("17_24_year_olds_excluded_from_education_scaled_health_and_welfare_indicator":"ident")

# The following variables will only be included in the dvv_core file instead of the municipality metadata file:
# demographic_dependency_ratio, economic_dependency_ratio, general_at_risk_of_poverty_rate_for_the_municipality,
# intermunicipal_net_migration_1000_inhabitants, sale_of_alcoholic_beverages_per_capita_as_litres_of_pure_alcohol,
# self_rated_health_moderate_or_poor_scaled_health_and_welfare_indicator


sotka2 <- sotka2 %>% select(ident, everything())
colnames(sotka2)
fwrite(sotka2, "~/dvv_ext_municip.csv")



dvv_core <- sotka1 %>% select(-"17_24_year_olds_excluded_from_education_scaled_health_and_welfare_indicator":unemployed_people_as_p_of_labour_force")
dvv_core <- dvv_core %>% select(-vuosi)




fwrite(dvv_core, "~/dvv_ext_core.csv")

