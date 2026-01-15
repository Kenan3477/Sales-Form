import sqlite3

conn = sqlite3.connect('asis_autonomous_research_fixed.db')
cursor = conn.cursor()

print("Research Findings Table Structure:")
cursor.execute('PRAGMA table_info(research_findings)')
for col in cursor.fetchall():
    print(f"  {col}")

print("\nActual Research Finding:")
cursor.execute('SELECT * FROM research_findings ORDER BY id DESC LIMIT 1')
finding = cursor.fetchone()
if finding:
    print(f"  Finding data: {finding}")
else:
    print("  No findings found")

print("\nResearch Sessions:")
cursor.execute('SELECT * FROM research_sessions ORDER BY id DESC LIMIT 1')
session = cursor.fetchone()
if session:
    print(f"  Latest session: {session}")

conn.close()
