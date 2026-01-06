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
  [key: string]: any; 
}

export interface ModelPrediction {
  prediction: number;
  probabilities: {
    class_0: number;
    class_1: number;
    class_2: number;
  };
  confidence: number;
}

export interface PredictionResult {
  msg: string;
  predictions: {
    logistic?: ModelPrediction;
    random_forest?: ModelPrediction;
    gradient_boost?: ModelPrediction;
  };
  is_saved: boolean;
  // Stare pola dla backward compatibility (opcjonalne)
  result?: number; 
  probability?: number; 
}

export interface DailyLog {
  id?: number;
  date?: string; 
  ate_fruit?: boolean;
  ate_veggie?: boolean;
  physical_activity?: boolean;
  alcohol_drinks?: number;
  bad_mental_day?: boolean;
  bad_physical_day?: boolean;
  weight?: number;
  height?: number;
}