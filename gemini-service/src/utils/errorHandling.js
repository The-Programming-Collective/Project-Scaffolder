import { StatusCodes } from 'http-status-codes';
import Logger from '../logger/Logger.js';

export class ApiError extends Error {
	constructor(statusCode, message) {
		super(message);
		this.status = `${statusCode}`.startsWith('4') ? 'fail' : 'error';
		this.statusCode = statusCode;
		this.isOperational = true;
		Error.captureStackTrace(this, this.constructor);
	}
}

// catching errors from asynchronous functions used in services
export const catchAsyncError = (fn) => {
	return (req, res, next) => {
		fn(req, res, next).catch((err) => {
			next(err);
		});
	};
};

// for invalid requested routes or methods
export const invalidRoutes = (req, res, next) => {
	const { method, originalUrl } = req;
	next(
		new ApiError(StatusCodes.NOT_FOUND, `can't find: ${method} ${originalUrl}`)
	);
};

const sendErrorDev = (err, res) => {
	return res.status(err.statusCode).json({
		status: err.status,
		error: err,
		message: err.message,
		stack: err.stack,
	});
};

const sendErrorProd = (err, res) => {
	// operational (trusted error)
	if (err.isOperational)
		return res
			.status(err.statusCode)
			.json({ status: err.status, message: err.message });
	// unknown errors from outside or programmatic
	else {
		Logger.error('ERROR 💥 ', err);
		// generic error message
		return res.status(StatusCodes.INTERNAL_SERVER_ERROR).json({
			status: 'error',
			message: 'Something went wrong!',
		});
	}
};

export const unhandledRejection = (app) => {
	process.on('unhandledRejection', (err) => {
		Logger.warn('UNHANDLED REJECTION! 💥 Shutting down...');
		console.log(err);
		app.close(() => {
			// exit with uncaught exception
			process.exit(1);
		});
	});
};

export const uncaughtException = () => {
	process.on('uncaughtException', (err) => {
		Logger.warn('UNCAUGHT EXCEPTION! 💥 Shutting down...');
		console.log(err);
		process.exit(1);
	});
};

// handler function to handle any error in the app
export const globalErrorHandler = (err, req, res, next) => {
	err.statusCode = err.statusCode || StatusCodes.INTERNAL_SERVER_ERROR;
	err.status = err.status || 'error';
	err.message = err.message;
	console.log(err);
	// get error stack only in development mode
	return res.status(err.statusCode).json({
		status: err.status,
		error: err,
		message: err.message,
	});
};
