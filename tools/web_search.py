# tools/web_search.py

import http.client
import json
import os

def search_web(query: str) -> str:
    try:
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({
            "q": query,
            "gl": "pk"
        })

        headers = {
            'X-API-KEY': os.getenv("SERPER_API_KEY"),
            'Content-Type': 'application/json'
        }

        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()
        result = json.loads(data)

        # Extracting top results
        organic_results = result.get("organic", [])
        if not organic_results:
            return "🔍 No search results found."

        top_results = []
        for item in organic_results[:3]:  # Top 3 results
            title = item.get("title", "")
            link = item.get("link", "")
            snippet = item.get("snippet", "")
            top_results.append(f"🔹 *{title}*\n{snippet}\n🔗 {link}")

        return "\n\n".join(top_results)

    except Exception as e:
        return f"❌ Error fetching web results: {e}"
