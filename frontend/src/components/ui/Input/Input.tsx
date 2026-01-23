import styles from './Input.module.css';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  suffix?: React.ReactNode;
}

const Input = ({ label, className = '', error, suffix, ...props }: InputProps) => {
  return (
    <div className={styles.container}>
      {label && (
        <label htmlFor={props.name} className={styles.label}>
          {label}
        </label>
      )}
      <div className={styles.inputWrapper}>
        <input
          id={props.name}
          className={`${styles.input} ${error ? styles.inputError : ''} ${className}`}
          {...props}
        />
        {suffix && <div className={styles.suffix}>{suffix}</div>}
      </div>

      {error && <span className={styles.errorMessage}>{error}</span>}
    </div>
  );
};

export default Input;