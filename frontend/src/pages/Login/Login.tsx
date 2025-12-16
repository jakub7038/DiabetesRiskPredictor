import { useState } from 'react';
import AuthWrapper from '@/components/layout/AuthWrapper/AuthWrapper';
import Input from '@/components/ui/Input/Input';
import Button from '@/components/ui/Button/Button';
import { Link, useNavigate } from 'react-router-dom';
import { authService } from '@/api/authService';
import { useAuth } from '@/context/AuthContext';

const Login = () => {
  const navigate = useNavigate(); 
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null); 
  const [isLoading, setIsLoading] = useState(false); 
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
    if (error) setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const result = await authService.login(formData);
      
      console.log(result)

      if (result.data && result.data.access_token) {
          
          const userData = result.data.user || { id: '0', email: formData.email }; 
          
          login(result.data.access_token, userData);
          
          navigate('/konto');
      }
      
    } catch (err: any) {
      console.error(err);
      setError("Nieprawidłowy email lub hasło.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
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
                {isLoading ? 'Logowanie...' : 'Zaloguj się'}
            </Button> 
            </div>

            <p style={{ marginTop: '15px', fontSize: '0.9rem' }}>
            Nie masz konta? <Link to="/rejestracja" style={{ color: 'var(--color-secondary)', fontWeight: 'bold' }}>Zarejestruj się</Link>
            </p>

        </form>
        </AuthWrapper>
  );
};

export default Login;