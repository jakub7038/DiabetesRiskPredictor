import styles from './Footer.module.css'


const Footer = () => {

    return (
        <>
            <footer className={styles.footer}>
                
                <p>© 2025 Predyktor ryzyka zachorowania na cukrzyce</p>

                <p>Uwaga: Wynik uzyskany w kalkulatorze ma charakter wyłącznie informacyjny i edukacyjny. Nie zastępuje profesjonalnej porady medycznej, diagnozy ani leczenia. W przypadku jakichkolwiek wątpliwości dotyczących zdrowia, zawsze skonsultuj się z lekarzem pierwszego kontaktu lub diabetologiem.</p>

            </footer>
        </>
    )
}

export default Footer