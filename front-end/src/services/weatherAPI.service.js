import {convertDateToUTC} from './utilService'
import axios from 'axios'
const params = 'windDirection,windSpeed,swellHeight,swellDirection,swellPeriod';
const KEY = '8c27fa22-389a-11ec-b37c-0242ac130002-8c27fa90-389a-11ec-b37c-0242ac130002';

async function getConditions(location,date,time) {
  //gets data from stormglass.io to set conditions in  the review
  let timeOfStart=date.split("-").concat(time.split(":"))
  let timeOfEnd=new Date(timeOfStart[0],parseInt(timeOfStart[1])-1,timeOfStart[2],parseInt(timeOfStart[3])+1,timeOfStart[4]).toISOString()
  timeOfStart= new Date(timeOfStart[0],parseInt(timeOfStart[1])-1,timeOfStart[2],timeOfStart[3],timeOfStart[4]).toISOString()
  try {
    const res = await axios.get(`https://api.stormglass.io/v2/weather/point?start=${timeOfStart}&end=${timeOfEnd}&lat=${location.lat}&lng=${location.long}&params=${params}`,{ headers:{
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
        // const resoults
        return res.data.hours ;
    }
    catch (err) {
        console.log('Cannwot reach server:', err);
      }
    }

    
    
    export const weatherApiService = {
        getConditions,
    }	
    // // https://api.stormglass.io/v2/tide/extremes/point?lat=32.053&lng=34.75&start=2023-02-01&end=2023-02-01&key=8c27fa22-389a-11ec-b37c-0242ac130002-8c27fa90-389a-11ec-b37c-0242ac130002"
    // https://api.stormglass.io/v2/weather/point?start=2023-03-01T10:05:00.000Z&end=2023-03-01T11:05:00.000Z&lat=32.165804&lng=34.797245&params=windDirection,windSpeed,swellHeight,swellDirection,swellPeriod&key=8c27fa22-389a-11ec-b37c-0242ac130002-8c27fa90-389a-11ec-b37c-0242ac130002"
