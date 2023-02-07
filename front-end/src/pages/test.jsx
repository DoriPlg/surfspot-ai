import React, { Component, useEffect, useState } from 'react'
import { connect } from 'react-redux'
import { testService } from '../services/testApi.js';
import axios from "axios";
import { type } from 'os';

class _Test extends Component {
    state = {
        beaches:[]
    }

    async componentDidMount() {
        let beaches = await testService.query();
        beaches = beaches.Beaches;
        this.setState({beaches})
    }

    // async componentDidUpdate(prevProps) {
    //     }
    // }


    render() {
        // var beaches = "test failed"
        // axios
        //     .get("http://127.0.0.1:8000/which_beaches",{
        //         crossDomain: true
        //     })
        //     .then(function (response) {
        //         beaches = response.data;
        //     });
        const {beaches} =this.state
        if (!beaches.length) return 'Loading...'
        return (
           <div>
            {beaches.map((beach)=>{
                return <h1>{beach}</h1>
            })}
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
}


export const Test = connect(mapStateToProps, mapDispatchToProps)(_Test)


