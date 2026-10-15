# week6_skills_package

Skill Creation 과제. 주제는 **로블록스 숏츠(유튜브 쇼츠, 틱톡)용 키워드 분석 + 한국어 대본 작성**이다. 같은 과제를 스킬 없이(A) 한 번, 오픈소스 스킬 패키지를 적용해서(B) 한 번 수행하고 비교했다.

## 1. 과제

`data/roblox_games.csv`(RoWatcher 2026-06-10 스냅샷, 16개 게임)로 숏츠 키워드를 분석하고, 게임 3개를 골라 25~40초 한국어 대본을 1편씩 쓴다. 검색량 데이터는 구하지 못해서, 키워드는 후보이고 수요는 동시 접속자와 누적 방문수로 본 대리 지표다.

## 2. 폴더 구조

```
week6_skills_package/
├── data/                      A와 B가 같이 쓰는 입력 (roblox_games.csv)
├── A_baseline/                스킬 없음
│   ├── prompt.md              사용한 프롬프트
│   ├── code/analyze.py        분석에 쓴 코드
│   └── output/                keyword_analysis.md, scripts_ko.md
├── B_skills/                  스킬 패키지 적용
│   ├── prompt.md              사용한 프롬프트(파이프라인 지시 포함)
│   ├── skills/                스킬 묶음 (8개)
│   ├── scripts/               keyword_analysis.py, ko_slopcheck.py
│   └── output/                keyword_analysis.md, scripts_ko.md, skill_usage_log.md, artifacts/
├── compare/                   A/B 비교(COMPARISON.md)와 채점 로그
└── THIRD_PARTY_NOTICES.md     스킬 출처와 라이선스
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

자세한 비교는 `compare/COMPARISON.md`, 스킬별 기여는 `B_skills/output/skill_usage_log.md`.

- B는 CSV에 없는 게임 내용을 지어내지 않았다. 대신 촬영 후에 채울 빈칸이 6개 남았다.
- 대사만 검사한 한국어 슬롭 점수는 A 8점, B 0점이다. B가 이 검사기의 금지 목록을 보고 썼기 때문에 B에 유리한 지표다.
- 영어 기반 도구(`slopcheck.py`, `hookscore.py`)는 한국어에서 쓸모가 없었다. 일부러 나쁘게 쓴 한국어 문단에 100점을 줬다.
- 한 번씩만 돌린 결과다. 조회수 같은 실제 성과는 재지 않았다.

## 5. 다시 돌려 보기

```bash
# B 분석
python3 B_skills/scripts/keyword_analysis.py --csv data/roblox_games.csv --out /tmp/kw
# 한국어 슬롭 검사
python3 B_skills/scripts/ko_slopcheck.py B_skills/output/scripts_ko.md
python3 B_skills/scripts/ko_slopcheck.py A_baseline/output/scripts_ko.md
# A 분석 (화면 출력 없이 A_baseline/output/keyword_analysis.md를 다시 만든다)
python3 A_baseline/code/analyze.py
```

Python 3 표준 라이브러리만 쓴다.
