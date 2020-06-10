import React, { useState, useEffect, useContext } from 'react'
import Cure from './Cure'
import Location from './Location'
import { backend } from '../utils/api'
import Actions from './Actions'
import jwtDecode from "jwt-decode";
import { AuthContext } from '../contexts/AuthContext'
import Alert from '@material-ui/lab/Alert';
import { makeStyles } from '@material-ui/core'
import { Redirect } from 'react-router-dom'

function Board() {

  const colors=['Azul', 'Preto', 'Amarelo', 'Vermelho']
  const colorCodes=['blue', 'black', 'yellow', 'red']
  const [researchCenters, setResearchCenters] = useState([])
  const authContext = useContext(AuthContext);
  const [selectedType, setSelectedType] = useState('')

  const [redCured, setRedCured] = useState(false);
  const [yellowCured, setYellowCured] = useState(false);
  const [blueCured, setBlueCured] = useState(false);
  const [blackCured, setBlackCured] = useState(false);

  const [redErradicated, setRedErradicated] = useState(false);
  const [yellowErradicated, setYellowErradicated] = useState(false);
  const [blueErradicated, setBlueErradicated] = useState(false);
  const [blackErradicated, setBlackErradicated] = useState(false);

  const [infectionsSum, setInfectionsSum] = useState([0, 0, 0, 0])

  const [infections, setInfections] = useState(Array(48).fill(Array(4).fill(0)))
  const [players, setPlayers] = useState(Array.from(new Array(48), () => []))
  const [role, setRole] = useState()

  const [turn, setTurn] = useState(false)
  const [played, setPlayed] = useState(0)

  const [infectionSpeed, setInfectionSpeed] = useState(2)
  const [gameId, setGameId] = useState('')
  const [logout, setLogout] = useState(false)
  const [possibleMoves, setPossibleMoves] = useState([{'name':'Atlanta', 'id':0}])
  const [healable, setHealable] = useState([{name: 'NA', id: -1}])
  const [cards, setCards] = useState([{id: -1, type: 'null'}])
  const [canBuild, setCanBuild] = useState(false)
  const [curable, setCurable]=useState([{name:'NA', id:-1}])
  const [lost, setLost] = useState(false)
  const [confirmedLost, setConfirmedLost] = useState(false)
  const [discard, setDiscard] = useState(0)

  function update(){
    backend.get("/game", { headers: { Authorization: `Bearer ${localStorage.getItem('loginToken')}` } }).then(response => {
      console.log(response)
      setLost(response.data.lost)
      setGameId(response.data.game_id)
      setInfectionSpeed(response.data.infection_speed)
      setRedCured(response.data.cures.Vermelho)
      setYellowCured(response.data.cures.Amarelo)
      setBlackCured(response.data.cures.Preto)
      setBlueCured(response.data.cures.Azul)
      setInfections(Object.values(response.data.infections))
      setInfectionsSum(response.data.infections_sum)
      setResearchCenters(response.data.research_centers)
      setDiscard(response.data.discard)
      let decode = jwtDecode(localStorage.getItem('loginToken'));
      setTurn(response.data.users[response.data.turn.player] == authContext.data.id || response.data.users[response.data.turn.player] == decode.primarysid)
      response.data.users.map((id, i) => {
         if (id == authContext.data.id || id == decode.primarysid) {
           let location = response.data.players[i].location
           let playerRole = response.data.players[i].role
           setRole(playerRole) 
           setPossibleMoves(response.data.players[i].possible_moves)
           let locationInfections = Object.values(response.data.infections)[location]
           setHealable(locationInfections.map((v, index) => {if (v > 0) {return {name: colors[index], id: index} }}).filter(v => v!=null))
           let playerCards = response.data.players[i].cards
           let playerCityCards = playerCards.filter(v => v.type=='city')
           let amountToCure =  playerRole == 'Scientist'?4:5
           let colorsCurable = Array(0)
           for (let i=0; i<4; i++){
            if (playerCards.filter(v => v.city.color == i).length >= amountToCure){
              colorsCurable = colorsCurable.concat({name:colors[i], id: i})
            }
           }
           setCurable(colorsCurable)
           setCards(playerCards)
           console.log()
           if ((playerCityCards.filter((value) => location == value.id).length > 0 
                    || response.data.players[i].role == 'Operations Expert') 
                    && !(response.data.research_centers.filter(v => v==location).length > 0)){
             setCanBuild(true)
           } else {
             setCanBuild(false)
           }
           
         } 
      })
      var arr = Array.from(new Array(48), () => []);
      for (let player of response.data.players) {
        arr[player.location].push({ role: player.role.toLowerCase().replace(" ", "_") })
      }
      setPlayers(arr)
    }).catch(err =>{
      console.log(err)
    })
  }

  useEffect(() => {
    update()
  }, [played])

  useEffect(() => {
    const interval = setInterval(() => {
      update()
    }, 2000);
    return () => clearInterval(interval);
  }, []);


  return (
    <div class='App'>
      {lost && <Alert severity='error' style={{position: 'absolute', alignItems:'center', top:'5vw', zIndex: '20',width: '40vw', alignSelf:'center', flexDirection:'row'}} onClose={() => {
        backend.delete("/game/"+gameId, { headers: { Authorization: `Bearer ${localStorage.getItem('loginToken')}`}}).then(response => {
          setConfirmedLost(true)
         })
      }}><strong>Você perdeu o jogo!</strong></Alert>}
      {confirmedLost && <Redirect to={{
                    pathname: "/"
                  }}/>}
      <div style={{ color: "#efefef", fontSize: '1.3vw', fontWeight: 'bold', padding: '2vh',position: 'absolute', top: '1vh', right:'5vw', alignSelf:'center', borderRadius: '5px', backgroundColor: '#606060bb', display: 'flex', flexDirection: 'column', alignItems:'center', width: '13vw'}}>
        <img src={process.env.PUBLIC_URL+'/player_'+role.toLowerCase().replace(' ','_')+'512.png'} style={{ width: '3vw', margin: '1vh', marginLeft: '2vh', opacity:'100%' }} />
        <label>Você é</label>
        <label>{role}</label>
        <img src={process.env.PUBLIC_URL+'/information.png'} style={{position: "absolute", top: '1vh', right:'1vh', width:'1.5vw', height:'1.5vw'}}/>
      </div>

      <div style={{display: 'flex', flexDirection:'column', paddingTop:'1vh', paddingBottom: '1vh', position:'absolute', left:'68vw', bottom:'3vh', alignSelf: 'center', backgroundColor:'#606060', borderRadius:'5px', width:'10vw'}}>
        {cards.map((card, i) => 
          <div style={{display: 'flex', flexDirection:'row', justifyContent:'space-between', backgroundColor: i%2==0?"#454545":"#555555", alignItems: 'center'}}>
          <label style={{color: '#efefef', paddingLeft: '1vh'}}>
            {card.type == 'city'?card.city.name:card.action}
          </label>
          {card.type == 'city' && <img style={{width:'1vh', height: '1vh', paddingRight:'1vh'}} src={process.env.PUBLIC_URL+'/location_'+colorCodes[card.city.color]+'.png'}/>}
          </div>
        )}
      </div>  

      <div style={{ position: 'absolute', top: '3vh', width: '94vw', marginTop: '0', color: '#cfcfcf', height: '3rem' }}>
        <h1 style={{ position: 'absolute', top: '0', fontSize: '4rem', margin: '0', marginLeft: '6vw', opacity: '1', zIndex: '1' }}>Man VS Virus</h1>
        <div style={{ position: 'relative', top: '40%', marginLeft: '1vw', color: '#cbcbcb', opacity: '0.6', backgroundImage: 'url(' + process.env.PUBLIC_URL + '/ekg.png)', backgroundSize: "25% 100%", backgroundRepeat: 'no-repeat', height: '100%', width: '100%' }} />
      </div>

      <div style={{ position: 'absolute', top: '13vh', left: '67vw', marginTop: '0', color: '#cfcfcf', height: '4rem', display: "flex", flexDirection: 'row', alignItems: 'center' }}>
        <h3>Velocidade <br />de Infecção</h3>
        <div style={{ width: '4vw', height: '4vw', marginLeft: '1vw', textAlign: 'center', position: 'relative' }} class='gradSpeed'>
          <img src={process.env.PUBLIC_URL + infectionSpeed > 2 ? infectionSpeed > 3 ? '/speed_high.png' : '/speed_medium.png' : '/speed_low.png'}
            style={{ position: 'relative', top: '0', left: '0', width: '4vw', height: '4vw' }} />
          <label style={{ position: 'absolute', top: '15%', left: '30%', fontSize: '2.5vw', fontWeight: 'bold' }}>{infectionSpeed}</label>
        </div>
      </div>

      <div style={{ position: 'absolute', top: '0', alignSelf:'center', backgroundColor: '#606060', borderRadius: '0 0 5px 5px' }}>
        <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', color: '#efefef', fontSize: '1.5vw' }}>
          <label style={{ marginLeft: '0.5vw' }}>{infectionsSum[0]}/24</label>
          <img src={process.env.PUBLIC_URL + '/cube_blue.png'} style={{ width: '1.5vw', margin: '1vh' }} />
          <label style={{ marginLeft: '0.5vw' }}>{infectionsSum[1]}/24</label>
          <img src={process.env.PUBLIC_URL + '/cube_black.png'} style={{ width: '1.5vw', margin: '1vh' }} />
          <label style={{ marginLeft: '0.5vw' }}>{infectionsSum[2]}/24</label>
          <img src={process.env.PUBLIC_URL + '/cube_yellow.png'} style={{ width: '1.5vw', margin: '1vh' }} />
          <label style={{ marginLeft: '0.5vw' }}>{infectionsSum[3]}/24</label>
          <img src={process.env.PUBLIC_URL + '/cube_red.png'} style={{ width: '1.5vw', margin: '1vh' }} />
          <label style={{ margin: '1vh' }}> <span style={{fontWeight: 'bold'}}>Id:</span> {gameId}</label>
        </div>
      </div>
      <Actions selectedType={selectedType} setSelectedType={setSelectedType} curable={curable} discard={discard} build={canBuild} infected={healable} cards={cards} turn={turn} gameId={gameId} played={played} setPlayed={setPlayed} destinations={possibleMoves}/>
      <Cure key='red' color='red' top='50vh' cured={redCured} erradicated={redErradicated} />
      <Cure key='yellow' color='yellow' top='60vh' cured={yellowCured} erradicated={yellowErradicated} />
      <Cure key='blue' color='blue' top='70vh' cured={blueCured} erradicated={blueErradicated} />
      <Cure key='black' color='black' top='80vh' cured={blackCured} erradicated={blackErradicated} />
      <Location color={0} name='Atlanta' key='0' players={players[0]} x='10vw' y='33vh' researchCenter={researchCenters.includes(0)} infections={infections[0]} />
      <Location color={0} name='Montreal' key='10' players={players[10]} x='13vw' y='18vh' researchCenter={researchCenters.includes(10)} infections={infections[10]} />
      <Location color={0} name='New York' key='3' players={players[3]} x='23vw' y='21vh' researchCenter={researchCenters.includes(3)} infections={infections[3]} />
      <Location color={0} name='Chicago' key='1' players={players[1]} x='6vw' y='21vh' researchCenter={researchCenters.includes(1)} infections={infections[1]} />
      <Location color={0} name='São Francisco' key='2' players={players[2]} x='1vw' y='28vh' researchCenter={researchCenters.includes(2)} infections={infections[2]} />
      <Location color={0} name='Washington' key='4' players={players[4]} x='16vw' y='28vh' researchCenter={researchCenters.includes(4)} infections={infections[4]} />
      <Location color={0} name='Londres' key='8' players={players[8]} x='40vw' y='15vh' researchCenter={researchCenters.includes(8)} infections={infections[8]} />
      <Location color={0} name='Madri' key='9' players={players[9]} x='40vw' y='27vh' researchCenter={researchCenters.includes(9)} infections={infections[9]} />
      <Location color={0} name='Paris' key='11' players={players[11]} x='44.5vw' y='22vh' researchCenter={researchCenters.includes(11)} infections={infections[11]} />
      <Location color={0} name='Essen' key='6' players={players[6]} x='49vw' y='15vh' researchCenter={researchCenters.includes(6)} infections={infections[6]} />
      <Location color={0} name='São Petersburgo' key='5' players={players[5]} x='55vw' y='10vh' researchCenter={researchCenters.includes(5)} infections={infections[5]} />
      <Location color={0} name='Milão' key='7' players={players[7]} x='49vw' y='25vh' researchCenter={researchCenters.includes(7)} infections={infections[7]} />
      <Location color={2} name='Los Angeles' key='24' players={players[24]} x='5vw' y='39vh' researchCenter={researchCenters.includes(24)} infections={infections[24]} />
      <Location color={2} name='Miami' key='25' players={players[25]} x='17vw' y='40vh' researchCenter={researchCenters.includes(25)} infections={infections[25]} />
      <Location color={2} name='Cidade do México' key='27' players={players[27]} x='10vw' y='44vh' researchCenter={researchCenters.includes(27)} infections={infections[27]} />
      <Location color={2} name='Bogotá' key='30' players={players[30]} x='20vw' y='54vh' researchCenter={researchCenters.includes(30)} infections={infections[30]} />
      <Location color={2} name='Lima' key='34' players={players[34]} x='18vw' y='66vh' researchCenter={researchCenters.includes(34)} infections={infections[34]} />
      <Location color={2} name='Santiago' key='33' players={players[33]} x='18vw' y='86vh' researchCenter={researchCenters.includes(33)} infections={infections[33]} />
      <Location color={2} name='São Paulo' key='29' players={players[29]} x='26vw' y='70vh' researchCenter={researchCenters.includes(29)} infections={infections[29]} />
      <Location color={2} name='Buenos Aires' key='28' players={players[28]} x='23vw' y='79vh' researchCenter={researchCenters.includes(28)} infections={infections[28]} />
      <Location color={2} name='Lagos' right key='26' players={players[26]} x='42vw' y='49vh' researchCenter={researchCenters.includes(26)} infections={infections[26]} />
      <Location color={2} name='Kinshasa' key='35' players={players[35]} x='47vw' y='63vh' researchCenter={researchCenters.includes(35)} infections={infections[35]} />
      <Location color={2} name='Johanesburgo' key='31' players={players[31]} x='50vw' y='77vh' researchCenter={researchCenters.includes(31)} infections={infections[31]} />
      <Location color={2} name='Cartum' key='32' players={players[32]} x='52vw' y='48vh' researchCenter={researchCenters.includes(32)} infections={infections[32]} />
      <Location color={1} name='Cairo' key='21' players={players[21]} x='50vw' y='37vh' researchCenter={researchCenters.includes(21)} infections={infections[21]} />
      <Location color={1} name='Argel' key='23' players={players[23]} x='43vw' y='35vh' researchCenter={researchCenters.includes(23)} infections={infections[23]} />
      <Location color={1} name='Moscou' key='22' players={players[22]} x='57vw' y='19vh' researchCenter={researchCenters.includes(22)} infections={infections[22]} />
      <Location color={1} name='Istambul' key='16' players={players[16]} x='54vw' y='26vh' researchCenter={researchCenters.includes(16)} infections={infections[16]} />
      <Location color={1} name='Bagdá' key='18' players={players[18]} x='56vw' y='35vh' researchCenter={researchCenters.includes(18)} infections={infections[18]} />
      <Location color={1} name='Riad' key='19' players={players[19]} x='59vw' y='43vh' researchCenter={researchCenters.includes(19)} infections={infections[19]} />
      <Location color={1} name='Teerã' key='17' players={players[17]} x='59vw' y='28vh' researchCenter={researchCenters.includes(17)} infections={infections[17]} />
      <Location color={1} name='Carachi' key='20' players={players[20]} x='63vw' y='35vh' researchCenter={researchCenters.includes(20)} infections={infections[20]} />
      <Location color={1} name='Bombaim' key='13' players={players[13]} x='66.5vw' y='42vh' researchCenter={researchCenters.includes(13)} infections={infections[13]} />
      <Location color={1} name='Chennai' key='15' players={players[15]} x='68vw' y='50vh' researchCenter={researchCenters.includes(15)} infections={infections[15]} />
      <Location color={1} name='Deli' key='14' players={players[14]} x='68vw' y='32vh' researchCenter={researchCenters.includes(14)} infections={infections[14]} />
      <Location color={1} name='Calcutá' key='12' players={players[12]} x='71vw' y='38vh' researchCenter={researchCenters.includes(12)} infections={infections[12]} />
      <Location color={3} name='Sidney' key='45' players={players[45]} x='90vw' y='75vh' researchCenter={researchCenters.includes(45)} infections={infections[45]} />
      <Location color={3} name='Jacarta' key='47' players={players[47]} x='78vw' y='60vh' researchCenter={researchCenters.includes(47)} infections={infections[47]} />
      <Location color={3} name='Manila' key='44' players={players[44]} x='84vw' y='50vh' researchCenter={researchCenters.includes(44)} infections={infections[44]} />
      <Location color={3} name='Ho Chi Min' key='46' players={players[46]} x='78vw' y='48vh' researchCenter={researchCenters.includes(46)} infections={infections[46]} />
      <Location color={3} name='Bangkok' key='41' players={players[41]} x='74vw' y='45vh' researchCenter={researchCenters.includes(41)} infections={infections[41]} />
      <Location color={3} name='Hong Kong' key='37' players={players[37]} x='79vw' y='40vh' researchCenter={researchCenters.includes(37)} infections={infections[37]} />
      <Location color={3} name='Taipé' key='43' players={players[43]} x='82.5vw' y='38vh' researchCenter={researchCenters.includes(43)} infections={infections[43]} />
      <Location color={3} name='Osaka' key='40' players={players[40]} x='86vw' y='32vh' researchCenter={researchCenters.includes(40)} infections={infections[40]} />
      <Location color={3} name='Tóquio' key='39' players={players[39]} x='89vw' y='26vh' researchCenter={researchCenters.includes(39)} infections={infections[39]} />
      <Location color={3} name='Seul' key='42' players={players[42]} x='83.5vw' y='22.5vh' researchCenter={researchCenters.includes(42)} infections={infections[42]} />
      <Location color={3} name='Pequim' key='36' players={players[36]} x='76vw' y='23vh' researchCenter={researchCenters.includes(36)} infections={infections[36]} />
      <Location color={3} name='Xangai' key='38' players={players[38]} x='79vw' y='31vh' researchCenter={researchCenters.includes(38)} infections={infections[38]} />
    </div>
  );
}

export default Board;
