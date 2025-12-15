import styles from './Input.module.css';

type InputProps = {
  label: string;
  type?: 'text' | 'password' | 'email' | 'number';
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  error?: string; 
};

const Input = ({ label, type = 'text', name, value, onChange, placeholder, error }: InputProps) => {
  return (
    <div className={styles.container}>
      <label htmlFor={name} className={styles.label}>
        {label}
      </label>
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className={`${styles.input} ${error ? styles.inputError : ''}`}
      />

      {error && <span className={styles.errorMessage}>{error}</span>}
    </div>
  );
};

export default Input;