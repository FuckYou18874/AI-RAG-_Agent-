<template>
  <div class="app-container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1>🤖 智扫通</h1>
        <p class="subtitle">机器人智能客服</p>
      </div>

      <div class="session-info">
        <div class="label">当前会话ID</div>
        <div class="value">{{ shortSessionId }}</div>
      </div>

      <button class="new-session-btn" @click="startNewSession">
        <span>➕</span>
        <span>开始新会话</span>
      </button>

      <div class="sidebar-footer">
        <p>💡 提示：新会话将清除所有对话历史</p>
      </div>
    </aside>

    <main class="main-content">
      <header class="chat-header">
        <div class="robot-icon">🤖</div>
        <div>
          <h2>智能客服助手</h2>
          <p class="status">{{ connectionStatus }}</p>
        </div>
      </header>

      <div class="chat-container" ref="chatContainer">
        <div v-if="messages.length === 0" class="welcome-message">
          <div class="icon">🤖</div>
          <h2>欢迎使用智扫通智能客服</h2>
          <p>我是您的扫地机器人专家助手，可以帮您解答产品使用、故障排除、维护保养等问题。</p>
        </div>

        <div v-else class="messages">
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="message"
            :class="message.role"
          >
            <div class="message-avatar">
              {{ message.role === 'user' ? '👤' : '🤖' }}
            </div>
            <div class="message-content" v-html="formatMessage(message.content)"></div>
          </div>

          <div v-if="isTyping" class="message assistant">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="input-container">
        <div class="input-wrapper">
          <textarea
            v-model="userInput"
            @keydown.enter.exact.prevent="sendMessage"
            placeholder="输入您的问题..."
            :disabled="isLoading"
            rows="1"
            ref="inputArea"
          ></textarea>
          <button
            class="send-btn"
            @click="sendMessage"
            :disabled="isLoading || !userInput.trim()"
          >
            <span v-if="isLoading">发送中...</span>
            <span v-else>发送 ➤</span>
          </button>
        </div>
        <div v-if="messageCount > 0" class="memory-status">
          📝 已保存到会话记忆 ({{ messageCount }}条消息)
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick } from 'vue'
import chatService from './api/chat.js'

export default {
  name: 'App',
  setup() {
    const messages = ref([])
    const userInput = ref('')
    const sessionId = ref(null)
    const isLoading = ref(false)
    const isTyping = ref(false)
    const connectionStatus = ref('正在连接...')
    const chatContainer = ref(null)
    const inputArea = ref(null)

    const shortSessionId = computed(() => {
      if (!sessionId.value) return '未创建'
      return sessionId.value.substring(0, 8) + '...'
    })

    const messageCount = computed(() => messages.value.length)

    const scrollToBottom = async () => {
      await nextTick()
      if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight
      }
    }

    const formatMessage = (content) => {
      if (!content) return ''
      return content
        .replace(/\n/g, '<br>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
    }

    const sendMessage = async () => {
      const message = userInput.value.trim()
      if (!message || isLoading.value) return

      messages.value.push({
        role: 'user',
        content: message
      })

      userInput.value = ''
      isLoading.value = true
      isTyping.value = true

      await scrollToBottom()

      let assistantMessage = ''
      let messageIndex = messages.value.length

      try {
        await chatService.sendMessageStream(
          message,
          sessionId.value,
          (chunk) => {
            isTyping.value = false
            assistantMessage += chunk
            
            if (messages.value.length === messageIndex) {
              messages.value.push({
                role: 'assistant',
                content: assistantMessage
              })
            } else {
              messages.value[messageIndex].content = assistantMessage
            }
            scrollToBottom()
          },
          () => {
            isLoading.value = false
          },
          (newSessionId) => {
            sessionId.value = newSessionId
          }
        )
      } catch (error) {
        console.error('发送消息失败:', error)
        messages.value.push({
          role: 'assistant',
          content: '抱歉，系统暂时无法处理您的请求。请稍后重试。'
        })
        isLoading.value = false
        isTyping.value = false
      }

      await scrollToBottom()
    }

    const startNewSession = async () => {
      try {
        const result = await chatService.createNewSession()
        sessionId.value = result.session_id
        messages.value = []
        connectionStatus.value = '已连接'
      } catch (error) {
        console.error('创建新会话失败:', error)
      }
    }

    const checkConnection = async () => {
      try {
        await chatService.healthCheck()
        connectionStatus.value = '已连接'
      } catch (error) {
        connectionStatus.value = '连接失败'
        console.error('健康检查失败:', error)
      }
    }

    onMounted(() => {
      checkConnection()
      inputArea.value?.focus()
    })

    return {
      messages,
      userInput,
      sessionId,
      shortSessionId,
      isLoading,
      isTyping,
      connectionStatus,
      messageCount,
      chatContainer,
      inputArea,
      sendMessage,
      startNewSession,
      formatMessage
    }
  }
}
</script>
