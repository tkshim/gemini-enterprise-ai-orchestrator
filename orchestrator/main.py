import os
import json
from typing import Any
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, FunctionDeclaration

# =====================================================================
# 環境変数からGCPプロジェクト設定を読み込む
# 本番環境では .env ファイルまたはSecret Managerで管理する
# =====================================================================
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-project-id")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
MODEL_NAME = "gemini-1.5-pro"

# Vertex AI SDKを初期化（GCPプロジェクトとリージョンを指定）
vertexai.init(project=PROJECT_ID, location=LOCATION)


class OrchestratorAgent:
    """
    Google Geminiを中核としたオーケストレーターエージェント。
    
    役割：
    - エンドユーザーのリクエストをGemini Enterprise UIから受け取る
    - Geminiでリクエストの意図を分析し、適切なSaaSエージェントに振り分ける
    - A2AプロトコルでSaaS AIエージェントと通信する
    - 結果を検証してGemini Enterprise UIに返却する
    """

    def __init__(self):
        # Gemini 1.5 Proモデルを初期化
        # system_instructionでオーケストレーターとしての役割を定義
        self.model = GenerativeModel(
            MODEL_NAME,
            system_instruction="""
            You are an enterprise AI orchestrator. 
            Analyze the user request and determine which SaaS agent 
            (ServiceNow, Salesforce, Workday) should handle the task.
            Always respond in structured JSON format.
            """
        )
        
        # 連携するSaaSエージェントをディクショナリで管理
        # キー名がルーティングの判断キーになる
        self.agents = {
            "servicenow": ServiceNowAgent(),   # IT service management
            "salesforce": SalesforceAgent(),   # CRM / sales workflow
            "workday": WorkdayAgent(),         # HR / finance workflow
        }

    def process_request(self, user_request: str) -> dict:
        """
        メインエントリーポイント。
        Gemini Enterprise UIからのユーザーリクエストを処理する。
        
        処理フロー：
        1. Geminiでリクエストの意図を分析
        2. 対象SaaSエージェントにA2Aプロトコルで委譲
        3. 結果を検証してUIに返却
        
        Args:
            user_request: エンドユーザーの自然言語リクエスト
            
        Returns:
            SaaS AIエージェントからの集約済み結果
        """
        print(f"[Orchestrator] Received request: {user_request}")

        # Step 1: Geminiでユーザーの意図を分析し、ルーティング先を決定
        routing_decision = self._analyze_intent(user_request)
        print(f"[Orchestrator] Routing decision: {routing_decision}")

        # Step 2: ルーティング先エージェントの存在確認
        target_agent = routing_decision.get("target_agent")
        if target_agent not in self.agents:
            # 未知のエージェントが指定された場合はエラーを返す
            return {"status": "error", "message": f"Unknown agent: {target_agent}"}

        # Step 3: A2AプロトコルでSaaS AIエージェントにタスクを委譲
        agent_response = self.agents[target_agent].handle(
            task=routing_decision.get("task"),
            parameters=routing_decision.get("parameters", {})
        )

        # Step 4: エージェントの結果を検証し、UIに返却
        return self._validate_and_respond(agent_response)

    def _analyze_intent(self, user_request: str) -> dict:
        """
        Geminiを使ってユーザーリクエストの意図を分析する。
        
        Geminiにプロンプトを送り、以下を含むJSONを生成させる：
        - target_agent: 処理すべきSaaSエージェント名
        - task: 実行するタスクの種類
        - parameters: タスク実行に必要なパラメータ
        """
        prompt = f"""
        Analyze the following user request and return a JSON object with:
        - target_agent: one of [servicenow, salesforce, workday]
        - task: specific task to perform
        - parameters: relevant parameters extracted from the request
        
        User request: {user_request}
        """
        
        # GeminiにプロンプトをHTTPリクエストで送信
        response = self.model.generate_content(prompt)
        
        # GeminiのレスポンスをJSONとしてパース
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            # JSONパースに失敗した場合はServiceNowへのデフォルトルーティング
            return {
                "target_agent": "servicenow",
                "task": "general_inquiry",
                "parameters": {"query": user_request}
            }

    def _validate_and_respond(self, agent_response: dict) -> dict:
        """
        SaaSエージェントからの結果を検証する。
        
        成功時：結果をGemini Enterprise UIに返却
        失敗時：追加処理をリクエスト（Noルートで再ルーティング）
        
        これがフロー図の「結果を受け取り、問題なければUIへ、
        問題あれば追加処理を依頼」のロジックに対応する。
        """
        if agent_response.get("status") == "success":
            # 正常完了：ユーザーへの完了通知と追加リクエスト確認
            return {
                "status": "success",
                "message": "Your request has been completed.",
                "data": agent_response.get("data"),
                "additional_requests": True   # UIで「追加の要望はありますか？」を表示
            }
        else:
            # 異常検知：再処理ルートに誘導（フロー図のNoルート）
            return {
                "status": "retry",
                "message": "Processing additional steps...",
                "error": agent_response.get("error")
            }
