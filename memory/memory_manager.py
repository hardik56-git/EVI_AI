import json
import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class MemoryManager:
    def __init__(self):
        db_path = os.path.join(BASE_DIR, "memory", "short_term.db")
        self.short_term = sqlite3.connect(db_path)
        cursor = self.short_term.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT)')
        self.short_term.commit()
        self.lessons = self._load_json("lessons.json")
        self.skills = self._load_json("skills.json")
        
    def _load_json(self, filename):
        try:
            path = os.path.join(BASE_DIR, "memory", filename)
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {}
            
    def remember(self, key, value, long_term=False):
        if long_term:
            path = os.path.join(BASE_DIR, "memory", "experiences.json")
            with open(path, 'a') as f:
                json.dump({key: value, "timestamp": str(datetime.now())}, f)
        else:
            cursor = self.short_term.cursor()
            cursor.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))
            self.short_term.commit()
            
    def recall(self, key):
        cursor = self.short_term.cursor()
        cursor.execute("SELECT value FROM memory WHERE key = ?", (key,))
        result = cursor.fetchone()
        return result[0] if result else None