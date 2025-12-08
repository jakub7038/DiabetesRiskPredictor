import { useState } from 'react';
import AuthWrapper from '@/components/layout/AuthWrapper/AuthWrapper';
import Input from '@/components/ui/Input/Input';
import Button from '@/components/ui/Button/Button';
import { Link } from 'react-router-dom';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value 
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Dane do wysłania:', formData);
  };

  return (

    <main>
        <AuthWrapper title="Zaloguj się">
        <form onSubmit={handleSubmit}>
            
            <Input
            label="Adres Email"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="np. jan@kowalski.pl"
            />

            <Input
            label="Hasło"
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="*******"
            />

            <div style={{ marginTop: '20px' }}>
            <Button size="lg" variant="primary">
                Zaloguj się
            </Button> 
            </div>

            <p style={{ marginTop: '15px', fontSize: '0.9rem' }}>
            Nie masz konta? <Link to="/rejestracja" style={{ color: 'var(--color-secondary)', fontWeight: 'bold' }}>Zarejestruj się</Link>
            </p>

        </form>
        </AuthWrapper>
    </main>
  );
};

export default Login;