import React from 'react'
import ReactDOM from 'react-dom/client'
import Hero from './Hero/hero.jsx'
import Explore from './Explore/explore.jsx'
import Explain from './Explain/explain.jsx'
import CreateTrip2 from './tripcreator/createTrip2.jsx'
import Footer from './footer/footer.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Hero />
    <Explain />
    <Explore />
    <CreateTrip2 />
    <Footer />
  </React.StrictMode>,
)