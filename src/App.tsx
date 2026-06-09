import { useState, useEffect, useCallback } from 'react';
import { MessageCircle, Send, User, Bot, AlertTriangle, CheckCircle, Star, RefreshCw } from 'lucide-react';
import { sendChatMessage, getChatHistory, submitFeedback, type Message, type UserInfo, type ChatResponse } from './services/api';

function App() {
  const [sessionId] = useState(() => {
    const existing = localStorage.getItem('medical_agent_session');
    return existing || `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  });

  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [showUserInfoForm, setShowUserInfoForm] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [consultationId, setConsultationId] = useState<number | null>(null);
  const [feedbackRating, setFeedbackRating] = useState(0);
  const [feedbackComment, setFeedbackComment] = useState('');
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [riskLevel, setRiskLevel] = useState<string | null>(null);
  const [showRiskIndicator, setShowRiskIndicator] = useState(false);

  useEffect(() => {
    localStorage.setItem('medical_agent_session', sessionId);
  }, [sessionId]);

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const history = await getChatHistory(sessionId);
        setMessages(history);
      } catch {
        setMessages([]);
      }
    };
    loadHistory();
  }, [sessionId]);

  const handleSend = useCallback(async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: inputMessage.trim(),
      created_at: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const request = {
        session_id: sessionId,
        message: inputMessage.trim(),
        user_info: userInfo || undefined,
      };

      const response: ChatResponse = await sendChatMessage(request);
      
      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.response,
        created_at: new Date().toISOString(),
      };

      setMessages(prev => [...prev, assistantMessage]);
      setConsultationId(response.consultation_id);
      setIsComplete(response.is_complete);
      
      if (response.response.includes('高风险') || response.response.includes('紧急') || response.response.includes('立即就医')) {
        setRiskLevel('high');
        setShowRiskIndicator(true);
      } else if (response.response.includes('中风险')) {
        setRiskLevel('medium');
        setShowRiskIndicator(true);
      } else if (response.response.includes('低风险')) {
        setRiskLevel('low');
        setShowRiskIndicator(true);
      }

      if (response.is_complete) {
        setShowUserInfoForm(false);
      }
    } catch (error) {
      const errorMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: '抱歉，系统暂时无法响应，请稍后重试。',
        created_at: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [inputMessage, isLoading, sessionId, userInfo]);

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleUserInfoSubmit = (info: UserInfo) => {
    setUserInfo(info);
    setShowUserInfoForm(false);
  };

  const handleFeedbackSubmit = async () => {
    if (!consultationId || feedbackRating === 0) return;

    try {
      await submitFeedback({
        consultation_id: consultationId,
        rating: feedbackRating,
        comment: feedbackComment,
      });
      setFeedbackSubmitted(true);
    } catch {
      alert('提交反馈失败，请稍后重试');
    }
  };

  const handleRestart = () => {
    const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('medical_agent_session', newSessionId);
    window.location.reload();
  };

  const getRiskColor = () => {
    switch (riskLevel) {
      case 'high': return 'bg-red-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getRiskText = () => {
    switch (riskLevel) {
      case 'high': return '高风险';
      case 'medium': return '中风险';
      case 'low': return '低风险';
      default: return '未知';
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white/10 backdrop-blur-md border-b border-white/20">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-purple-500 rounded-xl flex items-center justify-center">
              <MessageCircle className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">医疗智能体</h1>
              <p className="text-xs text-white/70">AI辅助问诊系统</p>
            </div>
          </div>
          <button
            onClick={handleRestart}
            className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white text-sm transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            新对话
          </button>
        </div>
      </header>

      {showRiskIndicator && (
        <div className={`px-4 py-2 ${getRiskColor()} flex items-center justify-center gap-2 text-white text-sm font-medium`}>
          <AlertTriangle className="w-4 h-4" />
          当前评估风险等级：{getRiskText()}
        </div>
      )}

      <main className="flex-1 max-w-4xl mx-auto w-full px-4 py-6">
        {!showUserInfoForm && messages.length === 0 && !isComplete && (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="w-20 h-20 bg-white/10 backdrop-blur-md rounded-full flex items-center justify-center mb-6">
              <Bot className="w-10 h-10 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">欢迎使用医疗智能体</h2>
            <p className="text-white/70 mb-6 max-w-md">
              我是您的AI医疗助手，可以帮助您进行初步的健康咨询。<br />
              请告诉我您的症状，我会为您提供专业的建议。
            </p>
            <button
              onClick={() => setShowUserInfoForm(true)}
              className="px-6 py-3 bg-white/20 hover:bg-white/30 rounded-xl text-white font-medium transition-colors"
            >
              填写个人信息
            </button>
          </div>
        )}

        {showUserInfoForm && (
          <div className="bg-white rounded-2xl shadow-xl p-6 max-w-lg mx-auto">
            <h2 className="text-xl font-bold text-gray-800 mb-6">请填写您的个人信息</h2>
            <UserInfoForm onSubmit={handleUserInfoSubmit} />
          </div>
        )}

        {!showUserInfoForm && messages.length > 0 && (
          <div className="space-y-4 mb-6">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${message.role === 'user' ? 'flex-row-reverse' : ''}`}
              >
                <div
                  className={`w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center ${
                    message.role === 'user'
                      ? 'bg-gradient-to-br from-blue-400 to-purple-500'
                      : 'bg-gray-200'
                  }`}
                >
                  {message.role === 'user' ? (
                    <User className="w-5 h-5 text-white" />
                  ) : (
                    <Bot className="w-5 h-5 text-gray-600" />
                  )}
                </div>
                <div
                  className={`max-w-[80%] px-4 py-3 rounded-2xl ${
                    message.role === 'user'
                      ? 'bg-gradient-to-br from-blue-500 to-purple-600 text-white rounded-tr-md'
                      : 'bg-white text-gray-800 rounded-tl-md shadow-sm'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  <p className={`text-xs mt-1 ${
                    message.role === 'user' ? 'text-white/70' : 'text-gray-400'
                  }`}>
                    {new Date(message.created_at).toLocaleTimeString('zh-CN', {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </p>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex gap-3">
                <div className="w-10 h-10 rounded-full bg-gray-200 flex-shrink-0 flex items-center justify-center">
                  <Bot className="w-5 h-5 text-gray-600" />
                </div>
                <div className="bg-white px-4 py-3 rounded-2xl rounded-tl-md shadow-sm">
                  <div className="flex gap-2">
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {isComplete && !feedbackSubmitted && (
          <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
            <div className="flex items-center gap-2 mb-4">
              <CheckCircle className="w-6 h-6 text-green-500" />
              <h3 className="text-lg font-bold text-gray-800">问诊已完成</h3>
            </div>
            <p className="text-gray-600 mb-4">感谢您使用医疗智能体！请为本次服务评分：</p>
            <div className="flex gap-2 mb-4">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  onClick={() => setFeedbackRating(star)}
                  className={`p-2 transition-transform hover:scale-110 ${
                    star <= feedbackRating
                      ? 'text-yellow-500'
                      : 'text-gray-300'
                  }`}
                >
                  <Star className={`w-8 h-8 ${star <= feedbackRating ? 'fill-current' : ''}`} />
                </button>
              ))}
            </div>
            <textarea
              value={feedbackComment}
              onChange={(e) => setFeedbackComment(e.target.value)}
              placeholder="请输入您的反馈（可选）"
              className="w-full p-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={3}
            />
            <button
              onClick={handleFeedbackSubmit}
              disabled={feedbackRating === 0}
              className="mt-4 w-full py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-medium hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
            >
              提交反馈
            </button>
          </div>
        )}

        {feedbackSubmitted && (
          <div className="bg-green-50 border border-green-200 rounded-2xl p-4 mb-6 flex items-center gap-3">
            <CheckCircle className="w-6 h-6 text-green-500" />
            <span className="text-green-700">感谢您的反馈！您的意见对我们非常重要。</span>
          </div>
        )}

        {!isComplete && !showUserInfoForm && (
          <div className="bg-white rounded-2xl shadow-xl p-4">
            <div className="flex gap-3">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="请描述您的症状或问题..."
                className="flex-1 px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isLoading}
              />
              <button
                onClick={handleSend}
                disabled={!inputMessage.trim() || isLoading}
                className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-medium hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <Send className="w-5 h-5" />
                发送
              </button>
            </div>
            <p className="text-xs text-gray-400 mt-2">
              提示：按 Enter 键发送，Shift + Enter 换行
            </p>
          </div>
        )}
      </main>

      <footer className="bg-white/10 backdrop-blur-md border-t border-white/20 py-4">
        <div className="max-w-4xl mx-auto px-4 text-center text-white/70 text-sm">
          <p>医疗智能体仅供参考，不能替代专业医疗诊断</p>
          <p className="mt-1">如遇紧急情况，请立即拨打急救电话或前往医院就诊</p>
        </div>
      </footer>
    </div>
  );
}

interface UserInfoFormProps {
  onSubmit: (info: UserInfo) => void;
}

function UserInfoForm({ onSubmit }: UserInfoFormProps) {
  const [age, setAge] = useState<string>('');
  const [gender, setGender] = useState<string>('');
  const [medicalHistory, setMedicalHistory] = useState('');
  const [medication, setMedication] = useState('');
  const [allergies, setAllergies] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      age: age ? parseInt(age) : undefined,
      gender: gender as UserInfo['gender'] || undefined,
      medical_history: medicalHistory || undefined,
      medication: medication || undefined,
      allergies: allergies || undefined,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">年龄</label>
        <input
          type="number"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          placeholder="请输入年龄"
          className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
          min="0"
          max="150"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">性别</label>
        <select
          value={gender}
          onChange={(e) => setGender(e.target.value)}
          className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">请选择性别</option>
          <option value="男">男</option>
          <option value="女">女</option>
          <option value="其他">其他</option>
        </select>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">既往病史（可选）</label>
        <textarea
          value={medicalHistory}
          onChange={(e) => setMedicalHistory(e.target.value)}
          placeholder="请描述您的既往病史"
          className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          rows={2}
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">当前用药（可选）</label>
        <textarea
          value={medication}
          onChange={(e) => setMedication(e.target.value)}
          placeholder="请描述您正在服用的药物"
          className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          rows={2}
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">过敏史（可选）</label>
        <textarea
          value={allergies}
          onChange={(e) => setAllergies(e.target.value)}
          placeholder="请描述您的过敏史"
          className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          rows={2}
        />
      </div>
      <button
        type="submit"
        className="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-medium hover:opacity-90 transition-opacity"
      >
        确认提交
      </button>
    </form>
  );
}

export default App;
