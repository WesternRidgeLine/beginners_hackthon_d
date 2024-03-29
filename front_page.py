import tkinter as tk
from search import SearchApp
from index import NotepadApp

class FrontPage(tk.Tk):
    """メモ帳アプリケーションのフロントページ"""

    def __init__(self):
        """アプリケーションの初期化"""
        super().__init__()
        self.title("ズボラメモ")
        self.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        """ウィジェットの作成"""
        self.new_note_button = tk.Button(self, text="新規メモ", command=self.open_notepad)
        self.new_note_button.pack(pady=10)

        self.search_button = tk.Button(self, text="検索", command=self.open_search)
        self.search_button.pack(pady=10)

        # 新規メモのフレーム
        self.notepad_window = tk.Frame(self)
        self.notepad_app = None  # 検索アプリケーションのインスタンスを格納する変数

        # 検索画面のフレーム
        self.search_frame = tk.Frame(self)
        self.search_app = None  # 検索アプリケーションのインスタンスを格納する変数

    def open_notepad(self):
        """メモ帳を開く"""
        # もしも、すでにメモ帳を開いていたら、メモ帳を非表示にする。
        if hasattr(self, 'search_frame'):
            self.hide_search_frame()
        #　もしも、すでに新規メモ画面が開いていたら、検索画面を非表示にする。
        if self.notepad_app:
            self.hide_notepad_frame()
            self.geometry("300x200")
            self.notepad_app = None
        else:
            self.show_notepad_frame()

    def open_search(self):
        """検索画面を開く"""
        # もしも、すでにメモ帳を開いていたら、メモ帳を非表示にする。
        if hasattr(self, 'notepad_window'):
            self.hide_notepad_frame()
        #　もしも、すでに検索画面が開いていたら、検索画面を非表示にする。
        if self.search_app:
            self.hide_search_frame()
            self.geometry("300x200")
            self.search_app = None
        else:
            self.show_search_frame()

    def show_search_frame(self):
        """検索画面を表示する"""
        self.search_frame.destroy()  # 既存のフレームを破棄して新しいフレームを作成
        self.search_frame = tk.Frame(self)
        self.search_app = SearchApp(self.search_frame)
        self.geometry("400x400")
        self.search_frame.pack()

    def hide_search_frame(self):
        """検索画面を非表示にする"""
        if hasattr(self, 'search_frame'):
            self.search_frame.destroy()

    def show_notepad_frame(self):
        """検索画面を表示する"""
        self.notepad_window.destroy()  # 既存のフレームを破棄して新しいフレームを作成
        self.notepad_window = tk.Frame(self)
        self.notepad_app = NotepadApp(self.notepad_window, root=self)
        self.geometry("400x400")
        self.notepad_window.pack()

    def hide_notepad_frame(self):
        """検索画面を非表示にする"""
        if hasattr(self, 'notepad_window'):
            self.notepad_window.destroy()

def main():
    """メイン関数"""
    app = FrontPage()
    app.mainloop()

if __name__ == "__main__":
    main()
