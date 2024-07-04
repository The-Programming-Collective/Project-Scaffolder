import express from 'express';
import { config } from 'dotenv';
import morganMiddleware from './src/logger/morgan.middlware.js';
import Logger from './src/logger/Logger.js';
import {
	globalErrorHandler,
	invalidRoutes,
	uncaughtException,
	unhandledRejection,
} from './src/utils/errorHandling.js';
import GeminiRouter from './src/routes/gemini.routes.js';
import cors from 'cors';
config();
uncaughtException();
const app = express();
const port = process.env.PORT || 3000;

// run();
app.use(express.json());
app.use(cors());
app.use(morganMiddleware);
app.use('/api/v1', GeminiRouter);

app.all('*', invalidRoutes);
app.use(globalErrorHandler);
app.listen(port, () => {
	Logger.info(`Server running on port ${port}`);
});

unhandledRejection();
