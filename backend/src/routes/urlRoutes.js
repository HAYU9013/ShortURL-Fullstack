const express = require('express');
const Url = require('../models/urlModels');
const authMiddleware = require('../middleware/authMiddleware');
const shortUrl = require('../controllers/shortUrlController');

const router = express.Router();

router.get('/', (req, res) => {
    res.send('URL shortener');
});

// Create short URL from long URL
router.post('/shorten', async (req, res) => {
    const { long_url } = req.body;
    const short_id = shortUrl.generate();
    short_url = `${process.env.Base_URL}:${process.env.Expose_PORT}/api/url/r/${short_id}`;
    console.log(long_url + " " + short_url);
    username = "Anonymous";
    console.log(username);
    console.log(req.user);
    const newUrl = new Url({
        username: username,
        long_url,
        short_id
    });
    await newUrl.save();
    res.json({ short_url });
});


// Create short URL from long URL
router.post('/u/shorten', authMiddleware, async (req, res) => {
    const { long_url } = req.body;
    const short_id = shortUrl.generate();
    short_url = `${process.env.Base_URL}:${process.env.Expose_PORT}/api/url/r/${short_id}`;
    console.log(long_url + " " + short_url);
    username = "Anonymous";
    if(req.user){
        username = req.user.username;
    }
    console.log(username);
    console.log(req.user);
    const newUrl = new Url({
        username: username,
        long_url,
        short_id
    });
    await newUrl.save();
    res.json({ short_url });
});

// Redirect to long URL based on short URL
router.get('/r/:short_id', async (req, res) => {
    const { short_id } = req.params;
    const url = await Url.findOne({ short_id });
    if (url) {
        res.redirect(url.long_url);
    } else {
        res.status(404).send('URL not found');
    }
});

// See all URLs created by the logged-in user
router.get('/my-urls', authMiddleware, async (req, res) => {
    let urls = await Url.find({ username: req.user.username });
    for (let i = 0; i < urls.length; i++) {
        urls[i] = {
            short_url: `${process.env.Base_URL}:${process.env.Expose_PORT}/api/url/r/${urls[i].short_id}`,
            long_url: urls[i].long_url
        };
    }
    res.json(urls);
});

// Delete a URL created by the logged-in user
router.delete('/d/:short_id', authMiddleware, async (req, res) => {
    const { short_id } = req.params;
    const url = await Url.findOneAndDelete({ short_id, username: req.user.username });
    if (url) {
        res.json({ message: 'URL deleted' });
    } else {
        res.status(404).send('URL not found or not authorized');
    }
});

module.exports = router;