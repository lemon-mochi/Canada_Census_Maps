import { useState } from 'react';
import styles from '@/components/CharacteristicNode.module.scss';
import {
  COLUMN_LABELS,
} from '@/constants/Columns.jsx';


const CharacteristicNode = ({ node, onSelect }) => {
  const [expanded, setExpanded] = useState(false);
  const hasChildren = node.children.length > 0;

  return (
    <div style={{ width: '100%', minWidth: 0 }}>
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

export default CharacteristicNode;