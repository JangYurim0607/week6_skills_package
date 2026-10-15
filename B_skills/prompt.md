# B 프롬프트 (스킬 패키지 적용)

A와 같은 과제를 하되, `skills/` 폴더의 스킬 패키지를 쓴다.

과제: `../data/roblox_games.csv`로 로블록스 숏츠(유튜브 쇼츠, 틱톡)용 키워드를 분석하고, 게임 3개를 골라 한국어 숏츠 대본 1편씩(25~40초) 쓴다. 분석은 `output/keyword_analysis.md`, 대본은 `output/scripts_ko.md`에 저장한다.

## 파이프라인

1. **키워드 분석**: `skills/seo-keyword-research/SKILL.md`(시드 확장, 의도 분류, 클러스터링)와 `skills/social/SKILL.md`·`references/short-form-video.md`(플랫폼별 숏폼 기준)를 읽고 방법론을 따른다. 계산은 `scripts/keyword_analysis.py`로 한다.
2. **대본 구조**: `skills/yt-script/SKILL.md`(훅 5개 작성 후 `hookscore.py`로 채점, 상위 2개 유지), `skills/yt-shorts/SKILL.md`, `skills/ai-video-storyboard/SKILL.md`(훅·전개·결과·CTA 구조)를 따른다.
3. **한국어 문체**: `skills/roblox-shorts-ko/SKILL.md`의 톤과 금지 패턴을 따른다. 쓴 뒤 `scripts/ko_slopcheck.py`로 검사하고 고친다.
4. **슬롭 제거**: `skills/anti-ai-slop/SKILL.md`와 `skills/humanizer/SKILL.md`의 원칙(구체성, 리듬 변화, 근거 없는 주장 삭제)을 적용하고, 가능한 검사 스크립트(`skills/anti-ai-slop/scripts/`)를 실행해 결과를 남긴다.
5. 어떤 스킬이 어떤 단계에 기여했는지 `output/skill_usage_log.md`에 기록한다.
