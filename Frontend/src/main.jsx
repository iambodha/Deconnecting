import React from 'react'
import ReactDOM from 'react-dom/client'
import Hero from './Hero/hero.jsx'
import Explore from './Explore/explore.jsx'
import Explain from './Explain/explain.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Hero />
    <Explore />
    <Explain />
  </React.StrictMode>,
)
