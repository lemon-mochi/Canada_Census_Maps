import styles from '@/components/YearGeoForm.module.scss';
import {
  CENSUS_YEARS
} from '@/constants/CensusYears.jsx';

const YearGeoForm = ({
    censusYear,
    setCensusYear,
    geoLevel,
    setGeoLevel,
    geoLevels
}) => {
    return (
    <>
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
    </>
    );
};

export default YearGeoForm;