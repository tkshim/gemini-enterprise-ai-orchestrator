import requests
import os
from typing import Any


class ServiceNowAgent:
    """
    ServiceNow AIエージェントコネクター。
    
    役割：
    - OrchestratorからA2Aプロトコルでタスクを受け取る
    - ServiceNow REST APIを呼び出してITSMタスクを実行する
    - 処理結果をOrchestratorに返却する
    
    対応業務：
    - インシデント作成・管理
    - サービスリクエスト処理
    - チェンジリクエスト処理
    - AIによるチケット自動分類
    """

    # ServiceNowインスタンスのベースURL（環境変数から取得）
    BASE_URL = os.environ.get("SERVICENOW_INSTANCE_URL", "https://your-instance.service-now.com")
    API_VERSION = "v2"

    def __init__(self):
        # ServiceNow APIへの認証セッションを初期化
        # Basic認証を使用（本番環境ではOAuth2.0を推奨）
        self.session = requests.Session()
        self.session.auth = (
            os.environ.get("SERVICENOW_USERNAME"),
            os.environ.get("SERVICENOW_PASSWORD")
        )
        # JSONでのやりとりを指定するHTTPヘッダーを設定
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def handle(self, task: str, parameters: dict) -> dict:
        """
        OrchestratorからA2Aプロトコルで受け取ったタスクを処理する。
        
        タスク種別に応じて対応するハンドラーメソッドを呼び出す。
        未知のタスクはgeneral_inquiryにフォールバック。
        
        Args:
            task: タスク種別（例：create_incident, resolve_ticket）
            parameters: タスク実行パラメータ
            
        Returns:
            処理結果をOrchestratorに返却
        """
        print(f"[ServiceNow Agent] Received task: {task}")

        # タスク種別とハンドラーメソッドのマッピング
        task_handlers = {
            "create_incident": self._create_incident,
            "get_ticket_status": self._get_ticket_status,
            "resolve_ticket": self._resolve_ticket,
            "classify_request": self._classify_with_ai,
        }

        # タスク種別に対応するハンドラーを取得（未知の場合はデフォルト）
        handler = task_handlers.get(task, self._general_inquiry)
        return handler(parameters)

    def _create_incident(self, parameters: dict) -> dict:
        """
        ServiceNowにインシデントを新規作成する。
        
        Table API（/api/now/v2/table/incident）にPOSTリクエストを送信。
        PoC段階のためAPIコールはコメントアウトし、モックレスポンスを返す。
        """
        endpoint = f"{self.BASE_URL}/api/now/{self.API_VERSION}/table/incident"
        
        # APIリクエストのペイロードを組み立て
        payload = {
            "short_description": parameters.get("description"),  # インシデントの概要
            "urgency": parameters.get("urgency", "3"),           # 緊急度（1:高〜3:低）
            "category": parameters.get("category", "inquiry"),   # カテゴリ
            "caller_id": parameters.get("user_id")               # 申請者ID
        }

        # 本番実装時はこちらのAPIコールを有効化する
        # response = self.session.post(endpoint, json=payload)
        # return response.json()
        
        # PoC用モックレスポンス
        return {
            "status": "success",
            "data": {
                "incident_number": "INC0012345",
                "sys_id": "abc123xyz",
                "state": "New",
                "message": "Incident created successfully"
            }
        }

    def _get_ticket_status(self, parameters: dict) -> dict:
        """
        指定チケットIDのステータスをServiceNowから取得する。
        Table APIのGETリクエストでインシデントレコードを取得。
        """
        ticket_id = parameters.get("ticket_id")
        endpoint = f"{self.BASE_URL}/api/now/{self.API_VERSION}/table/incident/{ticket_id}"

        # 本番実装時はこちらのAPIコールを有効化する
        # response = self.session.get(endpoint)
        # return response.json()
        
        # PoC用モックレスポンス
        return {
            "status": "success",
            "data": {
                "incident_number": ticket_id,
                "state": "In Progress",
                "assigned_to": "IT Support Team",
                "updated": "2026-04-26T10:00:00Z"
            }
        }

    def _classify_with_ai(self, parameters: dict) -> dict:
        """
        ServiceNow AIを使ってリクエストを自動分類・ルーティングする。
        
        ServiceNow Now Intelligence APIを呼び出し、
        機械学習モデルによるカテゴリ予測と担当グループ推奨を取得。
        """
        # PoC用モックレスポンス（本番ではNow Intelligence APIを呼び出す）
        return {
            "status": "success",
            "data": {
                "classification": "Hardware Issue",
                "recommended_category": "hardware",
                "confidence_score": 0.92,          # 分類の信頼スコア（0〜1）
                "suggested_assignment_group": "Desktop Support"
            }
        }

    def _resolve_ticket(self, parameters: dict) -> dict:
        """チケットを解決済みに更新する。"""
        return {
            "status": "success",
            "data": {
                "incident_number": parameters.get("ticket_id"),
                "state": "Resolved",
                "resolution_notes": parameters.get("resolution_notes")
            }
        }

    def _general_inquiry(self, parameters: dict) -> dict:
        """未定義タスクのフォールバックハンドラー。"""
        return {
            "status": "success",
            "data": {"message": "Request received and being processed."}
        }
