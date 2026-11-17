import {
    LIGHTEST_BLUE,
    DARKEST_BLUE
} from '@/constants/DataHelpers.js';

export function getColourPalette(numColours) {
  if (numColours <= 1) {
    return [DARKEST_BLUE];
  }

  return Array.from({ length: numColours }, (_, index) => {
    return LIGHTEST_BLUE.map((start, i) => {
      const end = DARKEST_BLUE[i];

      return Math.round(
        start +
          ((end - start) * index) /
            (numColours - 1)
      );
    });
  });
}