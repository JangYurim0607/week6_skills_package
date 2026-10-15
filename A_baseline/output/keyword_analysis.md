# 로블록스 숏츠 키워드 분석

- 데이터: `data/roblox_games.csv` (16개 게임, 출처 rowatcher 2026-06-10 스냅샷)
- 주의: 이 CSV에는 **검색량 데이터가 없습니다**. 아래 키워드는 게임명·장르에서 뽑은 후보이며, 실제 검색량은 YouTube/TikTok/Google Trends에서 별도 확인이 필요합니다.
- 동접(live_players_approx)은 15개 게임에서만 제공되고, 누적 방문(lifetime_visits_b, 십억)은 9개 게임에서만 제공됩니다. 빈 값은 0이 아니라 "미확인"으로 처리했습니다.

## 1. 동접 상위 게임

| 순위 | 게임 | 장르 | 동접(근사) | 동접 비중 | 누적 방문(십억) |
|---|---|---|---|---|---|
| 1 | Brookhaven RP | Roleplay | 497,000 | 16.6% | 83.4 |
| 2 | Adopt Me! | Pet-trading | 324,000 | 10.8% | 43.8 |
| 3 | +1 Speed Keyboard Escape (Candy & Chocolate) | Fast-cycle obby | 307,000 | 10.2% | - |
| 4 | 99 Nights in the Forest | Survival/Horror | 285,000 | 9.5% | 27.2 |
| 5 | RIVALS | Competitive shooter | 222,000 | 7.4% | 15.6 |
| 6 | Blox Fruits | Anime grind RPG | 218,000 | 7.3% | 62.0 |
| 7 | Murder Mystery 2 | Social deduction | 199,000 | 6.6% | 26.2 |
| 8 | Jujutsu Shenanigans | Anime action-combat | 178,000 | 5.9% | - |
| 9 | Steal a Brainrot | Meme/Steal-game | 151,000 | 5.0% | 69.8 |
| 10 | Fish It! | Fishing simulator | 143,000 | 4.8% | - |
| 11 | Sell Lemons | Idle/tycoon | 135,000 | 4.5% | - |
| 12 | Kick a Lucky Block | RNG clicker | 107,000 | 3.6% | - |
| 13 | Dress To Impress | Fashion competition | 79,000 | 2.6% | 10.3 |
| 14 | Pet Simulator 99 | Simulator | 78,000 | 2.6% | - |
| 15 | Catalog Avatar Creator | Avatar sandbox | 76,000 | 2.5% | - |
| 16 | Grow a Garden | Simulator | - | - | 35.5 |

동접 합계(15개 게임): 2,999,000

## 2. 장르 묶음별 동접 비중 (직접 분류)

| 묶음 | 동접 합 | 비중 | 게임 |
|---|---|---|---|
| 롤플레이/소셜 | 497,000 | 16.6% | Brookhaven RP |
| 펫/수집 | 402,000 | 13.4% | Adopt Me!, Pet Simulator 99 |
| 애니 계열 | 396,000 | 13.2% | Blox Fruits, Jujutsu Shenanigans |
| 방치/시뮬/RNG | 385,000 | 12.8% | Fish It!, Sell Lemons, Kick a Lucky Block |
| 오비/탈출 | 307,000 | 10.2% | +1 Speed Keyboard Escape (Candy & Chocolate) |
| 공포/서바이벌 | 285,000 | 9.5% | 99 Nights in the Forest |
| 전투/PvP | 222,000 | 7.4% | RIVALS |
| 소셜 추리 | 199,000 | 6.6% | Murder Mystery 2 |
| 패션/아바타 | 155,000 | 5.2% | Dress To Impress, Catalog Avatar Creator |
| 밈/훔치기 | 151,000 | 5.0% | Steal a Brainrot |

## 3. 현재 열기 vs 누적 방문 (동접 / 누적 방문)

누적 방문 대비 동접이 높을수록 "지금 뜨는" 게임, 낮을수록 "오래된 대형" 게임으로 해석할 수 있습니다. (두 값이 모두 있는 게임만)

| 게임 | 동접 | 누적(십억) | 동접 per 십억 방문 |
|---|---|---|---|
| RIVALS | 222,000 | 15.6 | 14,231 |
| 99 Nights in the Forest | 285,000 | 27.2 | 10,478 |
| Dress To Impress | 79,000 | 10.3 | 7,670 |
| Murder Mystery 2 | 199,000 | 26.2 | 7,595 |
| Adopt Me! | 324,000 | 43.8 | 7,397 |
| Brookhaven RP | 497,000 | 83.4 | 5,959 |
| Blox Fruits | 218,000 | 62.0 | 3,516 |
| Steal a Brainrot | 151,000 | 69.8 | 2,163 |

- RIVALS, 99 Nights in the Forest가 가장 높아 누적 대비 현재 열기가 큼(비교적 신흥). Blox Fruits, Steal a Brainrot, Brookhaven은 낮아 누적 방문이 이미 크게 쌓인 게임. 단, 서비스 기간 정보가 CSV에 없어 "신작"이라 단정할 수는 없음.
- Steal a Brainrot은 누적 69.8B로 Blox Fruits(62.0B)보다 크면서 동접도 151,000 — 동접 per 방문 비율은 최저라 최근 열기보다 누적 규모가 두드러지는 게임.
- Grow a Garden은 동접이 없고 누적 35.5B만 있어 현재 열기는 판단 불가(이 데이터 한계).

## 4. 게임별 한국어 키워드 후보

| 게임 | 키워드 후보 |
|---|---|
| Brookhaven RP | 브룩헤이븐, 브룩헤이븐 비밀, 로블록스 롤플레이 |
| Adopt Me! | 입양하세요, 어답트미 펫, 어답트미 교환 |
| +1 Speed Keyboard Escape (Candy & Chocolate) | 스피드 키보드 탈출, 로블록스 오비, 탈출맵 |
| 99 Nights in the Forest | 숲속의 99일 밤, 99일 밤 공포, 로블록스 공포게임 |
| RIVALS | 라이벌즈, 로블록스 FPS, 로블록스 슈팅 |
| Blox Fruits | 블록스 피스, 블록스 피스 과일, 로블록스 애니 RPG |
| Murder Mystery 2 | 머더 미스터리 2, 마더미, 로블록스 마피아류 |
| Jujutsu Shenanigans | 주술회전 로블록스, 주술 셰너니건스, 로블록스 애니 격투 |
| Steal a Brainrot | 브레인롯 훔치기, 스틸 어 브레인롯, 브레인롯 밈 |
| Fish It! | 피시 잇, 로블록스 낚시, 낚시 시뮬레이터 |
| Sell Lemons | 레몬 팔기, 로블록스 방치형, 타이쿤 |
| Kick a Lucky Block | 럭키블록, 킥 어 럭키 블록, RNG 게임 |
| Dress To Impress | 드레스 투 임프레스, 로블록스 패션, 로블록스 코디 |
| Pet Simulator 99 | 펫 시뮬레이터 99, 펫 시뮬, 로블록스 펫 |
| Catalog Avatar Creator | 카탈로그 아바타 크리에이터, 로블록스 아바타 꾸미기, 로블록스 코디 |
| Grow a Garden | 그로우 어 가든, 정원 키우기, 로블록스 농사 |

공통 롱테일 후보(형식 키워드): `로블록스 {게임명} 꿀팁`, `로블록스 {게임명} 처음 하면`, `로블록스 {게임명} 모르면 손해`, `#로블록스 #roblox #shorts`

## 5. 대본용 3개 선정

| 게임 | 선정 이유 (데이터 근거) |
|---|---|
| Steal a Brainrot | 동접 151,000 + 누적 69.8B로 두 지표 모두 상위. 밈 장르라 숏츠 친화적일 것으로 추정(데이터로 검증된 것은 아님) |
| 99 Nights in the Forest | 동접 285,000(4위)인데 누적 27.2B 대비 동접 비율이 2위(RIVALS 다음)로 누적 대비 열기가 큼. 공포 장르는 숏츠 훅 만들기 쉬움 |
| Dress To Impress | 동접 79,000으로 상위권은 아니지만 누적 10.3B 대비 비율은 3위. 패션 장르 대표로 액션 위주 후보와 시청층이 달라 차별화됨(시청층 차이는 추정) |

## 6. 한계

- 검색량, 조회수, 경쟁 영상 수 데이터 없음 -> 키워드 "인기"는 게임 동접 기준 추정일 뿐입니다.
- 한국어 표기는 일반적으로 쓰이는 표기를 제가 붙인 후보라 실제 검색어와 다를 수 있습니다. 게시 전 확인하세요.
- 스냅샷이 2026-06-10 기준이라 시간이 지나면 순위가 달라질 수 있습니다.
