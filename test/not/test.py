import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import FontDialog

def change_font():
    # 创建字体选择对话框
    font_dialog = FontDialog()
    font_dialog.show()

    # 获取用户选择的字体
    chosen_font = font_dialog.result

    # 应用选择的字体到标签
    label.config(font=chosen_font)

# 创建主窗口
root = tk.Tk()
root.title("Font Change Example")

# 设置 ttkbootstrap 样式
style = Style(theme="default")

# 创建一个标签用于显示文本
label = tk.Label(root, text="Hello, World!", font=("Arial", 12))
label.pack(pady=20)

# 创建一个按钮，点击时弹出字体选择对话框
change_font_btn = tk.Button(root, text="Change Font", command=change_font)
change_font_btn.pack(pady=10)

# 运行主循环
root.mainloop()
