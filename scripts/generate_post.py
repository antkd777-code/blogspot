"""Claude API로 SEO 최적화 블로그 포스트 생성"""
import json
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
- 구글 검색 스니펫에 최적화된 간결한 답변 단락을 글 도입부에 배치합니다(AEO).
- 출력은 반드시 아래 JSON 형식만 반환합니다."""

USER_PROMPT_TEMPLATE = """키워드: {keyword}
카테고리: {category}

다음 JSON 형식으로 블로그 포스트를 작성하세요:
{{
  "title": "클릭을 유도하는 SEO 제목 (55자 이내, 키워드 포함)",
  "meta_description": "검색 결과에 표시될 설명 (150자 이내, 키워드 포함)",
  "labels": ["태그1", "태그2", "태그3"],
  "body_html": "<h2>...</h2><p>...</p> 형식의 전체 HTML 본문",
  "faqs": [
    {{"question": "질문1", "answer": "답변1"}},
    {{"question": "질문2", "answer": "답변2"}},
    {{"question": "질문3", "answer": "답변3"}}
  ]
}}

body_html 작성 지침:
1. 첫 단락: 키워드에 대한 핵심 요약 (구글 스니펫 최적화)
2. H2 소제목 최소 4개
3. 번호 목록 또는 불릿 목록 최소 2개
4. 마지막 H2: "자주 묻는 질문 (FAQ)" — faqs 필드 내용과 동일하게 HTML로도 작성
5. 자연스러운 내부 링크 문구 포함 (실제 URL 없이 앵커 텍스트만)"""


def generate_post(keyword: str, category: str) -> dict:
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    message = client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(
                    keyword=keyword, category=category
                ),
            }
        ],
    )

    raw = message.content[0].text.strip()

    # JSON 블록 추출 (```json ... ``` 감싸는 경우 대비)
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    data = json.loads(raw)

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
