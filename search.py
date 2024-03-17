import tkinter as tk

import sqlite3


class SearchApp:
    """検索画面のアプリケーションクラス"""

    def __init__(self, master):
        """アプリケーションの初期化"""
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.title_label = tk.Label(self.frame, text="検索画面")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.search_label = tk.Label(self.frame, text="検索:")
        self.search_label.grid(row=1, column=0, padx=10, pady=10)

        self.search_entry = tk.Entry(self.frame)
        self.search_entry.grid(row=1, column=1, padx=10, pady=10)

        self.search_button = tk.Button(self.frame, text="検索", command=self.search)
        self.search_button.grid(row=1, column=2, padx=10, pady=10)

        self.tag_search_button = tk.Button(self.frame, text="タグ検索", command=self.tag_search)
        self.tag_search_button.grid(row=1, column=3, padx=10, pady=10)

        self.result_label = tk.Label(self.frame, text="")
        self.result_label.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

        self.result_label = tk.Label(self.frame, text="")
        self.result_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.conn = sqlite3.connect('notes.db')
        self.cursor = self.conn.cursor()
        self.tag_conn = sqlite3.connect('tags.db')
        self.tag_cursor = self.tag_conn.cursor()
        self.notes_tags_conn = sqlite3.connect('notes_tags.db')
        self.notes_tags_cursor = self.notes_tags_conn.cursor()

    def search(self):
        """検索ボタンがクリックされたときの処理"""
        search_text = self.search_entry.get()
        self.cursor.execute("SELECT file_name FROM notes WHERE file_name LIKE ?", ('%' + search_text + '%',))
        rows = self.cursor.fetchall()
        files = [row[0] for row in rows]
        if files:
            files_text = "\n".join(files)
            self.result_label.config(text=f"検索結果:\n{files_text}")
        else:
            self.result_label.config(text="検索結果: ファイルが見つかりませんでした")
    def tag_search(self):
            """タグ検索ボタンがクリックされたときの処理"""
            search_text = self.search_entry.get()

            # タグDBから入力されたタグに一致するタグIDを取得
            self.tag_cursor.execute("SELECT tags_id FROM tags WHERE tag_name LIKE ?", ('%' + search_text + '%',))
            tag_rows = self.tag_cursor.fetchall()
            tag_ids = [str(row[0]) for row in tag_rows]

            # ファイル名を検索して一致するタグIDを持つレコードを取得
            files = []
            for tag_id in tag_ids:
                self.notes_tags_cursor.execute("SELECT file_name FROM notes_tags WHERE tag_id=?", (tag_id,))
                rows = self.notes_tags_cursor.fetchall()
                files += [row[0] for row in rows]

            if files:
                files_text = "\n".join(files)
                self.result_label.config(text=f"検索結果:\n{files_text}")
            else:
                self.result_label.config(text="検索結果: ファイルが見つかりませんでした")

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()
