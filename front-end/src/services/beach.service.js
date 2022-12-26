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
    const res = await axios.get(`${BASE_URL}`, { params: filterBy })
    return res.data
}

