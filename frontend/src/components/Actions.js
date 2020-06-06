import React, { useState } from 'react' 
import { backend } from '../utils/api'
import SimpleDialog from './Dialog'


const Actions = ({turn, gameId, played, setPlayed, destinations, infected}) => {
    const [open, setOpen] = useState(false)
    const [selectedType, setSelectedType] = useState('')
    const [options, setOptions] = useState([])

    console.log(infected)

    function action(value){
        backend.put("/game/"+gameId,{type: selectedType, data: value.toString()},{ headers: { Authorization: `Bearer ${localStorage.getItem('loginToken')}`}}).then(response => {
            setPlayed(played+1)
           })
    }

    const handleClickMove = () => {
        if (turn){
            setOpen(true);
            setSelectedType('move');
            setOptions(destinations);
        }
    };
    const handleClickTreat = () => {
        if (turn){
            setOpen(true);
            setSelectedType('heal');
            setOptions(infected)
        }
    };
    
      const handleClose = (value) => {
        
        setOpen(false);
        if(value == 'abort'){
            return
        }
        action(value);
      };

    return(
        <div style={{display: 'flex', flexDirection:'row', position:'absolute', left:'30vw', bottom:'0vh', alignSelf: 'center', backgroundColor:'#606060', borderRadius:'5px 5px 0 0', height:'8vh'}}>
            <img src={process.env.PUBLIC_URL + '/move.png'} 
                 style={{ opacity: turn?1:0.5 }}
                 className='action'
                 onClick={handleClickMove}
            />
            <img src={process.env.PUBLIC_URL + '/treat.png'}
                 style={{ opacity: (turn && infected.length>0)?1:0.5 }} 
                 className='action' 
                 onClick={handleClickTreat}
            />
            <img src={process.env.PUBLIC_URL + '/travel.png'}                   style={{ opacity: turn?1:0.5 }} className='action' onClick={() => { }}/>
            <img src={process.env.PUBLIC_URL + '/research_center_action.png'}   style={{ opacity: turn?1:0.5 }} className='action' onClick={() => { }}/>
            <SimpleDialog type={selectedType} list={options} open={open} onClose={handleClose} />
            
        </div>
    )
}

export default Actions;