const axios = require('axios');

const date = new Date(); // the datetime object you want to pass

axios.get(`https://your-api-url.com/${date.toISOString()}`)
  .then(response => {
    const dictionary = response.data;
    console.log(dictionary);
  })
  .catch(error => {
    console.error(error);
  });
