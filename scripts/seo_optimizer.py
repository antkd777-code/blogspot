"""SEO / AEO / GEO 최적화 유틸리티"""
import re
from datetime import date


def build_schema_article(title: str, description: str, url: str, author: str) -> str:
    today = date.today().isoformat()
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{description}",
  "author": {{"@type": "Person", "name": "{author}"}},
  "datePublished": "{today}",
  "dateModified": "{today}",
  "url": "{url}",
  "publisher": {{
    "@type": "Organization",
    "name": "{author}"
  }}
}}
</script>"""


def build_faq_schema(faqs: list[dict]) -> str:
    """faqs: [{"question": ..., "answer": ...}, ...]"""
    items = ",\n".join(
        f'{{"@type":"Question","name":"{q["question"]}","acceptedAnswer":{{"@type":"Answer","text":"{q["answer"]}"}}}}'
        for q in faqs
    )
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{items}]
}}
</script>"""


def build_og_tags(title: str, description: str, url: str, blog_name: str) -> str:
    return f"""<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{description}"/>
<meta property="og:url" content="{url}"/>
<meta property="og:type" content="article"/>
<meta property="og:site_name" content="{blog_name}"/>
<meta name="twitter:card" content="summary"/>
<meta name="twitter:title" content="{title}"/>
<meta name="twitter:description" content="{description}"/>"""


def wrap_post_html(
    keyword: str,
    title: str,
    meta_description: str,
    body_html: str,
    faqs: list[dict],
    blog_url: str,
    blog_name: str,
    author: str,
) -> str:
    """최종 포스트 HTML 조립 (Schema.org + OG 태그 포함)"""
    post_url = f"{blog_url}/search/label/{keyword.replace(' ', '+')}"

    schema_article = build_schema_article(title, meta_description, post_url, author)
    schema_faq = build_faq_schema(faqs) if faqs else ""
    og_tags = build_og_tags(title, meta_description, post_url, blog_name)

    return f"""{og_tags}
{schema_article}
{schema_faq}
{body_html}"""


def truncate(text: str, max_len: int) -> str:
    return text[:max_len].rsplit(" ", 1)[0] if len(text) > max_len else text


def slug_from_title(title: str) -> str:
    title = re.sub(r"[^\w\s-]", "", title, flags=re.UNICODE)
    return re.sub(r"\s+", "-", title.strip()).lower()
