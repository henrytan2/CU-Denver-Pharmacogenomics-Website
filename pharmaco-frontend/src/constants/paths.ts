const enum PATH_NAME {
  METABOLOVIGILANCE,
  METABOLOVIGILANCE_SIDE_EFFECT_RESULTS,
  METABOLOVIGILANCE_SIDE_EFFECT_FDA,
  METABOLOVIGILANCE_DRUGS_RANKED,
  METABOLOVIGILANCE_METABOLITES,
  PRECURSOR_RESULTS,
  GTEXOME,
  GTEXOME_EXAC,
  GTEXOME_EXOME,
  GTEXOME_RANGE_RESULTS,
  GTEXOME_RATIO_RESULTS,
  DOCKING,
  PEOPLE,
  CONTACT,
  API_ACCESS,
  PDBGEN_RESULTS,
  PASSWORD_RESET,
  CREATE_ACCOUNT,
  LOGOUT
}

const enum API_URL_NAME {
  GET_SIDE_EFFECTS,
  GET_DRUGS_BY_SELECTED_SIDE_EFFECTS,
  GET_DRUGS,
  FDA,
  GET_RANKED_DRUGS,
  GET_TISSUE_TYPES,
  GET_RANGE_RESULTS,
  GET_RATIO_RESULTS,
  METABOLITES_FOR_ONE_PRECURSOR,
  METABOLITES_FOR_MULTIPLE_PRECURSORS,
  FETCH_PRECURSORS_FOR_DRUGS,
  GTEXOME_GENE_SEARCH_RESULTS,
  DOWNLOAD_DOCKING_RESULTS,
  FIND_RESOLUTION,
  FIND_PLDDT,
  FASPR_PREP,
  FASPR_RUN,
  PASSWORD_RESET,
  STORE_PDB_GEN_DATA,
  GET_API_TOKEN,
  CREATE_ACCOUNT,
  FASPR_PREP_FILE_UPLOAD,
  FASPR_PREP_UPLOAD
}

const paths: { [key in PATH_NAME]: string } = {
  [PATH_NAME.METABOLOVIGILANCE]: '/pharmacogenomics/side-effects',
  [PATH_NAME.METABOLOVIGILANCE_SIDE_EFFECT_RESULTS]: '/pharmacogenomics/side-effects/results',
  [PATH_NAME.METABOLOVIGILANCE_SIDE_EFFECT_FDA]: '/pharmacogenomics/side-effects/fda',
  [PATH_NAME.METABOLOVIGILANCE_DRUGS_RANKED]: '/pharmacogenomics/side-effects/drugs-ranked',
  [PATH_NAME.METABOLOVIGILANCE_METABOLITES]: '/metabolites',
  [PATH_NAME.GTEXOME]: '/gtexome',
  [PATH_NAME.GTEXOME_EXOME]: '/gtexome/exome',
  [PATH_NAME.GTEXOME_RANGE_RESULTS]: '/gtexome/range-reults',
  [PATH_NAME.GTEXOME_RATIO_RESULTS]: '/gtexome/ratio-results',
  [PATH_NAME.DOCKING]: '/docking',
  [PATH_NAME.PEOPLE]: '/people',
  [PATH_NAME.CONTACT]: '/contact',
  [PATH_NAME.API_ACCESS]: '/user_accounts/profile/',
  [PATH_NAME.PASSWORD_RESET]: '/user_accounts/password/reset/',
  [PATH_NAME.CREATE_ACCOUNT]: '/user_accounts/create-account/',
  [PATH_NAME.LOGOUT]: 'user_accounts/logout/',
  [PATH_NAME.GTEXOME_EXAC]: '/gtexome/exac',
  [PATH_NAME.PDBGEN_RESULTS]: '/pdbgen/results',
  [PATH_NAME.PRECURSOR_RESULTS]: '/precursors/results'
}

const apiUrls: { [key in API_URL_NAME]: string | ((...args: any[]) => string) } = {
  [API_URL_NAME.GET_SIDE_EFFECTS]: '/pharmacogenomics/get-side-effects',
  [API_URL_NAME.GET_DRUGS_BY_SELECTED_SIDE_EFFECTS]:
    '/pharmacogenomics/get-drugs-by-selected-sideeffects',
  [API_URL_NAME.GET_DRUGS]: '/precursors/fetchall',
  [API_URL_NAME.FDA]: (drugName: string) =>
    `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:${drugName}&count=patient.reaction.reactionmeddrapt.exact`,
  [API_URL_NAME.GET_RANKED_DRUGS]: '/pharmacogenomics/ranked-drugs',
  [API_URL_NAME.METABOLITES_FOR_ONE_PRECURSOR]: '/metabolites/get-metabolites-for-one-precursor',
  [API_URL_NAME.METABOLITES_FOR_MULTIPLE_PRECURSORS]:
    '/metabolites/get-metabolites-for-multiple-precursors',
  [API_URL_NAME.FETCH_PRECURSORS_FOR_DRUGS]: '/precursors/fetch-precursors-for-drugs',
  [API_URL_NAME.GET_TISSUE_TYPES]: '/gtexome/get-tissue-types',
  [API_URL_NAME.GET_RANGE_RESULTS]: '/gtexome/get-range-results',
  [API_URL_NAME.GET_RATIO_RESULTS]: '/gtexome/get-ratio-results',
  [API_URL_NAME.GTEXOME_GENE_SEARCH_RESULTS]: 'https://gnomad.broadinstitute.org/api',
  [API_URL_NAME.DOWNLOAD_DOCKING_RESULTS]: '/api/download-docking-results',
  [API_URL_NAME.FIND_RESOLUTION]: '/api/best-resolution',
  [API_URL_NAME.FIND_PLDDT]: '/api/plddt-score',
  [API_URL_NAME.FASPR_PREP]: '/api/faspr-prep',
  [API_URL_NAME.FASPR_RUN]: '/api/faspr-run',
  [API_URL_NAME.STORE_PDB_GEN_DATA]: '/pdbgen-backend/save-data',
  [API_URL_NAME.GET_API_TOKEN]: '/user_accounts/api-token',
  [API_URL_NAME.CREATE_ACCOUNT]: '/user_accounts/sign-up',
  [API_URL_NAME.PASSWORD_RESET]: '/user_accounts/send-reset-email',
  [API_URL_NAME.FASPR_PREP_FILE_UPLOAD]: '/api/faspr-prep-file-upload',
  [API_URL_NAME.FASPR_PREP_UPLOAD]: '/api/faspr-prep-upload'
}

export { PATH_NAME, API_URL_NAME, paths, apiUrls }
