import { NavLink } from "react-router-dom";
// import logo from '../assets/img/logo.png'

export function AppHeader() {
    return (
        <header className="app-header flex">
                {/* <img src={logo} alt="" /> */}
                <NavLink className="fas fa-search" to="/search"></NavLink>
        </header>
    )
}