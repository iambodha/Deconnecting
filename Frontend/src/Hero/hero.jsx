import React, { useState } from 'react';
import './hero.css';
import heroImage from '../assets/bgimage2.jpg'; // hero img header
import logoImage from '../assets/Deconnectingtextlogo-removebg-preview.png';

function Hero() {
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
            <li className='archivo special'>Explore</li>
          </div>
        </ul>
      </nav>

      <div className='heroContainer'>
        <img className='heroImage' src={heroImage} alt="Hero Image" />
        <div className='textOverlay'>
          <h1 className='heroTitle archivo'>Find unforgettable trips</h1>
          <p>Go to places you would have never thought about with Deconnecting.</p>
        </div>
      </div>
    </div>
  );
}

export default Hero;
