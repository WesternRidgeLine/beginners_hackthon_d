import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox

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

        # 保存ボタンを追加
        self.save_button = tk.Button(master, text="保存", command=self.save_file)
        self.save_button.pack(side=tk.BOTTOM, padx=5, pady=5)

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
            messagebox.showinfo("保存", "ファイルが保存されました。")

def main():
    """メイン関数"""
    root = tk.Tk()
    file_name = "Untitled"  # デフォルトのファイル名を設定する
    app = NotepadApp(root, file_name)
    root.mainloop()

if __name__ == "__main__":
    main()
