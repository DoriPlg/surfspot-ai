import { BeachPreview } from "../cmps/beach-preview";
import { Loading } from "../cmps/loading";
import hero from "../assets/img/hero.jpg";
import React, { Component } from 'react'
import { connect } from 'react-redux'
import { loadBeaches } from '../store/actions/beach.actions';
import { AddReview } from "../cmps/add-review";
// import { stationServiceNew } from '../services/station.service.js';

class _BestBeach extends Component {
    state = {
    }

    async componentDidMount() {
        // await this.props.loadBeaches();

    }
    handleChange = (ev) => {
        const field = ev.target.name;
        const value = ev.target.value;
        this.setState({ ...this.state, [field]: value });
    }
    getBestBeach=(ev)=>{

    }

    render() {
        return (
            <section className="bestBeach">
                <form onSubmit={(ev) => { ev.preventDefault(); }} >
                    <input type="date"
                        name="date"
                        onChange={this.handleChange} />
                    <input type="time"
                        name="time"
                        onChange={this.handleChange} />
                    <button onClick={this.getBestBeach}></button>
                </form>
                {/* previeew of the forcast for that date and time */}
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


export const BestBeach = connect(mapStateToProps, mapDispatchToProps)(_BestBeach)


