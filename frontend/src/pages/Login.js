import React, { useState } from 'react'
import { usersApi } from '../utils/api'
import { store } from "react-notifications-component";

const Login = ({history, locations
}) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e){
        setLoading(true);
        e.preventDefault();
        try {
            const response = await usersApi.post("/users/login",{
                email: email,
                password: password,
            });
            localStorage.setItem("loginToken", response.data.data.token);
            setLoading(false);
            history.push({
                pathname:"/"
            });
            window.location.reload();
        } catch (err){
            let errors = [];
            let erro;
            if (err.response && err.response.data && err.response.data.data) {
                err.response.data.data.map((er) => errors.push(er.message));
                // setErrorMsg(errors.join("\n"));
                erro = errors.join("\n");
            } else if (err.response.data) {
                if (err.response.data.message === "Unauthorized") {
                // setErrorMsg("Senha incorreta");
                erro = "Senha incorreta";
                } else {
                // setErrorMsg(err.response.data.message);
                erro = err.response.data.message;
                }
            } else {
                // setErrorMsg("Ocorreu um erro :( \n Tente novamente mais tarde.");
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
                    <label htmlFor="email">Email:</label> <input type="email" id="email" required value={email} class='detalhesJogo' style={{width: '25vw'}} onChange={e => {setEmail(e.target.value)}}/>
                </div>
                <div class='entrada'>
                    <label htmlFor="password">Senha:</label> <input id="password" required value={password} class='detalhesJogo' style={{width: '25vw'}} onChange={e => {setPassword(e.target.value)}} type="password"/>
                </div>
                <div class='containerButton'>
                    <button type="submit" disabled={loading} class='buttonDetail confirmCreate' style={{marginTop:"5vh"}}>Login</button>
                </div>
            </form>
            <div class='entrada'>
                <button class='cadastro' style={{marginTop:"5vh", marginBottom:"1vh"}} onClick={() => {history.push({ pathname:"/cadastrar" });}}>Criar nova conta</button>
            </div>
            <div class='entrada'>
                <button class='cadastro' style={{marginTop:"5vh", marginBottom:"1vh"}} onClick={() => {history.push({ pathname:"/jogo" });}}>Criar nova conta</button>
            </div>
        </div>
        
        </>
    )
}

export default Login;