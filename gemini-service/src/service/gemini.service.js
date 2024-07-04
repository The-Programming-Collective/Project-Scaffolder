import {
	GoogleGenerativeAI,
	HarmBlockThreshold,
	HarmCategory,
} from '@google/generative-ai';
import { config } from 'dotenv';
config();
const apiKey = process.env.GEMINI_API_KEY;
const genAI = new GoogleGenerativeAI(apiKey);

const model = genAI.getGenerativeModel({
	model: 'gemini-1.5-pro',
	systemInstruction:
		'You are an assistive ai chat model in a scaffolding project. The user enters his thoughts or what he want to build (in software development context) and you will help him recommend a tech stack to use based on some choices\nFrontend:\nReactjs or Angular\nBackend:\nJavaee, fiber or flask\ndatabase:\npostgres or mongodb\nYou are not allowed to answer on any prompt outside this context and apologize for it.\nOur project name is Scaffolder and the slogan is Happy Coding 🚀',
});

const generationConfig = {
	temperature: 1,
	topP: 0.95,
	topK: 64,
	maxOutputTokens: 8192,
	responseMimeType: 'text/plain',
};

// const safetySetting = [
// 	{
// 		category: HarmCategory.HARM_CATEGORY_HARASSMENT,
// 		threshold: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
// 	},
// 	{
// 		category: HarmCategory.HARM_CATEGORY_HATE_SPEECH,
// 		threshold: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
// 	},
// ];

export const chatWithGemini = async (history, text) => {
	const chatSession = model.startChat({
		generationConfig,
		// safetySetting,
		history,
	});

	const { response } = await chatSession.sendMessage(text);
	return response.text();
};
