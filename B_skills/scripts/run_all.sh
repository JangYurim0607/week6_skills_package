#!/usr/bin/env bash
# B_skills 파이프라인 재현. 작업 디렉터리: week6_skills_package/B_skills
set -e
D=../data; A=output/artifacts
python3 scripts/keyword_analysis.py --csv $D/roblox_games.csv --notes $D/game_notes.md --out $A/keyword_run
python3 scripts/build_keyword_pdf.py
python3 scripts/build_storyboard_pdf.py          # script_final.md 도 같이 만든다
S=$A/slop
python3 scripts/ko_slopcheck.py $S/script_final.md
python3 scripts/fact_check.py $S/script_final.md $D/game_notes.md $D/roblox_games.csv
python3 skills/anti-ai-slop/scripts/slopcheck.py $S/script_final_sanitized.md
for f in ep1_brookhaven ep2_adoptme ep3_99nights; do
  python3 skills/yt-script/hookscore.py $A/hooks/${f}_ko.txt > $A/hooks/${f}_ko_hookscore.txt
  python3 skills/yt-script/hookscore.py $A/hooks/${f}_en_gloss.txt > $A/hooks/${f}_en_gloss_hookscore.txt
done
