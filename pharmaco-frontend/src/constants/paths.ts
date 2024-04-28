const enum PATH_NAME {
  METABOLOVIGILANCE,
  METABOLOVIGILANCE_SIDE_EFFECT_RESULTS,
  METABOLOVIGILANCE_SIDE_EFFECT_FDA,
  METABOLOVIGILANCE_DRUGS_RANKED,
  METABOLOVIGILANCE_METABOLITES,
  GTEXOME,
  PEOPLE,
  CONTACT,
  API_ACCESS
}

const enum API_URL_NAME {
  GET_SIDE_EFFECTS,
  GET_DRUGS_BY_SELECTED_SIDE_EFFECTS,
  GET_DRUGS,
  FDA,
  GET_RANKED_DRUGS,
  METABOLITES_FOR_ONE_PRECURSOR,
  METABOLITES_FOR_MULTIPLE_PRECURSORS
}

const paths: { [key in PATH_NAME]: string } = {
  [PATH_NAME.METABOLOVIGILANCE]: '/pharmacogenomics/side-effects',
  [PATH_NAME.METABOLOVIGILANCE_SIDE_EFFECT_RESULTS]: '/pharmacogenomics/side-effects/results',
  [PATH_NAME.METABOLOVIGILANCE_SIDE_EFFECT_FDA]: '/pharmacogenomics/side-effects/fda',
  [PATH_NAME.METABOLOVIGILANCE_DRUGS_RANKED]: '/pharmacogenomics/side-effects/drugs-ranked',
  [PATH_NAME.METABOLOVIGILANCE_METABOLITES]: '/metabolites',
  [PATH_NAME.GTEXOME]: '/gtexome',
  [PATH_NAME.PEOPLE]: '/people',
  [PATH_NAME.CONTACT]: '/contact',
  [PATH_NAME.API_ACCESS]: '/user_accounts/profile/'
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
    '/metabolites/get-metabolites-for-multiple-precursors'
}

export { PATH_NAME, API_URL_NAME, paths, apiUrls }
