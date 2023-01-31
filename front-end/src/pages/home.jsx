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
        // await this.props.loadBeaches();
    }

    // async componentDidUpdate(prevProps) {
    //     }
    // }


    render() {
        // let { beaches } = this.props
        // if (!beaches) return <Loading />
        return (
            <section className="home">
                <div className="hero">
                    <h1>BestBeach</h1>
                    <h4>Find the right beach for you</h4>
                    <div className='findbtn'>Find</div>
                </div>
                <div className="wall">
                    {/* <BeachPreview beaches={beaches} /> */}
                    <AddReview/>
                    {/* <iframe src="http://localhost:8000/numcrunch" title="Pull from main"> </iframe> */}
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


