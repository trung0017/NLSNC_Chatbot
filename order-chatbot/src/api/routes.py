from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
from fastapi.responses import HTMLResponse

from src.chatbot.chain import create_chatbot_chain

app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    customer_id: Optional[int] = None
    context: Optional[Dict] = None

class ChatResponse(BaseModel):
    response: str
    context: Dict

@app.get("/")
async def root():
    return {"status": "Chatbot API is running"}

@app.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        # Tạo chatbot chain
        components = create_chatbot_chain(request.customer_id)
        chatbot = components["chain"]
        
        # Xử lý tin nhắn
        response, new_context = chatbot.generate_response(
            request.message,
            request.context
        )
        
        return ChatResponse(
            response=response,
            context=new_context
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) 

@app.get("/chat-ui", response_class=HTMLResponse)
async def chat_ui():
    # Minimal chat UI for quick manual testing
    return """
<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Order Chatbot</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; background:#f7f7f8; margin:0; }
    .wrap { max-width: 800px; margin: 0 auto; padding: 24px; }
    h1 { font-size: 20px; margin: 0 0 16px 0; }
    #log { background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:16px; height:420px; overflow:auto; }
    .row { display:flex; gap:12px; margin-top:12px; }
    input[type=text] { flex:1; padding:12px 14px; border:1px solid #e5e7eb; border-radius:10px; outline:none; }
    button { padding:12px 16px; border:0; background:#2563eb; color:#fff; border-radius:10px; cursor:pointer; }
    .msg { margin:8px 0; }
    .me { color:#111827; }
    .bot { color:#0f766e; white-space:pre-wrap; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Order Chatbot</h1>
    <div id="log"></div>
    <div class="row">
      <input id="msg" type="text" placeholder="Nhập câu hỏi... ví dụ: Mình cần laptop học lập trình tầm 15 triệu" />
      <button id="send">Gửi</button>
    </div>
  </div>
  <script>
    const log = document.getElementById('log');
    const msg = document.getElementById('msg');
    const send = document.getElementById('send');

    function append(type, text) {
      const div = document.createElement('div');
      div.className = 'msg ' + type;
      div.textContent = text;
      log.appendChild(div);
      log.scrollTop = log.scrollHeight;
    }

    async function callChat(m) {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: m, customer_id: 1, context: {} })
      });
      if (!res.ok) {
        const t = await res.text();
        append('bot', 'Lỗi: ' + res.status + ' ' + t);
        return;
      }
      const data = await res.json();
      append('bot', data.response ?? JSON.stringify(data));
    }

    send.addEventListener('click', () => {
      const m = msg.value.trim();
      if (!m) return;
      append('me', m);
      msg.value = '';
      callChat(m).catch(e => append('bot', 'Lỗi: ' + e.message));
    });
    msg.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') send.click();
    });
  </script>
</body>
</html>
    """