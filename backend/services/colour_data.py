import numpy as np
import pandas as pd


LIGHTEST = np.array([247, 251, 255], dtype=np.uint8)
DARKEST = np.array([0, 7, 93], dtype=np.uint8)
NO_DATA = (200, 200, 200)

def generate_colour_labels(
    lightest: np.ndarray,
    darkest: np.ndarray,
    num_colours: int,
) -> list[tuple[int, int, int]]:
    """Generates RGB colour code labels linearly interpolated between
    lightest and darkest.
    """
    colours = (
        np.linspace(
            lightest,
            darkest,
            num=num_colours,
        )
        .round()
        .astype(int)
    )

    return [tuple(colour) for colour in colours]


def assign_colours(
    df: pd.DataFrame, num_colours: int, equal_width: bool, col: str
) -> tuple[pd.DataFrame, np.ndarray | list]:
    labels = generate_colour_labels(LIGHTEST, DARKEST, num_colours)
    palette = [*labels, NO_DATA]

    values = df[col]
    valid = values.notna()
    boundaries: np.ndarray | list = []

    if not valid.any():
        codes = np.full(len(df), -1, dtype=np.int64)
    elif values[valid].nunique() <= 1:
        codes = np.where(valid, len(labels) - 1, -1)
    else:
        v = values[valid]
        if equal_width:
            binned, boundaries = pd.cut(
                v, bins=num_colours, labels=False,
                include_lowest=True, retbins=True,
            )
        else:
            binned, boundaries = pd.qcut(
                v, q=num_colours, labels=False,
                duplicates="drop", retbins=True,
            )
        codes = np.full(len(df), -1, dtype=np.int64)
        codes[valid.to_numpy()] = binned.to_numpy()

    out = df.assign(Colour_bin=[palette[c] for c in codes])

    # JSON can't encode NaN/inf, so convert them to None (null) on every path
    num_cols = out.select_dtypes(include="number").columns
    if len(num_cols):
        block = out[num_cols].astype(object)
        out[num_cols] = block.where(np.isfinite(out[num_cols]), None)

    return out, boundaries
