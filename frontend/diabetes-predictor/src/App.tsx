import './App.css'
import '@/styles/variables.css'
import Header from '@/components/layout/Header/Header'
import Footer from '@/components/layout/Footer/Footer'
import HomePageBody from '@/components/layout/HomePageBody/HomePageBody'

const App = () => {

  return (
    <>
      <Header />
      <HomePageBody />
      <Footer />
    </>
  )
}

export default App
