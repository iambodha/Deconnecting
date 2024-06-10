import React, { useState, useEffect, useRef } from 'react';
import './mapcomponent.css';
import * as d3 from 'd3';
import { feature } from 'topojson-client';
import worldData from '../createTripassets/world-110m.json'; // Import your TopoJSON world map

const MapComponent = ({ setSelectedCountry }) => {
    const [tooltip, setTooltip] = useState({ visible: false, content: '', x: 0, y: 0 });
    const [selectedCountry, setSelectedCountryState] = useState(null);
    const svgRef = useRef();

    useEffect(() => {
        const svg = d3.select(svgRef.current);
        const width = 960;
        const height = 600;

        // Center the projection on Europe
        const projection = d3.geoMercator()
            .center([20, 50]) // Center on Europe
            .scale(520) // Adjust the scale
            .translate([width / 2, height / 2]); // Center the map in the SVG

        const path = d3.geoPath().projection(projection);
        const countries = feature(worldData, worldData.objects.countries).features;

        svg.selectAll('.map-country')
            .data(countries)
            .enter()
            .append('path')
            .attr('class', 'map-country')
            .attr('d', path)
            .on('click', (event, d) => handleCountryClick(d))
            .on('mouseover', (event, d) => handleMouseOver(event, d.properties.name))
            .on('mouseout', handleMouseOut);
    }, []);

    const handleCountryClick = (d) => {
        const country = d.properties.name;
        setSelectedCountryState(country);
        console.log(country);
        if (setSelectedCountry) {
            setSelectedCountry(country);
        }

        // Update class for selected country
        d3.select(svgRef.current)
            .selectAll('.map-country')
            .attr('class', 'map-country')
            .filter(data => data.properties.name === country)
            .attr('class', 'map-country selected');
    };

    const handleMouseOver = (event, country) => {
        setTooltip({
            visible: true,
            content: country,
            x: event.clientX,
            y: event.clientY
        });
    };

    const handleMouseOut = () => {
        setTooltip({ visible: false, content: '', x: 0, y: 0 });
    };

    return (
        <div className="map-container">
            <svg ref={svgRef} className="map"></svg>
            <div
                className={`map-tooltip ${tooltip.visible ? 'visible' : ''}`}
                style={{ top: tooltip.y + 10, left: tooltip.x + 10 }}
            >
                {tooltip.content}
            </div>
        </div>
    );
};

export default MapComponent;
