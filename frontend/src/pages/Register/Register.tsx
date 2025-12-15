import { useState } from 'react';
import AuthWrapper from '@/components/layout/AuthWrapper/AuthWrapper';
import Input from '@/components/ui/Input/Input';
import Button from '@/components/ui/Button/Button';
import { Link } from 'react-router-dom';

const Register = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirmPassword: ''
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (formData.password !== formData.confirmPassword) {
            alert("Hasła nie są takie same!");
            return;
        }
        console.log('Rejestracja:', formData);
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