import '@/styles/variables.css'
import Header from '@/components/layout/Header/Header'
import Footer from '@/components/layout/Footer/Footer'
import Home from '@/pages/Home/Home'
import Login from '@/pages/Login/Login'
import Register from '@/pages/Register/Register'
import RiskPredictor from '@/pages/RiskPredictor/RiskPredictor'
import UserProfile from '@/pages/UserProfile/UserProfile'
import PredictionResult from '@/pages/PredictionResult/PredictionResult'
import History from '@/pages/History/History'


import { Routes, Route } from 'react-router-dom'
import ProtectedRoute from '@/components/auth/ProtectedRoute'
import PublicRoute from '@/components/auth/PublicRoute'

const App = () => {

  return (
    <>
      <Header />

      <main>
        <Routes>

          {/* Public routes */}
          <Route path="/home" element={<Home />} />
          <Route path="/" element={<Home />} />
          <Route path='/predyktor-ryzyka' element={<RiskPredictor />}></Route>
          <Route path='/wynik' element={<PredictionResult />}></Route>

          {/* Guest only routes */}
          <Route path="/logowanie" element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          } />
          <Route path="/rejestracja" element={
            <PublicRoute>
              <Register />
            </PublicRoute>
          } />

          {/* Protected routes */}
          <Route path="/historia" element={
            <ProtectedRoute>
              <History />
            </ProtectedRoute>
          } />

          <Route path='/konto' element={
            <ProtectedRoute>
              <UserProfile />
            </ProtectedRoute>
          }></Route>

        </Routes>
      </main>
      <Footer />
    </>
  )
}

export default App
