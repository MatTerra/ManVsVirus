import React, { useState } from 'react'
import { usersApi } from '../utils/api'
import { store } from "react-notifications-component";
import Loader from "react-loader-spinner";
import "react-notifications-component/dist/theme.css"

const Cadastro = ({history, locations}) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [confirmPassword, setConfirmPassword] = useState('')

    async function handleSubmit(e){
        setLoading(true);
        e.preventDefault();
        try {
            const response = await usersApi.post("/users",{
                email: email,
                password: password,
                passwordConfirmation: confirmPassword,
            });
            localStorage.setItem("loginToken", response.data.data.token);
            setLoading(false);
            history.push({
                pathname:"/entrar"
            })
            window.location.reload();
        } catch (err){

            let erro;
            if (err.response.data.message) {
                if (err.response.data.message === "Unauthorized") {
                    erro = "Senha incorreta";
                } else {
                    erro = err.response.data.message;
                }
            } else {
                erro = "Ocorreu um erro :( \n Tente novamente mais tarde.";
            }
        
            store.addNotification({
                title: "Erro",
                message: erro,
                type: "danger",
                insert: "top",
                container: "top-right",
                animationIn: ["animated", "fadeIn"],
                animationOut: ["animated", "fadeOut"],
                dismiss: {
                duration: 5000,
                onScreen: true,
                },
            });
            setLoading(false);
        }
    }

    return (
        <>
        <h1 style={{color: "white", marginBottom:"20vh", alignSelf: "center", fontSize:"6rem"}}>Man VS Virus</h1>
        <div class='login'>
            <form onSubmit={handleSubmit}>
                <div class='entrada'>
                    <label htmlFor="email">Email:</label> <input type="email" id="email" required value={email} class='detalhesJogo' style={{width: '20vw'}} onChange={e => {setEmail(e.target.value)}}/>
                </div>
                <div class='entrada'>
                    <label htmlFor="password">Senha:</label> <input id="password" required value={password} class='detalhesJogo' style={{width: '20vw'}} onChange={e => {setPassword(e.target.value)}} type="password"/>
                </div>
                <div class='entrada'>
                    <label htmlFor="password">Senha:</label> <input id="confirmPassword" required value={confirmPassword} class='detalhesJogo' style={{width: '20vw'}} onChange={e => {setConfirmPassword(e.target.value)}} type="password"/>
                </div>
                <div class='containerButton'>
                    { loading?<Loader
                            type="TailSpin"
                            color="#5cb50dbb"
                            height="1.5rem"
                            width="1.5rem"
                            />:
                        <button type="submit" disabled={loading} class='buttonDetail confirmCreate' style={{marginTop:"5vh"}}>Cadastrar</button>                       
                    }
                </div>
            </form>
        </div>
        
        </>
    )
}

export default Cadastro;