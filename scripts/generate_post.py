"""Claude API로 SEO 최적화 블로그 포스트 생성"""
import anthropic
import config
from scripts.seo_optimizer import wrap_post_html, truncate


SYSTEM_PROMPT = """당신은 한국어 SEO 전문 블로그 작가입니다.

규칙:
- 독자에게 실질적으로 도움이 되는 정보성 글을 작성합니다.
- 광고, 쿠팡파트너스, 제휴 링크는 절대 포함하지 않습니다.
- 글 길이는 최소 1500자 이상(HTML 태그 제외 텍스트 기준).
- H2·H3 소제목으로 논리적 구조를 만듭니다.
- 핵심 정보는 <ul>/<ol> 목록으로 정리합니다.
- 마지막에 FAQ 섹션(3~5개 Q&A)을 추가합니다.
- 구글 검색 스니펫에 최적화된 간결한 답변 단락을 글 도입부에 배치합니다(AEO)."""

USER_PROMPT_TEMPLATE = """키워드: {keyword}
카테고리: {category}

위 키워드로 블로그 포스트를 작성하고 write_post 도구를 호출하세요.

body_html 작성 지침:
1. 첫 단락: 키워드에 대한 핵심 요약 (구글 스니펫 최적화)
2. H2 소제목 최소 4개
3. 번호 목록 또는 불릿 목록 최소 2개
4. 마지막 H2: "자주 묻는 질문 (FAQ)"
5. 자연스러운 내부 링크 문구 포함 (실제 URL 없이 앵커 텍스트만)"""

TOOL = {
    "name": "write_post",
    "description": "완성된 블로그 포스트 데이터를 저장합니다.",
    "input_schema": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "클릭을 유도하는 SEO 제목 (55자 이내, 키워드 포함)",
            },
            "meta_description": {
                "type": "string",
                "description": "검색 결과에 표시될 설명 (150자 이내, 키워드 포함)",
            },
            "labels": {
                "type": "array",
                "items": {"type": "string"},
                "description": "블로그 태그 3~5개",
            },
            "body_html": {
                "type": "string",
                "description": "전체 HTML 본문 (<h2>, <p>, <ul>, <ol> 태그 사용)",
            },
            "faqs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "answer": {"type": "string"},
                    },
                    "required": ["question", "answer"],
                },
                "description": "FAQ 3~5개",
            },
        },
        "required": ["title", "meta_description", "labels", "body_html", "faqs"],
    },
}


def generate_post(keyword: str, category: str) -> dict:
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    message = client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=8000,
        system=SYSTEM_PROMPT,
        tools=[TOOL],
        tool_choice={"type": "any"},
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(
                    keyword=keyword, category=category
                ),
            }
        ],
    )

    tool_block = next(b for b in message.content if b.type == "tool_use")
    data = tool_block.input

    title = truncate(data["title"], 55)
    meta_description = truncate(data["meta_description"], 150)
    faqs = data.get("faqs", [])

    final_html = wrap_post_html(
        keyword=keyword,
        title=title,
        meta_description=meta_description,
        body_html=data["body_html"],
        faqs=faqs,
        blog_url=config.BLOG_URL,
        blog_name=config.BLOG_NAME,
        author=config.BLOG_AUTHOR,
    )

    labels = list(set(data.get("labels", []) + config.POST_LABELS + [category]))

    return {
        "title": title,
        "content": final_html,
        "labels": labels,
        "meta_description": meta_description,
    }
