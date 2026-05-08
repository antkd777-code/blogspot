"""Blogger API v3로 포스트 발행"""
from scripts.auth import get_blogger_service
import config


def publish_post(title: str, content: str, labels: list[str]) -> str:
    """포스트를 발행하고 URL을 반환한다."""
    service = get_blogger_service()

    body = {
        "title": title,
        "content": content,
        "labels": labels,
    }

    result = (
        service.posts()
        .insert(blogId=config.BLOGGER_BLOG_ID, body=body, isDraft=False)
        .execute()
    )

    post_url = result.get("url", "")
    post_id = result.get("id", "")
    print(f"[publish] 포스트 발행 완료 — id={post_id}, url={post_url}")
    return post_url


def publish_page(title: str, content: str) -> str:
    """정적 페이지(개인정보처리방침·소개)를 발행하고 URL을 반환한다."""
    service = get_blogger_service()

    body = {"title": title, "content": content}

    result = (
        service.pages()
        .insert(blogId=config.BLOGGER_BLOG_ID, body=body, isDraft=False)
        .execute()
    )

    page_url = result.get("url", "")
    print(f"[publish] 페이지 발행 완료 — title={title}, url={page_url}")
    return page_url
