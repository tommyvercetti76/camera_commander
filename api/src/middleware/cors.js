const cors = require('cors');

const allowedOrigins = [
  'https://kaaykostore.web.app',
  'https://kaaykostore.firebaseapp.com',
  'https://kaayko.com',
  'http://localhost:5173',
  'http://localhost:5000',
];

module.exports = cors({
  origin: (origin, callback) => {
    // Allow requests with no origin (mobile apps, curl, etc.)
    if (!origin) return callback(null, true);
    if (allowedOrigins.includes(origin)) {
      return callback(null, true);
    }
    return callback(new Error('Not allowed by CORS'));
  },
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: false,
  maxAge: 86400,
});
