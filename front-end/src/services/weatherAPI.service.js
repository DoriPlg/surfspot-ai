import {convertDateToUTC} from './utilService'
import axios from 'axios'
const params = 'windDirection,windSpeed,swellHeight,swellDirection,swellPeriod';
const KEY = '8c27fa22-389a-11ec-b37c-0242ac130002-8c27fa90-389a-11ec-b37c-0242ac130002';

async function getConditions(location,date,time) {
  //gets data from stormglass.io to set conditions in  the review
  const timeInUtc=convertDateToUTC(date,time)
  return timeInUtc
  try {
    const res = await axios.get(`https://api.stormglass.io/v2/weather/point?start=${timeInUtc}&lat=${location.lat}&lng=${location.long}&params=${params}`,{ headers:{
      'Authorization': KEY
    }})
        // const trackResult = res.data.items.map((track, idx) => {
        //   return {
        //     id: track.id.videoId,
        //     title: track.snippet.title,
        //     imgUrl: track.snippet.thumbnails.high ? track.snippet.thumbnails.high.url : track.snippet.thumbnails.default.url,
        //     duration: duration[idx]
        //   }
        // })
    }
    catch (err) {
        console.log('Cannwot reach server:', err);
      }
    }

    
    
    export const weatherApiService = {
        getConditions,
    }	
    // https://api.stormglass.io/v2/tide/extremes/point?lat=32.053&lng=34.75&start=2023-01-31&end=2023-02-01&key=8c27fa22-389a-11ec-b37c-0242ac130002-8c27fa90-389a-11ec-b37c-0242ac130002"
    // https://api.stormglass.io/v2/weather/point?lat=32.1&lng=34.7&start=2023-01-31T12:00&end=2023-01-31T13:00&params=windDirection,windSpeed,waveHeight,wavePeriod,swellHeight,swellDirection,swellPeriod&key=8c27fa22-389a-11ec-b37c-0242ac130002-8c27fa90-389a-11ec-b37c-0242ac130002