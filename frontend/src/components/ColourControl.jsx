import styles from '@/components/ColourControl.module.scss';
import { getColourPalette } from '@/constants/DataHelpers.jsx';
import {
  MAX_COLOURS,
  MIN_COLOURS
} from '@/constants/DataHelpers.jsx';

const ColourControl = ({
    colourCount,
    changeColourCount,
    equalWidth,
    setEqualWidth,
    onEqualWidthChange
}) => {
    return (
      <>
        <div className={styles.legendSection}>
            <div className={styles.legendHeader}>
            <span>Map colours:</span>

            <div className={styles.colourCountControl}>
                <button
                type="button"
                onClick={() => changeColourCount(-1)}
                disabled={colourCount === MIN_COLOURS}
                aria-label="Decrease number of colours"
                >
                −
                </button>

                <span>{colourCount}</span>

                <button
                type="button"
                onClick={() => changeColourCount(1)}
                disabled={colourCount === MAX_COLOURS}
                aria-label="Increase number of colours"
                >
                +
                </button>
            </div>
            </div>

            <div className={styles.colourLegend}>
            {getColourPalette(colourCount).map((colour, index) => (
                <span
                key={index}
                className={styles.legendColour}
                style={{
                    backgroundColor: `rgb(${colour[0]}, ${colour[1]}, ${colour[2]})`,
                }}
                />
            ))}
            </div>
        </div>

        <div className={styles.colourMethodControl}>
            <label>
            <input
                type="radio"
                name="colourMethod"
                checked={equalWidth}
                onChange={() => {
                setEqualWidth(true);
                onEqualWidthChange(true);
                }}
            />
            Equal width
            </label>

            <label>
            <input
                type="radio"
                name="colourMethod"
                checked={!equalWidth}
                onChange={() => {
                setEqualWidth(false);
                onEqualWidthChange(false);
                }}
            />
            Equal frequency
            </label>
        </div>      
      </>
    );
};

export default ColourControl;