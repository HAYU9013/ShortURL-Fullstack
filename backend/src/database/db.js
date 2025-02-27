// filepath: /c:/coding/testing/messageBoard/backend/src/db.js
const mongoose = require('mongoose');
const User = require('../models/userModels');
const Url = require('../models/urlModels');
// const redis = require('redis');
const connectDB = async () => {
    try {
        // const dburl = 'mongodb://localhost:27017/UsersData';
        const dburl = process.env.MONGO_URL || 'mongodb://localhost:27017/UsersData';
        console.log('dburl:', dburl);
        await mongoose.connect(dburl, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });

        const checkAndCreateCollection = async (model, collectionName) => {
            const collections = await mongoose.connection.db.listCollections().toArray();
            const collectionExists = collections.some(col => col.name === collectionName);
            if (!collectionExists) {
                await model.createCollection();
                console.log(`${collectionName} collection created`);
            } else {
                console.log(`${collectionName} collection already exists`);
            }
        };

        await checkAndCreateCollection(User, 'users');
        await checkAndCreateCollection(Url, 'urls');
        console.log('MongoDB connected');
    } catch (error) {
        console.error('MongoDB connection error:', error);
        process.exit(1);
    }
};

module.exports = { connectDB };