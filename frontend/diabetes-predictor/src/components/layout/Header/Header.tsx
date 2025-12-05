import styles from './Header.module.css'
import Button from '@/components/ui/Button/Button'


const Header = () => {

    type NavLink = {
        label: string;
        href: string;
    };

    const links: NavLink[] = [
        { label: 'Oblicz ryzyko', href: '/' },
        { label: 'Logowanie', href: '/' },
        { label: 'Rejestracja', href: '/' },
    ];


    return (
        <header className={styles.header}>
            <h1>Kalkulator ryzyka zachorowania na cukrzyce</h1>
            <nav className="nav">
                {links.map((link) => (
                    <Button size={link.label === 'Oblicz ryzyko' ? 'lg' : 'md'} variant={link.label === 'Oblicz ryzyko' ? 'primary' : 'secondary'}>
                        <a
                        key={link.label}
                        href={link.href}
                        className=""
                        >
                        {link.label}
                        </a>
                    </Button>
                ))}
            </nav>
        </header>
    )
}

export default Header