import tkinter as tk
from tkinter import ttk

class BoxCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("框数板数计算器")
        self.root.geometry("360x640")
        self.root.resizable(False, False)
        self.root.config(bg="white")
        
        # 设置中文字体
        self.font_large = ("微软雅黑", 14)
        self.font_medium = ("微软雅黑", 12)
        self.font_small = ("微软雅黑", 10)
        
        # 历史记录列表
        self.history = []
        
        # 创建界面元素
        self.create_widgets()
        
        # 绑定输入事件
        self.input_entry.bind("<KeyRelease>", self.calculate_realtime)
    
    def create_widgets(self):
        # 标题
        title_label = ttk.Label(self.root, text="框数板数计算器", font=self.font_large, background="white")
        title_label.pack(pady=10)
        
        # 输入框
        input_frame = ttk.Frame(self.root, width=340, height=100)
        input_frame.pack(pady=10, padx=10)
        input_frame.pack_propagate(False)
        
        self.input_entry = tk.Text(input_frame, font=self.font_medium, wrap="word", height=4)
        self.input_entry.pack(fill="both", expand=True)
        
        # 结果显示
        result_frame = ttk.Frame(self.root, width=340)
        result_frame.pack(pady=10, padx=10)
        
        box_count_label = ttk.Label(result_frame, text="框数:", font=self.font_medium, background="white")
        box_count_label.pack(side="left", padx=5)
        
        self.box_count_var = tk.StringVar()
        self.box_count_var.set("0")
        box_count_value = ttk.Label(result_frame, textvariable=self.box_count_var, font=self.font_medium, background="white")
        box_count_value.pack(side="left", padx=5)
        
        board_count_label = ttk.Label(result_frame, text="板数:", font=self.font_medium, background="white")
        board_count_label.pack(side="left", padx=5)
        
        self.board_count_var = tk.StringVar()
        self.board_count_var.set("0")
        board_count_value = ttk.Label(result_frame, textvariable=self.board_count_var, font=self.font_medium, background="white")
        board_count_value.pack(side="left", padx=5)
        
        # 计算按钮
        calculate_button = ttk.Button(self.root, text="计算", command=self.save_history, width=20)
        calculate_button.pack(pady=10)
        
        # 历史记录标题
        history_label = ttk.Label(self.root, text="历史记录", font=self.font_medium, background="white")
        history_label.pack(pady=5)
        
        # 历史记录列表
        history_frame = ttk.Frame(self.root, width=340, height=200)
        history_frame.pack(pady=5, padx=10)
        history_frame.pack_propagate(False)
        
        self.history_listbox = tk.Listbox(history_frame, font=self.font_small, selectmode="single")
        self.history_listbox.pack(fill="both", expand=True)
    
    def calculate_realtime(self, event):
        expression = self.input_entry.get("1.0", "end-1c").strip()
        if expression:
            try:
                box_count, board_count = self.calculate(expression)
                self.box_count_var.set(str(box_count))
                self.board_count_var.set(str(board_count))
            except Exception as e:
                self.box_count_var.set("错误")
                self.board_count_var.set("错误")
        else:
            self.box_count_var.set("0")
            self.board_count_var.set("0")
    
    def calculate(self, expression):
        # 处理最后的"+"或"*"
        if expression.endswith("+") or expression.endswith("*"):
            expression = expression[:-1]
        
        # 分割表达式
        terms = expression.split("+")
        box_count = 0
        board_count = 0
        
        for term in terms:
            term = term.strip()
            if not term:
                continue
            
            # 处理"-"情况
            if term.startswith("-"):
                term = term[1:]
                sign = -1
            else:
                sign = 1
            
            if "*" in term:
                # 乘法项
                factors = term.split("*")
                if len(factors) == 2:
                    try:
                        factor1 = int(factors[0].strip())
                        factor2 = int(factors[1].strip())
                        box_count += sign * factor1 * factor2
                        board_count += factor2
                    except ValueError:
                        pass
            else:
                # 非乘法项
                try:
                    value = int(term)
                    box_count += sign * value
                    board_count += 1
                except ValueError:
                    pass
        
        return box_count, board_count
    
    def save_history(self):
        expression = self.input_entry.get("1.0", "end-1c").strip()
        if expression:
            try:
                box_count, board_count = self.calculate(expression)
                # 保存历史记录
                history_item = f"{expression} → 框数: {box_count}, 板数: {board_count}"
                self.history.insert(0, history_item)
                # 保持最多5条历史记录
                if len(self.history) > 5:
                    self.history = self.history[:5]
                # 更新历史记录列表
                self.update_history_list()
            except Exception as e:
                pass
    
    def update_history_list(self):
        self.history_listbox.delete(0, "end")
        for item in self.history:
            self.history_listbox.insert("end", item)

if __name__ == "__main__":
    root = tk.Tk()
    app = BoxCalculator(root)
    root.mainloop()