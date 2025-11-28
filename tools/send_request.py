from langchain_core.tools import tool
import requests
import json
from typing import Any, Dict, Optional

@tool
def post_request(url: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Any:
    headers = headers or {"Content-Type": "application/json"}
    try:
        print(f"\nSending Answer \n{json.dumps(payload, indent=4)}\n to url: {url}")
        response = requests.post(url, json=payload, headers=headers)

        response.raise_for_status()

        data = response.json()
        delay = data.get("delay", 0)
        delay = delay if isinstance(delay, (int, float)) else 0
        correct = data.get("correct")
        if not correct and delay < 180:
            del data["url"]
        if delay >= 180:
            data = {
                "url": data.get("url")
            }
        print("Got the response: \n", json.dumps(data, indent=4), '\n')
        return data
    except requests.HTTPError as e:
        err_resp = e.response

        try:
            err_data = err_resp.json()
        except ValueError:
            err_data = err_resp.text

        print("HTTP Error Response:\n", err_data)
        return err_data

    except Exception as e:
        print("Unexpected error:", e)
        return str(e)