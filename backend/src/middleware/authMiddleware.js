const jwt = require('jsonwebtoken');
const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret';

const authMiddleware = (req, res, next) => {
    console.log(req.headers.cookie);
    const token = req.headers.cookie ? req.headers.cookie.split('; ').find(row => row.startsWith('token=')).split('=')[1] : null;
    if (!token) {
        return res.send('not login yet');
    }
    jwt.verify(token, JWT_SECRET, (err, decoded) => {
        if (err) {
            console.log(err)
            return res.send('Bad hacker');
        }
        req.user = decoded;
        next();
    });
};

module.exports = authMiddleware;
