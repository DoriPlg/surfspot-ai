import Axios from 'axios'

const axios = Axios.create({
    withCredentials: true
});
const BASE_URL = (process.env.NODE_ENV === 'production')
    ? '/api/station'
    : 'http://localhost:3030/api/beach';

export const beachService = {
    query
}

async function query(filterBy = {}) {
    // call of get from mongo backend to get list of beaches
    const res = await axios.get(`${BASE_URL}`, { params: filterBy })
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



