import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox, simpledialog
import os

import tag_extract

class NotepadApp:
    """テキストエディタのアプリケーションクラス"""

    def __init__(self, master, file_name=None, root=None):
        """アプリケーションの初期化

        Args:
            master (tk.Tk): アプリケーションの親ウィンドウ
            file_name (str, optional): ファイル名。デフォルトはNone。
            root (tk.Tk, optional): 最初の画面の親ウィンドウ。デフォルトはNone。
        """
        self.master = master
        self.root = root  # 最初の画面の親ウィンドウを保持
        self.master.geometry("600x450")  # ウィンドウの高さを調整
        self.file_name = file_name if file_name else "Untitled"  # ファイル名の初期値を設定
        self.master.title(self.file_name)  # ウィンドウのタイトルをファイル名に設定

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill="both")
        self.create_menu()

        # 保存ボタンを追加
        self.save_button = tk.Button(master, text="保存", command=self.save_file)
        self.save_button.pack(side=tk.BOTTOM, padx=5, pady=5)

        # 『#タグ』が格納されたlist
        self.hash_tag_list = ["#Python", "#GUI", "#Tkinter", "#Programming"]

        # 保存先ディレクトリ
        self.save_directory = "memo_directory"

        # 保存先ディレクトリが存在しない場合は作成
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

    def create_menu(self):
        """メニューバーを作成"""
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="新規作成", command=self.new_file)
        filemenu.add_command(label="開く", command=self.open_file)
        filemenu.add_separator()
        filemenu.add_command(label="閉じる", command=self.close_notepad)
        menubar.add_cascade(label="ファイル", menu=filemenu)
        self.master.config(menu=menubar)

    def new_file(self):
        """新規ファイルを作成"""
        # ウィンドウを閉じて最初の画面に戻る
        self.close_notepad()

    def open_file(self):
        """ファイルを開く"""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, file.read())
            self.file_name = os.path.basename(file_path)  # ファイル名を更新
            self.master.title(self.file_name)  # ウィンドウのタイトルを更新

    def save_file(self):
        """ファイルを保存"""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")],
                                                initialdir=self.save_directory)
        if file_path:
            # テキストエリアの内容を取得してmemo_text_contentに格納
            memo_text_content = self.text_area.get(1.0, tk.END)
            print(memo_text_content)
            tag = tag_extract.extract_tag_chatgpt(memo_text_content, []) #生成したタグを持ってくる,既存のタグを入れたい
            # ポップアップで複数のタグを指定
            selected_tags = self.choose_tags()
            if selected_tags is None:
                return  # キャンセルされた場合は保存を中止
            with open(file_path, "w") as file:
                # テキストエリアの内容をファイルに書き込む
                file.write(memo_text_content)
            self.file_name = os.path.basename(file_path)  # ファイル名を更新
            self.master.title(self.file_name)  # ウィンドウのタイトルを更新
            messagebox.showinfo("保存", "ファイルが保存されました。\n指定されたタグ: {}".format(selected_tags))


    def choose_tags(self):
        """複数のタグを選択"""
        # 空の文字列で初期化
        selected_tags = ""
        # タグのリストをスペースで区切って入力させる
        selected_tags = simpledialog.askstring("タグ選択", "保存するタグを選択してください（スペースで区切って入力）:", parent=self.master)
        # 入力があるかどうかをチェックし、なければNoneを返す
        if selected_tags:
            return selected_tags
        else:
            return None

    def close_notepad(self):
        """メモ画面を閉じる"""
        # self.master.destroy()
        self.master.deiconify()
        #self.root.deiconify()  # 最初の画面を表示

def main():
    """メイン関数"""
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
