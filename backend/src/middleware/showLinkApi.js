const showLinkApi = (req, res, next) => {
    console.log(`API Request: ${req.method} ${req.originalUrl}`);
    next();
};

module.exports = showLinkApi;