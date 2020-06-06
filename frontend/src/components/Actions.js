import React from 'react' 

const Actions = ({turn}) => {
    return(
        <div style={{display: 'flex', flexDirection:'row', position:'absolute', left:'30vw', bottom:'0vh', alignSelf: 'center', backgroundColor:'#606060', borderRadius:'5px 5px 0 0', height:'8vh'}}>
            <img src={process.env.PUBLIC_URL + '/move.png'}                     style={{ opacity: turn?1:0.5 }} className='action'/>
            <img src={process.env.PUBLIC_URL + '/treat.png'}                    style={{ opacity: turn?1:0.5 }} className='action'/>
            <img src={process.env.PUBLIC_URL + '/travel.png'}                   style={{ opacity: turn?1:0.5 }} className='action'/>
            <img src={process.env.PUBLIC_URL + '/research_center_action.png'}   style={{ opacity: turn?1:0.5 }} className='action'/>
        </div>
    )
}

export default Actions;