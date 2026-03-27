class TestCalculator:
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

# 测试不同的表达式
test_cases = [
    "40*4+12+48+16+40 5+48+36",
    "40*8+40+32+-1",
    "40*12",
    "12+34*5",
    "12+34*5+",
    "12+34*5*",
    "",
    "12+-34",
    "40*8+40+32+-1+50*2"
]

calculator = TestCalculator()

print("测试结果：")
print("-" * 60)
for test_case in test_cases:
    box_count, board_count = calculator.calculate(test_case)
    print(f"表达式: {test_case}")
    print(f"框数: {box_count}, 板数: {board_count}")
    print("-" * 60)