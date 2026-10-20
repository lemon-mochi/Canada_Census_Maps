import { useState, useEffect, useMemo } from 'react';
import styles from '@/components/CensusForm.module.scss';
import {
  API_URL,
  CENSUS_YEARS,
  SOURCES,
  geoLevelsFor,
  COLUMN_LABELS,
  toApiYear,
  buildTree,
  getColourPalette,
  getColValue
} from '@/constants/Constants.jsx';

// Characteristics are static per year, so cache them for the session.
const characteristicsCache = new Map();

function useCharacteristics(apiYear) {
  const [state, setState] = useState({ chars: [], loading: true, error: null });

  useEffect(() => {
    const cached = characteristicsCache.get(apiYear);
    if (cached) {
      setState({ chars: cached, loading: false, error: null });
      return undefined;
    }

    const controller = new AbortController();
    // Clear stale data from the previous year right away.
    setState({ chars: [], loading: true, error: null });

    if (apiYear >= 1981) {
      async function load() {
        try {
          const res = await fetch(
            `${API_URL}/api/characteristics?census_year=${apiYear}`,
            { signal: controller.signal }
          );
          if (!res.ok) throw new Error(`HTTP ${res.status}`);

          const json = await res.json();
          const chars = Array.isArray(json) ? json : json.data || [];

          characteristicsCache.set(apiYear, chars);
          setState({ chars, loading: false, error: null });
        } catch (err) {
          if (err.name === 'AbortError') return;
          console.error('Failed to load census characteristics:', err);
          setState({
            chars: [],
            loading: false,
            error: `Couldn't load characteristics for ${apiYear}. Try again.`,
          });
        }
      }

      load();
    } else {
      console.log('here');
      const chars = [{
        CHARACTERISTIC_ID: 1,
        CHARACTERISTIC_NAME: `Population, ${apiYear}`,
        level: 0,
        columns: [{
          "column_id": 1,
          "column_name": "COUNT_TOTAL"
        }]
      }];
      characteristicsCache.set(apiYear, chars);
      setState({ chars, loading: false, error: null }); 
    }

    return () => controller.abort();
  }, [apiYear]);

  return state;
}

/* ------------------------------------------------------------------ */
/* Components                                                           */
/* ------------------------------------------------------------------ */

/*
 * `onSelect({ charId, columnId, columnName })` fires when a data button
 * is clicked.
 */

const MIN_COLOURS = 3;
const MAX_COLOURS = 10;

const CensusForm = ({
  censusYear,
  setCensusYear,
  geoLevel,
  setGeoLevel,
  charName,
  columnId,
  onSelect = () => {},
  onColourCountChange = () => {},
  onEqualWidthChange = () => {},
}) => {

  const { chars, loading, error } = useCharacteristics(toApiYear(censusYear));

  const [colourCount, setColourCount] = useState(5);
  const [equalWidth, setEqualWidth] = useState(true);

  const tree = useMemo(() => buildTree(chars), [chars]);
  const geoLevels = geoLevelsFor(censusYear);
  const source = SOURCES[censusYear];  

  const changeColourCount = (amount) => {
    setColourCount((prev) => {
      const next = Math.min(
        MAX_COLOURS,
        Math.max(MIN_COLOURS, prev + amount)
      );

      onColourCountChange(next);
      return next;
    });
  };  

  return (
    <div className={styles.censusForm}>
      <div className={styles.formGroup}>
        <h1>
          Canada Census Maps 🇨🇦
        </h1>
        <div className='link_to_github'>
          Check out the Github repository&nbsp;
          <a
            href="https://github.com/lemon-mochi/Canada_Census_Maps"
            target="_blank"
          >
            here
          </a>
        </div>

        <label htmlFor="census_year">Choose census year:</label>
        <select 
          id="census_year" 
          value={censusYear} 
          onChange={(e) => setCensusYear(e.target.value)} 
        >
          {CENSUS_YEARS.map((year) => (
            <option key={year} value={year}>
              {year}
            </option>
          ))}
        </select>
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="geo_level">Choose geographic level:</label>
        <select
          id="geo_level"
          value={geoLevel}
          onChange={(e) => setGeoLevel(e.target.value)}
        >
          {geoLevels.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      <br></br>

      {source && (
        <a
          className={styles.sourceLink}
          href={source}
          target="_blank"
          rel="noreferrer"
        >
          Source: Statistics Canada
        </a>
      )}

      <p>
        NOTICE: Not all characteristics are available for all geographic levels.
      </p>        

      {censusYear == 2011 && (
        <p>
          ADDITONAL NOTICE: 2011 National Household Survey (NHS) data is available for dissemination areas by selecting 2011 NHS DA for census year.
        </p>
      )}

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

      <p>
        Currently displaying: <br></br>
        Characteristic: {charName} <br></br>
        Value: {
          columnId != null
          ? getColValue(toApiYear(censusYear), columnId)
          : 'None'
          
        }
      </p>

      <h3>
        Button legend
      </h3>

      {(censusYear === "2021") && (
        <p>
          C1_T: C1_COUNT_TOTAL <br></br>
          C2_M: C2_COUNT_MEN+ <br></br>
          C3_F: C3_COUNT_WOMEN+ <br></br>
          C4_R: C10_RATE_TOTAL <br></br>
          C5_R: C11_RATE_MEN+ <br></br>
          C6_R: C12_RATE_WOMEN+
        </p>
      )}

      {(censusYear !== "2021") && (
        <p>
          C_T: COUNT_TOTAL <br></br>
          C_M: COUNT_MALE <br></br>
          C_F: COUNT_FEMALE <br></br>
          R_T: RATE_TOTAL <br></br>
          R_M: RATE_MALE <br></br>
          R_F: RATE_FEMALE
        </p>
      )}


      <h2 className={styles.heading}>Characteristics</h2>

      {loading && (
        <p className={styles.status} role="status">
          Loading characteristics…
        </p>
      )}
      {error && (
        <p className={styles.error} role="alert">
          {error}
        </p>
      )}

      <div className={styles.characteristics}>
        {tree.map((node) => (
          <CharacteristicNode
            key={node.CHARACTERISTIC_ID}
            node={node}
            onSelect={onSelect}
            colourCount={colourCount}
            equalWidth={equalWidth}
          />
        ))}
      </div>
    </div>
  );
};

const CharacteristicNode = ({ node, onSelect }) => {
  const [expanded, setExpanded] = useState(false);
  const hasChildren = node.children.length > 0;

  return (
    <div>
      <div
        className={styles.characteristicRow}
        style={{ paddingLeft: `${node.level * 20}px` }}
      >
        <div className={styles.characteristicName}>
          {hasChildren ? (
            <button
              type="button"
              className={styles.expandButton}
              onClick={() => setExpanded((prev) => !prev)}
              aria-expanded={expanded}
              aria-label={`${expanded ? 'Collapse' : 'Expand'} ${node.CHARACTERISTIC_NAME}`}
            >
              {expanded ? '▼' : '▶'}
            </button>
          ) : (
            <span className={styles.expandPlaceholder} />
          )}

          <span>{node.CHARACTERISTIC_NAME}</span>
        </div>

        <div 
          className={styles.dataButtons}
          style={{ '--button-count': node.columns.length }}
        >
          {node.columns.map((column) => (
            <button
              type="button"
              className={styles.dataButton}
              style={{ '--button-count': node.columns.length }}
              key={column.column_id}
              title={column.column_name}
              aria-label={`${node.CHARACTERISTIC_NAME}: ${column.column_name}`}
              onClick={() =>
                onSelect({
                  charId: node.CHARACTERISTIC_ID,
                  charName: node.CHARACTERISTIC_NAME,
                  columnId: column.column_id,
                  columnName: column.column_name,
                })
              }
            >
              {COLUMN_LABELS[column.column_name] ?? column.column_name}
            </button>
          ))}
        </div>
      </div>

      {expanded &&
        node.children.map((child) => (
          <CharacteristicNode
            key={child.CHARACTERISTIC_ID}
            node={child}
            onSelect={onSelect}
          />
        ))}
    </div>
  );
};

export default CensusForm;
