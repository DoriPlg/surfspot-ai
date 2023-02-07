import { BeachPreview } from "../cmps/beach-preview";
import { Loading } from "../cmps/loading";
import hero from "../assets/img/hero.jpg";
import React, { Component } from 'react'
import { connect } from 'react-redux'
import { loadBeaches } from '../store/actions/beach.actions';
import { AddReview } from "../cmps/add-review";
// import { stationServiceNew } from '../services/station.service.js';

class _Test extends Component {
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
           <div>
            <h1>here we do tests</h1>
           </div>
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


export const Test = connect(mapStateToProps, mapDispatchToProps)(_Test)


