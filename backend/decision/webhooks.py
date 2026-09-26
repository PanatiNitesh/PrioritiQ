import os
import json
import hmac
import hashlib
import time
import urllib.request
import urllib.error
import threading
from datetime import datetime
from typing import Dict, Any, List, Optional
from ..database.db import get_connection, _db_lock

class WebhookDispatcher:
    """
    Enterprise Webhook Dispatcher for PrioritiQ.
    Dispatches cryptographically signed HMAC-SHA256 event payloads to external endpoints
    (Slack, HubSpot, Salesforce, Zapier, Make, internal microservices).
    """

    @staticmethod
    def register_webhook(url: str, event_types: List[str], secret: Optional[str] = None) -> Dict[str, Any]:
        webhook_id = f"WHK-{hashlib.md5(f'{url}:{time.time()}'.encode()).hexdigest()[:8].upper()}"
        secret_key = secret or hashlib.sha256(f"{webhook_id}:{time.time()}".encode()).hexdigest()[:32]
        events_str = ",".join(event_types)

        with _db_lock:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
            INSERT OR REPLACE INTO webhooks (id, url, event_types, secret, is_active, created_at)
            VALUES (?, ?, ?, ?, 1, ?)
            """, (webhook_id, url, events_str, secret_key, datetime.now().isoformat()))
            conn.commit()
            conn.close()

        return {
            "webhook_id": webhook_id,
            "url": url,
            "event_types": event_types,
            "secret": secret_key,
            "is_active": True
        }

    @staticmethod
    def list_webhooks() -> List[Dict[str, Any]]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, url, event_types, is_active, created_at FROM webhooks")
        rows = cur.fetchall()
        conn.close()
        return [
            {
                "id": r["id"],
                "url": r["url"],
                "event_types": r["event_types"].split(","),
                "is_active": bool(r["is_active"]),
                "created_at": r["created_at"]
            }
            for r in rows
        ]

    @staticmethod
    def delete_webhook(webhook_id: str) -> bool:
        with _db_lock:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM webhooks WHERE id = ?", (webhook_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            conn.close()
            return deleted

    @classmethod
    def dispatch_event_async(cls, event_type: str, payload: Dict[str, Any]):
        """
        Non-blocking background thread dispatch of registered webhooks.
        """
        thread = threading.Thread(target=cls._dispatch_worker, args=(event_type, payload), daemon=True)
        thread.start()

    @classmethod
    def _dispatch_worker(cls, event_type: str, payload: Dict[str, Any]):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, url, event_types, secret FROM webhooks WHERE is_active = 1")
        webhooks = cur.fetchall()
        conn.close()

        event_envelope = {
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": payload
        }
        json_data = json.dumps(event_envelope, sort_keys=True).encode("utf-8")

        for wh in webhooks:
            subscribed_types = [t.strip() for t in wh["event_types"].split(",")]
            if event_type in subscribed_types or "*" in subscribed_types:
                url = wh["url"]
                secret = wh["secret"]
                signature = hmac.new(secret.encode("utf-8"), json_data, hashlib.sha256).hexdigest()

                req = urllib.request.Request(
                    url,
                    data=json_data,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "PrioritiQ-Webhook-Dispatcher/2.0",
                        "X-PrioritiQ-Event": event_type,
                        "X-PrioritiQ-Signature": f"sha256={signature}"
                    },
                    method="POST"
                )

                try:
                    with urllib.request.urlopen(req, timeout=5) as response:
                        _ = response.read()
                except Exception as e:
                    # Log failure in dev environments or offline endpoints
                    pass
