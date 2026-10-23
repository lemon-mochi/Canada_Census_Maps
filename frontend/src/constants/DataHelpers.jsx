/* ------------------------------------------------------------------ */
/* Data helpers                                                         */
/* ------------------------------------------------------------------ */

/*
 * Turn the flat, ordered list from the backend into a tree using each
 * item's `level` (0 = top level):
 *
 * Population
 *   └── Age groups
 *       └── 0 to 14
 *           └── 0 to 4
 */
export const buildTree = (characteristics) => {
  const root = [];
  const stack = [];

  characteristics.forEach((char) => {
    const node = { ...char, children: [] };

    // Pop back up to this node's parent.
    while (stack.length > 0 && stack[stack.length - 1].level >= node.level) {
      stack.pop();
    }

    if (stack.length === 0) {
      root.push(node);
    } else {
      stack[stack.length - 1].children.push(node);
    }

    stack.push(node);
  });

  return root;
};

export const LIGHTEST_BLUE = [247, 251, 255];
export const DARKEST_BLUE = [0, 7, 93];

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
