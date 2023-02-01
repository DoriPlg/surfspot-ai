const axios = require('axios');
const express = require('express');
const app = express();

app.get('/response', (req, res) => {
  const date = new Date(); // the datetime object you want to pass

  axios.get(`https://your-api-url.com/${date.toISOString()}`)
    .then(response => {
      const dictionary = response.data;
      res.json(dictionary);
    })
    .catch(error => {
      console.error(error);
      res.status(500).send('Error getting dictionary from API');
    });
});

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});
