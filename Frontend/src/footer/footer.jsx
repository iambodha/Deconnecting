import React, { useState, useEffect } from 'react';
import '../Hero/hero.css';
import './footer.css';

function Footer() {
    return (
        <footer class="footer">
            <div class="footer-container">
                <div class="footer-branding">
                    <h1 className='archivo'>Deconnecting<sup>®</sup></h1>
                    <p>Free forever.</p>
                    <button class="get-started-button">Get Started →</button>
                </div>
                <div class="footer-links">
                    <div class="footer-column">
                        <h2 className='archivo'>Company</h2>
                        <a href="#">Company</a>
                        <a href="#">Resources</a>
                        <a href="#">About</a>
                        <a href="#">Careers</a>
                        <a href="#">Learn</a>
                        <a href="#">Blog</a>
                        <a href="#">Follow Us</a>
                    </div>
                    <div class="footer-column">
                        <h2 className='archivo'>Resources</h2>
                        <a href="#">Advertise</a>
                        <a href="#">Partners</a>
                        <a href="#">Affiliate</a>
                        <a href="#">Docs</a>
                        <a href="#">Support</a>
                        <a href="#">Github</a>
                        <a href="#">API Access</a>

                    </div>
                    <div class="footer-column">
                        <h2 className='archivo'>Connect</h2>
                        <a href="#">Newsletter</a>
                        <a href="#">Instagram</a>
                        <a href="#">Twitter (X)</a>
                        <a href="#">LinkedIn</a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>Copyright © 2024 Deconnecting UG</p>
                <div class="footer-bottom-links">
                    <a href="#">Terms and Conditions</a>
                    <a href="#">Privacy Policy</a>
                </div>
            </div>
        </footer>
    );
}

export default Footer;
