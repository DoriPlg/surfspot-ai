import React from 'react'

// const { Switch, Route } = ReactRouterDOM
import { Routes as Switch, Route } from 'react-router'
import { AppHeader } from './cmps/header.jsx'

import routes from './routes.js'

//import {AppHeader} from './cmps/app-header.jsx'
// import {AppFooter} from './cmps/app-footer.jsx'

export class RootCmp extends React.Component {

    render() {
        return (
            <div>
                <AppHeader/>
                <main>
                    <Switch>
                        {routes.map(route => <Route key={route.path} element={route.component} path={route.path} />)}
                    </Switch>
                </main>
            </div>
        )
    }
}


