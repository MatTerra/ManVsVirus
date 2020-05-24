import React, { useState } from 'react'
import '../assets/App.css'
import Button from '../components/Button'

const NewGame = () => {
    const [nPlayers, setNPlayers] = useState(2)
    const [dificuldade, setDificuldade] = useState(0)
    const [senha, setSenha] = useState('')

    return(
        <>
        <h1 style={{color: "white", marginBottom:"20vh", alignSelf: "center", fontSize:"6rem"}}>Man VS Virus</h1>
        <div class='newGame'>
            <div class='entrada' style={{justifyContent: 'space-between', minWidth:"20vw"}}>
                <p style={{width: "50%"}}>Senha do Jogo: </p> <input class='detalhesJogo' style={{width: '10rem'}} onChange={e => {setSenha(e.target.value)}}/>
            </div>
            <div class='entrada' style={{justifyContent: 'space-between', minWidth:"20vw"}}> 
                <p>Número de Jogadores: </p>
                <div class = 'entrada'style={{justifyContent: 'space-between', paddingRight:'0px'}}> 
                    <button class="buttonDetail" onClick={() =>{if (nPlayers>2){setNPlayers(nPlayers-1)}}}>-</button> 
                    <input class='detalhesJogo' value = {nPlayers} disabled/> 
                    <button class="buttonDetail" style={{marginRight: '0vw'}} onClick={() =>{if (nPlayers<4){setNPlayers(nPlayers+1)}}}>+</button>
                </div>
            </div>
            <div class='entrada' style={{minWidth: "20vw"}}>
                <p>Dificuldade: </p> 
                <Button assignedClass="buttonDetail" onClick={() => {setDificuldade(0)}} color={dificuldade==0?"#5cb50d99":"#20202099"} text="Fácil"/> 
                <Button assignedClass="buttonDetail" onClick={() => {setDificuldade(1)}} color={dificuldade==1?"#5cb50d99":"#20202099"} text="Médio"/> 
                <Button assignedClass="buttonDetail" onClick={() => {setDificuldade(2)}} color={dificuldade==2?"#5cb50d99":"#20202099"} text="Difícil"/>
                <Button assignedClass="buttonDetail" onClick={() => {setDificuldade(3)}} color={dificuldade==3?"#5cb50d99":"#20202099"} text="Heróico"/>
            </div>
            <div class='entrada'>
                <button class='buttonDetail confirmCreate' style={{marginTop:"5vh", marginBottom:'2vh'}}>Criar novo jogo</button>
            </div>
        </div>
        </>
    )
}

export default NewGame