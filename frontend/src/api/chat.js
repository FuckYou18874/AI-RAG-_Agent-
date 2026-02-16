import axios from 'axios'

const API_BASE = '/api'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const chatService = {
  async sendMessage(message, sessionId = null) {
    const response = await api.post('/chat', {
      message,
      session_id: sessionId
    })
    return response.data
  },

  async sendMessageStream(message, sessionId = null, onMessage, onDone, onSession) {
    const requestBody = {
      message: message,
      session_id: sessionId
    }
    
    console.log('Sending request:', JSON.stringify(requestBody))
    
    const response = await fetch(`${API_BASE}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    })

    console.log('Response status:', response.status)
    
    if (!response.ok) {
      const errorText = await response.text()
      console.error('Error response:', errorText)
      throw new Error(`HTTP ${response.status}: ${errorText}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const text = decoder.decode(value)
      const lines = text.split('\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6))
            
            if (data.type === 'session' && onSession) {
              onSession(data.session_id)
            } else if (data.type === 'content' && onMessage) {
              onMessage(data.content)
            } else if (data.type === 'done' && onDone) {
              onDone()
            }
          } catch (e) {
            console.error('解析SSE数据失败:', e)
          }
        }
      }
    }
  },

  async createNewSession() {
    const response = await api.post('/session/new')
    return response.data
  },

  async clearSession(sessionId) {
    const response = await api.delete(`/session/${sessionId}`)
    return response.data
  },

  async getSessionInfo(sessionId) {
    const response = await api.get(`/session/${sessionId}/info`)
    return response.data
  },

  async listSessions() {
    const response = await api.get('/sessions')
    return response.data
  },

  async healthCheck() {
    const response = await api.get('/health')
    return response.data
  }
}

export default chatService