import React from 'react';
import styles from './Button.module.css';

type ButtonVariant = 'primary' | 'secondary' | 'outline';
type ButtonSize = 'sm' | 'md' | 'lg';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
}

export const Button = ({
  children,
  className = '',
  variant = 'primary', // Domyślny wariant
  size = 'md',         // Domyślny rozmiar
  ...props             // Reszta propsów (onClick, id, style itp.)
}: ButtonProps) => {
  
  // Łączenie klas CSS w jeden ciąg znaków
  // styles.button - klasa bazowa
  // styles[variant] - klasa dynamiczna zależna od wariantu
  // styles[size] - klasa dynamiczna zależna od rozmiaru
  const classNames = [
    styles.button,
    styles[variant],
    styles[size],
    className // Pozwala na nadpisanie stylów z zewnątrz
  ].join(' ');

  return (
    <button className={classNames} {...props}>
      {children}
    </button>
  );
};
export default Button