import os


class WorkdayAgent:
    """
    Workdayエージェントコネクター。
    
    役割：
    - OrchestratorからA2Aプロトコルでタスクを受け取る
    - Workday REST APIを呼び出してHR・財務処理を実行する
    - 処理結果をOrchestratorに返却する
    
    対応業務：
    - 従業員情報の取得
    - 休暇申請の処理
    - 給与情報の照会
    - 組織構造のクエリ
    """

    def __init__(self):
        # Workday接続情報を環境変数から取得
        # Workday OAuth 2.0クライアント認証を使用
        self.tenant_url = os.environ.get("WORKDAY_TENANT_URL")       # テナントURL
        self.client_id = os.environ.get("WORKDAY_CLIENT_ID")         # OAuthクライアントID
        self.client_secret = os.environ.get("WORKDAY_CLIENT_SECRET") # OAuthクライアントシークレット

    def handle(self, task: str, parameters: dict) -> dict:
        """
        OrchestratorからA2Aプロトコルで受け取ったタスクを処理する。
        タスク種別に応じて対応するハンドラーメソッドを呼び出す。
        """
        print(f"[Workday Agent] Received task: {task}")

        # タスク種別とハンドラーメソッドのマッピング
        task_handlers = {
            "get_employee_info": self._get_employee_info,
            "submit_leave_request": self._submit_leave_request,
            "get_payroll_info": self._get_payroll_info,
        }

        handler = task_handlers.get(task, self._general_inquiry)
        return handler(parameters)

    def _get_employee_info(self, parameters: dict) -> dict:
        """
        Workdayから従業員情報を取得する。
        Workday People Analytics APIのWorkers エンドポイントを使用。
        """
        # PoC用モックレスポンス
        return {
            "status": "success",
            "data": {
                "employee_id": parameters.get("employee_id"),
                "department": "Engineering",
                "manager": "Jane Smith",
                "location": "Tokyo, Japan"
            }
        }

    def _submit_leave_request(self, parameters: dict) -> dict:
        """
        Workdayに休暇申請を送信する。
        Absence Management APIを使用して休暇申請レコードを作成。
        申請後は承認ワークフローが自動的に起動される。
        """
        return {
            "status": "success",
            "data": {
                "request_id": "LR-2026-00456",
                "type": parameters.get("leave_type", "Annual Leave"),  # 休暇種別
                "status": "Pending Approval",                           # 承認待ち状態
                "start_date": parameters.get("start_date"),
                "end_date": parameters.get("end_date")
            }
        }

    def _get_payroll_info(self, parameters: dict) -> dict:
        """
        給与情報を照会する。
        Workday Payroll APIを使用して給与明細・支払い状況を取得。
        """
        return {
            "status": "success",
            "data": {
                "pay_period": "April 2026",
                "status": "Processed",           # 処理済み
                "next_pay_date": "2026-04-30"    # 次回支払日
            }
        }

    def _general_inquiry(self, parameters: dict) -> dict:
        """未定義タスクのフォールバックハンドラー。"""
        return {
            "status": "success",
            "data": {"message": "Workday request processed successfully."}
        }
