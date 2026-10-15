# 로블록스 숏츠 키워드 분석

데이터: `data/roblox_games.csv` (RoWatcher 2026-06-10 스냅샷, 16개 게임). 계산: `scripts/keyword_analysis.py`. 원본 출력은 `output/artifacts/`의 `keywords.csv`, `cluster_summary.md`, `top_picks.json`에 있습니다.

## 0. 먼저 알아둘 한계

- 검색량, 키워드 난이도(KD), CPC, 경쟁 채널 데이터가 없습니다. `seo-keyword-research` 스킬의 우선순위 공식(검색량 x CTR x 사업 가치 / 난이도)은 입력이 없어서 계산하지 않았습니다. 값을 지어내지 않았습니다.
- 대신 쓴 것은 "수요 점수"입니다. 동시 접속자(60%)와 누적 방문수(40%)를 로그 스케일로 섞은 0~100 점수입니다. 게임이 얼마나 많이 플레이되는지를 보여 주는 값이고, 그 게임에 대한 영상 검색이 얼마나 되는지는 알려 주지 않습니다.
- 키워드 128개는 "게임 이름 x 수식어 8개" 템플릿으로 만든 후보입니다. 실제로 검색되는 표현인지 확인하지 않았습니다.
- 스냅샷이 2026-06-10 기준입니다. 오늘(2026-10-15)과 4개월 차이가 나서 순위는 이미 달라졌을 수 있습니다. 대본에 "6월 10일 기준"을 넣은 이유입니다.
- 누적 방문수가 빈 게임이 7개, 동접이 빈 게임이 1개(Grow a Garden)입니다. 점수는 있는 값만으로 계산해서 값이 있는 게임과 완전히 같은 기준이 아닙니다.

## 1. 시드와 키워드 풀 (seo-keyword-research 1단계)

시드는 CSV의 게임 16개입니다. 스킬이 말하는 시드 출처 중 오프라인에서 쓸 수 있는 것은 "수식어 확장"뿐이었습니다. 자동완성 수집, People Also Ask, 포럼 조사는 이 환경에서 할 수 없어서 하지 않았습니다.

수식어 8개를 모두 붙여 키워드 후보 128개가 나왔습니다.

| 의도 | 개수 | 수식어 | 숏츠 앵글 |
|---|---|---|---|
| informational | 48 | 꿀팁, 공략, 모르면 손해 | 30초 꿀팁, 막히는 구간 해결, 흔한 실수 3개 |
| commercial | 32 | 아이템 순위, vs | 아이템 티어 정리, 두 선택지 비교 |
| entertainment | 32 | 신기록, 버그 | 기록 도전, 웃긴 버그 모음 |
| news | 16 | 업데이트 | 신규 업데이트 요약 |

의도 분류에서 빠진 것과 어색한 것이 있습니다.

- 스킬의 4분류 중 navigational(게임 이름만 검색)이 템플릿에 없습니다. 게임 이름 자체가 가장 흔한 검색일 가능성이 큰데 이 파일에서는 측정도 못 했습니다.
- "아이템 순위"와 "vs"를 commercial로 분류했지만 로블록스 숏츠에서 구매 의도가 있는지는 알 수 없습니다. 스킬은 의도를 SERP로 확인하라고 하는데 그 확인을 못 했습니다. 템플릿 라벨이라고 보는 편이 맞습니다.
- 한국 시청자가 게임 이름을 한글 표기로 검색할 수 있습니다. 템플릿은 영문 이름만 씁니다. 한글 표기 후보는 유튜브 자동완성으로 확인해서 추가해야 합니다.

## 2. 게임별 수요 점수

수요 점수 순서입니다. rank는 CSV의 동접 순위입니다.

| 동접 순위 | 게임 | 장르 | 동접 | 누적 방문(십억) | 클러스터 | 수요 점수 |
|---|---|---|---|---|---|---|
| 1 | Brookhaven RP | Roleplay | 497,000 | 83.4 | social_rp | 99.0 |
| 3 | +1 Speed Keyboard Escape (Candy & Chocolate) | Fast-cycle obby | 307,000 | 없음 | obby | 87.5 |
| 2 | Adopt Me! | Pet-trading | 324,000 | 43.8 | grind_collect | 84.7 |
| 6 | Blox Fruits | Anime grind RPG | 218,000 | 62.0 | combat | 82.8 |
| 9 | Steal a Brainrot | Meme/Steal-game | 151,000 | 69.8 | grind_collect | 78.6 |
| 4 | 99 Nights in the Forest | Survival/Horror | 285,000 | 27.2 | horror_survival | 77.1 |
| 8 | Jujutsu Shenanigans | Anime action-combat | 178,000 | 없음 | combat | 73.6 |
| 16 | Grow a Garden | Simulator | 없음 | 35.5 | grind_collect | 72.2 |
| 7 | Murder Mystery 2 | Social deduction | 199,000 | 26.2 | social_rp | 71.1 |
| 10 | Fish It! | Fishing simulator | 143,000 | 없음 | grind_collect | 68.0 |
| 5 | RIVALS | Competitive shooter | 222,000 | 15.6 | combat | 66.6 |
| 11 | Sell Lemons | Idle/tycoon | 135,000 | 없음 | grind_collect | 66.5 |
| 12 | Kick a Lucky Block | RNG clicker | 107,000 | 없음 | grind_collect | 60.6 |
| 14 | Pet Simulator 99 | Simulator | 78,000 | 없음 | grind_collect | 52.5 |
| 15 | Catalog Avatar Creator | Avatar sandbox | 76,000 | 없음 | fashion_avatar | 51.8 |
| 13 | Dress To Impress | Fashion competition | 79,000 | 10.3 | fashion_avatar | 45.8 |

점수 구성에서 눈에 띄는 점이 두 가지 있습니다.

- 방문수 비중이 40%라서 오래된 게임이 유리합니다. RIVALS는 동접이 22만 2천으로 5위지만 방문수가 156억이라 점수 66.6으로 Murder Mystery 2(동접 19만 9천, 점수 71.1)보다 낮습니다. 숏츠는 지금 뜨는 게임이 중요할 수 있어서 이 가중치는 한 번 의심해 볼 만합니다.
- 반대로 동접만으로 줄 세워도 클러스터별 1위(Brookhaven RP, Adopt Me!, +1 Speed Keyboard Escape)는 같습니다. 그래서 선정 결과는 가중치에 크게 흔들리지 않습니다. 이 비교는 스크립트가 아니라 표를 보고 직접 확인했습니다.

## 3. 클러스터

`cluster_summary.md`의 장르 클러스터 6개입니다. 평균 수요 점수 순서입니다.

| 클러스터 | 게임 수 | 평균 점수 | 게임 |
|---|---|---|---|
| obby | 1 | 87.5 | +1 Speed Keyboard Escape |
| social_rp | 2 | 85.0 | Brookhaven RP, Murder Mystery 2 |
| horror_survival | 1 | 77.1 | 99 Nights in the Forest |
| combat | 3 | 74.3 | Blox Fruits, Jujutsu Shenanigans, RIVALS |
| grind_collect | 7 | 69.0 | Adopt Me!, Steal a Brainrot, Grow a Garden, Fish It!, Sell Lemons, Kick a Lucky Block, Pet Simulator 99 |
| fashion_avatar | 2 | 48.8 | Catalog Avatar Creator, Dress To Impress |

클러스터는 장르 문자열에 들어 있는 단어로 나눈 것이라 거칩니다. grind_collect에 7개가 몰려 있어 펫 거래, 낚시, 방치형이 한 묶음이 됩니다. Blox Fruits(Anime grind RPG)는 장르 문자열의 "anime"와 "rpg" 단어에 걸려 combat으로 들어갔습니다. 스킬이 말하는 필러-클러스터 구조(핵심 페이지 아래 하위 주제)로 쓰려면 사람이 한 번 다시 묶어야 합니다.

## 4. 대본 3편 선정

`top_picks.json`은 점수 순으로 보되 클러스터당 1개만 뽑습니다. 장르가 겹치는 대본 3개를 피하려는 규칙입니다.

| 대본 | 게임 | 클러스터 | 점수 | 대표 키워드(후보) | 앵글 |
|---|---|---|---|---|---|
| 1 | Brookhaven RP | social_rp | 99.0 | 로블록스 Brookhaven RP 꿀팁 | 숫자로 시작하는 정보형 |
| 2 | +1 Speed Keyboard Escape (Candy & Chocolate) | obby | 87.5 | 로블록스 +1 Speed Keyboard Escape (Candy & Chocolate) 신기록 | 5분 기록 도전 |
| 3 | Adopt Me! | grind_collect | 84.7 | 로블록스 Adopt Me! 공략 | 처음 해보는 사람의 거래 체험 |

이 규칙 때문에 빠진 게임이 있습니다. 99 Nights in the Forest는 동접 4위(28만 5천)인데 점수가 77.1로 Adopt Me!보다 낮아서 horror_survival 대표 자리를 못 얻었습니다. RIVALS(동접 5위)도 combat 안에서 Blox Fruits에 밀렸습니다. 두 게임은 다음 편 후보입니다.

+1 Speed Keyboard Escape는 누적 방문수가 CSV에 없어서 점수가 동접 하나로만 계산됐습니다. 그래서 대본 2에는 방문수를 쓰지 않았습니다.

## 5. 숏폼 기준 (social 스킬과 short-form-video 참고)

대본에 실제로 반영한 항목만 적습니다.

- 길이: 과제는 25~40초입니다. 스킬의 권장은 틱톡 15~60초, 쇼츠 30~60초라서 쇼츠 하한 30초를 넘기도록 28~34초로 잡았습니다.
- 3초 규칙: 첫 비트에 화면, 대사, 자막이 동시에 나오게 했습니다. 모든 훅 비트에 `[화면: ... / 자막: ...]`가 있습니다.
- 자막: 화면에 최대 2줄, 한 줄 3~5단어 기준. 한국어는 단어 수로 재기 어려워서 자막을 짧은 명사구로 썼습니다(예: "방문수 834억", "2위, 6/10 집계").
- 구조: 문제-해결(Problem-Solution)이나 튜토리얼 틀을 6비트로 나눴습니다. 훅 / 전개 2 / 결과 2 / CTA 1입니다.
- CTA: 행동 하나만 요청합니다. 댓글 질문 2편, 팔로우 1편입니다.
- 쇼츠는 검색 가능한 제목이 중요하다고 스킬이 말합니다. 제목에는 위 대표 키워드를 그대로 넣을 수 있습니다. 다만 그 키워드가 실제로 검색되는지는 검증하지 못했습니다.
- 스킬의 훅 라이브러리와 일반 조언(올리는 시간대, 하루 업로드 횟수 등)은 한국 시장 데이터가 아니라서 가져오지 않았습니다.

## 6. 발행 순서와 다음 후보

1. Brookhaven RP (점수 99.0)
2. +1 Speed Keyboard Escape (87.5)
3. Adopt Me! (84.7)
4. 후보: Blox Fruits (82.8), 99 Nights in the Forest (77.1, 동접 4위), Steal a Brainrot (78.6), RIVALS (동접 5위)

순서는 점수 순입니다. 시즌, 업데이트 일정, 경쟁 영상 수는 데이터가 없어서 반영하지 못했습니다.

## 7. 키워드 맵

| 대본 | 주 키워드 | 보조 키워드(같은 게임) | 의도 |
|---|---|---|---|
| 1 | 로블록스 Brookhaven RP 꿀팁 | 공략, 모르면 손해 | informational |
| 2 | 로블록스 +1 Speed Keyboard Escape (Candy & Chocolate) 신기록 | 버그, 꿀팁 | entertainment |
| 3 | 로블록스 Adopt Me! 공략 | 꿀팁, vs | informational |

경쟁 격차 분석(competitor gap)과 퀵윈(기존 순위에서 발견되는 기회)은 채널 데이터와 검색 데이터가 없어서 작성하지 않았습니다.

## 8. 다음에 필요한 데이터

- 유튜브와 틱톡 자동완성에서 확인한 실제 검색어(한글 표기 포함)
- 후보 키워드별 상위 쇼츠의 조회수와 업로드 날짜
- 최신 스냅샷. 6월 10일 값은 이미 4개월 지났습니다.
