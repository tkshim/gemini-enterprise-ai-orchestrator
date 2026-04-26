🌐 日本語は英語の後に続きます

# Gemini Enterprise AI Orchestrator (PoC)

## Overview
A proof-of-concept multi-agent orchestration platform built on Google Gemini,
designed to integrate enterprise SaaS applications via A2A protocol and REST APIs.
This architecture automates cross-platform business workflows and aggregates
results into a unified Google UI.

## Architecture
<img width="1566" height="915" alt="Google Orchestrator v1 0" src="https://github.com/user-attachments/assets/cf7f6cc3-9495-42dd-b6ce-53d930a8b1b8" />

## Background & Motivation
Built on 20+ years of enterprise architecture experience combined with
hands-on AI Agent implementation (currently spending ~30% of work time
on AI Agent adoption and deployment in production environments).

This PoC explores how Google Gemini can serve as a central orchestrator
to unify fragmented enterprise SaaS workflows across ServiceNow,
Salesforce, and Workday — reducing manual handoffs and enabling
intelligent automation at scale.

## Tech Stack
- **Orchestrator**: Google Gemini 1.5 Pro (via Vertex AI)
- **Protocol**: A2A (Agent-to-Agent), REST API, Connector
- **Agents**:
  - ServiceNow AI Agent (hands-on production experience)
  - Salesforce Agentforce (6 years as Salesforce Technical Architect)
  - Workday Agent
- **Language**: Python

## Use Case Example
1. User submits a cross-functional request via Gemini Enterprise UI
2. Orchestrator Agent interprets intent and delegates to relevant SaaS agents
3. ServiceNow handles IT service tasks, Salesforce manages CRM actions,
   Workday processes HR workflows
4. Results are collected and presented back in a unified Google UI


# Gemini Enterprise AI Orchestrator (PoC)
<img width="1566" height="915" alt="Google Orchestrator v1 0" src="https://github.com/user-attachments/assets/cf7f6cc3-9495-42dd-b6ce-53d930a8b1b8" />

## Overview
Google Gemini を中核としたマルチエージェント・オーケストレーション基盤のPoCです。
エンタープライズSaaSをA2AプロトコルおよびREST APIで統合し、
業務処理の自動化と結果の一元表示を実現するアーキテクチャを設計・実装しています。

## Architecture


## Background & Motivation
20年超のエンタープライズアーキテクト経験をベースに、
AI Agentの実務導入経験（現職にてAI Agent導入支援に約30%従事）を活かし、
マルチSaaS環境でのAIオーケストレーション基盤を設計。

## Tech Stack
- **Orchestrator**: Google Gemini 1.5 Pro (via Vertex AI)
- **Protocol**: A2A (Agent-to-Agent), REST API, Connector
- **Agents**:
  - ServiceNow AI Agent
  - Salesforce Agentforce
  - Workday Agent
- **Language**: Python

