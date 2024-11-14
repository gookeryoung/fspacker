import tkinter as tk


def main():
    # 创建主窗口
    root = tk.Tk()
    root.title("输入框和文本框示例")

    # 创建标签
    label = tk.Label(root, text="请输入文本:")
    label.pack(pady=10)

    # 创建输入框
    entry = tk.Entry(root)
    entry.pack(pady=10)

    # 创建文本框
    text = tk.Text(root, height=10, width=40)
    text.pack(pady=10)

    # 创建按钮
    def on_button_click():
        input_text = entry.get()
        text.insert(tk.END, f"输入的文本: {input_text}\n")

    button = tk.Button(root, text="提交", command=on_button_click)
    button.pack(pady=10)

    # 进入主循环
    root.mainloop()
