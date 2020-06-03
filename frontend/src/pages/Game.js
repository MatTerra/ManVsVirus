import React, { useEffect, useState } from 'react';
import Board from '../components/Board';
import isOnGame from '../utils/isOnGame'
import { Redirect } from 'react-router-dom'

const Game = ({history}) => {
    const [noGame, setNoGame] = useState(false)

    useEffect(() => { 
        async function changePage(){
            let data = await isOnGame()
            setNoGame(!data)
        }
        changePage()
    },[])

    return (
        <>
            {noGame && <Redirect to={{
                    pathname: "/"
                  }}/>}
            <Board/>
        </>
    )
};

export default Game;