const express = require('express');
const authMiddleware = require('../middleware/authMiddleware');
const jwt = require('jsonwebtoken');
const router = express.Router();
const User = require('../models/userModels');



router.post('/register', async (req, res) => {
    try {
        const { username, password } = req.body;
        const existingUser = await User.findOne({ username });
        if (existingUser) {
            return res.status(400).send('User already exists');
        }
        const user = new User({ username, password });
        console.log(user);
        await user.save();
        res.status(201).send('User registered');
    } catch (error) {
        res.status(400).send('Error registering user');
    }
});

router.post('/login', async (req, res) => {
    const { username, password } = req.body;
    try {
        const user = await User.findOne({ username, password });
        if (user) {
            const token = jwt.sign({ username: user.username }, '999', { expiresIn: '6000s' });
            res.cookie('token', token, { httpOnly: false, secure: true, sameSite: 'None' });

            res.json({ token, username: user.username });
        } else {
            res.status(401).send('Invalid credentials');
        }
    } catch (error) {
        res.status(500).send('Error logging in');
    }
});

router.post('/logout', (req, res) => {
    res.clearCookie('token');
    res.send('Logged out');
});

// list all users
router.get('/list', async (req, res) => {
    const users = await User.find();
    res.json(users);
});


router.use(authMiddleware);
router.get('/me', (req, res) => {
    res.send(req.user.username + ' are authenticated');
});
router.post('/changePassword', async (req, res) => { 
    const { newPassword } = req.body;
    console.log(newPassword)
    const username = req.user.username
    const user = await User.findOne({ username });
    if (user) {
        user.password = newPassword;
        console.log(user);
        await user.save();
        res.send('Password changed');
    } else {
        res.status(401).send('Invalid credentials');
    }
});



module.exports = router;