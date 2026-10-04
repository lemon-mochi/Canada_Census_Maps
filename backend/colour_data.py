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
    """
    This helper function assigns each data value a colour based on its value.
    Parameters;
    df: The pandas dataframe that contains the values
    num_colours: The number of bins to split the data into (each bin has its own colour).
    equal_width: When true the data will be put into equal width bins. When false,
    each bin will be roughly the same size.
    col: the column to be used to split the data (for example, TOTAL_COUNT will split the data by TOTAL_COUNT)
    """

    lightest = np.array([247, 251, 255], dtype=np.uint8)
    darkest = np.array([8, 48, 107], dtype=np.uint8)

    labels = generate_colour_labels(
        lightest,
        darkest,
        num_colours,
    )

    if df.empty:
        df["Colour_bin"] = pd.Series(dtype=object)
        return df

    if df[col].nunique() <= 1:
        df["Colour_bin"] = [labels[-1]] * len(df)
        return df

    if equal_width:
        df["Colour_bin"] = pd.cut(
            df[col],
            bins=num_colours,
            labels=labels,
            include_lowest=True,
        )
    else:
        df["Colour_bin"] = pd.qcut(
            df[col],
            q=num_colours,
            labels=labels,
            duplicates="drop",
        )

    return df

    