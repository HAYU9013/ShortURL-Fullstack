const fs = require('fs');
const path = require('path');
const mongoose = require('mongoose');
const User = require('../models/userModels');
const Url = require('../models/urlModels');
const logger = require('../utils/logger');

const resolveCaFile = () => {
  if (process.env.MONGO_TLS_CA_FILE) {
    return process.env.MONGO_TLS_CA_FILE;
  }

  if (process.env.MONGO_TLS_CA_B64) {
    const caPath = path.join('/tmp', 'mongo-ca.pem');
    if (!fs.existsSync(caPath)) {
      fs.writeFileSync(caPath, Buffer.from(process.env.MONGO_TLS_CA_B64, 'base64'));
    }
    return caPath;
  }

  return undefined;
};

const connectDB = async () => {
  try {
    const dburl = process.env.MONGO_URL || 'mongodb://localhost:27017/UsersData';
    const isTlsEnabled = String(process.env.MONGO_TLS || '').toLowerCase() === 'true';

    const mongoOptions = {
      useNewUrlParser: true,
      useUnifiedTopology: true,
      serverSelectionTimeoutMS: parseInt(process.env.MONGO_SERVER_SELECTION_TIMEOUT_MS || '30000', 10),
    };

    if (process.env.MONGO_MAX_POOL_SIZE) {
      mongoOptions.maxPoolSize = parseInt(process.env.MONGO_MAX_POOL_SIZE, 10);
    }

    if (process.env.MONGO_MIN_POOL_SIZE) {
      mongoOptions.minPoolSize = parseInt(process.env.MONGO_MIN_POOL_SIZE, 10);
    }

    if (process.env.MONGO_REPLICA_SET) {
      mongoOptions.replicaSet = process.env.MONGO_REPLICA_SET;
    }

    if (process.env.MONGO_READ_PREFERENCE) {
      mongoOptions.readPreference = process.env.MONGO_READ_PREFERENCE;
    }

    if (isTlsEnabled) {
      mongoOptions.tls = true;
      const tlsCAFile = resolveCaFile();
      if (tlsCAFile) {
        mongoOptions.tlsCAFile = tlsCAFile;
      }

      if (!process.env.MONGO_RETRY_WRITES) {
        mongoOptions.retryWrites = false;
      }
    }

    if (process.env.MONGO_RETRY_WRITES) {
      mongoOptions.retryWrites = String(process.env.MONGO_RETRY_WRITES).toLowerCase() === 'true';
    }

    const safeUrl = dburl.replace(/:[^:@/]*@/, '://****:****@');
    logger.info({ dburl: safeUrl }, 'Connecting to MongoDB');
    await mongoose.connect(dburl, mongoOptions);

    const checkAndCreateCollection = async (model, collectionName) => {
      const collections = await mongoose.connection.db.listCollections().toArray();
      const collectionExists = collections.some((col) => col.name === collectionName);
      if (!collectionExists) {
        await model.createCollection();
        logger.info({ collectionName }, 'Collection created');
      } else {
        logger.debug({ collectionName }, 'Collection already exists');
      }
    };

    await checkAndCreateCollection(User, 'users');
    await checkAndCreateCollection(Url, 'urls');
    logger.info('MongoDB connected');
  } catch (error) {
    logger.error({ err: error }, 'MongoDB connection error');
    process.exit(1);
  }
};

module.exports = { connectDB };
