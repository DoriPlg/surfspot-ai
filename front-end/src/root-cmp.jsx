import React from 'react'
import { Routes as Switch, Route } from 'react-router'
import { AppHeader } from './cmps/header.jsx'
import { Footer } from './cmps/footer.jsx'
import { AddReview } from './cmps/add-review.jsx'
import routes from './routes.js'

export class RootCmp extends React.Component {

    render() {
        return (
            <div>
                <AppHeader />
                <main>
                    <Switch>
                        {routes.map(route => <Route key={route.path} element={route.component} path={route.path} />)}
                    </Switch>
                </main>
                <AddReview />
                <Footer />
            </div>
        )
    }
}


