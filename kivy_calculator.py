from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

class BoxCalculatorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = []
    
    def build(self):
        # 设置窗口大小
        Window.size = (360, 640)
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title_label = Label(text="框数板数计算器", font_size=20, size_hint_y=None, height=50)
        main_layout.add_widget(title_label)
        
        # 输入框
        input_layout = BoxLayout(size_hint_y=None, height=120)
        self.input_entry = TextInput(multiline=True, font_size=16)
        input_layout.add_widget(self.input_entry)
        main_layout.add_widget(input_layout)
        
        # 结果显示
        result_layout = BoxLayout(size_hint_y=None, height=50)
        
        box_count_label = Label(text="框数:", font_size=16)
        result_layout.add_widget(box_count_label)
        
        self.box_count_var = Label(text="0", font_size=16)
        result_layout.add_widget(self.box_count_var)
        
        board_count_label = Label(text="板数:", font_size=16)
        result_layout.add_widget(board_count_label)
        
        self.board_count_var = Label(text="0", font_size=16)
        result_layout.add_widget(self.board_count_var)
        
        main_layout.add_widget(result_layout)
        
        # 计算按钮
        calculate_button = Button(text="计算", size_hint_y=None, height=50, font_size=16)
        calculate_button.bind(on_press=self.save_history)
        main_layout.add_widget(calculate_button)
        
        # 历史记录标题
        history_label = Label(text="历史记录", font_size=16, size_hint_y=None, height=40)
        main_layout.add_widget(history_label)
        
        # 历史记录列表
        scroll_view = ScrollView(size_hint_y=1)
        self.history_list = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.history_list.bind(minimum_height=self.history_list.setter('height'))
        scroll_view.add_widget(self.history_list)
        main_layout.add_widget(scroll_view)
        
        # 绑定输入事件
        self.input_entry.bind(text=self.calculate_realtime)
        
        return main_layout
    
    def calculate_realtime(self, instance, value):
        expression = value.strip()
        if expression:
            try:
                box_count, board_count = self.calculate(expression)
                self.box_count_var.text = str(box_count)
                self.board_count_var.text = str(board_count)
            except Exception as e:
                self.box_count_var.text = "错误"
                self.board_count_var.text = "错误"
        else:
            self.box_count_var.text = "0"
            self.board_count_var.text = "0"
    
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
    
    def save_history(self, instance):
        expression = self.input_entry.text.strip()
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
        # 清空历史记录列表
        self.history_list.clear_widgets()
        # 添加历史记录
        for item in self.history:
            history_label = Label(text=item, font_size=14, size_hint_y=None, height=40)
            self.history_list.add_widget(history_label)

if __name__ == "__main__":
    BoxCalculatorApp().run()