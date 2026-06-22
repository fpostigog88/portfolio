---
type: Project
title: Hermes Agent Framework
description: Open source autonomous AI agent with persistent memory, Chrome CDP browser automation, Discord and WhatsApp messaging, Gmail automation, terminal operations, and Kanban task coordination.
resource: https://github.com/fpostigog88/hermes-automation-suite
tags: [hermes, ai-agent, automation, chrome-cdp, discord, whatsapp, gmail, python]
timestamp: 2026-06-22T00:00:00Z
---

# Hermes Agent Framework

**Type:** Open source software project  
**GitHub:** https://github.com/fpostigog88/hermes-automation-suite  
**License:** Open source  
**Status:** Active  

## What it is

An autonomous AI agent framework built for personal and professional workflow automation. Hermes runs as a persistent background agent with persistent memory, making decisions and taking actions based on context that accumulates over time.

## Core capabilities

### Messaging
- **Discord:** Sends and receives messages, manages webhooks, supports multi-server configuration
- **WhatsApp:** Bridge integration with WhatsApp Web, message send/receive automation
- **Email (Gmail):** Automated email sending and receiving via Gmail API with OAuth

### Browser Automation
- **Chrome CDP:** Full Chrome DevTools Protocol integration for browser control
- Runs on Windows with CDP port 9522 (Chrome DevTools debugging port)
- Automates web scraping, form filling, and web-based workflows

### Terminal and File Operations
- Full terminal command execution (PowerShell, bash)
- File read/write operations with structured data support
- Directory management and glob-based file operations

### Task Coordination
- **Kanban board:** SQLite-based task queue with multi-agent coordination
- Cron scheduling for recurring tasks
- Subagent spawning via `delegate_task` for parallel work

### AI Integration
- Multi-provider support: MiniMax M2, OpenAI, Anthropic, Fireworks, local models
- Local LLM inference via llama.cpp and vLLM
- Persistent memory and context management
- Skill system for reusable procedural knowledge

### Memory and Context
- Session history with full-text search
- Persistent cross-session memory
- Semantic search capability via GBrain (PGLite vector database)

## Architecture

- **Gateway:** HTTP server routing messages to platform adapters
- **Adapters:** Discord, WhatsApp, Gmail, Chrome CDP — each platform has a dedicated adapter
- **Agent loop:** Context assembly → LLM reasoning → tool execution → response
- **Scheduler:** Cron-based recurring task execution
- **Skill system:** YAML-defined reusable procedures loaded by the agent

## Related projects

- [Multi-Agent Orchestrator](https://github.com/fpostigog88/multi-agent-orchestrator) — dependency resolution and parallel execution framework

## Source articles

- [Building Agentic Workflow Systems with Hermes and OpenClaw](https://felipepostigo.com/articles/building-agentic-workflow-systems-with-hermes-and-openclaw/)
- [How I Built a 6-Agent AI Operating System](https://felipepostigo.com/articles/how-i-built-a-6-agent-ai-operating-system/)

## Related concepts

- [Applied AI and AI agents](/skills/applied-ai)
- [Workflow automation](/skills/workflow-automation)
