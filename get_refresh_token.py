"""
Google OAuth2 리프레시 토큰 1회성 발급 스크립트
로컬에서 한 번만 실행하고, 출력된 refresh_token을 GitHub Secrets에 저장하세요.

사전 준비:
  1. Google Cloud Console → API 및 서비스 → Blogger API v3 활성화
  2. OAuth 2.0 클라이언트 ID 생성 (유형: 데스크톱 앱)
  3. 아래 환경변수 설정 후 실행:
     export GOOGLE_CLIENT_ID=<클라이언트ID>
     export GOOGLE_CLIENT_SECRET=<클라이언트시크릿>
     python get_refresh_token.py
"""
import os
import json
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:8080"
SCOPES = "https://www.googleapis.com/auth/blogger"

auth_code_holder = {}


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        auth_code_holder["code"] = params.get("code", [None])[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write("<h2>인증 완료! 이 창을 닫아도 됩니다.</h2>".encode("utf-8"))

    def log_message(self, *args):
        pass


def main():
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode({
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
    })

    print(f"\n브라우저에서 다음 URL을 여세요:\n{auth_url}\n")
    webbrowser.open(auth_url)

    server = HTTPServer(("localhost", 8080), CallbackHandler)
    print("콜백 대기 중 (localhost:8080)...")
    server.handle_request()

    code = auth_code_holder.get("code")
    if not code:
        print("인증 코드를 받지 못했습니다.")
        return

    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }, timeout=30)
    resp.raise_for_status()
    tokens = resp.json()

    print("\n========== GitHub Secrets에 저장할 값 ==========")
    print(f"GOOGLE_REFRESH_TOKEN = {tokens['refresh_token']}")
    print("================================================\n")

    with open(".refresh_token_backup.json", "w") as f:
        json.dump(tokens, f, indent=2)
    print("백업 파일 저장 완료: .refresh_token_backup.json (절대 커밋하지 마세요!)")


if __name__ == "__main__":
    main()
