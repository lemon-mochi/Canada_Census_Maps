import { useState, useEffect, useMemo } from 'react';
import styles from '@/components/CensusForm.module.scss';
import {
  SOURCES,
  geoLevelsFor,
  toApiYear
} from '@/constants/CensusYears.jsx';
import { getColValue } from '@/constants/Columns.jsx';
import { buildTree } from '@/constants/DataHelpers.jsx';
import { getFavicon } from '@/constants/Favicons';
import CharacteristicNode from '@/components/CharacteristicNode.jsx';
import { 
  useCharacteristics,
  filterTree
} from '@/constants/useCharacteristics.js';
import {
  MAX_COLOURS,
  MIN_COLOURS
} from '@/constants/DataHelpers.jsx';
import SearchBar from '@/components/SearchBar.jsx';
import YearGeoForm from '@/components/YearGeoForm.jsx';
import ColourControl from '@/components/ColourControl.jsx';

/*
 * `onSelect({ charId, columnId, columnName })` fires when a data button
 * is clicked.
 */

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
  const [searchQuery, setSearchQuery] = useState('');

  const filteredTree = useMemo(
    () => filterTree(tree, searchQuery),
    [tree, searchQuery]
  );

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

  useEffect(() => {
    const favicon = document.querySelector("link[rel='icon']");

    if (favicon) {
      favicon.href = getFavicon(toApiYear(censusYear));
    }
  }, [censusYear]);

  return (
    <div className={styles.censusForm}>
      <YearGeoForm
        censusYear={censusYear}
        setCensusYear={setCensusYear}
        geoLevel={geoLevel}
        setGeoLevel={setGeoLevel}
        geoLevels={geoLevels}
      />

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
        NOTICE: Not all characteristics are available for all geographic levels. See the&nbsp;
          <a 
            href='https://github.com/lemon-mochi/Canada_Census_Maps/blob/main/docs/Missing_Characteristics.md'
            target='_blank'
          >
            documentation
          </a>
          &nbsp;for more information.
      </p>        

      {censusYear == 2011 && (
        <p>
          ADDITONAL NOTICE: 2011 National Household Survey (NHS) data is available for dissemination areas by selecting 2011 NHS DA for census year.
        </p>
      )}

      <ColourControl
        colourCount={colourCount}
        changeColourCount={changeColourCount}
        equalWidth={equalWidth}
        setEqualWidth={setEqualWidth}
        onEqualWidthChange={onEqualWidthChange}
      />

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

      <SearchBar
        value={searchQuery}
        setSearchQuery={setSearchQuery}
      />

      <div className={styles.characteristics}>
        {filteredTree.length > 0 ? (
          filteredTree.map((node) => (
            <CharacteristicNode
              key={node.CHARACTERISTIC_ID}
              node={node}
              onSelect={onSelect}
              colourCount={colourCount}
              equalWidth={equalWidth}
              searching={searchQuery.trim().length > 0}
            />
          ))
        ) : (
          <p>No matching characteristics found.</p>
        )}
      </div>
    </div>
  );
};

export default CensusForm;
