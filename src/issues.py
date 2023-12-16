# 每期消息发布的时间

import json
import re
from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass
class Issue:
    comment: int
    play: int
    description: str
    title: str
    author: str
    mid: int
    created: int
    length: str
    video_review: int


ISSUES: list[Dict[str, Any]] = []

ISSUE_PATTERN = re.compile(r"【睡前消息\s?([\d.]+)】")


for page in range(1, 27):
    with open(f"./data/{page}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data["data"]["list"]["vlist"]:
        filtered_params = {
            k: v for k in Issue.__annotations__ if (v := item.get(k)) is not None
        }
        ISSUES.append(asdict(Issue(**filtered_params)))


BEDTIME_NEWS = [issue for issue in ISSUES if "【睡前消息" in issue["title"]]
for i, issue in enumerate(BEDTIME_NEWS[-11:], start=-11):
    issue["title"] = issue["title"].replace("【睡前消息】", f"【睡前消息{-i}】")

BEDTIME_NEWS.pop(498)

for issue in BEDTIME_NEWS:
    issue["issue"] = ISSUE_PATTERN.search(issue["title"]).group(1)

if __name__ == "__main__":
    with open("./issues.json", "w", encoding="utf-8") as f:
        json.dump(ISSUES, f, ensure_ascii=False, indent=2)

    with open("./bedtime_news.json", "w", encoding="utf-8") as f:
        json.dump(BEDTIME_NEWS, f, ensure_ascii=False, indent=2)
