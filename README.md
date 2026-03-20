# Python Examples Repository

A curated collection of Python examples and architectural patterns, ranging from low-level network protocols to modern ORM comparisons and cloud-native practices.

---

## 📚 Catalog

| Feature | Description | Link |
| :--- | :--- | :--- |
| **12-Factor App** | Best practices for building cloud-native apps | [12-Factor Notes](12factor.md) |
| **ORM Comparison** | Detailed comparison of Python ORMs | [ORM Guide](orm.md) |
| **Security** | JWT generation and validation | [JWT2](jwt2/) |
| **Protocols** | HTTP/2 and Server-Sent Events (SSE) | [H2](h2-examples/), [SSE](sse/) |
| **Storage** | MongoDB integration | [Mongo](mongo/) |
| **Task Scheduling** | Blocking and threaded schedulers | [Sched](sched/) |
| **Audio** | Audio processing examples | [Audios](audios/) |
| **AI/ML Serving** | TorchServe and Triton Inference Server | [TorchServe](torchsrv/), [Triton](tritonsrv/) |
| **Observability** | Prometheus metrics integration | [Prometheus](prom/) |
| **CLI Tools** | Documentation and search utilities | [Docli](docli/), [Esearch](esearch/) |

---

## 🚀 Getting Started

### Environment Setup

You can use a standard virtual environment or the modern **uv** package manager.

```bash
# Using standard venv
python3 -m venv venv
source venv/bin/activate

# Or using uv (recommended)
uv sync
```

---

## 🛠 Usage Examples

### 🔐 JWT (JSON Web Tokens)
Generate keys and run the main application logic:
```bash
cd jwt2
bash genkey.sh
python main.py
```

### 🌐 HTTP/2
Server with automated certificate generation:
```bash
cd h2
bash gencert.sh
hypercorn server:app -c hyper.toml

# Test with curl
curl https://localhost:8000/ -i -k
```

### 📡 Server-Sent Events (SSE)
Real-time server-to-client streaming:
```bash
cd sse
uvicorn server:app --log-config=log-config.yml

# Test sending a message
curl localhost:8000?name=world -i -X POST
# Test receiving stream
python client.py
```

### ⏱ Scheduler
Explore different scheduling paradigms:
```bash
cd sched
python blocking.py  # Synchronous blocking
python thread.py    # Multi-threaded execution
```

---

## 🏗 Architectural Patterns

This repository follows the **12-Factor App** methodology for modern software development. See the dedicated [12-Factor Notes](12factor.md) for a deep dive into how these principles apply to Python.

---
*Maintained as a reference for Python best practices.*
