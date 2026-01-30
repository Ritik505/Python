import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("SELECT id, fullname, email, username FROM users")
rows = cursor.fetchall()

print("\n========================= USERS TABLE =======================================\n")
print(f"{'ID':<5} {'Full Name':<20} {'Email':<30} {'Username':<15}")
print("-" * 75)

for row in rows:
    id, fullname, email, username = row
    print(f"{id:<5} {fullname:<20} {email:<30} {username:<15}")

print("\n=============================================================================\n")

conn.close()
