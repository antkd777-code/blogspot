import os

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
GOOGLE_REFRESH_TOKEN = os.environ["GOOGLE_REFRESH_TOKEN"]
BLOGGER_BLOG_ID = os.environ["BLOGGER_BLOG_ID"]

# 블로그 메타 정보 — 자신의 블로그에 맞게 수정
BLOG_NAME = "정보공유 블로그"
BLOG_URL = "https://your-blog.blogspot.com"
BLOG_AUTHOR = "블로그 운영자"
BLOG_DESCRIPTION = "생활, 건강, 금융, IT에 관한 유용한 정보를 공유합니다."

# Claude 모델 설정
CLAUDE_MODEL = "claude-sonnet-4-6"

# 포스트 설정
MIN_WORD_COUNT = 1500    # 애드센스 승인을 위한 최소 글자 수
POST_LABELS = ["정보", "생활정보"]  # 기본 라벨(태그)

KEYWORDS_CSV = "keywords/keywords.csv"
