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
    try {
        const { long_url, note } = req.body;
        if (!long_url) {
            return res.status(400).json({ message: 'Long URL is required' });
        }
        const short_id = shortUrl.generate();
        const short_url = `${process.env.Base_URL}:${process.env.Expose_PORT}/api/url/r/${short_id}`;
        const username = 'Anonymous';
        const newUrl = new Url({
            username,
            long_url,
            short_id,
            note: note || ''
        });
        await newUrl.save();
        res.json({ short_url });
    } catch (error) {
        console.error('Failed to create anonymous short URL', error);
        res.status(500).json({ message: 'Failed to create short URL' });
    }
});


// Create short URL from long URL
router.post('/u/shorten', authMiddleware, async (req, res) => {
    try {
        const { long_url, note } = req.body;
        if (!long_url) {
            return res.status(400).json({ message: 'Long URL is required' });
        }
        const short_id = shortUrl.generate();
        const short_url = `${process.env.Base_URL}:${process.env.Expose_PORT}/api/url/r/${short_id}`;
        const username = req.user ? req.user.username : 'Anonymous';
        const newUrl = new Url({
            username,
            long_url,
            short_id,
            note: note || ''
        });
        await newUrl.save();
        res.json({ short_url });
    } catch (error) {
        console.error('Failed to create user short URL', error);
        res.status(500).json({ message: 'Failed to create short URL' });
    }
});

// Redirect to long URL based on short URL
router.get('/r/:short_id', async (req, res) => {
    const { short_id } = req.params;
    const url = await Url.findOneAndUpdate(
        { short_id },
        { $inc: { visit_count: 1 } },
        { new: true }
    );
    if (url) {
        res.redirect(url.long_url);
    } else {
        res.status(404).send('URL not found');
    }
});

// See all URLs created by the logged-in user
router.get('/my-urls', authMiddleware, async (req, res) => {
    try {
        const urls = await Url.find({ username: req.user.username });
        const response = urls.map((url) => ({
            short_id: url.short_id,
            short_url: `${process.env.Base_URL}:${process.env.Expose_PORT}/api/url/r/${url.short_id}`,
            long_url: url.long_url,
            note: url.note || '',
            visit_count: url.visit_count || 0
        }));
        res.json(response);
    } catch (error) {
        console.error('Failed to load URLs', error);
        res.status(500).json({ message: 'Failed to load URLs' });
    }
});

// Delete a URL created by the logged-in user
router.delete('/d/:short_id', authMiddleware, async (req, res) => {
    try {
        const { short_id } = req.params;
        const url = await Url.findOneAndDelete({ short_id, username: req.user.username });
        if (url) {
            res.json({ message: 'URL deleted' });
        } else {
            res.status(404).json({ message: 'URL not found or not authorized' });
        }
    } catch (error) {
        console.error('Failed to delete URL', error);
        res.status(500).json({ message: 'Failed to delete URL' });
    }
});

router.patch('/note/:short_id', authMiddleware, async (req, res) => {
    try {
        const { short_id } = req.params;
        const { note } = req.body;
        const updatedUrl = await Url.findOneAndUpdate(
            { short_id, username: req.user.username },
            { note: note || '' },
            { new: true }
        );
        if (!updatedUrl) {
            return res.status(404).json({ message: 'URL not found or not authorized' });
        }
        res.json({
            short_id: updatedUrl.short_id,
            short_url: `${process.env.Base_URL}:${process.env.Expose_PORT}/api/url/r/${updatedUrl.short_id}`,
            long_url: updatedUrl.long_url,
            note: updatedUrl.note || ''
        });
    } catch (error) {
        console.error('Failed to update note', error);
        res.status(500).json({ message: 'Failed to update note' });
    }
});

module.exports = router;
