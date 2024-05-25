import React, { useEffect, useRef } from 'react';
import './explore.css'; // css for image track thingy also
import card1 from '../assets/card1.jpg';
import card2 from '../assets/card2.jpg';
import card3 from '../assets/card3.jpg';
import card4 from '../assets/card4.jpg';
import card5 from '../assets/card5.jpg';
import icelandIcon from '../assets/iceland.png'; // country icon for the mini icons at the top
import germanIcon from '../assets/germany.png'; // country icon for the mini icons at the top
import italyIcon from '../assets/italy.png'; // country icon for the mini icons at the top
import finlandIcon from '../assets/finland.png'; // country icon for the mini icons at the top
import ukIcon from '../assets/uk.png'; // country icon for the mini icons at the top

function Explore() {
  const trackRef = useRef(null);

  useEffect(() => {
    const track = trackRef.current;

    const handleOnDown = (e) => {
      track.dataset.mouseDownAt = e.clientX || e.touches[0].clientX;
    };

    const handleOnUp = () => {
      track.dataset.mouseDownAt = '0';
      track.dataset.prevPercentage = track.dataset.percentage;
    };

    const handleOnMove = (e) => {
      if (track.dataset.mouseDownAt === '0') return;

      const clientX = e.clientX || e.touches[0].clientX;
      const mouseDelta = parseFloat(track.dataset.mouseDownAt) - clientX;
      const maxDelta = window.innerWidth / 2;

      const percentage = (mouseDelta / maxDelta) * -100;
      const nextPercentageUnconstrained =
        parseFloat(track.dataset.prevPercentage) + percentage;
      const nextPercentage = Math.max(Math.min(nextPercentageUnconstrained, 0), -100);

      track.dataset.percentage = nextPercentage;

      track.animate(
        {
          transform: `translate(${nextPercentage}%, -50%)`,
        },
        { duration: 3200, fill: 'forwards' }
      );

      for (const image of track.getElementsByClassName('image')) {
        image.animate(
          {
            objectPosition: `${100 + nextPercentage}% center`,
          },
          { duration: 3200, fill: 'forwards' }
        );
      }
    };

    window.addEventListener('mousedown', handleOnDown);
    window.addEventListener('touchstart', handleOnDown);

    window.addEventListener('mouseup', handleOnUp);
    window.addEventListener('touchend', handleOnUp);

    window.addEventListener('mousemove', handleOnMove);
    window.addEventListener('touchmove', handleOnMove);

    return () => {
      window.removeEventListener('mousedown', handleOnDown);
      window.removeEventListener('touchstart', handleOnDown);

      window.removeEventListener('mouseup', handleOnUp);
      window.removeEventListener('touchend', handleOnUp);

      window.removeEventListener('mousemove', handleOnMove);
      window.removeEventListener('touchmove', handleOnMove);
    };
  }, []);

  return (
    <div className='exploreContainerMain'>
      <div class="header__glow"></div>
      <div class="header__glow-4"></div>
      <h1 className='exploreText archivo'>Have a look at our <em>favourite</em> trips</h1>
      <h2 className='archivo'>with <em>flexible</em> pricing</h2>
      <div className='exploreContent'>
        <div id="image-track" ref={trackRef} data-mouse-down-at="0" data-prev-percentage="0">
          <div className="card">
            <img className="image" src={card1} draggable="false" />
            <div className="card-overlay">
              <div className="country-info">
                <img className="country-icon" src={icelandIcon} alt="Country Icon" />
                <span className="country-name">Iceland</span>
              </div>
              <div className="card-title">Iceland Explorer</div>
              <div className="card-subtitle">11-Day Trip</div>
              <div className="card-text">Experience the best of Iceland's wildlife, conservation efforts and some of the most iconic hotels</div>
              <div className="card-footer">
                <div className="card-price">From 899€ p.p*</div>
                <button className="card-button">Discover Trip</button>
              </div>
            </div>
          </div>
          <div className="card">
            <img className="image" src={card2} draggable="false" />
            <div className="card-overlay">
              <div className="country-info">
                <img className="country-icon" src={germanIcon} alt="Country Icon" />
                <span className="country-name">Germany</span>
              </div>
              <div className="card-title">German Tales</div>
              <div className="card-subtitle">4-Day Trip</div>
              <div className="card-text">Description for card 2</div>
              <div className="card-footer">
                <div className="card-price">From 329€ p.p*</div>
                <button className="card-button">Discover Trip</button>
              </div>
            </div>
          </div>
          <div className="card">
            <img className="image" src={card3} draggable="false" />
            <div className="card-overlay">
              <div className="country-info">
                <img className="country-icon" src={italyIcon} alt="Country Icon" />
                <span className="country-name">Italy</span>
              </div>
              <div className="card-title">Tuscany Dreamer</div>
              <div className="card-subtitle">5-Day Trip</div>
              <div className="card-text">Indulge in the beautiful hills and wine of Tuscany while exploring new and ecologically divine hotels.</div>
              <div className="card-footer">
                <div className="card-price">From 299€ p.p*</div>
                <button className="card-button">Discover Trip</button>
              </div>
            </div>
          </div>
          <div className="card">
            <img className="image" src={card4} draggable="false" />
            <div className="card-overlay">
              <div className="country-info">
                <img className="country-icon" src={finlandIcon} alt="Country Icon" />
                <span className="country-name">Finland</span>
              </div>
              <div className="card-title">Finnish Nights</div>
              <div className="card-subtitle">2-Day Trip</div>
              <div className="card-text">Description for card 4</div>
              <div className="card-footer">
                <div className="card-price">From 300€ p.p*</div>
                <button className="card-button">Discover Trip</button>
              </div>
            </div>
          </div>
          <div className="card">
            <img className="image" src={card5} draggable="false" />
            <div className="card-overlay">
              <div className="country-info">
                <img className="country-icon" src={ukIcon} alt="Country Icon" />
                <span className="country-name">United Kingdom</span>
              </div>
              <div className="card-title">Title 5</div>
              <div className="card-subtitle">Subtitle for card 5</div>
              <div className="card-text">Description for card 5</div>
              <div className="card-footer">
                <div className="card-price">From 300€ p.p*</div>
                <button className="card-button">Discover Trip</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Explore;
