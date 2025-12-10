# A2A MCP Hello Agent

MCP Hello Server를 호출하는 A2A (Agent-to-Agent) 에이전트입니다.

## 구조

```
a2a-mcp-hello-py/
├── src/
│   ├── __init__.py         # 패키지 초기화
│   ├── mcp_client.py       # MCP 클라이언트 (MCP 서버 호출)
│   ├── agent.py            # 에이전트 로직
│   ├── agent_executor.py   # A2A Agent Executor
│   └── server.py           # A2A 서버 메인
├── .env                    # 환경 변수 설정
├── .env.example            # 환경 변수 예시
├── requirements.txt        # 의존성
├── pyproject.toml          # 프로젝트 메타데이터
└── README.md               # 이 파일
```

## 설치

```bash
# 가상 환경 생성
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

## 환경 변수 설정

`.env` 파일을 생성하거나 수정합니다:

```bash
# .env 파일 내용
MCP_SERVER_URL=https://mcp-hello-py-666155174404.asia-northeast3.run.app/mcp
HOST=0.0.0.0
PORT=9999
```

## 실행

```bash
python src/server.py

# 또는
python3 src/server.py
```

## A2A Agent Card

서버 실행 후 Agent Card 확인:

```bash
curl http://localhost:9999/.well-known/agent.json
```

## 테스트

### A2A Inspector 사용

1. [A2A Inspector](https://github.com/a2aproject/a2a-inspector) 설치
2. Agent URL 입력: `http://localhost:9999/`
3. 메시지 전송: "김철수에게 인사해줘"

### curl로 테스트

```bash
# Agent Card 확인
curl http://localhost:9999/.well-known/agent.json

# 메시지 전송
curl -X POST http://localhost:9999/tasks/send \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tasks/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"type": "text", "text": "김철수에게 인사해줘"}]
      }
    }
  }'
```

## 아키텍처

```
┌─────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  A2A Client │ ───▶  │  A2A MCP Hello  │ ───▶  │  MCP Hello      │
│  (Inspector)│       │  Agent (Python) │       │  Server (Cloud  │
│             │ ◀───  │                 │ ◀───  │  Run)           │
└─────────────┘       └─────────────────┘       └─────────────────┘
     A2A                    HTTP                     MCP
   Protocol                                       Protocol
```

## 주요 기능

- **say_hello**: 한 사람에게 인사
- **say_hello_multiple**: 여러 사람에게 인사

## 참고

- [A2A Protocol](https://a2a-protocol.org)
- [A2A Python SDK](https://github.com/a2aproject/a2a-python)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
