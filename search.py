import tkinter as tk

class SearchApp(tk.Tk):
    """検索画面のアプリケーションクラス"""

    def __init__(self):
        """アプリケーションの初期化"""
        super().__init__()
        self.title("検索画面")
        self.geometry("400x200")

        self.create_widgets()

    def create_widgets(self):
        """ウィジェットの作成"""
        self.search_label = tk.Label(self, text="検索:")
        self.search_label.grid(row=0, column=0, padx=10, pady=10)

        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        self.search_button = tk.Button(self, text="検索", command=self.search)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    def search(self):
        """検索ボタンがクリックされたときの処理"""
        search_text = self.search_entry.get()
        # ここで検索の処理を実行する
        self.result_label.config(text=f"検索結果: {search_text}")

if __name__ == "__main__":
    app = SearchApp()
    app.mainloop()
