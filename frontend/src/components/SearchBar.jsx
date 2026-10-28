import styles from '@/components/SearchBar.module.scss';
import { updateSearchQuery } from '@/constants/updateSearchQuery.js';

const SearchBar = ({ value, setSearchQuery }) => {
  return (
    <div className={styles.searchBar}>
      <label htmlFor="characteristic-search" className={styles.srOnly}>
        Search characteristics
      </label>

      <input
        type="search"
        id="characteristic-search"
        value={value}
        onChange={(e) => updateSearchQuery(e.target.value, setSearchQuery)}
        placeholder="Search characteristics..."
      />
    </div>
  );
};

export default SearchBar;