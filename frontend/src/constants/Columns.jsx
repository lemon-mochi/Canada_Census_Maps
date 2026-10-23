/* ------------------------------------------------------------------ */
/* Constants (outside the component so they aren't recreated per render) */
/* ------------------------------------------------------------------ */

export const COLUMN_LABELS = {
  C1_COUNT_TOTAL: 'C1_T',
  'C2_COUNT_MEN+': 'C2_M',
  'C3_COUNT_WOMEN+': 'C3_F',
  C10_RATE_TOTAL: 'C4_R',
  'C11_RATE_MEN+': 'C5_R',
  'C12_RATE_WOMEN+': 'C6_R',
  COUNT_TOTAL: 'C_T',
  COUNT_MALE: 'C_M',
  COUNT_FEMALE: 'C_F',
  RATE_TOTAL: 'R_T',
  RATE_MALE: 'R_M',
  RATE_FEMALE: 'R_F',
};

const VALUE_LEGACY = {
  1: 'COUNT_TOTAL',
  2: 'COUNT_MALE',
  3: 'COUNT_FEMALE',
  4: 'RATE_TOTAL',
  5: 'RATE_MALE',
  6: 'RATE_FEMALE'
};

const VALUE_NEW = {
  1: 'C1_COUNT_TOTAL',
  2: 'C2_COUNT_MEN+',
  3: 'C3_COUNT_WOMEN+',
  4: 'C10_RATE_TOTAL',
  5: 'C11_RATE_MEN+',
  6: 'C12_RATE_WOMEN+'
}

export function getColValue(apiYear, columnID) {
  if (apiYear >= 2021) {
    return VALUE_NEW[columnID];
  } else {
    return VALUE_LEGACY[columnID];
  }
}
