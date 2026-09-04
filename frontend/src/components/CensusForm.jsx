import React, { useState, useEffect } from 'react';
import styles from '@/components/CensusForm.module.scss';

const CensusForm = () => {
  const [censusYear, setCensusYear] = useState('2021');
  const [geoLevel, setGeoLevel] = useState('auto');
  const [chars, setChars] = useState([]);
  const [source, setSource] = useState(
    'https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/index.cfm?Lang=E'
  );

  const censusYears = [
    '1871', '1881', '1891', '1901', '1911', '1921', '1931', '1941', '1951',
    '1961', '1971', '1981', '1991', '1996', '2001', '2006', '2011',
    '2016', '2021'
  ];

  const geoLevels_2021 = [
    { value: 'auto', label: 'Automatically decide based on zoom level' },
    { value: 'Province', label: 'Provinces/Territories' },
    { value: 'Census division', label: 'Census divisions' },
    { value: 'Census subdivision', label: 'Census subdivisions' },
    {
      value: 'Federal electoral district (2023 Representation Order)',
      label: 'Federal electoral districts (2023 Representation Order)'
    },
    {
      value: 'Federal electoral district (2013 Representation Order)',
      label: 'Federal electoral districts (2013 Representation Order)'
    },
    {
      value: 'Aggregate dissemination area',
      label: 'Aggregate dissemination areas'
    },
    {
      value: 'Dissemination area',
      label: 'Dissemination areas'
    },
  ];

  // Fetch characteristics
  useEffect(() => {
    async function getCharacteristics() {
      try {
        const res = await fetch(
          `http://localhost:8000/api/characteristics`
        );

        const json = await res.json();

        setChars(Array.isArray(json) ? json : json.data || []);
      } catch (err) {
        console.error(
          'Failed to load census characteristics:',
          err
        );
      }
    }

    getCharacteristics();
  }, [censusYear]);


  /*
   * Convert the flat list returned by the backend into a tree.
   *
   * Example:
   *
   * Population
   *   Age groups
   *     0 to 14
   *       0 to 4
   *
   * becomes:
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
      const level = getIndentLevel(char.CHARACTERISTIC_NAME);

      const node = {
        ...char,
        name: char.CHARACTERISTIC_NAME.trim(),
        level,
        children: []
      };

      // Remove parents from stack when moving back up
      while (
        stack.length > 0 &&
        stack[stack.length - 1].level >= level
      ) {
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


  const getIndentLevel = (name) => {
    const leadingSpaces = name.match(/^ */)[0].length;

    return Math.floor(leadingSpaces / 2);
  };


  const tree = buildTree(chars);


  return (
    <div className={styles.censusForm}>

      {/* Census Year */}
      <div className={styles.formGroup}>
        <label htmlFor="census_year">
          Choose census year:
        </label>

        <select
          id="census_year"
          value={censusYear}
          onChange={(e) => setCensusYear(e.target.value)}
        >
          {censusYears.map((year) => (
            <option key={year} value={year}>
              {year}
            </option>
          ))}
        </select>
      </div>


      {/* Geographic Level */}
      <div className={styles.formGroup}>
        <label htmlFor="geo_level">
          Choose geographic level:
        </label>

        <select
          id="geo_level"
          value={geoLevel}
          onChange={(e) => setGeoLevel(e.target.value)}
        >
          {geoLevels_2021.map((option) => (
            <option
              key={option.value}
              value={option.value}
            >
              {option.label}
            </option>
          ))}
        </select>
      </div>


      <a
        href={source}
        target="_blank"
        rel="noreferrer"
      >
        Source
      </a>


      {/* Characteristics */}
      <div className={styles.characteristics}>

        <div className={styles.characteristicsHeader}>
          <div className={styles.characteristicName}>
            Characteristic
          </div>

          <div>Count Total</div>
          <div>Count Men+</div>
          <div>Count Women+</div>
          <div>Rate Total</div>
          <div>Rate Men+</div>
          <div>Rate Women+</div>
        </div>


        {tree.map((node) => (
          <CharacteristicNode
            key={node.CHARACTERISTIC_ID}
            node={node}
          />
        ))}

      </div>

    </div>
  );
};


/*
 * Individual characteristic/tree node
 */
const CharacteristicNode = ({ node }) => {

  const [expanded, setExpanded] = useState(false);

  const hasChildren = node.children.length > 0;


  return (
    <div>

      <div
        className={styles.characteristicRow}
        style={{
          paddingLeft: `${node.level * 20}px`
        }}
      >

        {/* Name */}
        <div className={styles.characteristicName}>

          {hasChildren ? (
            <button
              className={styles.expandButton}
              onClick={() => setExpanded(!expanded)}
            >
              {expanded ? '▼' : '▶'}
            </button>
          ) : (
            <span className={styles.expandPlaceholder} />
          )}

          <span>
            {node.name}
          </span>

        </div>


        {/* Buttons */}
        <button>Count</button>
        <button>Men+</button>
        <button>Women+</button>
        <button>Rate</button>
        <button>Men+</button>
        <button>Women+</button>

      </div>


      {/* Children */}
      {expanded &&
        node.children.map((child) => (
          <CharacteristicNode
            key={child.CHARACTERISTIC_ID}
            node={child}
          />
        ))
      }

    </div>
  );
};

export default CensusForm;