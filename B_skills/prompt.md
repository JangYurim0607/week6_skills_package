# B 프롬프트 (스킬 패키지 적용)

A와 같은 과제를 하되, `skills/` 폴더의 스킬 패키지를 써서 한다. `data/task_spec.md`의 명세는 A와 똑같다.

- 입력: `data/roblox_games.csv`, `data/game_notes.md`
- 결과물: `output/keyword_analysis.pdf`, `output/storyboard.pdf`
- 분석·PDF 생성 코드는 `scripts/`에 둔다. 기존 `scripts/keyword_analysis.py`는 확장해도 된다. 스킬 파일(`skills/`)은 수정하지 않는다.

## 파이프라인 (각 단계 전에 해당 SKILL.md와 참조 파일을 읽고 따른다)

1. **키워드 분석**: `skills/seo-keyword-research`(시드 확장, 검색 의도 분류, 클러스터링, 우선순위)와 `skills/social`(+`references/short-form-video.md`, `platforms.md`: 플랫폼별 숏폼 기준)을 따른다. 계산은 스크립트로 한다.
2. **편 기획**: `skills/yt-script`(훅 5개를 쓰고 `hookscore.py`로 채점해 비교), `skills/yt-shorts`를 따른다.
3. **스토리보드**: `skills/ai-video-storyboard`의 샷 구조(훅, 전개, 결과, CTA)와 샷 목록 형식을 따른다. 이 스킬은 AI 영상 생성용 영어 프롬프트를 쓰라고 하지만, 이번에는 플레이 화면을 녹화하는 숏츠라서 생성 프롬프트 부분은 "촬영 장면 설명"으로 바꿔 적용한다.
4. **한국어 문체**: `skills/roblox-shorts-ko`의 톤과 금지 패턴을 따르고, 내레이션과 자막에 `scripts/ko_slopcheck.py`를 돌려 고친다.
5. **슬롭 제거**: `skills/anti-ai-slop`과 `skills/humanizer`의 원칙을 적용하고, 가능한 검사 스크립트를 실행한다. 영어 전용이라 한국어에 쓸모없으면 그렇다고 기록한다.
6. **기록**: `output/skill_usage_log.md`에 스킬마다 "그 스킬 때문에 결과물에서 구체적으로 달라진 것"과 "도움이 안 된 것"을 솔직하게 적는다. 스크립트 실행 결과 원본은 `output/artifacts/`에 저장한다.
