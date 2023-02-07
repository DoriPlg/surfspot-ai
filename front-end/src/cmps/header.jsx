import React, { Component } from 'react'
import { NavLink } from "react-router-dom";
// import logo from '../assets/img/logo.png'

export class AppHeader extends Component {
    state = {
        isNavOpen: false
    }
    onNavClick = () => {
        this.setState(prevState => ({ isNavOpen: !prevState.isNavOpen }))
        console.log('change')
    }

    render() {
        const { isNavOpen } = this.state
        return (
            <div className="flex column">
                <header className="app-header flex">
                    <div className={isNavOpen ? "fas fa-xmark" : "fas fa-bars"} onClick={this.onNavClick}></div>
                </header>
                {isNavOpen &&
                    <>
                        <NavLink to="/" className={({ isActive }) => (isActive ? "link active" : "link")}>
                            Home
                        </NavLink>
                        <NavLink to="/bestBeach" className={({ isActive }) => (isActive ? "link active" : "link")}>
                            Find Beach
                        </NavLink>
                        <NavLink to="/test" className={({ isActive }) => (isActive ? "link active" : "link")}>
                            test enviorment
                        </NavLink>
                        <NavLink to="/test" className={({ isActive }) => (isActive ? "link active" : "link")}>
                            test enviorment
                        </NavLink>
                        <NavLink to="/test" className={({ isActive }) => (isActive ? "link active" : "link")}>
                            test enviorment
                        </NavLink>
                    </>
                }
            </div>
        )
    }
}