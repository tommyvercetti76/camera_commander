const functions = require('firebase-functions');
const admin = require('firebase-admin');
const express = require('express');
const corsMiddleware = require('./middleware/cors');
const rateLimitMiddleware = require('./middleware/rateLimit');

// Initialize Firebase Admin once
if (!admin.apps.length) {
  admin.initializeApp();
}

const app = express();

// Middleware — order matters
app.use(corsMiddleware);
app.use(express.json({ limit: '10kb' }));
app.use(rateLimitMiddleware);

// Routes
app.use('/cameras', require('./routes/cameras'));
app.use('/lenses', require('./routes/lenses'));
app.use('/presets/smart', require('./routes/smart'));
app.use('/presets', require('./routes/presets'));

// Health check
app.get('/health', (req, res) => res.json({ status: 'ok', version: '1.0.0' }));

// 404 handler
app.use((req, res) => res.status(404).json({
  error: { code: 'NOT_FOUND', message: `Route ${req.path} does not exist` }
}));

// Error handler
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({
    error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' }
  });
});

exports.api = functions.https.onRequest(app);
