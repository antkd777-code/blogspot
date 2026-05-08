# Blogspot 애드센스 자동 발행 시스템

Claude API + Blogger API v3 + GitHub Actions 기반의 자동 블로그 포스팅 시스템입니다.

## 파일 구조

```
├── .github/workflows/auto-post.yml   # 하루 2회 자동 실행
├── scripts/
│   ├── main.py                        # 진입점
│   ├── generate_post.py               # Claude API 글 생성
│   ├── publish_post.py                # Blogger API 발행
│   ├── keyword_manager.py             # CSV 키워드 관리
│   ├── auth.py                        # OAuth2 인증
│   └── seo_optimizer.py               # SEO/AEO/GEO 최적화
├── keywords/keywords.csv              # 키워드 목록 (30개 기본 제공)
├── templates/
│   ├── privacy_policy.html            # 개인정보처리방침 템플릿
│   └── about.html                     # 소개 페이지 템플릿
├── config.py                          # 설정 (환경변수 로드)
├── setup_pages.py                     # 1회성: 정적 페이지 발행
├── get_refresh_token.py               # 1회성: Google 리프레시 토큰 발급
└── requirements.txt
```

## 셋업 순서

### 1단계: Google Cloud Console 설정

1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 새 프로젝트 생성 (또는 기존 프로젝트 선택)
3. **API 및 서비스 → 라이브러리** → `Blogger API v3` 검색 후 **사용 설정**
4. **API 및 서비스 → 사용자 인증 정보 → 사용자 인증 정보 만들기 → OAuth 클라이언트 ID**
   - 애플리케이션 유형: **데스크톱 앱**
   - 이름: 임의 입력
5. 생성된 **클라이언트 ID**와 **클라이언트 보안 비밀**을 복사

### 2단계: Blogger 블로그 ID 확인

Blogger 관리 페이지 URL에서 확인:
`https://www.blogger.com/blog/posts/XXXXXXXXXX` → `XXXXXXXXXX`가 Blog ID

### 3단계: Google 리프레시 토큰 발급 (로컬 1회)

```bash
pip install -r requirements.txt
export GOOGLE_CLIENT_ID=your_client_id
export GOOGLE_CLIENT_SECRET=your_client_secret
python get_refresh_token.py
```

브라우저 인증 후 터미널에 출력된 `GOOGLE_REFRESH_TOKEN` 값을 복사합니다.

### 4단계: GitHub Secrets 등록

GitHub 레포 → Settings → Secrets and variables → Actions → **New repository secret**

| Secret 이름            | 값                        |
|------------------------|---------------------------|
| `ANTHROPIC_API_KEY`    | Anthropic API 키           |
| `GOOGLE_CLIENT_ID`     | OAuth 클라이언트 ID         |
| `GOOGLE_CLIENT_SECRET` | OAuth 클라이언트 보안 비밀  |
| `GOOGLE_REFRESH_TOKEN` | 3단계에서 발급한 토큰       |
| `BLOGGER_BLOG_ID`      | 블로그 ID (숫자)            |

### 5단계: config.py 수정

```python
BLOG_NAME   = "내 블로그 이름"
BLOG_URL    = "https://my-blog.blogspot.com"
BLOG_AUTHOR = "홍길동"
```

### 6단계: 개인정보처리방침·소개 페이지 발행 (로컬 1회)

```bash
export ANTHROPIC_API_KEY=...
export GOOGLE_CLIENT_ID=...
export GOOGLE_CLIENT_SECRET=...
export GOOGLE_REFRESH_TOKEN=...
export BLOGGER_BLOG_ID=...
python setup_pages.py
```

### 7단계: 키워드 추가

`keywords/keywords.csv`에 원하는 키워드를 추가하세요:

```csv
keyword,category,used,used_date
알고 싶은 주제,카테고리,false,
```

---

## 자동 실행 시간

| 트리거 | 한국 시간 | UTC |
|--------|----------|-----|
| 1회차  | 오전 08:00 | 23:00 (전날) |
| 2회차  | 오후 08:00 | 11:00 |

워크플로우 탭에서 **Run workflow** 버튼으로 수동 실행도 가능합니다.

## 애드센스 승인 체크리스트

- [ ] 개인정보처리방침 페이지 발행 완료
- [ ] 소개(About) 페이지 발행 완료
- [ ] 포스트 10개 이상 발행
- [ ] 각 포스트 1500자 이상
- [ ] 광고·제휴 링크 없음
- [ ] Blogger 기본 네비게이션에 페이지 링크 추가
- [ ] 구글 서치콘솔 sitemap 등록
