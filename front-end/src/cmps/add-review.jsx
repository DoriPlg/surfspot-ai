import React, { Component } from 'react'
import { connect } from 'react-redux'
import { weatherApiService } from '../services/weatherAPI.service'
import { loadBeaches } from '../store/actions/beach.actions';
var MongoClient = require('mongodb').MongoClient; // Part of what Dori did


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
        const { date, time, rating } = this.state.review
        let conditions = weatherApiService.getConditions({ lat: 32.165804, long: 34.797245 },date,time)
        //let rateInsert = {
        //    "Wind Sp": conditions["windSpeed"],
        //    "Wind Dir": conditions["windDirection"], 
        //    "Swell Hgt": conditions["swellHeight"], 
        //    "Swell Dir": conditions["swellDirection"], 
        //    "Swell Prd": conditions["swellPeriod"], 
        //    "Tide": conditions["Tide"],
        //    "Rating": rating
        //}
        //MongoClient.connect("mongodb+srv://DoriP:<password>@cluster0.s7lzszz.mongodb.net/?retryWrites=true&w=majority", function(err, db) {
        //    if (err) throw err;
        //    var dbo = db.db("Reviews");
        //    dbo.collection("From Web").insertOne(rateInsert, function(err, res) {
        //      if (err) throw err;
        //      console.log("1 document inserted");
        //      db.close();
        //    });
        //});
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


