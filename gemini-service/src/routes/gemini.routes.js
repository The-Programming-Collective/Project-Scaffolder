import { Router } from 'express';
import { geminiChat } from '../controller/gemini.controller.js';

const router = Router();

router.post('/chat', geminiChat);

export default router;
