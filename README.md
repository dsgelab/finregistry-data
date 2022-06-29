# Finregistry data

This repository contains data preprocessing scripts for the following datasets in FinRegistry:

- DVV Extended
- Minimal Phenotype
- FICC Intensive Care
- KELA Kanta (drug prescriptions & drug deliveries)
- THL Birth 
- THL Cancer
- THL Infectious Diseases
- THL Malformations
- THL Vaccination
- ETK Pension

The preprocessing steps of each dataset are summarized in the [GitHub Releases](https://github.com/dsgelab/finregistry-data/releases). The code used for generating the processed dataset is attached to each release.

The repository also includes scripts used for profiling each dataset for the [FinRegistry data dictionary](https://docs.google.com/spreadsheets/d/1qpa9KFp36x1qQff14OEhtviQqrJQO-qQIKuqt-QX_qA/edit). Please note that profiling list-type columns is not currently implemented.

## GitHub guide 

1. Create a new branch or use an existing branch.
2. Upload the code. Make sure the code does not include any personal data.
3. Create a pull request.
4. Create a GitHub Release summarizing what was changed. Point the tag to the latest commit of your branch. 
