import { Link } from 'react-router-dom';
import { Loading } from "../cmps/loading";
import hero from "../assets/img/hero.jpg";

export function Home() {
    return (
        <section className="home">
            <div className="hero">
                <h1>BestBeach</h1>
                <h4>Find the right beach for you</h4>
                <div className='findbtn'>Find</div>
            </div>
            <div className="wall">

            </div>
        </section>
    )
}