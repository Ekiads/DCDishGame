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


// the users routers

import express from 'express';
import { v4 as uuidv4 } from 'uuid';

const router = express.Router();

let users = [];

// all routes in here are starting with /users
router.get('/', (req, res) => {
    res.send(users);
});

router.post('/', (req, res) => {
    const user = req.body;

    users.push({ ...user, id: uuidv4() });

    res.send(`User with the name ${user.firstName} added to the database!`);
});

// /users/2 => req.params { id: 2}

router.get('/:id', (req, res) => {
    const { id } = req.params;

    const foundUser = users.find((user) => user.id == id);

    res.send(foundUser)
})

router.delete('/:id', (req,res) => {
    const { id } = req.params;

    users = users.filter((user) => user.id !== id);

    res.send(`User with the id ${id} deleted from the database.`)
})

router.patch('/:id', (req, res) => {
    const { id } = req.params;

    const { firstName, lastName, age } = req.body;

    const user = users.find((user) => user.id == id);

    if(firstName) user.firstName = firstName;
    if(lastName) user.lastName = lastName; 
    if(age)  user.age = age; 

    res.send(`User with the id ${id} has been updated`);
})

export default router;
