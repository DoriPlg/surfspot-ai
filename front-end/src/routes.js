//import {HomePage} from './pages/home-page.jsx'
//import {AboutUs} from './pages/about-us.jsx'
//import {CarApp} from './pages/car-app.jsx'

import { BestBeach } from "./pages/bestBeach";
import { Home } from "./pages/home";
import { Test } from "./pages/test";

const routes = [
    {
        path:'/',
        component: <Home/>,
    },
    {
       path:'/test',
       component: <Test/>,
    },
    {
        path:'/bestBeach',
        component: <BestBeach/>,
     }
    //{
    //    path:'/about',
    //    component: AboutUs,
    //}
]

export default routes;