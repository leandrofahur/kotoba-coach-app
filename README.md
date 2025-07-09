# 🗣️ KotobaCoach — Master Japanese Pronunciation with AI (MVP repo)

**KotobaCoach** is a private educational app built in collaboration with [NihongoDekita](https://nihongodekita.com/), designed to help beginner learners of Japanese improve their speaking skills through guided AI pronunciation feedback. The app uses real teacher audio and intelligent scoring based on pitch and mora analysis to provide personalized feedback.

---

## 🚀 Project Overview

### 🎯 Goal

Empower Japanese language learners to practice and perfect their pronunciation using AI-driven audio analysis, comparing their voice to a native teacher's reference.

### 👨‍🏫 Built For
- Students of NihongoDekita (and internal usage)
- Beginner-level Japanese learners focused on pronunciation
- Future expansion to intermediate/advanced levels & mobile use

---

## 🛠️ Tech Stack

### 🔙 Backend (FastAPI)
- `FastAPI` — core REST API
- `openai-whisper` — transcription & speech-to-text
- `pyworld`, `pyopenjtalk`, `librosa` — pitch & mora analysis
- `prometheus-client` — monitoring
- `asyncpg`, `sqlalchemy`, `alembic` — database (PostgreSQL, future)
- `WebSockets` — real-time feedback (planned)

### 🎨 Frontend (React + Tailwind)
- `React`, `Vite`, `TypeScript`, `Shadcn/ui` — responsive UI
- Real-time waveform, feedback view
- Upload and record interface for user audio

### 📱 Mobile (React Native)
- Simple app to record, send audio, and display feedback
- Powered by the same FastAPI backend

---

## 🔄 Core Workflow

1. **Select a Phrase** — User picks a Japanese phrase (e.g., 「おはようございます」)
2. **Listen to Native Reference** — Pre-recorded teacher audio plays
3. **Record Your Voice** — User speaks and records their attempt
4. **AI Analysis Pipeline**
   - Transcribe via Whisper
   - Extract pitch + mora
   - Compare with ground truth (target audio)
   - Score + generate personalized feedback
5. **Feedback Displayed** — Accuracy, pitch graph, and improvement tips are shown

---

## 📂 Repository Structure

```bash
kotoba-coach/
├── backend/               # FastAPI app
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── services/      # Whisper, audio, scoring
│   │   ├── models/
│   │   └── utils/
│   ├── tests/
│   └── Dockerfile
├── frontend/              # React app
│   ├── src/
│   ├── public/
│   └── vite.config.ts
└── ...
```
