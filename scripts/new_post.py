from pathlib import Path
import datetime
import json
from dataclasses import dataclass
import pytz

def is_int(s):
    try:
        _ = int(s)
    except ValueError:
        return False
    return True

def try_int(s):
    if is_int(s):
        return int(s)
    else:
        return None

cwd = Path(__file__).absolute()

post_dir = cwd.parent.parent / "_posts"
draft_dir = cwd.parent.parent / "_draft"

today = datetime.datetime.now(tz=pytz.timezone("Asia/Tokyo"))

@dataclass
class DB:
    all_cat: list[str]

    @staticmethod
    def load(path):
        with open(path, "r") as f:
            db = json.load(f)
        return DB(db["categories"])
    
    def save(self, path):
        with open(path, "w") as f:
            json.dump({
                "categories": self.all_cat
            }, f)
        
db_path = cwd.parent / "db.json"
db = DB.load(db_path)

def ask_parameter():
    print("# Create Post")
    print(f": {today}")
    short_title = input(f"short_title:> ")
    title = input(f"title:> ")
    print(": All Categories")
    for cat in db.all_cat:
        print(f"{cat}")
    cats = set(input("cat:>").split())
    return short_title, title, cats

short_title, title, cats = ask_parameter()

md = draft_dir / f"{today.year}-{today.month:2d}-{today.day:2d}-{short_title}.markdown"
content = f"""---
layout: post
title:  "{title}"
date:   {today.strftime(r"%Y-%m-%d %H:%M:%S %z")}
categories: {" ".join(cats)}
---
"""

if md.exists():
    print("***ERROR: MDFile is existed***")
else:
    md.write_text(content, encoding="utf-8")
    db.all_cat = list(set(db.all_cat) + cats)
    db.save(db_path)
