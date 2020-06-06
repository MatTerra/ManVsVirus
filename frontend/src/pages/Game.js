import React, { useEffect, useState, useContext } from 'react';
import Board from '../components/Board';
import isOnGame from '../utils/isOnGame'
import { Redirect, withRouter } from 'react-router-dom'
import { AuthContext } from '../contexts/AuthContext'

const Game = ({history}) => {
    const [noGame, setNoGame] = useState(false)
    const authContext = useContext(AuthContext);

    useEffect(() => { 
        async function changePage(){
            let data = await isOnGame()
            setNoGame(!data)
        }
        changePage()
    },[])

    function logout(){
        localStorage.removeItem("loginToken");
        authContext.logout();
        history.push({
          pathname: "/",
        });
        window.location.reload()
    }

    return (
        <>
            <img src={process.env.PUBLIC_URL+'/logout.png'} style={{position: 'absolute', top:'1.5vw', right:'1.5vw', width: '2vw', height: '2vw'}} onClick={() => logout()}/>
            {noGame && <Redirect to={{
                    pathname: "/"
                  }}/>}
            <Board/>
        </>
    )
};

export default withRouter(Game);