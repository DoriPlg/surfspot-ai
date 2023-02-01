import React, { Component } from 'react'
import { connect } from 'react-redux'
import { weatherApiService } from '../services/weatherAPI.service'
import { loadBeaches } from '../store/actions/beach.actions';


// component of a form to add a review
class _AddReview extends React.Component {
    state = {
        review: {
            beachName: '',
            date: '',
            rating: '',
            time: '',
        },
    }

    // clearState = () => {
    //     const clearTemplate = {
    //         credentials: {
    //             username: '',
    //             password: '',
    //             fullname: ''
    //         },
    //         isSignup: false
    //     }
    //     this.setState({ clearTemplate })
    // }
    handleChange = (ev) => {
        const field = ev.target.name;
        const value = ev.target.value;
        this.setState({ review: { ...this.state.review, [field]: value } });
    }

    onAddReview = (ev) => {
        console.log(this.state);
        const { date, time } = this.state.review
        console.log(weatherApiService.getConditions({ lat: 32.165804, long: 34.797245 },date,time))
    }


    render() {
        const { beachName, rating } = this.state.review;
        return (
            <form onSubmit={(ev) => { ev.preventDefault(); }} >
                <input type="text"
                    name="beachName"
                    id="beachName"
                    label="BeachName"
                    placeholder="Beach Name"
                    value={beachName}
                    onChange={this.handleChange}
                />
                <input type="date"
                    name="date"
                    id=""
                    onChange={this.handleChange} />
                <input type="time"
                    name="time"
                    onChange={this.handleChange} />
                <input type="number"
                    name="rating"
                    id="rating"
                    label="rating"
                    value={rating}
                    onChange={this.handleChange}
                />
                <button onClick={this.onAddReview}>submit</button>
            </form>
        );
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


export const AddReview = connect(mapStateToProps, mapDispatchToProps)(_AddReview)


