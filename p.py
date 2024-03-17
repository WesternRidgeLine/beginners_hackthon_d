import sqlite3

# SQLiteデータベースに接続
conn = sqlite3.connect('tags.db')
cursor = conn.cursor()

# テーブルの構造を調べるSQLクエリを実行
cursor.execute("PRAGMA table_info(tags)")
rows = cursor.fetchall()

# テーブルの列情報を表示
for row in rows:
    print(row)

# 接続を閉じる
conn.close()