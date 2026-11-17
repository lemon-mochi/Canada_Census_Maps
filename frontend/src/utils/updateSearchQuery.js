const MAX_LEN = 100;


export function updateSearchQuery(searchQuery, setSearchQuery) {
    if (searchQuery.length > MAX_LEN) {
        return;
    }

    setSearchQuery(searchQuery);
}