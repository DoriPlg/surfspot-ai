import Axios from 'axios'

const axios = Axios.create({
    withCredentials: false
});
const BASE_URL = (process.env.NODE_ENV === 'production')
    ? '/which_beaches'
    : 'http://127.0.0.1:8000/which_beaches';

export const testService = {
    query
}
async function query(filterBy = {}) {
    // call of get from mongo backend to get list of beaches
    const res = await axios.get(`${BASE_URL}`, {
        crossDomain: true
    })
    return res.data
}
async function addReview(review) {
    // adding a review 
}
async function getReviews() {
    // getting the reviews 
}
async function getBeach(critiria) {
    // get a beach 
}



