import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import isLoggedIn from './isLoggedIn';

export default function ProtectedRoute({path, render}) {
  return (
      <>
        { isLoggedIn() ? 
            <Route path={path} exact render={render} />
            : <Redirect to={{
                pathname: "/entrar",
                search: "?msg=unauthorized"
              }}/>
        }
      </>
  );
}
