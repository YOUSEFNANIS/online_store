<template>
  <div class="messages-wrapper">
    <div class="messages-layout" :class="{ 'thread-open': activeId }">
      <!-- Conversation list -->
      <aside class="conversation-list">
        <header class="list-header">
          <h1 class="list-title">{{ $t('messages.title') }}</h1>
        </header>
        <div class="list-search">
          <input v-model="filter" type="search" :placeholder="$t('messages.search')" />
        </div>

        <div class="list-scroll">
          <p v-if="!loadingList && !conversations.length" class="empty">
            {{ $t('messages.empty') }}
            <span v-if="role === 'customer'">{{ $t('messages.emptyCustomer') }}</span>
          </p>
          <button
            v-for="c in filteredConversations"
            :key="c.id"
            type="button"
            class="conversation-item"
            :class="{ active: c.id === activeId }"
            @click="openConversation(c.id)"
          >
            <span class="avatar" aria-hidden="true">{{ initial(c.other_name) }}</span>
            <span class="conv-body">
              <span class="conv-top">
                <span class="conv-name">{{ c.other_name }}</span>
                <time class="conv-time" :class="{ unread: c.unread_count }">{{ listTime(c.last_message_at) }}</time>
              </span>
              <span class="conv-bottom">
                <span class="conv-last">{{ c.last_message }}</span>
                <span v-if="c.unread_count" class="badge">{{ c.unread_count }}</span>
              </span>
            </span>
          </button>
        </div>
      </aside>

      <!-- Chat pane -->
      <section class="thread">
        <div v-if="!activeConversation" class="thread-empty">
          <MessageSquare :size="56" aria-hidden="true" />
          <p>{{ $t('messages.selectConversation') }}</p>
        </div>

        <template v-else>
          <header class="thread-header">
            <button type="button" class="back-btn" :aria-label="$t('messages.back')" @click="activeId = null">
              <span class="back-arrow">←</span>
            </button>
            <span class="avatar" aria-hidden="true">{{ initial(activeConversation.other_name) }}</span>
            <strong class="thread-name">{{ activeConversation.other_name }}</strong>
          </header>

          <div ref="scroller" class="thread-messages">
            <button v-if="hasMore" type="button" class="load-older" :disabled="loadingOlder" @click="loadOlder">
              {{ $t('messages.loadOlder') }}
            </button>
            <template v-for="(m, i) in messages" :key="m.id">
              <div v-if="isNewDay(i)" class="day-chip"><span>{{ dayLabel(m.creation_date) }}</span></div>
              <div class="bubble-row" :class="{ mine: m.mine }">
                <div class="bubble">
                  <router-link v-if="m.product_info" :to="'/products/' + m.product_info.id" class="product-card">
                    <img v-if="m.product_info.first_image" :src="m.product_info.first_image" alt="" class="card-img" />
                    <span class="card-info">
                      <span class="card-name">{{ m.product_info.name }}</span>
                      <span class="card-price">{{ Number(m.product_info.price).toLocaleString('en-US', { maximumFractionDigits: 2 }) }} {{ $t('productPage.currency') }}</span>
                    </span>
                  </router-link>
                  <span class="bubble-text">{{ m.body }}</span>
                  <span class="bubble-meta">
                    <time>{{ clock(m.creation_date) }}</time>
                    <CheckCheck v-if="m.mine" :size="14" class="tick" :class="{ read: m.is_read }" aria-hidden="true" />
                  </span>
                </div>
              </div>
            </template>
          </div>

          <form class="composer" @submit.prevent="sendMessage">
            <textarea
              ref="input"
              v-model="draft"
              rows="1"
              maxlength="2000"
              :placeholder="$t('messages.placeholder')"
              @input="autoGrow"
              @keydown.enter.exact.prevent="sendMessage"
            ></textarea>
            <button type="submit" class="send-btn" :disabled="sending || !draft.trim()" :aria-label="$t('messages.send')">
              <SendHorizontal :size="20" class="send-icon" aria-hidden="true" />
            </button>
          </form>
        </template>
      </section>
    </div>

    <transition name="toast">
      <div v-if="error" class="toast error" role="alert">✕ {{ error }}</div>
    </transition>
  </div>
</template>

<script>
import api from '@/services/api'
import { useRoleStore } from '@/stores/role'
import { MessageSquare, SendHorizontal, CheckCheck } from '@lucide/vue'

const POLL_MS = 8000
const PAGE_SIZE = 30

export default {
  components: { MessageSquare, SendHorizontal, CheckCheck },
  data() {
    return {
      conversations: [],
      messages: [],
      hasMore: false,
      loadingOlder: false,
      activeId: null,
      draft: '',
      filter: '',
      sending: false,
      loadingList: true,
      error: '',
      pollTimer: null,
      errorTimer: null,
    }
  },
  computed: {
    role() {
      return useRoleStore().role
    },
    locale() {
      return this.$i18n.locale === 'ar' ? 'ar-EG' : 'en-US'
    },
    activeConversation() {
      return this.conversations.find((c) => c.id === this.activeId) || null
    },
    filteredConversations() {
      const q = this.filter.trim().toLowerCase()
      return q ? this.conversations.filter((c) => c.other_name.toLowerCase().includes(q)) : this.conversations
    },
  },
  async mounted() {
    await this.loadConversations()
    const fromRoute = Number(this.$route.query.c)
    if (fromRoute && this.conversations.some((c) => c.id === fromRoute)) {
      await this.openConversation(fromRoute)
    }
    this.pollTimer = setInterval(this.poll, POLL_MS)
  },
  beforeUnmount() {
    clearInterval(this.pollTimer)
    clearTimeout(this.errorTimer)
  },
  methods: {
    initial(name) {
      return (name || '?').trim().charAt(0).toUpperCase()
    },
    clock(iso) {
      return new Date(iso).toLocaleTimeString(this.locale, { hour: '2-digit', minute: '2-digit' })
    },
    sameDay(a, b) {
      return a.toDateString() === b.toDateString()
    },
    listTime(iso) {
      const d = new Date(iso)
      return this.sameDay(d, new Date())
        ? this.clock(iso)
        : d.toLocaleDateString(this.locale, { month: 'short', day: 'numeric' })
    },
    dayLabel(iso) {
      const d = new Date(iso)
      const today = new Date()
      const yesterday = new Date(today.getTime() - 86400000)
      if (this.sameDay(d, today)) return this.$t('messages.today')
      if (this.sameDay(d, yesterday)) return this.$t('messages.yesterday')
      return d.toLocaleDateString(this.locale, { year: 'numeric', month: 'long', day: 'numeric' })
    },
    isNewDay(i) {
      if (i === 0) return true
      return !this.sameDay(new Date(this.messages[i - 1].creation_date), new Date(this.messages[i].creation_date))
    },
    autoGrow() {
      const el = this.$refs.input
      if (!el) return
      el.style.height = 'auto'
      el.style.height = Math.min(el.scrollHeight, 120) + 'px'
    },
    showError(message) {
      this.error = message
      clearTimeout(this.errorTimer)
      this.errorTimer = setTimeout(() => { this.error = '' }, 3000)
    },
    async loadConversations() {
      try {
        const res = await api.get('messaging/conversations/', { skipGlobalError: true })
        this.conversations = res.data
      } catch (e) {
        console.error('load conversations failed', e)
        this.showError(this.$t('messages.loadFailed'))
      } finally {
        this.loadingList = false
      }
    },
    markReadUpTo(upto) {
      if (!upto) return
      for (const m of this.messages) {
        if (m.mine && m.id <= upto) m.is_read = true
      }
    },
    // Latest page of the open thread.
    async loadMessages() {
      if (!this.activeId) return
      const id = this.activeId
      try {
        const res = await api.get(`messaging/conversations/${id}/messages/`, {
          params: { limit: PAGE_SIZE },
          skipGlobalError: true,
        })
        if (id !== this.activeId) return
        this.messages = res.data.results
        this.hasMore = res.data.has_more
        this.markReadUpTo(res.data.read_upto)
        this.scrollToBottom()
      } catch (e) {
        console.error('load messages failed', e)
        this.showError(this.$t('messages.loadFailed'))
      }
    },
    // Only messages newer than the ones already shown (used by poll and after send).
    async loadNewMessages() {
      if (!this.activeId) return
      if (!this.messages.length) return this.loadMessages()
      const id = this.activeId
      try {
        const res = await api.get(`messaging/conversations/${id}/messages/`, {
          params: { after: this.messages[this.messages.length - 1].id },
          skipGlobalError: true,
        })
        if (id !== this.activeId) return
        const known = new Set(this.messages.map((m) => m.id))
        const fresh = res.data.results.filter((m) => !known.has(m.id))
        if (fresh.length) {
          this.messages.push(...fresh)
          this.scrollToBottom()
        }
        this.markReadUpTo(res.data.read_upto)
      } catch (e) {
        console.error('load new messages failed', e)
        this.showError(this.$t('messages.loadFailed'))
      }
    },
    async loadOlder() {
      if (!this.activeId || this.loadingOlder || !this.hasMore || !this.messages.length) return
      const id = this.activeId
      this.loadingOlder = true
      const el = this.$refs.scroller
      const prevHeight = el ? el.scrollHeight : 0
      try {
        const res = await api.get(`messaging/conversations/${id}/messages/`, {
          params: { before: this.messages[0].id, limit: PAGE_SIZE },
          skipGlobalError: true,
        })
        if (id !== this.activeId) return
        const known = new Set(this.messages.map((m) => m.id))
        this.messages = [...res.data.results.filter((m) => !known.has(m.id)), ...this.messages]
        this.hasMore = res.data.has_more
        // Keep the viewport on the message the user was reading.
        this.$nextTick(() => {
          if (el) el.scrollTop += el.scrollHeight - prevHeight
        })
      } catch (e) {
        console.error('load older failed', e)
        this.showError(this.$t('messages.loadFailed'))
      } finally {
        this.loadingOlder = false
      }
    },
    async openConversation(id) {
      this.activeId = id
      this.messages = []
      this.hasMore = false
      await this.loadMessages()
      // Thread fetch marks messages as read server-side; clear the badge locally.
      const conv = this.conversations.find((c) => c.id === id)
      if (conv) conv.unread_count = 0
      window.dispatchEvent(new CustomEvent('messages-read'))
    },
    async poll() {
      await this.loadConversations()
      if (this.activeId) await this.loadNewMessages()
      const conv = this.activeConversation
      if (conv) conv.unread_count = 0
    },
    async sendMessage() {
      const body = this.draft.trim()
      if (!body || this.sending || !this.activeId) return
      this.sending = true
      try {
        await api.post(`messaging/conversations/${this.activeId}/messages/`, { body }, { skipGlobalError: true })
        this.draft = ''
        this.$nextTick(this.autoGrow)
        await this.loadNewMessages()
        this.loadConversations()
      } catch (e) {
        console.error('send message failed', e)
        this.showError(this.$t('messages.sendFailed'))
      } finally {
        this.sending = false
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const el = this.$refs.scroller
        if (el) el.scrollTop = el.scrollHeight
      })
    },
  },
}
</script>

<style scoped>
/* Fill the viewport under the fixed navbar + side menu (50px), WhatsApp Web style. */
.messages-wrapper {
  position: fixed; top: calc(var(--app-bar-live-h, var(--app-bar-h)) + 50px); bottom: 0; inset-inline: 0;
  width: auto; height: auto; margin: 0; display: block;
  background: var(--color-bg);
}
.messages-layout {
  display: grid; grid-template-columns: 360px minmax(0, 1fr);
  width: 100%; height: 100%; max-width: 1400px; margin: 0 auto;
  background: var(--color-surface);
  border-inline: 1px solid var(--color-border);
  text-align: start;
}

/* ---------- list ---------- */
.conversation-list { display: flex; flex-direction: column; min-height: 0; border-inline-end: 1px solid var(--color-border); }
.list-header { display: flex; align-items: center; height: 60px; padding: 0 16px; background: var(--color-primary-soft); flex: none; }
.list-title { margin: 0; font-size: 1.2rem; color: var(--color-text); }
.list-search { padding: 8px 12px; flex: none; border-bottom: 1px solid var(--color-border); }
.list-search input {
  width: 100%; padding: 8px 14px; font: inherit; font-size: 0.9rem;
  background: var(--color-bg); border: 1px solid transparent; border-radius: 999px;
}
.list-search input:focus { outline: none; border-color: var(--color-primary); background: var(--color-surface); }
.list-scroll { flex: 1; overflow-y: auto; }
.load-older {
  display: block; margin: 0 auto 8px; padding: 6px 16px; font: inherit; font-size: 0.85rem; cursor: pointer;
  color: var(--color-primary); background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 999px;
}
.load-older:disabled { opacity: 0.6; cursor: default; }
.empty { padding: 16px; color: var(--color-text-muted); font-size: 0.95rem; }

.conversation-item {
  display: flex; align-items: center; gap: 12px; width: 100%; padding: 10px 16px;
  background: none; border: none; text-align: start; cursor: pointer; color: var(--color-text);
}
.conversation-item:hover { background: var(--color-bg); }
.conversation-item.active { background: var(--color-primary-soft); }
.avatar {
  flex: none; width: 46px; height: 46px; display: flex; align-items: center; justify-content: center;
  background: var(--color-primary); color: #fff; border-radius: 50%; font-weight: 700; font-size: 1.1rem;
}
.conv-body { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; padding-bottom: 10px; border-bottom: 1px solid var(--color-border); margin-bottom: -10px; padding-top: 10px; margin-top: -10px; }
.conv-top, .conv-bottom { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.conv-name { font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.conv-time { flex: none; font-size: 0.75rem; color: var(--color-text-muted); }
.conv-time.unread { color: var(--color-primary); font-weight: 600; }
.conv-last { min-width: 0; font-size: 0.88rem; color: var(--color-text-muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.badge {
  flex: none; min-width: 20px; padding: 0 6px; text-align: center; line-height: 20px;
  font-size: 0.75rem; font-weight: 700; color: #fff; background: var(--color-primary); border-radius: 999px;
}

/* ---------- thread ---------- */
.thread { display: flex; flex-direction: column; min-width: 0; min-height: 0; background: var(--color-bg); }
.thread-empty { margin: auto; display: flex; flex-direction: column; align-items: center; gap: 8px; color: var(--color-text-muted); }
.thread-header {
  flex: none; display: flex; align-items: center; gap: 12px; height: 60px; padding: 0 16px;
  background: var(--color-primary-soft); border-bottom: 1px solid var(--color-border);
}
.thread-header .avatar { width: 40px; height: 40px; font-size: 1rem; }
.thread-name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.back-btn { display: none; background: none; border: none; font-size: 1.3rem; cursor: pointer; color: var(--color-text); padding: 0; }
[dir=rtl] .back-arrow { display: inline-block; transform: scaleX(-1); }

.thread-messages {
  flex: 1; min-height: 0; overflow-y: auto; display: flex; flex-direction: column; gap: 3px; padding: 16px 8%;
  background-color: var(--color-bg);
  background-image: radial-gradient(var(--color-border) 1px, transparent 1px);
  background-size: 18px 18px;
}
.day-chip { display: flex; justify-content: center; margin: 10px 0; }
.day-chip span {
  padding: 4px 12px; font-size: 0.78rem; color: var(--color-text-muted);
  background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-sm); box-shadow: var(--shadow-sm);
}

.bubble-row { display: flex; justify-content: flex-start; }
.bubble-row.mine { justify-content: flex-end; }
.bubble {
  position: relative; max-width: min(65%, 520px); padding: 6px 10px 4px;
  background: var(--color-surface); color: var(--color-text);
  border-radius: 0 var(--radius-md) var(--radius-md) var(--radius-md); box-shadow: var(--shadow-sm);
  display: flex; flex-direction: column;
}
.bubble-row.mine .bubble {
  background: var(--color-primary-soft); border: 1px solid #cddcfb;
  border-radius: var(--radius-md) 0 var(--radius-md) var(--radius-md);
}
[dir=rtl] .bubble { border-radius: var(--radius-md) 0 var(--radius-md) var(--radius-md); }
[dir=rtl] .bubble-row.mine .bubble { border-radius: 0 var(--radius-md) var(--radius-md) var(--radius-md); }
.bubble-text { white-space: pre-wrap; overflow-wrap: anywhere; line-height: 1.45; }
.bubble-meta { align-self: flex-end; display: flex; align-items: center; gap: 4px; margin-top: 2px; font-size: 0.7rem; color: var(--color-text-muted); }
.tick { color: var(--color-text-muted); }
.tick.read { color: var(--color-primary); }

.product-card {
  display: flex; align-items: center; gap: 10px; margin: 2px 0 6px; padding: 8px;
  background: var(--color-bg); color: var(--color-text);
  border: 1px solid var(--color-border); border-inline-start: 4px solid var(--color-primary);
  border-radius: var(--radius-sm); text-decoration: none;
}
.card-img { width: 52px; height: 52px; object-fit: cover; border-radius: var(--radius-sm); }
.card-info { display: flex; flex-direction: column; min-width: 0; }
.card-name { font-weight: 600; font-size: 0.9rem; overflow-wrap: anywhere; }
.card-price { font-size: 0.85rem; color: var(--color-primary); }

.composer {
  flex: none; display: flex; align-items: flex-end; gap: 10px; padding: 10px 16px;
  background: var(--color-primary-soft); border-top: 1px solid var(--color-border);
}
.composer textarea {
  flex: 1; resize: none; max-height: 120px; padding: 10px 16px; font: inherit; line-height: 1.4;
  background: var(--color-surface); border: 1px solid transparent; border-radius: 22px;
}
.composer textarea:focus { outline: none; border-color: var(--color-primary); }
.send-btn {
  flex: none; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center;
  color: #fff; background: var(--color-primary); border: none; border-radius: 50%; cursor: pointer;
  transition: background var(--transition);
}
.send-btn:hover:not(:disabled) { background: var(--color-primary-hover); }
.send-btn:disabled { opacity: 0.5; cursor: default; }
[dir=rtl] .send-icon { transform: scaleX(-1); }

.toast {
  position: fixed; bottom: 24px; inset-inline-start: 50%; transform: translateX(-50%); z-index: 1000;
  padding: 12px 20px; color: #fff; background: #c0392b; border-radius: var(--radius-md); box-shadow: var(--shadow-md);
}
[dir=rtl] .toast { transform: translateX(50%); }
.toast-enter-active, .toast-leave-active { transition: opacity 0.25s; }
.toast-enter-from, .toast-leave-to { opacity: 0; }

@media (max-width: 760px) {
  .messages-layout { grid-template-columns: 1fr; border-inline: none; }
  .conversation-list { border-inline-end: none; }
  .messages-layout.thread-open .conversation-list { display: none; }
  .messages-layout:not(.thread-open) .thread { display: none; }
  .back-btn { display: block; }
  .thread-messages { padding: 12px; }
  .bubble { max-width: 85%; }
}
</style>
