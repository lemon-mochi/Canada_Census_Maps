import styles from '@/components/Legend.module.scss';

export default function Legend() {
    return (

    <div className={styles.legend}>
        <h4>2021 Population</h4>
        <div className={styles.legendItem}> &lt; 100,000</div>
        <div className={styles.legendItem}> 100,000 – 1,000,000</div>
        <div className={styles.legendItem}> 1,000,000 – 4,000,000</div>
        <div className={styles.legendItem}> 4,000,000 – 8,000,000</div>
        <div className={styles.legendItem}> 8,000,000+</div>
    </div>


    );
}
