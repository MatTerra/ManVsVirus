import React from 'react';
import './assets/App.css';
import Login from './pages/Login';
import Cadastro from './pages/Cadastro';
import NewGame from './pages/NewGame';
import Auth from './contexts/AuthContext';
import ProtectedRoute from './utils/ProtectedRoute'
import {BrowserRouter as Router, Switch, Route} from  'react-router-dom';

const App = () => {
  return(
    <Auth>
      <Router>
        <div className="App">
          <Switch>
            <Route path="/entrar" exact component={Login} />
            <Route path="/cadastrar" exact component={Cadastro} />
            <ProtectedRoute
              path="/"
              exact
              render={()=> <NewGame />}/>
          </Switch>
        </div>
      </Router>
    </Auth>
  )
}

export default App;