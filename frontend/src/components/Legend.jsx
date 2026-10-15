import styles from '@/components/Legend.module.scss';
import { getColourPalette } from '@/constants/Constants.jsx';

export default function Legend({
    title = 'Population',
    boundaries = [],
    colourCount
}) {
    if (boundaries.length < 2) return null;

    const intervalCount = boundaries.length - 1;
    const colours = getColourPalette(intervalCount);

    const formatValue = (value) =>
        new Intl.NumberFormat('en-CA', {
            notation: 'compact',
            maximumFractionDigits: 2,
        }).format(value);

    return (
        <div className={styles.legend}>
            <h4>{title}</h4>

            {boundaries.slice(0, -1).map((lower, i) => {
                const upper = boundaries[i + 1];

                const label =
                    i === 0
                        ? `≤ ${formatValue(upper)}`
                        : i === boundaries.length - 2
                            ? `${formatValue(lower)}+`
                            : `${formatValue(lower)} – ${formatValue(upper)}`;
                
                const colour = colours[i];

                if (!colour) return null;

                const backgroundColor = `rgb(${colour.join(', ')})`;

                return (
                    <div key={i} className={styles.legendItem}>
                        <span
                            className={styles.legendColour}
                            style={{ backgroundColor }}
                        />
                        <span>{label}</span>
                    </div>
                );
            })}
        </div>
    );
}