import { useState, useEffect } from 'react';
import { API_URL } from '@/constants/ApiURL.jsx';

// Characteristics are static per year, so cache them for the session.
const characteristicsCache = new Map();

export function useCharacteristics(apiYear) {
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

export function filterTree(nodes, query) {
  if (!query.trim()) return nodes;

  const search = query.toLowerCase();

  return nodes.reduce((filtered, node) => {
    const children = filterTree(node.children ?? [], query);

    const name = String(
      node.CHARACTERISTIC_NAME ?? ''
    ).toLowerCase();

    const matches = name.includes(search);

    if (matches || children.length > 0) {
      filtered.push({
        ...node,
        children,
        matchesSearch: matches,
        expanded: true,
      });
    }

    return filtered;
  }, []);
}