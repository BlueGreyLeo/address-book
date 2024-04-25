import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# 定义通讯录文件路径
LinkMan_FILE = 'LinkMan.csv'


# 创建通讯录文件（如果不存在）
def create_LinkMan_file():
    try:
        with open(LinkMan_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['姓名', '性别', '电话', '地址', '邮箱'])
    except IOError:
        messagebox.showerror("错误", f"无法创建通讯录文件: {LinkMan_FILE}")


# 添加联系人
def add_contact():
    name = name_entry.get()
    gender = gender_entry.get()
    phone = phone_entry.get()
    address = address_entry.get()
    email = email_entry.get()

    if not all([name, gender, phone, address, email]):
        messagebox.showwarning("警告", "请输入完整的联系人信息！")
    else:
        try:
            with open(LinkMan_FILE, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, gender, phone, address, email])
                messagebox.showinfo("成功", f"联系人 {name} 已成功添加！")
        except IOError:
            messagebox.showerror("错误", f"无法写入通讯录文件: {LinkMan_FILE}")


# 列出所有联系人
def list_LinkMan():
    try:
        with open(LinkMan_FILE, 'r') as file:
            reader = csv.reader(file)
            LinkMan = list(reader)

            window = tk.Toplevel()

            table = ttk.Treeview(window, columns=LinkMan[0], show='headings')
            for col in LinkMan[0]:
                table.heading(col, text=col)

            for row in LinkMan[1:]:
                table.insert('', 'end', values=row)

            table.pack()
    except IOError:
        messagebox.showerror("错误", f"无法读取通讯录文件: {LinkMan_FILE}")


# 查询联系人
def search_contact():
    name = name_entry.get()
    try:
        with open(LinkMan_FILE, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # 跳过标题行
            found = False
            for row in reader:
                if row[0] == name:
                    messagebox.showinfo("查询结果", f"姓名: {row[0]}\n性别: {row[1]}\n电话: {row[2]}\n地址: {row[3]}\n邮箱: {row[4]}")
                    found = True
                    break
            if not found:
                messagebox.showinfo("查询结果", f"联系人 {name} 未找到！")
    except IOError:
        messagebox.showerror("错误", f"无法读取通讯录文件: {LinkMan_FILE}")


# 删除联系人
def delete_contact():
    name = name_entry.get()
    try:
        with open(LinkMan_FILE, 'r') as file:
            reader = csv.reader(file)
            LinkMan = list(reader)

        with open(LinkMan_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            deleted = False
            for row in LinkMan:
                if row[0] == name:
                    deleted = True
                else:
                    writer.writerow(row)
            if deleted:
                messagebox.showinfo("成功", f"联系人 {name} 已成功删除！")
            else:
                messagebox.showinfo("结果", f"联系人 {name} 未找到！")
    except IOError:
        messagebox.showerror("错误", f"无法写入通讯录文件: {LinkMan_FILE}")


# 创建主窗口
window = tk.Tk()
window.title("通讯录管理程序")
window.config(background="#CCBBFF")

# 定义窗口的初始大小
window_width = 400
window_height = 300

# 计算放大比例
scale_factor = 2  # 放大比例为2倍

# 计算新的窗口大小
new_width = int(window_width * scale_factor)
new_height = int(window_height * scale_factor)

# 设置窗口大小
window.geometry(f"{new_width}x{new_height}")

# 定义自定义背景颜色
custom_bg_color = "#CCBBFF"

# 欢迎标签
Title_label = tk.Label(window, text="欢迎使用通讯录管理程序！", bg=custom_bg_color, font=("Arial", 14))
Title_label.pack(pady=(20, 10))

# 输入框布局
input_fields = [
    ("姓名：", "name"),
    ("性别：", "gender"),
    ("电话：", "phone"),
    ("地址：", "address"),
    ("邮箱：", "email")
]

for label_text, entry_name in input_fields:
    frame = tk.Frame(window, bg=custom_bg_color)
    frame.pack()

    label = tk.Label(frame, text=label_text, bg=custom_bg_color, width=8, font=("Arial", 12))
    label.pack(side=tk.LEFT)
    entry = ttk.Entry(frame, style="Custom.TEntry")  # 使用自定义样式
    entry.pack(side=tk.LEFT)

    globals()[f"{entry_name}_entry"] = entry


# 按钮布局
button_frame = tk.Frame(window, bg=custom_bg_color)
button_frame.pack(pady=(30, 0))

button_data = [
    ("增加联系人", add_contact),
    ("列出联系人", list_LinkMan),
    ("查询联系人", search_contact),
    ("删除联系人", delete_contact)
]

for button_text, button_command in button_data:
    button = ttk.Button(button_frame, text=button_text, command=button_command, style="Custom.TButton", width=15)
    button.pack(side=tk.LEFT, padx=10)


# 定义按钮样式
window.style = ttk.Style()
window.style.configure("Custom.TButton",
                        background=custom_bg_color,
                        foreground="black",
                        relief=tk.SOLID,
                        font=("Arial", 12),
                        padding=10)

# 定义输入框样式
window.style.configure("Custom.TEntry",
                        fieldbackground="white",  # 设置输入框的背景颜色为白色
                        font=("Arial", 12),
                        padding=5,
                        borderwidth=2)

# 运行主循环
create_LinkMan_file()
window.mainloop()
