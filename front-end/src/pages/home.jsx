import { BeachPreview } from "../cmps/beach-preview";
import { Loading } from "../cmps/loading";
import hero from "../assets/img/hero.jpg";
import React, { Component } from 'react'
import { connect } from 'react-redux'
import { loadBeaches } from '../store/actions/beach.actions';
import { AddReview } from "../cmps/add-review";
// import { stationServiceNew } from '../services/station.service.js';

class _Home extends Component {
    state = {
    }

    async componentDidMount() {
        await this.props.loadBeaches();
    }

    // async componentDidUpdate(prevProps) {
    //     }
    // }


    render() {
        let { beaches } = this.props
        if (!beaches) return <Loading />
        return (
            <section className="home">
                <div className="hero flex column">
                    <div className="flex  column align-center justify-center">
                    <h4 className="welcome">Welcome to:</h4>
                    <h1>BestBeach</h1>
                    <h4>Find the right beach for you</h4>
                    </div>
                    <div className="flex align-center justify-center">
                    <div className='findBtn flex align-center justify-center'>Find</div>
                    </div>
                </div>
                <div className="info">
                    <h2>About the app:</h2>
                    <h4>We found a way to caculate the best beach to the conditions.</h4>
                    <h4>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Aliquam delectus excepturi dolor aut minima animi cum</h4>
                    <h4> beatae dolorum possimus provident nulla, quia culpa quidem laborum tempora architecto soluta! Magni, modi!</h4>
                </div>
                <div className="beaches-in-area flex column">
                    <h2>Main beaches in your area:</h2>
                    <BeachPreview  beaches={beaches}/>
                </div>
            </section>
        )
    }


}

function mapStateToProps(state) {
    return {
        beaches: state.beachMoudle.beaches,
    }
}
const mapDispatchToProps = {
    loadBeaches
}


export const Home = connect(mapStateToProps, mapDispatchToProps)(_Home)


