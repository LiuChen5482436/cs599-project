import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
});

export interface UserInfo {
  age?: number;
  gender?: '男' | '女' | '其他';
  medical_history?: string;
  medication?: string;
  allergies?: string;
}

export interface ChatRequest {
  session_id: string;
  message: string;
  user_info?: UserInfo;
}

export interface ChatResponse {
  response: string;
  consultation_id: number;
  is_complete: boolean;
  needs_followup: boolean;
  followup_question?: string;
}

export interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface FeedbackRequest {
  consultation_id: number;
  rating: number;
  comment?: string;
}

export interface FeedbackResponse {
  success: boolean;
  message: string;
}

export interface RiskAssessmentRequest {
  symptoms: string;
  age?: number;
  medical_history?: string;
  special_condition?: string;
  temperature?: number;
}

export interface RiskAssessmentResponse {
  risk_level: string;
  risk_name: string;
  risk_description: string;
  score: number;
  factors: string[];
  advice: string;
}

export async function sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await api.post('/chat/', request);
  return response.data;
}

export async function getChatHistory(sessionId: string): Promise<Message[]> {
  const response = await api.get(`/chat/history/${sessionId}`);
  return response.data;
}

export async function submitFeedback(request: FeedbackRequest): Promise<FeedbackResponse> {
  const response = await api.post('/feedback/', request);
  return response.data;
}

export async function assessRisk(request: RiskAssessmentRequest): Promise<RiskAssessmentResponse> {
  const response = await api.post('/triage/risk', request);
  return response.data;
}

export async function getSummary(consultationId: number): Promise<{ summary: string; consultation_data: unknown }> {
  const response = await api.get(`/summary/${consultationId}`);
  return response.data;
}

export async function healthCheck(): Promise<{ status: string }> {
  const response = await api.get('/health');
  return response.data;
}
