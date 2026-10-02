import React, { useState, useEffect, useMemo } from 'react';
import styles from '@/components/CensusForm.module.scss';

/* ------------------------------------------------------------------ */
/* Constants (outside the component so they aren't recreated per render) */
/* ------------------------------------------------------------------ */

// Vite: VITE_API_URL in .env. Next.js: NEXT_PUBLIC_API_URL. Falls back to local dev.
const API_URL =
  import.meta.env?.VITE_API_URL ??
  (typeof process !== 'undefined' ? import.meta.env?.NEXT_PUBLIC_API_URL : undefined) ??
  'http://localhost:8000';

const NHS_DA_LABEL = '2011 NHS DA';
// The backend uses 2010 to mean "2011 NHS dissemination areas".
const NHS_DA_API_YEAR = 2010;

const CENSUS_YEARS = [
  '1871', '1881', '1891', '1901', '1911', '1921', '1931', '1941', '1951',
  '1961', '1971', '1981', '1991', '1996', '2001', '2006', '2011', NHS_DA_LABEL,
  '2016', '2021',
];

const SOURCES = {
  2021: 'https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/index.cfm?Lang=E',
  2016: 'https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/index.cfm?Lang=E',
  2011: 'https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/index-eng.cfm',
  [NHS_DA_LABEL]: 'https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/index-eng.cfm',
  2006: 'https://www12.statcan.gc.ca/census-recensement/2006/index-eng.cfm',
  2001: 'https://www12.statcan.gc.ca/english/census01/home/Index.cfm',
  1996: 'https://www12.statcan.gc.ca/english/census01/info/census96.cfm',
  1991: 'https://www12.statcan.gc.ca/datasets/Index-eng.cfm?Temporal=1991',
  1986: 'https://www12.statcan.gc.ca/datasets/Index-eng.cfm?Temporal=1986',
  1981: 'https://www12.statcan.gc.ca/datasets/Index-eng.cfm?Temporal=1981',
};

const GEO_LEVELS_2021 = [
  { value: 'auto', label: 'Automatically decide based on zoom level' },
  { value: 'Province', label: 'Provinces/Territories' },
  { value: 'Census division', label: 'Census divisions' },
  { value: 'Census subdivision', label: 'Census subdivisions' },
  {
    value: 'Federal electoral district (2023 Representation Order)',
    label: 'Federal electoral districts (2023 Representation Order)',
  },
  {
    value: 'Federal electoral district (2013 Representation Order)',
    label: 'Federal electoral districts (2013 Representation Order)',
  },
  { value: 'Aggregate dissemination area', label: 'Aggregate dissemination areas' },
  { value: 'Dissemination area', label: 'Dissemination areas' },
];

// If available levels differ by year, branch on the year here.
const geoLevelsFor = (_censusYear) => GEO_LEVELS_2021;

const COLUMN_LABELS = {
  C1_COUNT_TOTAL: 'C1_T',
  'C2_COUNT_MEN+': 'C2_M',
  'C3_COUNT_WOMEN+': 'C3_F',
  C10_RATE_TOTAL: 'C4_R',
  'C11_RATE_MEN+': 'C5_R',
  'C12_RATE_WOMEN+': 'C6_R',
  COUNT_TOTAL: 'C_T',
  COUNT_MALE: 'C_M',
  COUNT_FEMALE: 'C_F',
  RATE_TOTAL: 'R_T',
  RATE_MALE: 'R_M',
  RATE_FEMALE: 'R_F',
};

const toApiYear = (censusYear) =>
  censusYear === NHS_DA_LABEL ? NHS_DA_API_YEAR : parseInt(censusYear, 10);

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
const buildTree = (characteristics) => {
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

// Characteristics are static per year, so cache them for the session.
const characteristicsCache = new Map();

function useCharacteristics(censusYear) {
  const [state, setState] = useState({ chars: [], loading: true, error: null });

  useEffect(() => {
    const cached = characteristicsCache.get(censusYear);
    if (cached) {
      setState({ chars: cached, loading: false, error: null });
      return undefined;
    }

    const controller = new AbortController();
    // Clear stale data from the previous year right away.
    setState({ chars: [], loading: true, error: null });

    async function load() {
      try {
        const res = await fetch(
          `${API_URL}/api/characteristics?census_year=${toApiYear(censusYear)}`,
          { signal: controller.signal }
        );
        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const json = await res.json();
        const chars = Array.isArray(json) ? json : json.data || [];

        characteristicsCache.set(censusYear, chars);
        setState({ chars, loading: false, error: null });
      } catch (err) {
        if (err.name === 'AbortError') return;
        console.error('Failed to load census characteristics:', err);
        setState({
          chars: [],
          loading: false,
          error: `Couldn't load characteristics for ${censusYear}. Try again.`,
        });
      }
    }

    load();
    return () => controller.abort();
  }, [censusYear]);

  return state;
}

/* ------------------------------------------------------------------ */
/* Components                                                           */
/* ------------------------------------------------------------------ */

/*
 * `onSelect({ charId, columnId, columnName })` fires when a data button
 * is clicked.
 */
const CensusForm = ({ onSelect = () => {} }) => {
  const [censusYear, setCensusYear] = useState('2021');
  const [geoLevel, setGeoLevel] = useState('auto');

  const { chars, loading, error } = useCharacteristics(censusYear);

  const tree = useMemo(() => buildTree(chars), [chars]);
  const geoLevels = geoLevelsFor(censusYear);
  const source = SOURCES[censusYear];

  return (
    <div className={styles.censusForm}>
      <div className={styles.formGroup}>
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

      {source && (
        <a
          className={styles.sourceLink}
          href={source}
          target="_blank"
          rel="noreferrer"
        >
          Source
        </a>
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

        <div className={styles.dataButtons}>
          {node.columns.map((column) => (
            <button
              type="button"
              className={styles.dataButton}
              key={column.column_id}
              title={column.column_name}
              aria-label={`${node.CHARACTERISTIC_NAME}: ${column.column_name}`}
              onClick={() =>
                onSelect({
                  charId: node.CHARACTERISTIC_ID,
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
