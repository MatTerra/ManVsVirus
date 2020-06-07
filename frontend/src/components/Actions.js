import React, { useState, useEffect } from 'react' 
import { backend } from '../utils/api'
import SimpleDialog from './SimpleDialog'


const Actions = ({turn, gameId, played, setPlayed, destinations, infected, cards}) => {
    const [open, setOpen] = useState(false)
    const [selectedType, setSelectedType] = useState('')
    const [options, setOptions] = useState([])

    function action(value){
        backend.put("/game/"+gameId,{type: selectedType, data: value.toString()},{ headers: { Authorization: `Bearer ${localStorage.getItem('loginToken')}`}}).then(response => {
            setPlayed(played+1)
           })
    }
    
    const handleClose = (value) => {
        setSelectedType('')
        setOpen(false);
        if(value == 'abort'){
            return
        }
        action(value);
      };

    useEffect(() => {
        if (!turn || selectedType == ''){
            return
        }
        if(selectedType == 'skip'){
            action('')
        } else {
            setOpen(true)
            if (selectedType == 'heal'){
                setOptions(infected)
            } else if (selectedType == 'move'){
                setOptions(destinations)
            } else if (selectedType == 'travel'){
                destinations = cards.filter((card, i) => card.type == 'city')
                destinations = destinations.map((card, i) => {
                    return {name: card.city.name, id: card.city.id}
                })
                setOptions(destinations)
            }
        }
    }, [selectedType])

    return(
        <div style={{display: 'flex', flexDirection:'row', position:'absolute', left:'30vw', bottom:'0vh', alignSelf: 'center', backgroundColor:'#606060', borderRadius:'5px 5px 0 0', height:'8vh'}}>
            <img src={process.env.PUBLIC_URL + '/move.png'} 
                 style={{ opacity: turn?1:0.5 }}
                 className='action'
                 onClick={() => {setSelectedType('move')}}
            />
            <img src={process.env.PUBLIC_URL + '/treat.png'}
                 style={{ opacity: (turn && infected.length>0)?1:0.5 }}
                 className='action' 
                 onClick={() => {
                    if(infected.length>0){ 
                         setSelectedType('heal')
                    } else {
                        alert("Nada para tratar!")
                    }
                }}
            />
            <img src={process.env.PUBLIC_URL + '/travel.png'}  
                 style={{ opacity: turn && cards.length > 0?1:0.5 }} 
                 className='action' onClick={() => {
                    if(cards.length>0){ 
                        setSelectedType('travel')
                   } else {
                       alert("Não é possível viajar para lugar nenhum!")
                   }
                }}/>
            <img src={process.env.PUBLIC_URL + '/research_center_action.png'}   style={{ opacity: turn?1:0.5 }} className='action' onClick={() => { }}/>
            <img src={process.env.PUBLIC_URL + '/skip.png'}   
                 style={{ opacity: turn?1:0.5 }} 
                 className='action' 
                 onClick={() => {setSelectedType('skip')}}/>
            
            <SimpleDialog type={selectedType} list={options} open={open} onClose={handleClose} />
            
        </div>
    )
}

export default Actions;