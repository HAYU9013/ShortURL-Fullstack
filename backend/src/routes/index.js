const express = require('express');
const userRoutes = require('./userRoutes');
const { authMiddleware } = require('../middleware/authMiddleware');
const urlRoutes = require('./urlRoutes');
const setRoutes = (app) => {
    console.log('Setting routes');
    app.use('/api/users', userRoutes);
    app.use('/api/url', urlRoutes);
};

module.exports = {setRoutes};