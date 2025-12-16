import type { AuthCredentials, PredictionInput, PredictionResult } from '@/types';

const AUTH_URL = '/api';


export const authService = {
  
  // --- REJESTRACJA ---
  register: async (data: AuthCredentials) => {
    const response = await fetch(`${AUTH_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    
    const result = await response.json();
    if (!response.ok) throw new Error(result.msg || 'Błąd rejestracji');
    return result;
  },

  // --- LOGOWANIE ---
  login: async (data: AuthCredentials) => {
    const response = await fetch(`${AUTH_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    if (!response.ok) throw new Error(result.msg || 'Błąd logowania');

    // ZAPISZ TOKENY DO LOCALSTORAGE
    // Zakładam, że Twoja funkcja login_user zwraca słownik z access_token
    if (result.data && result.data.access_token) {
      localStorage.setItem('accessToken', result.data.access_token);
      // Opcjonalnie refresh token, jeśli go zwracasz
      if (result.data.refresh_token) {
        localStorage.setItem('refreshToken', result.data.refresh_token);
      }
    }
    return result;
  },

  // --- WYLOGOWANIE (Frontend only) ---
  logout: () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    // Tutaj można dodać przekierowanie, np. window.location.href = '/login';
  },

  // --- PREDICTION (Jest w auth_bp, więc dajemy tutaj) ---
  predict: async (data: PredictionInput): Promise<PredictionResult> => {
    const token = localStorage.getItem('accessToken'); 
    
    const headers: HeadersInit = { 
        'Content-Type': 'application/json' 
    };

    if (token && token !== "null" && token !== "undefined") {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${AUTH_URL}/predict`, {
      method: 'POST',
      headers: headers, 
      body: JSON.stringify(data),
    });

    const result = await response.json();
    
    // Obsługa wygasłego tokena (401)
    if (response.status === 401) {
       authService.logout();
       throw new Error("Sesja wygasła. Zaloguj się ponownie.");
    }

    if (response.status === 422) {
       localStorage.removeItem('accessToken');
       throw new Error("Błąd autoryzacji. Spróbuj ponownie.");
    }

    if (!response.ok) throw new Error(result.msg || 'Błąd predykcji');
    return result;
  },
  // Pomocnik do sprawdzania czy user jest zalogowany
  isAuthenticated: () => {
    return !!localStorage.getItem('accessToken');
  }
};