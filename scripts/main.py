"""GitHub Actions 진입점 — 키워드 선택 → 글 생성 → 발행"""
import os
import sys

# 루트를 PYTHONPATH에 추가 (scripts/ 하위에서 import config 가능하게)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.keyword_manager import get_next_keyword, mark_used
from scripts.generate_post import generate_post
from scripts.publish_post import publish_post


def main():
    # workflow_dispatch에서 키워드 직접 지정한 경우 우선 사용
    keyword_override = os.environ.get("KEYWORD_OVERRIDE", "").strip()

    if keyword_override:
        keyword = keyword_override
        category = "기타"
        print(f"[main] 수동 키워드: {keyword}")
    else:
        result = get_next_keyword()
        if result is None:
            print("[main] 사용할 키워드가 없습니다. keywords.csv를 업데이트하세요.")
            sys.exit(0)
        keyword, category = result
        print(f"[main] 키워드: {keyword} / 카테고리: {category}")

    print("[main] 포스트 생성 중...")
    post_data = generate_post(keyword, category)

    print(f"[main] 제목: {post_data['title']}")
    print(f"[main] 라벨: {post_data['labels']}")

    url = publish_post(
        title=post_data["title"],
        content=post_data["content"],
        labels=post_data["labels"],
    )

    if not keyword_override:
        mark_used(keyword)

    print(f"[main] 완료: {url}")


if __name__ == "__main__":
    main()
