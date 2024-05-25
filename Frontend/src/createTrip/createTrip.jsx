import React, { useState, useEffect } from 'react';
import '../Hero/hero.css';
import './createTrip.css';
import './gradients.css';

function CreateTrip() {
    // manage current state
    const [currentState, setCurrentState] = useState('start');
    const [groupType, setGroupType] = useState('');
    const [budget, setBudget] = useState('');

    // MESSY SHIT!!!!!!!
    let content;
    if (currentState === 'start') {
        content = (
            <div className="mainOutline">
                <h1 className='archivo mainHeader'>Get Started</h1>
                <button className='startButton' onClick={() => setCurrentState('chooseGroupType')}>Start</button>
            </div>
        );
    } else if (currentState === 'chooseGroupType') {
        content = (
            <div className="mainOutline">
                <h1 className='archivo mainHeader'>Choose Group Type</h1>
                <div className='buttonHolder'>
                    <button className='startButtons' onClick={() => setCurrentState('typeGroup')}>Group <br />(WIP)</button>
                    <button className='startButtons' onClick={() => setCurrentState('typeSolo')}>Solo</button>
                </div>
            </div>
        );
    } else if (currentState === 'typeGroup') {
        content = (
            <div className="mainOutline">
                <h1 className='archivo createHeader'>TESTGROUP</h1>
                <button className='startButton' onClick={() => setCurrentState('start')}>BACK TO START</button>
            </div>
        );
    } else if (currentState === 'typeSolo') {
        content = (
            <div className="mainOutline">
                <h1 className='archivo createHeader'>TESTSOLO</h1>
                <div className='buttonHolder2'>
                    <button className='startButtons' onClick={() => setCurrentState('enterBudget')}>Enter Budget</button>
                    <button className='startButtons' onClick={() => setCurrentState('start')}>Back</button>
                </div>
            </div>
        );
    } else if (currentState === 'enterBudget') {
        content = (
            <div className="mainOutline">
                <h1 className='archivo createHeader'>Budget</h1>
                <h2 className='archivo'>What is your budget?</h2>
                <div className='budgetContainer'>
                    <input
                        type="text"
                        value={budget}
                        onChange={(e) => setBudget(e.target.value)}
                        placeholder="Enter your budget"
                        className="budgetInput"
                    />
                    <button className='startButtons' onClick={() => setCurrentState('start')}>Submit</button>
                </div>
            </div>
        );
    } else if (currentState === 'budgetInput') {
        content = (
            <div className="mainOutline">
                <h1 className="archivo createHeader"></h1>
            </div>
        )
    }

    // handle what happens
    // idk api dings bums
    useEffect(() => {
        // fetch('https://api.example.com/group?type=${groupType}')
        //     .then(response => response.json())
        //     .then(data => {
        //      // api detail output
        //     })
        //     .catch(error => {
        //         console.error('Error fetching data:', error);
        //     });
    }, [groupType]);

    return(
        <div className='createTripContainer'>
            <div className="container">
                <div className="headerAndMain">
                <div class="header__glow"></div>
                <div class="header__glow-2"></div>
                <div class="header__glow-4"></div>
                    <div className="header">
                        <h1 className='archivo createHeader'>Create your <em>very own</em> adventure now</h1>
                    </div>
                    <div className="createTripMain box-shadow">
                        {content} {/* Render content based on current state */}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default CreateTrip;
