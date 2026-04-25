# Agentic Engineering: Fraud Detection System

This project demonstrates a **minimal agentic system** that:

- Generates a distributed system (Node.js + gRPC)
- Executes it locally
- Observes runtime behavior
- Validates correctness
- Applies fixes and retries autonomously

---

## 🧠 Key Idea

Move from:

code generation

to:

system generation + execution + validation

---

## 🏗 Architecture

Agent (Python)
  ├── planner
  ├── generator
  ├── executor
  └── validator
          ↓
Generated System (Node.js + gRPC)
  ├── Transaction Service
  ├── Decision Service
  └── Client Loop

---

## 🚀 Quick Start

```bash
cd agent
python agent.py
```

---

## 🔁 Agent Loop

PLAN → GENERATE → RUN → OBSERVE → VALIDATE  
                                ↓  
                             FIX → RETRY

---

## 📁 Structure

agent/
├── agent.py
├── planner.py
├── generator.py
├── executor.py
└── validator.py

generated/
├── proto/
├── services/
├── client.js
└── package.json

---

## ⚙️ Stack

- Python (agent)
- Node.js (generated system)
- gRPC
- (future) Kafka / RabbitMQ

---

## 🧪 Example Output

Transaction service running 50051  
Decision service running 50052  
10000 → BLOCK  
50 → APPROVE  

---

## 🔥 What Makes This Different

This system:

- does not assume correctness
- validates via execution
- fixes runtime failures
- converges toward a working state

---

