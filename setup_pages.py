"""
1회성 실행 스크립트 — 개인정보처리방침·소개 페이지를 Blogger에 발행합니다.

실행 방법 (로컬):
  export ANTHROPIC_API_KEY=...
  export GOOGLE_CLIENT_ID=...
  export GOOGLE_CLIENT_SECRET=...
  export GOOGLE_REFRESH_TOKEN=...
  export BLOGGER_BLOG_ID=...
  python setup_pages.py
"""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from scripts.publish_post import publish_page


def render(template_path: str) -> str:
    with open(template_path, encoding="utf-8") as f:
        html = f.read()
    return (
        html.replace("{{BLOG_NAME}}", config.BLOG_NAME)
        .replace("{{BLOG_URL}}", config.BLOG_URL)
        .replace("{{BLOG_AUTHOR}}", config.BLOG_AUTHOR)
        .replace("{{TODAY}}", date.today().isoformat())
    )


def main():
    print("개인정보처리방침 발행 중...")
    publish_page("개인정보처리방침", render("templates/privacy_policy.html"))

    print("소개 페이지 발행 중...")
    publish_page("블로그 소개", render("templates/about.html"))

    print("완료! Blogger 관리 페이지에서 확인하세요.")


if __name__ == "__main__":
    main()
