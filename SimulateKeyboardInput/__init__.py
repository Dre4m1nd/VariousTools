import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
import threading


class KeyboardSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("键盘输入模拟器")
        self.root.geometry("1200x800")  # 设置为1200x800尺寸
        self.root.resizable(False, False)

        # 设置主题和样式
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # 配置颜色主题
        self.bg_color = "#f0f0f0"
        self.card_color = "#ffffff"
        self.accent_color = "#4a90e2"
        self.text_color = "#333333"
        self.label_color = "#666666"

        # 配置全局样式 - 增大字体，移除阴影
        self.style.configure(".",
                             background=self.bg_color,
                             foreground=self.text_color,
                             font=("Microsoft YaHei", 12))  # 无阴影设置

        # 配置标签样式
        self.style.configure("TLabel",
                             foreground=self.label_color,
                             font=("Microsoft YaHei", 12))  # 无阴影

        # 配置按钮样式
        self.style.configure("TButton",
                             background=self.accent_color,
                             foreground="white",
                             font=("Microsoft YaHei", 12, "bold"),
                             padding=10)
        self.style.map("TButton",
                       background=[("active", "#3a80d2"), ("pressed", "#2a70c2")])

        # 配置输入框样式
        self.style.configure("TEntry",
                             fieldbackground="white",
                             font=("Microsoft YaHei", 12),
                             padding=8)

        # 配置进度条样式
        self.style.configure("TProgressbar",
                             troughcolor="#e0e0e0",
                             background=self.accent_color)

        # 主窗口背景
        self.root.configure(bg=self.bg_color)

        # 创建主框架
        self.main_frame = ttk.Frame(root, padding=40)  # 增加内边距
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建卡片式容器
        self.card_frame = ttk.Frame(self.main_frame, padding=40)
        self.card_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.card_frame.configure(style="Card.TFrame")

        # 自定义卡片样式
        self.style.configure("Card.TFrame",
                             background=self.card_color,
                             borderwidth=1,
                             relief="solid")

        # 标题 - 更大的字体，无阴影
        title_label = ttk.Label(
            self.card_frame,
            text="键盘输入模拟器",
            font=("Microsoft YaHei", 24, "bold"),  # 无阴影
            foreground=self.accent_color
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 40))

        # 输入框标签
        ttk.Label(self.card_frame, text="请输入要模拟的文本：").grid(
            row=1, column=0, sticky=tk.W, pady=(20, 10))

        # 输入框 - 更长的宽度
        self.text_entry = ttk.Entry(self.card_frame, width=55)
        self.text_entry.grid(row=1, column=1, pady=(20, 10), padx=10)
        self.text_entry.focus()  # 设置初始焦点

        # 延迟输入标签
        ttk.Label(self.card_frame, text="准备时间(秒)：").grid(
            row=2, column=0, sticky=tk.W, pady=10)

        # 延迟输入框
        self.delay_var = tk.StringVar(value="2")
        self.delay_entry = ttk.Entry(self.card_frame, textvariable=self.delay_var, width=12)
        self.delay_entry.grid(row=2, column=1, sticky=tk.W, pady=10, padx=10)

        # 输入速度标签
        ttk.Label(self.card_frame, text="输入速度(字符/秒)：").grid(
            row=3, column=0, sticky=tk.W, pady=10)

        # 输入速度选择
        self.speed_var = tk.StringVar(value="10")
        self.speed_combobox = ttk.Combobox(
            self.card_frame,
            textvariable=self.speed_var,
            values=["5", "10", "20", "30", "50"],
            state="readonly",
            width=10
        )
        self.speed_combobox.grid(row=3, column=1, sticky=tk.W, pady=10, padx=10)

        # 进度条区域
        progress_frame = ttk.Frame(self.card_frame, style="Card.TFrame", padding=12)
        progress_frame.grid(row=4, column=0, columnspan=2, pady=25, sticky=tk.EW)

        ttk.Label(progress_frame, text="输入进度：").pack(side=tk.LEFT, padx=(0, 15))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            length=600,  # 更长的进度条
            mode="determinate"
        )
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 按钮区域
        self.button_frame = ttk.Frame(self.card_frame)
        self.button_frame.grid(row=5, column=0, columnspan=2, pady=30)

        # 开始按钮
        self.start_button = ttk.Button(
            self.button_frame,
            text="开始输入",
            command=self.start_simulation,
            width=18
        )
        self.start_button.pack(side=tk.LEFT, padx=20)

        # 清空按钮
        self.clear_button = ttk.Button(
            self.button_frame,
            text="清空",
            command=self.clear_input,
            width=18
        )
        self.clear_button.pack(side=tk.LEFT, padx=20)

        # 状态区域
        status_frame = ttk.Frame(self.card_frame, style="Card.TFrame", padding=12)
        status_frame.grid(row=6, column=0, columnspan=2, pady=15, sticky=tk.EW)

        self.status_var = tk.StringVar(value="就绪")
        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            foreground=self.accent_color,
            font=("Microsoft YaHei", 12, "italic")  # 无阴影
        )
        self.status_label.pack(side=tk.LEFT)

        # 增加底部空白区域，使布局更均衡
        ttk.Label(self.card_frame, text="").grid(row=7, column=0, columnspan=2, pady=20)

        # 调整网格权重
        self.card_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # 标志变量
        self.is_running = False

    def clear_input(self):
        """清空输入框"""
        self.text_entry.delete(0, tk.END)
        self.text_entry.focus()
        self.progress_var.set(0)
        self.status_var.set("就绪")

    def simulate_typing(self, text, delay, interval):
        """模拟键盘输入"""
        try:
            # 等待指定的延迟时间
            for i in range(int(delay * 10)):
                if not self.is_running:
                    return
                self.status_var.set(f"将在 {delay - i * 0.1:.1f} 秒后开始输入... 请切换到目标窗口")
                time.sleep(0.1)

            self.status_var.set("正在输入...")
            total_chars = len(text)

            if total_chars == 0:
                self.status_var.set("输入完成")
                return

            # 逐个字符输入
            for i, char in enumerate(text):
                if not self.is_running:
                    return

                # 模拟输入字符
                pyautogui.typewrite(char)

                # 更新进度条
                progress = (i + 1) / total_chars * 100
                self.progress_var.set(progress)

                # 控制输入速度
                time.sleep(interval)

            # 删除完成提醒窗口，只更新状态标签
            self.status_var.set("输入完成!")

        except Exception as e:
            self.status_var.set(f"错误: {str(e)}")
            messagebox.showerror("错误", f"发生错误: {str(e)}")
        finally:
            self.is_running = False
            self.start_button.config(text="开始输入", command=self.start_simulation)

    def start_simulation(self):
        """开始模拟输入"""
        text = self.text_entry.get().strip()

        if not text:
            messagebox.showwarning("警告", "请输入要模拟的文本!")
            self.text_entry.focus()
            return

        try:
            delay = float(self.delay_var.get())
            if delay < 0:
                raise ValueError("延迟不能为负数")
        except ValueError:
            messagebox.showwarning("警告", "请输入有效的延迟时间!")
            self.delay_entry.focus()
            return

        try:
            speed = int(self.speed_var.get())
            if speed <= 0:
                raise ValueError("速度必须为正数")
            interval = 1.0 / speed  # 计算每个字符之间的间隔
        except ValueError:
            messagebox.showwarning("警告", "请选择有效的输入速度!")
            return

        # 如果正在运行，则停止
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="开始输入", command=self.start_simulation)
            self.status_var.set("已停止")
            return

        # 准备开始
        self.is_running = True
        self.start_button.config(text="停止", command=self.start_simulation)
        self.progress_var.set(0)

        # 在新线程中运行，避免界面冻结
        threading.Thread(
            target=self.simulate_typing,
            args=(text, delay, interval),
            daemon=True
        ).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardSimulator(root)
    root.mainloop()