'use client'

import { useState } from 'react'
import axios from 'axios'
import { Clock, AlertTriangle, MessageSquare, ArrowRight } from 'lucide-react'
import Image from 'next/image'

// ✅ Correct BASE_URL - your live backend
const BASE_URL = 'https://ca-landing-page.onrender.com'

export default function AIAssistant() {
  // Chat states
  const [chatMessage, setChatMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState<Array<{role: 'user' | 'assistant', content: string}>>([])
  const [conversationContext, setConversationContext] = useState<string>('')

  // Example questions
  const exampleQuestions = [
    "What is GST?",
    "How to save tax under 80C?",
    "ITR filing due dates",
    "TDS rates for salary",
    "Audit requirements",
    "Balance sheet basics"
  ]

  const sendChat = async () => {
    if (!chatMessage.trim()) return

    setMessages(prev => [...prev, { role: 'user', content: chatMessage }])
    setLoading(true)

    try {
      // ✅ Correct endpoint: /api/chat
      const res = await axios.post(`${BASE_URL}/api/chat`, {
        message: chatMessage
      })
      
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.reply }])
      
      // Store context
      setConversationContext(`${chatMessage} -> ${res.data.reply.substring(0, 100)}...`)
      
    } catch (error: any) {
      console.error('Chat error:', error)
      
      if (error.response?.status === 429 || error.message?.includes('429')) {
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: `⏳ **Daily Limit Reached**

The AI assistant has reached its daily request limit. This resets automatically every 24 hours.

✨ **Try these common questions instead:**
• What is GST?
• Tax saving tips under 80C
• ITR filing process
• TDS rates
• Audit requirements` 
        }])
      } else {
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: `⚠️ Service temporarily unavailable. Please try again. (${error.message})` 
        }])
      }
    } finally {
      setLoading(false)
      setChatMessage('')
    }
  }

  return (
    <section id="ai-assistant" className="py-24 px-4 bg-linear-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            Your AI <span className="text-transparent bg-clip-text bg-linear-to-r from-blue-600 to-purple-600">CA Assistant</span>
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Get instant answers to your accounting, tax, and finance questions – powered by advanced AI and CA expertise
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left - Avatar & Info */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-8 sticky top-24 border border-gray-100 dark:border-gray-700">
              {/* Avatar Image */}
              <div className="relative w-48 h-48 mx-auto mb-6">
                <div className="absolute inset-0 bg-linear-to-r from-blue-500 to-purple-600 rounded-full blur-xl opacity-50 animate-pulse" />
                <div className="relative w-full h-full rounded-full overflow-hidden border-4 border-white dark:border-gray-700 shadow-2xl">
                  <Image
                    src="/heroimg.jpg"
                    alt="CA Assistant"
                    width={200}
                    height={200}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="absolute -bottom-2 -right-2 w-12 h-12 bg-green-500 rounded-full border-4 border-white dark:border-gray-800 flex items-center justify-center">
                  <span className="text-white text-sm font-bold">AI</span>
                </div>
              </div>

              <h3 className="text-2xl font-bold text-center text-gray-900 dark:text-white mb-2">
                CA Assistant
              </h3>
              <p className="text-sm text-center text-gray-500 dark:text-gray-400 mb-6">
                Available 24/7 • Instant Responses
              </p>

              {/* Expertise Badges */}
              <div className="space-y-3 mb-6">
                <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
                  <span className="w-2 h-2 bg-green-500 rounded-full" />
                  <span>Taxation (GST, ITR, TDS)</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
                  <span className="w-2 h-2 bg-blue-500 rounded-full" />
                  <span>Audit & Assurance</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
                  <span className="w-2 h-2 bg-purple-500 rounded-full" />
                  <span>Financial Planning</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
                  <span className="w-2 h-2 bg-orange-500 rounded-full" />
                  <span>Business Advisory</span>
                </div>
              </div>

              {/* Example Questions */}
              <div className="mb-6">
                <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
                  <MessageSquare className="w-4 h-4" />
                  Try asking:
                </h4>
                <div className="space-y-2">
                  {exampleQuestions.slice(0, 4).map((question, idx) => (
                    <button
                      key={idx}
                      onClick={() => {
                        setChatMessage(question)
                        setTimeout(() => sendChat(), 500)
                      }}
                      className="w-full text-left text-sm p-2 bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition flex items-center justify-between group"
                    >
                      <span className="text-gray-700 dark:text-gray-300">{question}</span>
                      <ArrowRight className="w-4 h-4 text-gray-400 group-hover:text-blue-500 transition" />
                    </button>
                  ))}
                </div>
              </div>

              {/* Quota Info */}
              <div className="flex items-center justify-center gap-1 text-xs text-gray-400">
                <Clock className="w-3 h-3" />
                <span>Free tier: ~1,000 requests/day</span>
              </div>
            </div>
          </div>

          {/* Right - Chat Interface */}
          <div className="lg:col-span-2">
            <div className="bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-6 border border-gray-100 dark:border-gray-700">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <MessageSquare className="w-6 h-6 text-blue-600" />
                Chat with AI Assistant
              </h3>
              
              {/* Messages */}
              <div className="h-125 overflow-y-auto mb-4 p-4 bg-gray-50 dark:bg-gray-900 rounded-2xl">
                {messages.length === 0 ? (
                  <div className="h-full flex items-center justify-center text-gray-400">
                    <div className="text-center">
                      <div className="text-6xl mb-4 opacity-50">💬</div>
                      <p className="text-lg font-medium mb-2">Start a conversation</p>
                      <p className="text-sm max-w-md">
                        Ask me about GST, Income Tax, Audit, TDS, or any other CA-related topic
                      </p>
                    </div>
                  </div>
                ) : (
                  messages.map((msg, idx) => (
                    <div key={idx} className={`mb-4 ${msg.role === 'user' ? 'text-right' : ''}`}>
                      <div className={`inline-block max-w-[80%] p-4 rounded-2xl ${
                        msg.role === 'user' 
                          ? 'bg-linear-to-r from-blue-600 to-purple-600 text-white rounded-br-none' 
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white rounded-bl-none'
                      }`}>
                        <div className="prose prose-sm dark:prose-invert max-w-none">
                          {msg.content.split('\n').map((line, i) => {
                            if (line.startsWith('#')) {
                              return <h3 key={i} className="font-bold mt-2 mb-1">{line.replace('#', '').trim()}</h3>
                            } else if (line.startsWith('-')) {
                              return <li key={i} className="ml-4 list-disc">{line.substring(1).trim()}</li>
                            } else if (line.startsWith('•')) {
                              return <li key={i} className="ml-4 list-disc">{line.substring(1).trim()}</li>
                            } else {
                              return <p key={i} className="mb-2">{line}</p>
                            }
                          })}
                        </div>
                      </div>
                    </div>
                  ))
                )}
                {loading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-2xl rounded-bl-none">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Example Questions Row */}
              <div className="mb-4 flex flex-wrap gap-2">
                {exampleQuestions.slice(4, 6).map((example, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setChatMessage(example)
                      setTimeout(() => sendChat(), 500)
                    }}
                    className="px-4 py-2 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 transition"
                  >
                    {example}
                  </button>
                ))}
              </div>

              {/* Chat Input */}
              <div className="flex gap-2">
                <input
                  type="text"
                  value={chatMessage}
                  onChange={(e) => setChatMessage(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && sendChat()}
                  placeholder="Type your question..."
                  className="flex-1 px-4 py-3 border border-gray-200 dark:border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900"
                  disabled={loading}
                />
                <button
                  onClick={sendChat}
                  disabled={loading || !chatMessage.trim()}
                  className="px-6 py-3 bg-linear-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 transition font-medium"
                >
                  Send
                </button>
              </div>

              {/* Link to Audit Section */}
              <div className="mt-6 text-center">
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Need detailed document audit?{" "}
                  <button 
                    onClick={() => {
                      const element = document.getElementById('audit-section')
                      if (element) {
                        element.scrollIntoView({ behavior: 'smooth' })
                      }
                    }}
                    className="text-blue-600 dark:text-blue-400 hover:underline font-medium"
                  >
                    Try AI Audit →
                  </button>
                </p>
              </div>

              {/* Disclaimer */}
              <p className="text-xs text-gray-400 mt-4 text-center">
                🔒 AI-powered assistance • Always consult your CA for critical decisions
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}