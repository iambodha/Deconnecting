import React from 'react';
import '../Hero/hero.css';
import './explain.css';
import icon1 from '../assets/icon1.png'
import icon2 from '../assets/icon1.png'
import icon3 from '../assets/icon1.png'
import explainImg from '../assets/explain1.jpg'

function Explain() {
    return (
        <div className='explainContainer'>
            <h1 className='headertext archivo'>What is Deconnecting?</h1>
            <div className="explainMain">
                <div className='explainLeft'>
                    <h2 className='bigHeader'>Deconnecting is...</h2>
                    <div className='smallPoint'>
                        <img src={icon1} alt='Icon 1' className='icon'/>
                        <p>A sustainable & tailor-made trip creation tool</p>
                    </div>
                    <div className='smallPoint'>
                        <img src={icon2} alt='Icon 2' className='icon'/>
                        <p>Small Point 2</p>
                    </div>
                    <div className='smallPoint'>
                        <img src={icon3} alt='Icon 3' className='icon'/>
                        <p>Small Point 3</p>
                    </div>
                </div>
                <div className='explainRight'>
                    <img src={explainImg} alt='Explanation' className='explainImage'/>
                </div>
            </div>
        </div>
    );
}

export default Explain;
