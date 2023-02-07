import { BeachPreview } from "../cmps/beach-preview";
import { Loading } from "../cmps/loading";
import hero from "../assets/img/hero.jpg";
import React, { Component, useEffect, useState } from 'react'
import { connect } from 'react-redux'
import { loadBeaches } from '../store/actions/beach.actions';
import { AddReview } from "../cmps/add-review";
import axios from "axios";
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
        var beaches = "test failed"
        axios
            .get("http://127.0.0.1:8000/which_beaches",{
                crossDomain: true
            })
            .then(function (response) {
                beaches = response.data;
                console.log(beaches)
            });
        return (
           <div>
            <h1 id="content">{beaches}</h1>
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


