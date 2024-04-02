import psycopg2
import os
from telegram import Update

PG_DATABASE = os.environ["PG_DATABASE"]
PG_HOST = os.environ["PG_HOST"]
PG_PORT = os.environ["PG_PORT"]
PG_USER = os.environ["PG_USER"]
PG_PASSWORD = os.environ["PG_PASSWORD"]

print("[persistence] Connecting to database...")
db = psycopg2.connect(
  database=PG_DATABASE,
  host=PG_HOST,
  port=PG_PORT,
  user=PG_USER,
  password=PG_PASSWORD
)
cur = db.cursor()

sessions = {}

class Session:
  def __init__(self, chatid):
    self.chatid = str(chatid)

  def process(self, update: Update, **kwargs):
    return self.terminate(True, "What?")
    
  def save(self):
    cur.execute("INSERT INTO sessions (chatid, faculty, course, year, setting_faculty, setting_course, setting_year) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (chatid) DO UPDATE SET faculty = %s, course = %s, year = %s, setting_faculty = %s, setting_course = %s, setting_year = %s", (self.chatid, str(self.faculty), str(self.course), str(self.year), 1 if self.is_setting_faculty else 0, 1 if self.is_setting_course else 0, 1 if self.is_setting_year else 0, str(self.faculty), str(self.course), str(self.year), 1 if self.is_setting_faculty else 0, 1 if self.is_setting_course else 0, 1 if self.is_setting_year else 0))
    db.commit()

# print("[persistence] Dropping table (remove in production)...")
# cur.execute("DROP TABLE IF EXISTS sessions")

print("[persistence] Initializing database...")
cur.execute("CREATE TABLE IF NOT EXISTS sessions (chatid TEXT NOT NULL PRIMARY KEY)")
db.commit()

def retrieve_session(chatid):
  cur.execute("SELECT * FROM sessions WHERE chatid = %s", (str(chatid),))
  s = cur.fetchone()
  if not s:
    return None
  return Session(chatid)

def get_session(chatid):
  if chatid not in sessions:
    sessions[chatid] = retrieve_session(chatid)
  if not sessions[chatid]:
    sessions[chatid] = Session(chatid)
  return sessions[chatid]