require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const compression = require('compression');
const helmet = require('helmet');
const pinoHttp = require('pino-http');
const { connectDB } = require('./database/db');
const { setRoutes } = require('./routes/index');
const showLinkApi = require('./middleware/showLinkApi');
const logger = require('./utils/logger');

const app = express();
const port = parseInt(process.env.PORT || '3000', 10);
const allowedOrigins = (process.env.ALLOWED_ORIGINS || 'http://localhost:5173')
  .split(',')
  .map((origin) => origin.trim())
  .filter(Boolean);

connectDB();

const corsOptions = {
  origin(origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      logger.warn({ origin }, 'Blocked by CORS policy');
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
};

app.set('trust proxy', 1);
app.use(pinoHttp({ logger }));
app.use(helmet());
app.use(compression());
app.use(cors(corsOptions));

app.use(showLinkApi);
app.use(bodyParser.json({ limit: process.env.REQUEST_PAYLOAD_LIMIT || '1mb' }));
setRoutes(app);

app.get('/healthz', (_req, res) => {
  res.status(200).json({ status: 'ok' });
});

// Centralised error handler for known middleware failures
// eslint-disable-next-line no-unused-vars
app.use((err, _req, res, _next) => {
  if (err.message === 'Not allowed by CORS') {
    return res.status(403).json({ message: 'Forbidden origin' });
  }

  logger.error({ err }, 'Unhandled application error');
  return res.status(500).json({ message: 'Internal Server Error' });
});

app.listen(port, () => {
  logger.info({ port }, 'Server listening');
});

module.exports = app;
