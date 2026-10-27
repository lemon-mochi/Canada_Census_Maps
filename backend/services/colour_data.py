import numpy as np
import pandas as pd


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
) -> pd.DataFrame:
    lightest = np.array([247, 251, 255], dtype=np.uint8)
    darkest = np.array([0, 7, 93], dtype=np.uint8)

    labels = generate_colour_labels(
        lightest,
        darkest,
        num_colours,
    )

    valid = df[col].notna()

    df["Colour_bin"] = [(200, 200, 200)] * len(df)

    if not valid.any():
        return df, []

    if df.loc[valid, col].nunique() <= 1:
        df.loc[valid, "Colour_bin"] = pd.Series(
            [labels[-1]] * valid.sum(),
            index=df.index[valid],
            dtype=object,
        )
        return df, []

    df = df.astype(object).where(pd.notna(df), None)

    if equal_width:
        bins, boundaries = pd.cut(
            df.loc[valid, col],
            bins=num_colours,
            labels=False,
            include_lowest=True,
            retbins=True,
        )
    else:
        bins, boundaries = pd.qcut(
            df.loc[valid, col],
            q=num_colours,
            labels=False,
            duplicates="drop",
            retbins=True,
        )

    df.loc[valid, "Colour_bin"] = pd.Series(
        [
            labels[int(b)] if pd.notna(b) else (200, 200, 200)
            for b in bins
        ],
        index=df.index[valid],
        dtype=object,
    )

    return df, boundaries
