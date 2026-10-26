import styles from '@/components/SearchBar.module.scss';

const SearchBar = ({ value, onChange }) => {
  return (
    <div className={styles.searchBar}>
      <label htmlFor="characteristic-search" className={styles.srOnly}>
        Search characteristics
      </label>

      <input
        type="search"
        id="characteristic-search"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search characteristics..."
      />
    </div>
  );
};

export default SearchBar;