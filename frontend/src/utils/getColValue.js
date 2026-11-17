import {
    VALUE_LEGACY,
    VALUE_NEW
} from '@/constants/Columns.js';

export function getColValue(apiYear, columnID) {
  if (apiYear >= 2021) {
    return VALUE_NEW[columnID];
  } else {
    return VALUE_LEGACY[columnID];
  }
}
