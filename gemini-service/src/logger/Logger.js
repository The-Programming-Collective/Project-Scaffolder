import winston from 'winston';

const levels = {
	error: 0,
	warn: 1,
	info: 2,
	http: 3,
	debug: 4,
};
/**
 * adjust severty levels upon NODE_ENV
 */

const level = () => {
	const env = process.env.NODE_ENV || 'development';
	const isDevelopment = env === 'development';
	return isDevelopment ? 'debug' : 'warn';
};

const colors = {
	error: 'red',
	warn: 'yellow',
	info: 'blue',
	http: 'magenta',
	debug: 'green',
};

const format = winston.format.combine(
	winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss:ms' }),
	winston.format.printf(({ timestamp, level, message }) => {
		return `[${level.toUpperCase()}] [${timestamp}]: ${message}`;
	}),
	winston.format.colorize({ all: true, colors })
);

const transports = [
	new winston.transports.Console(),
	new winston.transports.File({
		filename: 'logs/error.log',
		level: 'error',
	}),
	new winston.transports.File({ filename: 'logs/all.log' }),
];
/**
 * custom logger using winston
 */
const Logger = winston.createLogger({
	level: level(),
	levels,
	format,
	transports,
});

export default Logger;
