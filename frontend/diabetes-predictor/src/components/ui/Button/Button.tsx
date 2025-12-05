import React from 'react';
import styles from './Button.module.css';

type ButtonVariant = 'primary' | 'secondary' | 'outline';
type ButtonSize = 'sm' | 'md' | 'lg';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
}

const Button = ({
  children,
  className = '',
  variant = 'primary', 
  size = 'md',         
  ...props             
}: ButtonProps) => {
  

  const classNames = [
    styles.button,
    styles[variant],
    styles[size],
    className 
  ].join(' ');

  return (
    <button className={classNames} {...props}>
      {children}
    </button>
  );
};
export default Button