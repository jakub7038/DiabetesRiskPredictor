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
            await authService.register({
                email: formData.email,
                password: formData.password
            });
            alert("Konto zostało założone! Możesz się teraz zalogować.");
            navigate('/logowanie');

        } catch (err: any) {
            console.error(err);
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


                {error && (
                    <div style={{
                        color: 'white',
                        backgroundColor: '#ff4d4f',
                        padding: '10px',
                        borderRadius: '4px',
                        marginBottom: '10px',
                        fontSize: '0.9rem'
                    }}>
                        {error}
                    </div>
                )}

                <div style={{ marginTop: '20px' }}>
                    <Button size="lg" variant="primary" disabled={isLoading}>
                        {isLoading ? 'Rejestracja...' : 'Zarejestruj się'}
                    </Button>
                </div>

                <p style={{ marginTop: '15px', fontSize: '0.9rem' }}>
                    Masz już konto? <Link to="/logowanie">Zaloguj się</Link>
                </p>
            </form>
        </AuthWrapper>
    );
};

export default Register;