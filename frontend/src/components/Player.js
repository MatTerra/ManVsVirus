import React from 'react'

const Player = ({role, x, y}) =>{
    console.log(x + '   '+y)
    return(
        <img style={{width:'2vw', position: 'absolute', left: (x*0.8)+0.2+'vw', top: ((y*1.5)-2)+'vh', zIndex: 1}}  src={process.env.PUBLIC_URL+'/player_'+role+'512.png'}/>
    )
}

export default Player