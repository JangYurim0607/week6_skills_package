# week6_skills_package

Skill Creation 과제. 주제는 **로블록스 숏츠(유튜브 쇼츠, 틱톡) 제작용 키워드 분석 PDF + 스토리보드 PDF**다. 같은 과제를 스킬 없이(A) 한 번, 오픈소스 스킬 패키지를 적용해서(B) 한 번 수행하고 비교했다.

## 1. 과제

`data/roblox_games.csv`(RoWatcher 2026-06-10 스냅샷, 16개 게임)와 `data/game_notes.md`(출처 있는 조사 노트)로 **키워드 분석 리포트(PDF)** 와 **숏츠 스토리보드(PDF, 3편)** 를 만든다. 명세는 `data/task_spec.md`. 검색량 데이터는 구하지 못해서 키워드는 후보이고, 수요는 동접과 누적 방문수로 본 대리 지표다.

## 2. 결과물 (여기를 열면 된다)

| | 키워드 분석 | 스토리보드 |
|---|---|---|
| A (스킬 없음) | `A_baseline/output/keyword_analysis.pdf` | `A_baseline/output/storyboard.pdf` |
| B (스킬 적용) | `B_skills/output/keyword_analysis.pdf` | `B_skills/output/storyboard.pdf` |

B는 `B_skills/output/skill_usage_log.md`에 스킬별로 무엇이 달라졌고 무엇이 도움이 안 됐는지 적었다.

```
week6_skills_package/
├── data/                  공통 입력: roblox_games.csv, game_notes.md, task_spec.md
├── A_baseline/
│   ├── prompt.md          사용한 프롬프트
│   ├── code/              analysis.py, storyboard.py, common.py
│   └── output/            keyword_analysis.pdf, storyboard.pdf
├── B_skills/
│   ├── prompt.md          프롬프트(파이프라인 지시 포함)
│   ├── skills/            스킬 묶음 8개
│   ├── scripts/           분석, PDF 생성, ko_slopcheck.py, fact_check.py, run_all.sh
│   └── output/            keyword_analysis.pdf, storyboard.pdf, skill_usage_log.md, artifacts/
├── compare/COMPARISON.md  A/B 비교
└── THIRD_PARTY_NOTICES.md 스킬 출처와 라이선스
```

## 3. 스킬 패키지 (B_skills/skills)

| 단계 | 스킬 | 출처 |
|---|---|---|
| 키워드 분석 | `seo-keyword-research` | claude-seo-skill |
| 키워드 분석, 숏폼 기준 | `social` | marketingskills |
| 대본 구조 | `yt-script`, `yt-shorts` | youtube-agent-skill |
| 대본 구조 | `ai-video-storyboard` | ai-video-storyboard-skill |
| 슬롭 제거 | `anti-ai-slop` | anti-ai-slop |
| 슬롭 제거 | `humanizer` | blader/humanizer |
| 한국어 문체 | `roblox-shorts-ko` | **직접 제작** |

오픈소스 스킬은 7개이고 직접 만든 스킬이 1개다. 영어용 슬롭 제거 스킬이 한국어에서 잘 안 먹혀서 한국어 전용 스킬과 검사기를 따로 만들었다. 자세한 출처는 `THIRD_PARTY_NOTICES.md`.

## 4. 결과 요약

자세한 비교와 한계는 `compare/COMPARISON.md`.

- 둘 다 명세의 항목(요약, 한계, 차트, 표, 키워드 후보, 선정 근거, 샷 목록, 9:16 스케치, 내레이션, 자막, 촬영 가이드, 길이 추정)을 채웠다. A는 6쪽+7쪽, B는 6쪽+11쪽.
- B는 검색 의도 분류, 클러스터, 플랫폼 배치 근거, 첫 3초 훅 칸이 추가됐다.
- 영어 기반 도구(`slopcheck.py`, `hookscore.py`)는 한국어에서 쓸모가 없어서 한국어 전용 스킬과 검사기를 직접 만들었다.
- 한 번씩만 만든 결과이고 조회수 같은 실제 성과는 재지 않았다.

## 5. 다시 돌려 보기

```bash
# B: 분석 + PDF 생성 + 검사 (B_skills 안에서)
cd B_skills && bash scripts/run_all.sh
# A: 분석 + PDF 생성 (A_baseline 안에서)
cd A_baseline/code && python3 analysis.py && python3 storyboard.py
```

PDF 생성에는 Playwright(Chromium), matplotlib, 폰트 Noto Sans CJK JP가 필요하다.
