import { StatusCodes } from 'http-status-codes';
import { chatWithGemini } from '../service/gemini.service.js';
import { catchAsyncError } from '../utils/errorHandling.js';

export const geminiChat = catchAsyncError(async (req, res) => {
	const { text, history } = req.body;
	return res
		.status(StatusCodes.OK)
		.json({ text: await chatWithGemini(history, text) });
});
