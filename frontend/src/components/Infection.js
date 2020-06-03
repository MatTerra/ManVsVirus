import React from 'react'

const Infection = ({color, x, y}) => {
    return (
        <img src={process.env.PUBLIC_URL+'/cube_'+color+'.png'} class='infection' style={{position:'absolute', bottom:(1.2-(1*y))+'vw', left: ((x*.8)-.2)+'vw', margin: '0', padding:'0', zIndex:'3', height:'1vw', width:'.8vw'}}/>
    )
}

export default Infection;