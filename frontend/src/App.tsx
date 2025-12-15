import '@/styles/variables.css'
import Header from '@/components/layout/Header/Header'
import Footer from '@/components/layout/Footer/Footer'
import Home from '@/pages/Home/Home'
import Login from '@/pages/Login/Login'
import Register from '@/pages/Register/Register'
import RiskPredictor from '@/pages/RiskPredictor/RiskPredictor'

import { Routes, Route } from 'react-router-dom'

const App = () => {

  return (
    <>
      <Header />

      <main>
        <Routes>

          <Route path="/home" element={<Home />} />
          <Route path="/logowanie" element={<Login />} />
          <Route path="/rejestracja" element={<Register />} />
          <Route path='/predyktor-ryzyka' element={<RiskPredictor />}></Route>
        
          <Route path="/" element={<Home />} />
        </Routes>
      </main>
      <Footer />
    </>
  )
}

export default App
