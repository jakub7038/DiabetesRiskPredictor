import styles from './AuthWrapper.module.css';

type AuthWrapperProps = {
  children: React.ReactNode; 
  title: string;
};

const AuthWrapper = ({ children, title }: AuthWrapperProps) => {
  return (
    <div className={styles.wrapper}>
      <div className={styles.card}>
        <h2 className={styles.title}>{title}</h2>
        {children}
      </div>
    </div>
  );
};

export default AuthWrapper;