const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const urlSchema = new Schema({
    username: { type: String, default: 'Anonymous' },
    long_url: { type: String, required: true },
    short_id: { type: String, required: true },
    createdAt: { type: Date, default: Date.now },
});

const Url = mongoose.model('Url', urlSchema);

module.exports = Url;