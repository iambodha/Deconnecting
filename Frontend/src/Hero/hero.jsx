import React, { useState } from 'react';
import './hero.css';
import heroImage from '../assets/bghero.jpg'; // import hero image (dont forget to implement changing each day)
import logoImage from '../assets/Deconnectingtextlogo-removebg-preview.png';

function Hero() {
  const [hover, setHover] = useState(false);

  return (
    <div className='heromainContainer'>
      <nav className="navbar">
        <div className="navbar-logo">
          <a href="#"><img src={logoImage} alt="Logo" /></a>
        </div>
        <ul className="navbar-items">
          <li className='archivo navitem'>Destinations</li>
          <li className='archivo navitem'>Travel Styles</li>
          <li className='archivo navitem'>About Us</li>
          <div className='special-button'>
            <i className="uil uil-envelope-search"></i>
            <span className='archivo special'>Create!</span>
          </div>
        </ul>
      </nav>

      <div className='heroContainer'>
        <img src={heroImage} alt="Hero Image" />
        <div className='textOverlay'>
          <h1 className='heroTitle lora'>Find unforgettable trips</h1>
          <p>Go to places you would have never thought about with Deconnecting.</p>
        </div>
        <div className='whereTake'>
          <i className="uil uil-globe"></i>
          <h2 className='archivo whereText'></h2>
        </div>
      </div>
    </div>
  );
}

export default Hero;
