import React, { useState } from 'react'
import Cure from './Cure'
import Location from './Location'

function Board() {
  const [redCured, setRedCured] = useState(true);
  const [yellowCured, setYellowCured] = useState(false);
  const [blueCured, setBlueCured] = useState(false);
  const [blackCured, setBlackCured] = useState(false);

  const [redErradicated, setRedErradicated] = useState(false);
  const [yellowErradicated, setYellowErradicated] = useState(true);
  const [blueErradicated, setBlueErradicated] = useState(false);
  const [blackErradicated, setBlackErradicated] = useState(false);

  const [infectionSpeed, setInfectionSpeed] = useState(2)

  return (
    <div class='App'>
      <div style={{ position: 'absolute', top: '1vh', width:'100%', marginTop: '0', color: '#cfcfcf', height: '3rem' }}>
        <h1 style={{ position: 'absolute', top: '0', fontSize: '4rem', margin: '0', marginLeft: '6vw', opacity: '1', zIndex: '1' }}>Man VS Virus</h1>
        <div style={{ position: 'relative', top:'40%', marginLeft: '1vw', color: '#cbcbcb', opacity: '0.6', backgroundImage: 'url(' + process.env.PUBLIC_URL + '/ekg.png)', backgroundSize: "25% 100%", backgroundRepeat: 'no-repeat', height: '100%', width: '100%' }} />

      </div>
      <div style={{ position: 'absolute', top: '13vh', left: '67vw', marginTop: '0', color: '#cfcfcf', height: '4rem', display: "flex", flexDirection: 'row', alignItems: 'center' }}>
        <h3>Velocidade <br />de Infecção</h3>
        <div style={{ width: '4vw', height: '4vw', marginLeft: '1vw', textAlign: 'center', position: 'relative' }} class='gradSpeed'>
          <img src={process.env.PUBLIC_URL + infectionSpeed > 2 ? infectionSpeed > 3 ? '/speed_high.png' : '/speed_medium.png' : '/speed_low.png'} 
          style={{ position: 'relative', top: '0', left: '0', width: '4vw', height: '4vw' }} onClick={() => {infectionSpeed==4?setInfectionSpeed(2):setInfectionSpeed(infectionSpeed+1)}}/>
          <label style={{ position: 'absolute', top: '20%', left: '30%', fontSize: '2.5vw', fontWeight: 'bold' }} onClick={() => {infectionSpeed==4?setInfectionSpeed(2):setInfectionSpeed(infectionSpeed+1)}} >{infectionSpeed}</label>
        </div>
      </div>
      <Cure color='red' top='50vh' cured={redCured} erradicated={redErradicated} />
      <Cure color='yellow' top='60vh' cured={yellowCured} erradicated={yellowErradicated} />
      <Cure color='blue' top='70vh' cured={blueCured} erradicated={blueErradicated} />
      <Cure color='black' top='80vh' cured={blackCured} erradicated={blackErradicated} />
      <Location color='blue' name='Atlanta' x='10vw' y='33vh'             infections={[3,1,1,0]}/>
      <Location color='blue' name='Montreal' x='13vw' y='18vh'            infections={[1,0,0,0]}/>
      <Location color='blue' name='New York' x='23vw' y='21vh'            infections={[1,0,0,0]}/>
      <Location color='blue' name='Chicago' x='6vw' y='21vh'              infections={[1,0,0,0]}/>
      <Location color='blue' name='São Francisco' x='1vw' y='28vh'        infections={[1,0,1,0]}/>
      <Location color='blue' name='Washington' x='16vw' y='28vh'          infections={[1,0,0,0]}/>
      <Location color='blue' name='Londres' x='40vw' y='15vh'             infections={[1,0,0,0]}/>
      <Location color='blue' name='Madri' x='40vw' y='27vh'               infections={[1,0,0,0]}/>
      <Location color='blue' name='Paris' x='44.5vw' y='22vh'             infections={[1,0,0,0]}/>
      <Location color='blue' name='Essen' x='49vw' y='15vh'               infections={[1,0,0,0]}/>
      <Location color='blue' name='São Petersburgo' x='55vw' y='10vh'     infections={[1,0,0,0]}/>
      <Location color='blue' name='Milão' x='49vw' y='25vh'               infections={[1,0,0,0]}/>
      <Location color='yellow' name='Los Angeles' x='5vw' y='39vh'        infections={[0,0,1,0]}/>
      <Location color='yellow' name='Miami' x='17vw' y='40vh'             infections={[0,0,1,0]}/>
      <Location color='yellow' name='Cidade do México' x='10vw' y='44vh'  infections={[0,0,1,0]}/>
      <Location color='yellow' name='Bogotá' x='20vw' y='54vh'            infections={[0,0,1,0]}/>
      <Location color='yellow' name='Lima' x='18vw' y='66vh'              infections={[0,0,1,0]}/>
      <Location color='yellow' name='Santiago' x='18vw' y='86vh'          infections={[0,0,1,0]}/>
      <Location color='yellow' name='São Paulo' x='26vw' y='70vh'         infections={[0,0,1,0]}/>
      <Location color='yellow' name='Buenos Aires' x='23vw' y='79vh'      infections={[0,0,1,0]}/>
      <Location color='yellow' name='Lagos' x='42vw' y='49vh'             infections={[0,0,1,0]}/>
      <Location color='yellow' name='Kinshasa' x='47vw' y='63vh'          infections={[0,0,1,0]}/>
      <Location color='yellow' name='Johanesburgo' x='50vw' y='77vh'      infections={[0,0,1,0]}/>
      <Location color='yellow' name='Cartum' x='52vw' y='48vh'            infections={[0,0,1,0]}/>
      <Location color='black' name='Cairo' x='50vw' y='37vh'              infections={[0,1,0,0]}/>
      <Location color='black' name='Argel' x='43vw' y='35vh'              infections={[0,1,0,0]}/>
      <Location color='black' name='Moscou' x='57vw' y='19vh'             infections={[0,1,0,0]}/>
      <Location color='black' name='Istambul' x='54vw' y='26vh'           infections={[0,1,0,0]}/>
      <Location color='black' name='Bagdá' x='56vw' y='35vh'              infections={[0,1,0,0]}/>
      <Location color='black' name='Riad' x='59vw' y='43vh'               infections={[0,1,0,0]}/>
      <Location color='black' name='Teerã' x='59vw' y='28vh'              infections={[0,1,0,0]}/>
      <Location color='black' name='Carachi' x='63vw' y='35vh'            infections={[0,1,0,0]}/>
      <Location color='black' name='Bombaim' x='66.5vw' y='42vh'          infections={[0,1,0,0]}/>
      <Location color='black' name='Chennai' x='68vw' y='50vh'            infections={[0,1,0,0]}/>
      <Location color='black' name='Deli' x='68vw' y='32vh'               infections={[0,1,0,0]}/>
      <Location color='black' name='Calcutá' x='71vw' y='38vh'            infections={[0,1,0,0]}/>
      <Location color='red' name='Sidney' x='90vw' y='75vh'               infections={[0,0,0,1]}/>
      <Location color='red' name='Jacarta' x='78vw' y='60vh'              infections={[0,0,0,1]}/>
      <Location color='red' name='Manila' x='84vw' y='50vh'               infections={[0,0,0,1]}/>
      <Location color='red' name='Ho Chi Min' x='78vw' y='48vh'           infections={[0,0,0,1]}/>
      <Location color='red' name='Bangkok' x='74vw' y='45vh'              infections={[0,0,0,1]}/>
      <Location color='red' name='Hong Kong' x='79vw' y='40vh'            infections={[0,0,0,1]}/>
      <Location color='red' name='Taipé' x='82.5vw' y='38vh'              infections={[0,0,0,1]}/>
      <Location color='red' name='Osaka' x='86vw' y='32vh'                infections={[0,0,0,1]}/>
      <Location color='red' name='Tóquio' x='89vw' y='26vh'               infections={[0,0,0,1]}/>
      <Location color='red' name='Seul' x='83.5vw' y='22.5vh'             infections={[0,0,0,1]}/>
      <Location color='red' name='Pequim' x='76vw' y='23vh'               infections={[0,0,0,1]}/>
      <Location color='red' name='Xangai' x='79vw' y='31vh'               infections={[0,0,0,1]}/>
    </div>
  );
}

export default Board;
