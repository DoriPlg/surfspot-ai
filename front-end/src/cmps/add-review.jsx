import React, { Component } from 'react';
import dayjs from 'dayjs';
import Button from '@mui/material/Button';
import { MobileDatePicker } from '@mui/x-date-pickers/MobileDatePicker';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import MenuItem from '@mui/material/MenuItem';
import Rating from '@mui/material/Rating';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { connect } from 'react-redux'
import { weatherApiService } from '../services/weatherAPI.service'
import { loadBeaches } from '../store/actions/beach.actions';

class _AddReview extends Component {
    state = {
        isReview: false,
        beachName: '',
        dateTime: '',
        rating: 3.5
    }
    componentDidMount() {
        const dateTime = new Date()
        this.setState((prevState) => ({ ...prevState, dateTime: dayjs(dateTime) }))
        this.props.loadBeaches()
    }
    onToggleReview = () => {
        this.setState(prevState => ({ ...prevState, isReview: !prevState.isReview }))
    }
    handleChange = (ev) => {
        this.setState((prevState) => ({ ...prevState, age: ev.target.value }))
    }
    handleChangeDate = (ev) => {
        this.setState((prevState) => ({ ...prevState, dateTime: ev }))
    }
    handleChangeRating = (ev, newValue) => {
        this.setState((prevState) => ({ ...prevState, rating: newValue }))
    }
    onAddReview = (ev) => {
        let { dateTime, rating, beachName } = this.state
        dateTime=dayjs(dateTime).toISOString()
        console.log(dateTime)
        let conditions = weatherApiService.getConditions({ lat: 32.165804, long: 34.797245 }, dateTime)
    }


    render() {
        const { isReview, beachName, dateTime, rating } = this.state
        const { beaches } = this.props
        // console.log(beaches)
        return (
            <>
                {!isReview &&
                    <div className="add-review flex justify-center align-center" onClick={this.onToggleReview} >
                        <div className="fas fa-plus"></div>
                    </div>
                }
                {isReview &&
                    <>
                        <div className="screen" onClick={this.onToggleReview}></div>

                        <div className="review-form">
                            <h1>Rate a Beach</h1>
                            <div className=" fas fa-xmark"></div>
                            <LocalizationProvider dateAdapter={AdapterDayjs}>
                                <FormControl fullWidth>
                                    <InputLabel id="demo-simple-select-label">Beach Name</InputLabel>
                                    <Select
                                        className='banana'
                                        labelId="demo-simple-select-label"
                                        id="demo-simple-select"
                                        value={beachName}
                                        label="Beach Name"
                                        onChange={this.handleChange}
                                    >
                                        {beaches.map((beach, idx) => {
                                            return (<MenuItem value={beach.name} key={idx}>{beach.name}</MenuItem>)
                                        })
                                        }
                                    </Select>
                                    <MobileDatePicker
                                        label="Date mobile"
                                        inputFormat="MM/DD/YYYY"
                                        className='banana'
                                        value={dateTime}
                                        onChange={this.handleChangeDate}
                                        renderInput={(params) => <TextField {...params} />}
                                    />
                                    <TimePicker
                                        label="Time"
                                        value={dateTime}
                                        onChange={this.handleChangeDate}
                                        className='banana'
                                        renderInput={(params) => <TextField {...params} />}
                                    />
                                    <Rating
                                        name="rating"
                                        max={7}
                                        precision={0.5}
                                        size="large"
                                        value={rating}
                                        onChange={this.handleChangeRating}
                                        className='banana'
                                    />
                                    <Button variant="contained" onClick={this.onAddReview}>Submit</Button>
                                </FormControl>
                            </LocalizationProvider>
                        </div>
                    </>
                }
            </>
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


