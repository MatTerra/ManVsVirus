import React, { useState, useEffect, useLayoutEffect } from 'react' 
import { backend } from '../utils/api'
import SimpleDialog from './SimpleDialog'
import Alert from '@material-ui/lab/Alert';


const Actions = ({turn, gameId, played, setPlayed, destinations, curable, infected, cards, build, discard}) => {
    const [open, setOpen] = useState(false)
    const [selectedType, setSelectedType] = useState('')
    const [options, setOptions] = useState([])
    const [title, setTitle] = useState('')
    const [cardsDiscard, setCardsDiscard] = useState([{name:'NA', id:-1}])

    console.log()

    function action(value){
        backend.put("/game/"+gameId,{type: selectedType, data: value.toString()},{ headers: { Authorization: `Bearer ${localStorage.getItem('loginToken')}`}}).then(response => {
            setPlayed(played+1)
            if (selectedType == 'discard'){
                let actions = cards.filter(v => v.type == 'action')
                cards = cards.filter(v => v.type == 'city').filter(v=>v.city.id != value) + actions
            }
        })
        setSelectedType('')
    }
    
    const handleClose = (value) => {
        setOpen(false);
        if(value == 'abort'){
            return
        }
        if (selectedType == 'discard'){
            let actions = cards.filter(v => v.type == 'action')
            cards = (cards.filter(v => v.type == 'city').filter(v=>v.city.id != value)).concat(actions)
            setOptions(cards)
        }
        action(value);
      };

    useEffect(() => {
        console.log(selectedType)
        if (!turn || selectedType == ''){
            return
        }
        if(selectedType == 'skip' || selectedType == 'build'){
            action('')
        } else {
            if (selectedType == 'heal'){
                if(infected.length == 1){
                    action(infected[0].id)
                    return
                }
                setOptions(infected)
                setTitle("Que cor deseja curar?")
            } else if (selectedType == 'move'){
                setOptions(destinations)
                setTitle("Para onde você deseja ir?")
            } else if (selectedType == 'travel'){
                let cardDestinations = cards.filter((card, i) => card.type == 'city')
                cardDestinations = cardDestinations.map((card, i) => {
                    return {name: card.city.name, id: card.city.id}
                })
                setOptions(cardDestinations)
                setTitle("Para onde deseja viajar?")
            } else if (selectedType == 'cure'){
                if(curable.length == 1){
                    action(curable[0].id)
                    return
                }
                setOptions(curable)
                setTitle("Que doença você deseja curar?")
            } else if (selectedType == 'discard'){
                let cardsDiscard = cards.map((card, i) => {
                    if (card.type == 'city'){
                        return {name: card.city.name, id: card.id}
                    } else {
                        return {name: card.action, id: card.id}
                    }
                })
                setOptions(cardsDiscard)
                setTitle("Você tem que descartar "+discard+" cartas")
            }
            setOpen(true)
        }
    }, [selectedType])

    useLayoutEffect(()=>{     
        if(turn && discard>0 && cards.length > 7 && !open){
            setOptions(cardsDiscard)
            setSelectedType('discard')
        }
        if(!(discard>0 && turn) && selectedType == 'discard'){
            setOpen(false)
        }
    })


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
            <img src={process.env.PUBLIC_URL + '/research_center_action.png'}
                 style={{ opacity: turn && build?1:0.5 }} 
                 className='action' 
                 onClick={() => { 
                    if (build){
                        setSelectedType('build')
                    } else {
                        alert("Você não pode construir agora!")
                    }
                 }}/>
            <img src={process.env.PUBLIC_URL + '/cure.png'}
                 style={{ opacity: (turn && curable.length>0)?1:0.5 }}
                 className='action' 
                 onClick={() => {
                    if(curable.length>0){ 
                         setSelectedType('cure')
                    } else {
                        alert("Nada para curar!")
                    }
                }}
            />
            <img src={process.env.PUBLIC_URL + '/skip.png'}   
                 style={{ opacity: turn?1:0.5 }} 
                 className='action' 
                 onClick={() => {setSelectedType('skip')}}/>
            <SimpleDialog title={title} list={options} open={open} onClose={handleClose} />
            {/* <SimpleDialog title="Qual carta você gostaria de descartar?" list={cardsDiscard} open={discard && turn} onClose={handleClose} /> */}
        </div>
    )
}

export default Actions;