const express = require('express');
const router = express.Router();
const { getDishes } = require('../controllers/dishController');

router.get('/', getDishes);

module.exports = router;


import express from 'express';
import bodyParser from 'body-parser';

import usersRoutes from './routes/users.js';

const app = express(); 
const PORT = 5000;

app.use(bodyParser.json());

app.use('/users', usersRoutes);

app.get('/', (req, res) => res.send('Hello from Homepage.'));

app.listen(PORT, () => console.log(`Server Running on port: http://localhost:${PORT}`));
