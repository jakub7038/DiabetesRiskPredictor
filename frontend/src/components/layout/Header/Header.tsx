import styles from './Header.module.css'
import Button from '@/components/ui/Button/Button'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'


const Header = () => {

    type NavLink = {
        label: string;
        href: string;
        requireAuth?: boolean;
        requireGuest?: boolean;
    };

    const links: NavLink[] = [
        { label: 'Oblicz ryzyko', href: '/predyktor-ryzyka' },
        { label: 'Logowanie', href: '/logowanie', requireGuest: true },
        { label: 'Rejestracja', href: '/rejestracja', requireGuest: true },
        { label: 'Moje konto', href: '/konto', requireAuth: true },
    ];

    const headerConfig: Record<
        string,
        { title: string; allowedLinks: string[] }
    > = {
        "/home": {
            title: "Predyktor ryzyka zachorowania na cukrzycę",
            allowedLinks: ["/predyktor-ryzyka", "/logowanie", "/rejestracja", "/konto"],
        },
        "/logowanie": {
            title: "Logowanie",
            allowedLinks: ["/rejestracja"],
        },
        "/rejestracja": {
            title: "Rejestracja",
            allowedLinks: ["/logowanie"],
        },
        "/predyktor-ryzyka": {
            title: "Oblicz ryzyko",
            allowedLinks: ["/logowanie", "/rejestracja", "/konto"],
        },
        "/konto": {
            title: "Konto",
            allowedLinks: ["/predyktor-ryzyka"]
        }
    };

    const { pathname } = useLocation();

    const config = headerConfig[pathname] ?? headerConfig["/home"];

    const { isLoggedIn, logout } = useAuth();

    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/home'); 
    };


    return (
        <header className={styles.header}>
            <Link to="/home"><h1 className={styles.h1}>Predyktor ryzyka zachorowania na cukrzyce</h1></Link>
            <nav>
                {links
                    .filter(link => {
                        const isAllowedOnPage = config.allowedLinks.includes(link.href)
                        if (!isAllowedOnPage) return false;

                        if (isLoggedIn) {
                            if (link.requireGuest) return false;
                        } else {
                            if (link.requireAuth) return false;
                        }

                        return true;
                    })
                    .map((link) => (
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
                    {isLoggedIn && (
                    <Button
                        className={styles.button}
                        size="md"
                        variant="secondary"
                        onClick={handleLogout} // Button musi obsługiwać onClick
                    >
                        Wyloguj
                    </Button>
                )}
            </nav>
        </header>
    )
}

export default Header