import numpy as np
import pandas as pd

def generate_colour_labels(
    lightest: np.ndarray, darkest: np.ndarray, num_colours: int
) -> np.ndarray:
    """Generates rgb colour code labels linearly interpolated between lightest and darkest."""
    # Interpolate RGB values across num_colours steps
    colours = np.linspace(lightest, darkest, num=num_colours).round().astype(int)

    return colours

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

    labels = generate_colour_labels(lightest, darkest, num_colours)

    if equal_width:
        df["Colour_bin"] = pd.cut(df[col], bins=num_colours, labels=labels)
    else:
        df["Colour_bin"] = pd.qcut(df[col], bins=num_colours, labels=labels)

    return df

    