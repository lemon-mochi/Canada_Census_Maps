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
    colours = np.linspace(
        lightest,
        darkest,
        num=num_colours,
    ).round().astype(int)

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

    df = df.dropna(subset=["value"])

    if df.empty:
        df["Colour_bin"] = pd.Series(dtype=object)
        return df

    if df[col].nunique() <= 1:
        df["Colour_bin"] = [labels[-1]] * len(df)
        return df

    if equal_width:
        bins = pd.cut(
            df[col],
            bins=num_colours,
            labels=False,
            include_lowest=True,
        )
    else:
        bins = pd.qcut(
            df[col],
            q=num_colours,
            labels=False,
            duplicates="drop",
        )

    df["Colour_bin"] = [
        labels[int(b)] if pd.notna(b) else (200, 200, 200)  # neutral "no data" grey
        for b in bins
    ]

    return df