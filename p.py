import sqlite3

# SQLite データベースに接続
conn = sqlite3.connect('notes.db')
cursor = conn.cursor()

# notes_tags テーブルからデータを取得
cursor.execute("SELECT * FROM notes_tags")
rows = cursor.fetchall()

# 取得したデータを表示
for row in rows:
    print(row)

# 接続を閉じる
conn.close()