import styles from './Header.module.css'
import Button from '@/components/ui/Button/Button'
import { Link } from 'react-router-dom' 


const Header = () => {

    type NavLink = {
        label: string;
        href: string;
    };

    const links: NavLink[] = [
        { label: 'Oblicz ryzyko', href: '/predyktor-ryzyka' },
        { label: 'Logowanie', href: '/logowanie' },
        { label: 'Rejestracja', href: '/rejestracja' },
    ];


    return (
        <header className={styles.header}>
            <Link to="/home"><h1 className={styles.h1}>Predyktor ryzyka zachorowania na cukrzyce</h1></Link>
            <nav>
                {links.map((link) => (
                    <Link key={link.label} to={link.href} style={{ textDecoration: 'none' }}>
                        <Button 
                            className={styles.button} 
                            size={link.label === 'Oblicz ryzyko' ? 'lg' : 'md'} 
                            variant={link.label === 'Oblicz ryzyko' ? 'primary' : 'secondary'}
                        >
                            {link.label}
                        </Button>
                    </Link>
                ))}
            </nav>
        </header>
    )
}

export default Header