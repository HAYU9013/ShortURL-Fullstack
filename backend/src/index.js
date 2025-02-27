const express = require('express');
const bodyParser = require('body-parser');
const { connectDB } = require('./database/db');
const { setRoutes } = require('./routes/index');
const showLinkApi = require('./middleware/showLinkApi'); // Corrected import
const cors = require('cors');

const app = express();
const port = 3000;

connectDB();

const corsOptions = {
  origin: 'http://localhost:5173', // 請求來源
  credentials: true, // 必須設為 true
};
app.use(cors(corsOptions));

app.use(showLinkApi);
app.use(bodyParser.json());
setRoutes(app);

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

module.exports = app;
