import React from 'react';
import './assets/App.css';
import Login from './pages/Login';
import Cadastro from './pages/Cadastro';
import NewGame from './pages/NewGame';
import Game from './pages/Game';
import JoinGame from './pages/JoinGame';
import Auth from './contexts/AuthContext';
import ProtectedRoute from './utils/ProtectedRoute';
import isOnGame from './utils/isOnGame';
import {BrowserRouter as Router, Switch, Route, Redirect} from  'react-router-dom';

const App = () => {
  return(
    <Auth>
      <Router>
        <div className="App">
          <Switch>
            <Route path="/entrar" exact component={Login} />
            <Route path="/cadastrar" exact component={Cadastro} />
            <ProtectedRoute path="/participar" exact render={() => <JoinGame />}/>
            <ProtectedRoute path="/jogo" exact render={() => <Game />} />
            <ProtectedRoute
              path="/"
              exact
              render={() => <NewGame />}/>
          </Switch>
        </div>
      </Router>
    </Auth>
  )
}

export default App;