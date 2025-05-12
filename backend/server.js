const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const dishRoutes = require('./routes/dishes');

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());

// Routes
app.use('/dishes', dishRoutes);

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
