export interface AuthCredentials {
  email: string;
  password?: string;
}

export interface LoginResponse {
  msg: string;
  data: {
    access_token: string;
    refresh_token: string;
    user: {
      id: number;
      email: string;
    };
  };
}

export interface PredictionInput {
  // Tutaj wpisz pola, których wymaga Twoja funkcja predict_diabetes_risk
  // np. age, gender, bmi, bp, etc.
  [key: string]: any; 
}


export interface PredictionResult {
  msg: string;
  result: number; // np. 0 lub 1
  probability: number; // np. 0.85
}

export interface DailyLog {
  id?: number;
  date?: string; // YYYY-MM-DD
  ate_fruit?: boolean;
  ate_veggie?: boolean;
  physical_activity?: boolean;
  alcohol_drinks?: number;
  bad_mental_day?: boolean;
  bad_physical_day?: boolean;
  weight?: number;
  height?: number;
}