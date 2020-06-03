import React, { useState, useEffect } from 'react';
import Infection from './Infection';
import Player from './Player';

const Location = ({ color, name, researchCenter, x, y, infections, players}) => {

    const colors=['blue', 'black', 'yellow', 'red']
    const indexes=[0,1,2,3].filter((_)=>_!=color)
    const [playersComponents, setPlayersComponents] = useState(<></>)

    useEffect(()=>{
        
        setPlayersComponents(players.map((player, i) => <Player role={player.role} 
                                                      x={(players.length%2==0)?(i%2==0?(players.length>1?-1:0):1):(i==0?0:(i%2==0?1:-1))} 
                                                      y={(players.length%2==0)?(i<2?(players.length>2?-1:0):1):(players.length>1?(i<1?-1:1):0)}/>))
    },[players, researchCenter, infections])

    return (
        <div class='radialGrad' style={{ position: 'absolute', top: y, left: x, display:'flex', alignItems:"center"}}>
            <div style={{position:'absolute', height:'2vw', width:'2vw'}}>
                {researchCenter || <img src={process.env.PUBLIC_URL+'/location_'+colors[color]+'.png'} alt="infection"style={{height: '100%', width:'100%', position:'relative'}}/>}
                {researchCenter && <img src={process.env.PUBLIC_URL+'/research_center.png'} style={{height:'120%', width:'120%', position:'relative', bottom:'30%'}}/>}
                {Array(infections[color]).fill(color).concat(Array(infections[indexes[0]]).fill(indexes[0]),
                                                          Array(infections[indexes[1]]).fill(indexes[1]),
                                                          Array(infections[indexes[2]]).fill(indexes[2])
                                                          ).map( 
                   (colorCode, i) => <Infection id={colorCode} color={colors[colorCode]} x={colorCode==color?i:i-infections[color]} y={(colorCode==color)?0:infections[color]==0?0:1}/> 
                )}
                {playersComponents}
            </div>
            <label style={{fontWeight: 'bold', position:'relative', top:'2vw'}}>{name}</label>
        </div>
    );
};

export default Location;