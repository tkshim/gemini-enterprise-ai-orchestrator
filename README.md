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
Built on 20+ years of enterprise architecture experience, combined with hands-on AI agent implementation and production deployment (currently dedicating ~30% of work time to AI agent adoption and operationalization).

This PoC explores an orchestrator-centric architecture using Google Gemini as the control layer, designed to unify fragmented enterprise workflows across ServiceNow, Salesforce, and Workday.

Rather than relying on traditional API-driven integrations, this approach adopts an **agent-to-agent (A2A) collaboration model**, where specialized AI agents are orchestrated based on responsibility and domain context.

This enables:

- Elimination of manual handoffs across business functions
- Context-aware task delegation while preserving workflow continuity
- A scalable foundation for enterprise-wide intelligent automation

## Tech Stack
- **Orchestrator**: Google Gemini 1.5 Pro (via Vertex AI)
- **Protocol**: A2A (Agent-to-Agent), REST API, Connector
- **Agents**:
  - ServiceNow AI Agent (hands-on production experience)
  - Salesforce Agentforce (6 years as Salesforce Technical Architect)
  - Workday Agent
- **Language**: Python

## Use Case Example
1. Users submit cross-functional requests via Gemini Enterprise UI
2. The Orchestrator Agent interprets user intent and dynamically routes tasks to appropriate SaaS agents
3. ServiceNow handles IT service operations, Salesforce manages CRM and customer-related actions, and Workday processes HR workflows
4. Results from each agent are aggregated and presented back to the user through a unified Google interface


# Gemini Enterprise AI Orchestrator (PoC)

## Overview
Google Gemini を中核としたマルチエージェント・オーケストレーション基盤のPoCです。
エンタープライズSaaSをA2AプロトコルおよびREST APIで統合し、
業務処理の自動化と結果の一元表示を実現するアーキテクチャを設計・実装しています。

## Architecture
<img width="1566" height="915" alt="Google Orchestrator v1 0" src="https://github.com/user-attachments/assets/cf7f6cc3-9495-42dd-b6ce-53d930a8b1b8" />

## Background & Motivation
20年以上にわたるエンタープライズアーキテクチャの経験に加え、AIエージェントの実装・本番導入に従事（現在、業務時間の約30%をAIエージェントの導入および運用に充当）。

本PoCでは、Google Gemini を中核としたオーケストレーションレイヤーを設計し、ServiceNow、Salesforce、Workday に分散する業務プロセスをAIエージェント単位で統合するアプローチを検証している。

従来のAPI連携中心のアーキテクチャではなく、**Agent-to-Agent（A2A）およびオーケストレーター型設計を前提とした「エージェント協調モデル」**を採用することで、以下を実現：

- 部門横断業務における手動ハンドオフの排除
- 業務コンテキストを維持したままのタスク分散処理
- スケーラブルなエンタープライズAI基盤の構築

## Use Case Example
- ユーザーは Gemini Enterprise UIを通じて、IT・CRM・HRをまたぐ複合的なリクエストを送信
- オーケストレーターエージェントが意図解析を行い、最適なSaaSエージェントへ動的にルーティング
- ServiceNowはITサービス処理、Salesforceは顧客データおよび営業アクション、Workdayは人事ワークフローを担当
- 各エージェントの処理結果は統合され、単一のUI上でユーザーに提示される

## Tech Stack
- **Orchestrator**: Google Gemini 1.5 Pro (via Vertex AI)
- **Protocol**: A2A (Agent-to-Agent), REST API, Connector
- **Agents**:
  - ServiceNow AI Agent
  - Salesforce Agentforce
  - Workday Agent
- **Language**: Python

