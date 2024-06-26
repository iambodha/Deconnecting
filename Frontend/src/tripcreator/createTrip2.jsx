import React, { useState, useEffect } from 'react';
import '../Hero/hero.css';
import './createTrip2.css';
import './button.css';
import './loader.css'
import './button.js'

import DateRangePicker from '../DateRangePicker/daterangepicker.jsx';
import MapComponent from '../MapComponent/mapcomponent.jsx'

function CreateTrip2() {
    // manage current state
    const [currentState, setCurrentState] = useState('click');
    const [loading, setLoading] = useState(false);
    const [groupType, setGroupType] = useState('');
    const [budget, setBudget] = useState('');
    const [startLocation, setStartLocation] = useState('');
    const [endLocation, setEndLocation] = useState('');
    const [selectedCountries, setSelectedCountries] = useState([]);

    // MESSY SHIT!!!!!!!
    let content;
    if (loading) {
        content = (
            <div className="mainOutline">
                <div className="banter-loader loading">
                    <div className="banter-loader__box"></div>
                    <div className="banter-loader__box"></div>
                    <div className="banter-loader__box"></div>
                    <div className="banter-loader__box"></div>
                    <div className="banter-loader__box"></div>
                    <div className="banter-loader__box"></div>
                    <div className="banter-loader__box"></div>
                    <div className="banter-loader__box"></div>
                    <div className="banter-loader__box"></div>
                </div>
            </div>
        );
    }

    else if (currentState === 'click') {
        content = (
        <div className="mainOutline">
            <div class="sparkle-button generateButton">
            <button onClick={() => {
                        setLoading(true);
                        setTimeout(() => {
                            setLoading(false);
                            setCurrentState('start');
                        }, 2000); // 4 sec delay
                    }}>
                <span class="spark"></span>
                <span class="backdrop"></span>
                <svg class="sparkle" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M14.187 8.096L15 5.25L15.813 8.096C16.0231 8.83114 16.4171 9.50062 16.9577 10.0413C17.4984 10.5819 18.1679 10.9759 18.903 11.186L21.75 12L18.904 12.813C18.1689 13.0231 17.4994 13.4171 16.9587 13.9577C16.4181 14.4984 16.0241 15.1679 15.814 15.903L15 18.75L14.187 15.904C13.9769 15.1689 13.5829 14.4994 13.0423 13.9587C12.5016 13.4181 11.8321 13.0241 11.097 12.814L8.25 12L11.096 11.187C11.8311 10.9769 12.5006 10.5829 13.0413 10.0423C13.5819 9.50162 13.9759 8.83214 14.186 8.097L14.187 8.096Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                    <path d="M6 14.25L5.741 15.285C5.59267 15.8785 5.28579 16.4206 4.85319 16.8532C4.42059 17.2858 3.87853 17.5927 3.285 17.741L2.25 18L3.285 18.259C3.87853 18.4073 4.42059 18.7142 4.85319 19.1468C5.28579 19.5794 5.59267 20.1215 5.741 20.715L6 21.75L6.259 20.715C6.40725 20.1216 6.71398 19.5796 7.14639 19.147C7.5788 18.7144 8.12065 18.4075 8.714 18.259L9.75 18L8.714 17.741C8.12065 17.5925 7.5788 17.2856 7.14639 16.853C6.71398 16.4204 6.40725 15.8784 6.259 15.285L6 14.25Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                    <path d="M6.5 4L6.303 4.5915C6.24777 4.75718 6.15472 4.90774 6.03123 5.03123C5.90774 5.15472 5.75718 5.24777 5.5915 5.303L5 5.5L5.5915 5.697C5.75718 5.75223 5.90774 5.84528 6.03123 5.96877C6.15472 6.09226 6.24777 6.24282 6.303 6.4085L6.5 7L6.697 6.4085C6.75223 6.24282 6.84528 6.09226 6.96877 5.96877C7.09226 5.84528 7.24282 5.75223 7.4085 5.697L8 5.5L7.4085 5.303C7.24282 5.24777 7.09226 5.15472 6.96877 5.03123C6.84528 4.90774 6.75223 4.75718 6.697 4.5915L6.5 4Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <span class="text">Generate Trip</span>
                </button>
                <div class="bodydrop"></div>
                <span aria-hidden="true" class="particle-pen">
                <svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg><svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg><svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg><svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg><svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg><svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg><svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg><svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg><svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg><svg class="particle" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.937 3.846L7.75 1L8.563 3.846C8.77313 4.58114 9.1671 5.25062 9.70774 5.79126C10.2484 6.3319 10.9179 6.72587 11.653 6.936L14.5 7.75L11.654 8.563C10.9189 8.77313 10.2494 9.1671 9.70874 9.70774C9.1681 10.2484 8.77413 10.9179 8.564 11.653L7.75 14.5L6.937 11.654C6.72687 10.9189 6.3329 10.2494 5.79226 9.70874C5.25162 9.1681 4.58214 8.77413 3.847 8.564L1 7.75L3.846 6.937C4.58114 6.72687 5.25062 6.3329 5.79126 5.79226C6.3319 5.25162 6.72587 4.58214 6.936 3.847L6.937 3.846Z" fill="black" stroke="black" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                </span>
            </div>
        </div>
        );
    }   
    
    else if (currentState === 'start') {
        content = (
            <div className="createTripMain">
                <div className="mainOutline">
                    <h1 className='archivo mainHeader'>Get Started</h1>
                    <button className='startButton' onClick={() => setCurrentState('chooseGroupType')}>
                        <h1 className='archivo buttonText'>Start</h1>
                    </button>
                </div>
            </div>
        );
    }   
    
    else if (currentState === 'chooseGroupType') {
        content = (
            <div className="createTripMain">            
                <div className="mainOutline">
                    <div className="topSection">
                        <a className='backIcon' onClick={() => setCurrentState('start')}><i class="uil uil-angle-left-b"></i></a>
                        <div className="apiHolder">
                        <i class="uil uil-flask"></i>
                        <p>Deconnecting API v0.12 Beta</p>
                        </div>
                    </div>
                    <h1 className='archivo mainHeader'>Choose Group Type</h1>
                    <div className='buttonHolder'>
                        <button className='startButtons' onClick={() => setCurrentState('typeGroup')}>
                        <h1 className='archivo buttonText'>Group</h1>
                        </button>
                        <button className='startButtons' onClick={() => setCurrentState('typeSolo')}>
                        <h1 className='archivo buttonText'>Solo</h1>
                        </button>
                    </div>
                </div>
            </div>
        );
    } else if (currentState === 'typeGroup') {
        content = (
            <div className="createTripMain">   
                <div className="mainOutline">
                    <h1 className='archivo createHeader'>TESTGROUP</h1>
                    <button className='startButton' onClick={() => setCurrentState('click')}>
                    <h1 className='archivo buttonText'>Back to Start</h1>
                    </button>
                </div>
            </div>
        );
    } else if (currentState === 'typeSolo') {
        content = (
            <div className="createTripMain">   
                <div className="mainOutline">
                <div className="topSection">
                        <a className='backIcon' onClick={() => setCurrentState('start')}><i class="uil uil-angle-left-b"></i></a>
                        <div className="apiHolder">
                        <i class="uil uil-flask"></i>
                        <p>Deconnecting API v0.12 Beta</p>
                        </div>
                    </div>
                    <div className="centerSection">
                        <div class="icon-bar">
                            <div class="icon active">
                                <i class="uil uil-dollar-sign"></i>
                            </div>
                            <div class="icon">
                                <i class="uil uil-calendar-alt"></i>
                            </div>
                            <div class="icon">
                                <i class="uil uil-map-marker"></i>
                            </div>
                            <div class="icon">
                                <i class="uil uil-globe"></i>
                            </div>
                            <div class="icon">
                                <i class="uil uil-car"></i>
                            </div>
                            <div class="icon">
                                <i class="uil uil-bed"></i>
                            </div>
                         </div>
                    </div>
                    <div className='budgetContainer'>
                        <input type="text"
                            value={budget}
                            onChange={(e) => setBudget(e.target.value)}
                            placeholder="Your Budget (EUR)"
                            className="budgetInput" />
                        <button className='budgetButton' onClick={() => setCurrentState('calendar')}>Next</button>
                    </div>
                </div>
            </div>
        );
    } else if (currentState === 'calendar') {
        content = (
            <div className="createTripMain">   
                <div className="mainOutline">
                    <div className="topSection">
                        <a className='backIcon' onClick={() => setCurrentState('typeSolo')}><i class="uil uil-angle-left-b"></i></a>
                        <div className="apiHolder">
                        <i class="uil uil-flask"></i>
                        <p>Deconnecting API v0.12 Beta</p>
                        </div>
                    </div>
                    <div className="centerSection">
                        <div class="icon-bar">
                            <div class="icon">
                                <i class="uil uil-dollar-sign"></i>
                            </div>
                            <div class="icon active">
                                <i class="uil uil-calendar-alt"></i>
                            </div>
                            <div class="icon">
                                <i class="uil uil-map-marker"></i>
                            </div>
                            <div class="icon">
                                <i class="uil uil-globe"></i>
                            </div>
                            <div class="icon">
                                <i class="uil uil-car"></i>
                            </div>
                            <div class="icon">
                                <i class="uil uil-bed"></i>
                            </div>
                         </div>
                         <h1 className='mainTitle'>Select your travel dates:</h1>
                    </div>
                    <DateRangePicker onDateRangeSelected={(range) => console.log(range)} />
                    <button className='budgetButton' onClick={() => setCurrentState('location')}>Next</button>
                </div>
            </div>
        );
    }  else if (currentState === 'location') {
        content = (
            <div className="createTripMain">   
                <div className="mainOutline">
                    <div className="topSection">
                        <a className='backIcon' onClick={() => setCurrentState('typeSolo')}><i class="uil uil-angle-left-b"></i></a>
                        <div className="apiHolder">
                        <i class="uil uil-flask"></i>
                        <p>Deconnecting API v0.12 Beta</p>
                        </div>
                    </div>
                    <div className="centerSection">
                        <div class="icon-bar">
                            <div class="icon">
                                <i class="uil uil-dollar-sign"></i>
                            </div>
                            <div class="icon">
                                <i class="uil uil-calendar-alt"></i>
                            </div>
                            <div class="icon active">
                                <i class="uil uil-map-marker"></i>
                            </div>
                            <div class="icon">
                                <i class="uil uil-globe"></i>
                            </div>
                            <div class="icon">
                                <i class="uil uil-car"></i>
                            </div>
                            <div class="icon">
                                <i class="uil uil-bed"></i>
                            </div>
                         </div>
                        <h1 className='mainTitle'>Start & End of your Trip</h1>
                        <div className="locationContainer">
                            <i class="uil uil-map-marker locationMarker"></i>
                            <input type="text"
                                        value={startLocation}
                                        onChange={(e) => setStartLocation(e.target.value)}
                                        placeholder="Starting location"
                                        className="locationInput" />
                        </div>
                        <div className="locationContainer">
                            <i class="uil uil-map-marker locationMarker"></i>
                            <input type="text"
                                        value={endLocation}
                                        onChange={(e) => setEndLocation(e.target.value)}
                                        placeholder="Ending location"
                                        className="locationInput" />
                        </div>
                    </div>
                    <button className='budgetButton' onClick={() => setCurrentState('countryChooser')}>Next</button>
                </div>
            </div>
        );
    } else if (currentState === 'countryChooser') {
        content = (
            <div className="createTripMain">
                <div className="mainOutline">
                    <div className="topSection">
                            <a className='backIcon' onClick={() => setCurrentState('typeSolo')}><i class="uil uil-angle-left-b"></i></a>
                            <div className="apiHolder">
                            <i class="uil uil-flask"></i>
                            <p>Deconnecting API v0.12 Beta</p>
                            </div>
                        </div>
                        <div className="centerSection">
                            <div class="icon-bar">
                                <div class="icon">
                                    <i class="uil uil-dollar-sign"></i>
                                </div>
                                <div class="icon">
                                    <i class="uil uil-calendar-alt"></i>
                                </div>
                                <div class="icon">
                                    <i class="uil uil-map-marker"></i>
                                </div>
                                <div class="icon active">
                                    <i class="uil uil-globe"></i>
                                </div>
                                <div class="icon">
                                    <i class="uil uil-car"></i>
                                </div>
                                <div class="icon">
                                    <i class="uil uil-bed"></i>
                                </div>
                            </div>
                        </div>
                        <h1 className="mainTitle">Select Countries to Visit</h1>
                        <MapComponent setSelectedCountries={setSelectedCountries} />
                        <div>Selected Countries: {selectedCountries.join(', ')}</div>
                        <button className='budgetButton' onClick={() => setCurrentState('location')}>Next</button>
                    </div>
            </div>
        );
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
                <div className="headerAndMain">
                    <div className="header">
                        <h1 className='archivo mainHeader'>Create your <em>very own</em> adventure now</h1>
                    </div>  
                        {content} {/* Render content based on current state */}
                </div>
        </div>
    );
}

export default CreateTrip2;