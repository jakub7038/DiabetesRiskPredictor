import { useState } from 'react';
import AuthWrapper from '@/components/layout/AuthWrapper/AuthWrapper';
import Input from '@/components/ui/Input/Input';
import Button from '@/components/ui/Button/Button';
import { Link, useNavigate } from 'react-router-dom';
import { authService } from '@/api/authService';

const Register = () => {
    const navigate = useNavigate();
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirmPassword: ''
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        // Walidacja frontendowa
        if (formData.password !== formData.confirmPassword) {
            setError("Hasła nie są takie same!");
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            // Wysyłamy tylko email i hasło (bez confirmPassword)
            await authService.register({
                email: formData.email,
                password: formData.password
            });

            // Sukces
            alert("Konto zostało założone! Możesz się teraz zalogować.");
            navigate('/logowanie'); // Przekierowanie do logowania

        } catch (err: any) {
            console.error(err);
            // Jeśli backend zwraca konkretny komunikat (np. "User already exists"), warto go wyświetlić
            // Zakładając, że authService rzuca Error z wiadomością:
            setError(err.message || "Wystąpił błąd podczas rejestracji.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
            <AuthWrapper title="Załóż konto">
                <form onSubmit={handleSubmit}>
                    <Input
                        label="Adres Email"
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                    />
                    <Input
                        label="Hasło"
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                    />
                    <Input
                        label="Powtórz hasło"
                        type="password"
                        name="confirmPassword"
                        value={formData.confirmPassword}
                        onChange={handleChange}
                    />

                    <div style={{ marginTop: '20px' }}>
                        <Button size="lg" variant="primary">Zarejestruj się</Button>
                    </div>

                    <p style={{ marginTop: '15px', fontSize: '0.9rem' }}>
                        Masz już konto? <Link to="/logowanie">Zaloguj się</Link>
                    </p>
                </form>
            </AuthWrapper>
    );
};

export default Register;