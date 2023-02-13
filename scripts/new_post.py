from pathlib import Path
import datetime
import json
from dataclasses import dataclass
import pytz
import readline

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
draft_dir = cwd.parent.parent / "draft"

today = datetime.datetime.now(tz=pytz.timezone("Asia/Tokyo"))

@dataclass
class DB:
    all_cat: list[str]
    all_tag: list[str]

    @staticmethod
    def load(path):
        with open(path, "r") as f:
            db = json.load(f)
        return DB(db["categories"], db["tags"])
    
    def save(self, path):
        with open(path, "w") as f:
            json.dump({
                "categories": self.all_cat,
                "tags": self.all_tag
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
    cat = input("(only one) cat:>").split()[0]

    print(": All Tags")
    for tag in db.all_tag:
        print(f"{tag}")
    tags = set(input("(multiple) tag:>").split())

    use_math = (input("are you use Tex ?:(y/n)>")[0] == 'y')
    return short_title, title, cat, tags, use_math

short_title, title, cat, tags, use_math = ask_parameter()

md = draft_dir / f"{today.year:04}-{today.month:02}-{today.day:02}-{short_title}.markdown"
content = f"""---
layout: post
title:  "{title}"
date:   {today.strftime(r"%Y-%m-%d %H:%M:%S %z")}
categories: {cat}
tags: [{", ".join(tags)}]
use_math: {"true" if use_math else "false"}
---
"""

if md.exists():
    print("***ERROR: MDFile is existed***")
else:
    md.write_text(content, encoding="utf-8")

    db.all_cat = list(set(db.all_cat) | {cat})
    db.all_tag = list(set(db.all_cat) | tags)
    db.save(db_path)
