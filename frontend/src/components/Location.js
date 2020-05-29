import React, { useState } from 'react';
import Infection from './Infection';

const Location = ({ color, name, x, y, infections}) => {

    const colors=['blue', 'black', 'yellow', 'red']

    return (
        <div class='radialGrad' style={{ position: 'absolute', top: y, left: x, display:'flex', alignItems:"center"}}>
            <div style={{position:'absolute', height:'2vw', width:'2vw'}}>
                <img src={process.env.PUBLIC_URL+'/location_'+colors[color]+'.png'} style={{height: '100%', width:'100%', position:'relative'}}/>
                {/* { arr = Array(4).fill(0).map( (_, rowIndex) => { Array(infections[rowIndex]).fill(0) } );
                arr.map((row, rowIndex) => {
                    row.map((_, columnIndex)=>{
                        <Infection color={colors[rowIndex]} x={columnIndex} y={rowIndex}/>
                    })
                })} */}
                {Array(infections[0]).fill('blue').map((_, i) => <Infection color='blue' x={i} y={color=='blue'?0:1}/>)}
                {Array(infections[1]).fill(<Infection color='black' y={color=='black'?0:1}/>)}
                {Array(infections[2]).fill(<Infection color='yellow' y={color=='yellow'?0:1}/>)}
                {Array(infections[3]).fill(<Infection color='red' y={color=='red'?0:1}/>)}
            </div>
            <label style={{fontWeight: 'bold', position:'relative', top:'2vw'}}>{name}</label>
        </div>
    );
};

export default Location;