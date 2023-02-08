import { convertDateToUTC } from './utilService'
import axios from 'axios'
const params = 'windDirection,windSpeed,swellHeight,swellDirection,swellPeriod';
const KEY = '8c27fa22-389a-11ec-b37c-0242ac130002-8c27fa90-389a-11ec-b37c-0242ac130002';

async function getConditions(location, dateTime) {
  //gets data from stormglass.io to set conditions in  the review
  let timeOfStart = new Date(dateTime)
  let timeOfEnd = new Date(timeOfStart.getFullYear(), timeOfStart.getMonth(), timeOfStart.getDate(), timeOfStart.getHours(), timeOfStart.getMinutes() + 1)
  // console.log(timeOfStart.toISOString());
  // console.log(timeOfEnd.toISOString());
  try {
    const res = await axios.get(`https://api.stormglass.io/v2/weather/point?start=${timeOfStart.toISOString()}&end=${timeOfEnd.toISOString()}&lat=${location.lat}&lng=${location.long}&params=${params}`, {
      headers: {
        'Authorization': KEY
      }
    })
    return res.data;
  }
  catch (err) {
    console.log('Cannot reach server:', err);
  }
}



export const weatherApiService = {
  getConditions,
}
    // // https://api.stormglass.io/v2/tide/extremes/point?lat=32.053&lng=34.75&start=2023-02-01&end=2023-02-01&key=8c27fa22-389a-11ec-b37c-0242ac130002-8c27fa90-389a-11ec-b37c-0242ac130002"
    // https://api.stormglass.io/v2/weather/point?start=2023-02-02T10:05:00.000Z&end=2023-02-02T11:05:00.000Z&lat=32.165804&lng=34.797245&params=windDirection,windSpeed,swellHeight,swellDirection,swellPeriod&key=8c27fa22-389a-11ec-b37c-0242ac130002-8c27fa90-389a-11ec-b37c-0242ac130002"
