import tkinter as tk
<<<<<<< HEAD
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
import sqlite3
=======
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
>>>>>>> fe3020fca203073569c53039b663028314b3a2b6

class NotepadApp:
    """テキストエディタのアプリケーションクラス"""

    def __init__(self, master, file_name):
        """アプリケーションの初期化

        Args:
            master (tk.Tk): アプリケーションの親ウィンドウ
            file_name (str): ファイル名
        """
        self.master = master
        self.master.geometry("600x450")  # ウィンドウの高さを調整
        self.master.title(file_name)
        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill="both")
        self.create_menu()

<<<<<<< HEAD
        # タグを追加するエントリーボックスとボタンを作成
        self.tag_info_label = tk.Label(master, text="使用タグ:")
        self.tag_info_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.tag_entry = tk.Entry(master)
        self.tag_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_tag_button_create = tk.Button(master, text="タグ作成", command=self.create_tag)
        self.add_tag_button_create.pack(side=tk.LEFT, padx=5, pady=5)

        self.tag_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE, exportselection=0)
        self.tag_listbox.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_tag_button_add = tk.Button(master, text="タグ追加", command=self.add_tag)
        self.add_tag_button_add.pack(side=tk.LEFT,padx=10, pady=10)

=======
>>>>>>> fe3020fca203073569c53039b663028314b3a2b6
        # 保存ボタンを追加
        self.save_button = tk.Button(master, text="保存", command=self.save_file)
        self.save_button.pack(side=tk.BOTTOM, padx=5, pady=5)

<<<<<<< HEAD
        # SQLiteデータベースを開く
        self.conn = sqlite3.connect('notes.db')
        self.cursor = self.conn.cursor()

        # タグデータベースを開く
        self.tag_conn = sqlite3.connect('tags.db')
        self.tag_cursor = self.tag_conn.cursor()

        # タグコンボボックスを更新
        self.update_tag_listbox()

=======
>>>>>>> fe3020fca203073569c53039b663028314b3a2b6
    def create_menu(self):
        """メニューバーを作成"""
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="新規作成", command=self.new_file)
        filemenu.add_command(label="開く", command=self.open_file)
        filemenu.add_separator()
        filemenu.add_command(label="閉じる", command=self.master.quit)
        menubar.add_cascade(label="ファイル", menu=filemenu)
        self.master.config(menu=menubar)

    def new_file(self):
        """新規ファイルを作成"""
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        """ファイルを開く"""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, file.read())

    def save_file(self):
        """ファイルを保存"""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
<<<<<<< HEAD

        # SQLiteにも保存
            content = self.text_area.get(1.0, tk.END)
            self.cursor.execute("INSERT INTO notes (file_name, content) VALUES (?, ?)", (file_path, content))
        
        # 直近に挿入された行のIDを取得
            note_id = self.cursor.lastrowid
        
        # ファイルに関連付けられたタグIDを notes_tags テーブルに保存
            for tag in self.text_area.tag_names():
                tag_id = self.get_tag_id(tag)
                if tag_id:
                    self.cursor.execute("INSERT INTO notes_tags (note_id, tag_id) VALUES (?, ?)", (note_id, tag_id))

            self.conn.commit()
    
    def create_tag(self):
        """タグを作成"""
        tag = self.tag_entry.get()
        if tag:
            # タグを別のデータベースに保存
            self.save_tag_to_db(tag)
            # タグを表示
            self.tag_entry.delete(0, tk.END)
            self.update_tag_listbox()
        else:
            messagebox.showwarning("タグを作成", "タグを入力してください。")

    def add_tag(self):
        """テキストにタグを追加"""
        selected_tags = self.tag_listbox.curselection()
        if selected_tags:
            for index in selected_tags:
                tag = self.tag_listbox.get(index)
                current_tags = self.text_area.tag_names()
                self.text_area.tag_add(tag, "1.0", tk.END)
                self.update_tag_listbox()
            self.update_tag_info()
        else:
            messagebox.showwarning("タグを追加", "タグを選択してください。")

    def save_tag_to_db(self, tag):
        """タグを別のデータベースに保存"""
        self.tag_cursor.execute("INSERT INTO tags (tag) VALUES (?)", (tag,))
        self.tag_conn.commit()
    
    def update_tag_listbox(self):
        """リストボックスにタグのリストを更新"""
        self.tag_cursor.execute("CREATE TABLE IF NOT EXISTS tags (tag TEXT)")
        self.tag_cursor.execute("SELECT tag FROM tags")
        tags = [row[0] for row in self.tag_cursor.fetchall()]
        self.tag_listbox.delete(0, tk.END)
        for tag in tags:
            self.tag_listbox.insert(tk.END, tag)
    
    def update_tag_info(self):
        """タグ情報を更新"""
        current_tags = self.text_area.tag_names()
        tag_info_text = "\n".join(f"タグ: {tag}, ID: {self.get_tag_id(tag)}" for tag in current_tags if self.get_tag_id(tag) is not None)
        self.tag_info_label.config(text=tag_info_text)

    def get_tag_id(self, tag):
        """タグのIDを取得"""
        self.tag_cursor.execute("SELECT rowid FROM tags WHERE tag=?", (tag,))
        row = self.tag_cursor.fetchone()
        if row:
            return row[0]
        else:
            return None
=======
            messagebox.showinfo("保存", "ファイルが保存されました。")
>>>>>>> fe3020fca203073569c53039b663028314b3a2b6

def main():
    """メイン関数"""
    root = tk.Tk()
    file_name = "Untitled"  # デフォルトのファイル名を設定する
    app = NotepadApp(root, file_name)
    root.mainloop()

if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> fe3020fca203073569c53039b663028314b3a2b6
