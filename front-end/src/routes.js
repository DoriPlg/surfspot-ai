
import { BestBeach } from "./pages/bestBeach";
import { Home } from "./pages/home";
import { Test } from "./pages/test";
// import { Test2 } from "./pages/test2";

const routes = [
    {
        path:'/',
        component: <Home/>,
    },
    {
       path:'/test',
       component: <Test/>,
    },
    // {
    //    path:'/test2',
    //    component: <Test2/>,
    // },
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