import React, { useState, useEffect, useContext } from 'react'
import {Redirect} from 'react-router-dom'
import isOnGame from '../utils/isOnGame'
import {backend} from '../utils/api'
import { AuthContext } from '../contexts/AuthContext'

const JoinGame = ({history}) => {
    const [senha, setSenha] = useState('')
    const [gameId, setGameId] = useState('')
    const [game, setGame] = useState(false)
    const authContext = useContext(AuthContext)

    useEffect(() => { 
        async function changePage(){
            let data = await isOnGame()
            setGame(data)
        }
        changePage()
    },[])

    async function handleSubmit(e){
        e.preventDefault();
        backend.post(`/game/${gameId}`, {'password':senha}, { headers: { Authorization: `Bearer ${localStorage.getItem('loginToken')}`}}).then(() => {
            setGame(true)
        })
        
    }

    function logout(){
        localStorage.removeItem("loginToken");
        authContext.logout();
        history.push({
          pathname: "/",
        });
        window.location.reload()
    }
        

    return(
        <>
        <img src={process.env.PUBLIC_URL+'/logout.png'} style={{position: 'absolute', top:'1.5vw', right:'1.5vw', width: '2vw', height: '2vw'}} onClick={() => logout()}/>
        {game && <Redirect to={{
                    pathname: "/jogo"
                  }}/>}
        <h1 style={{color: "white", marginBottom:"20vh", alignSelf: "center", fontSize:"6rem"}}>Man VS Virus</h1>
        <div class='newGame'>
            <div class='entrada' style={{justifyContent: 'space-between', minWidth:"20vw"}}>
                <p style={{width: "50%"}}>Código do Jogo: </p> 
                <input class='detalhesJogo' style={{width: '10rem'}} onChange={e => {setGameId(e.target.value)}}/>
            </div>
            <div class='entrada' style={{justifyContent: 'space-between', minWidth:"20vw"}}>
                <p style={{width: "50%"}}>Senha do Jogo: </p> 
                <input class='detalhesJogo' style={{width: '10rem'}} onChange={e => {setSenha(e.target.value)}}/>
            </div>
            <div class='entrada'>
                <button class='buttonDetail confirmCreate' style={{marginTop:"5vh", marginBottom:'2vh'}} onClick={e => handleSubmit(e)}>Entrar no Jogo</button>
            </div>
            <div class='entrada'>
                <button class='cadastro' style={{marginTop:"5vh", marginBottom:'2vh'}} onClick={() => history.push({pathname: '/'})}>Criar um novo jogo</button>
            </div>
        </div>
        </>
    )
}

export default JoinGame