import React from 'react'
import Cure from './Cure'

function Board() {
    const [redCured,    setRedCured] = useState(true);
    const [yellowCured, setYellowCured] = useState(false);
    const [blueCured,   setBlueCured] = useState(false);
    const [blackCured,  setBlackCured] = useState(false);
  
    const [redErradicated,    setRedErradicated] = useState(false);
    const [yellowErradicated, setYellowErradicated] = useState(true);
    const [blueErradicated,   setBlueErradicated] = useState(false);
    const [blackErradicated,  setBlackErradicated] = useState(false);
  
    return (
      <div style={{'background': process.env.PUBLIC_URL + '/map2.png'}} alt="board"  class='map'>
        <Cure color='red' top='40vh' cured={redCured} erradicated={redErradicated}/>
        <Cure color='yellow' top='50vh' cured={yellowCured} erradicated={yellowErradicated}/>
        <Cure color='blue' top='60vh'cured={blueCured} erradicated={blueErradicated}/>
        <Cure color='black' top='70vh' cured={blackCured} erradicated={blackErradicated}/>
      </div>
    );
  }
  
  export default Board;
  