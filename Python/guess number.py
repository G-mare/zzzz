import random

def main():
    # 默认游戏设置
    settings = {
        'min_range': 1,
        'max_range': 100,
        'dynamic_hint': False  # 默认禁用动态提示
    }
    
    while True:
        print("\n=== 猜数字游戏 ===")
        print("1. 开始游戏")
        print("2. 游戏设置")
        print("0. 退出游戏")
        
        choice = input("请选择(直接回车开始游戏): ").strip()
        
        # 直接回车则开始游戏
        if choice == '':
            choice = '1'
        
        if choice == '1':
            play_game(settings)
        elif choice == '2':
            settings = game_settings(settings)
        elif choice == '0':
            print("感谢游玩，再见！")
            break
        else:
            print("无效输入，请重新选择！")

def game_settings(current_settings):
    print("\n=== 游戏设置 ===")
    
    # 设置数字范围
    while True:
        range_input = input(f"请输入数字范围(格式: 最小值-最大值, 当前: {current_settings['min_range']}-{current_settings['max_range']}): ").strip()
        
        # 如果直接回车则保持当前设置
        if range_input == '':
            min_val = current_settings['min_range']
            max_val = current_settings['max_range']
        else:
            # 尝试解析范围格式
            try:
                if '-' in range_input:
                    parts = range_input.split('-')
                    if len(parts) != 2:
                        raise ValueError
                    min_val = int(parts[0].strip())
                    max_val = int(parts[1].strip())
                else:
                    # 如果只输入一个数字，则作为最大值，最小值为0
                    min_val = 0
                    max_val = int(range_input.strip())
            except ValueError:
                print("请输入有效的范围格式，如 '10-100' 或 '50'")
                continue
        
        # 验证范围
        if min_val < 0 or max_val < 0:
            print("请输入非负整数！")
        elif min_val > max_val:
            print("最大值必须大于或等于最小值！")
        elif max_val - min_val < 7 and min_val != max_val:  # 只有当范围不是单一数字时才提示
            confirm = input("⚠ 数字范围较小，游戏难度较低！是否继续？(y/n): ").lower()
            if confirm != 'y':
                continue
        else:
            current_settings['min_range'] = min_val
            current_settings['max_range'] = max_val
            break
    
    # 设置动态提示
    dynamic = input(f"启用动态范围提示? (当前: {'启用' if current_settings['dynamic_hint'] else '禁用'}) (y/n): ").lower()
    current_settings['dynamic_hint'] = dynamic == 'y'
    
    print("设置已保存！")
    return current_settings

def play_game(settings):
    min_val = settings['min_range']
    max_val = settings['max_range']
    
    # 特殊处理：当最小值和最大值相同时，直接使用该值
    if min_val == max_val:
        secret_number = min_val
        print(f"\n游戏开始！数字已经确定为 {secret_number}。")
    else:
        secret_number = random.randint(min_val, max_val)
        print(f"\n游戏开始！我已经想好了一个{min_val}到{max_val}之间的数字。")
    
    guess_count = 0
    
    # 动态提示范围
    current_min = min_val
    current_max = max_val
    
    while True:
        # 根据设置显示不同的提示
        if settings['dynamic_hint'] and (current_min != min_val or current_max != max_val):
            hint = f"({current_min}-{current_max})"
        else:
            hint = f"({min_val}-{max_val})"
        
        guess_input = input(f"请输入你的猜测{hint}: ")
        
        # 验证输入
        try:
            guess = int(guess_input)
            if guess < 0:
                print("请输入非负整数！")
                continue
        except ValueError:
            print("请输入有效的数字！")
            continue
        
        guess_count += 1
        
        # 判断猜测结果
        if guess < secret_number:
            print("你猜的数字太小了！")
            if settings['dynamic_hint'] and guess > current_min:
                current_min = guess
        elif guess > secret_number:
            print("你猜的数字太大了！")
            if settings['dynamic_hint'] and guess < current_max:
                current_max = guess
        else:
            print(f"恭喜你！猜对了！你总共猜了{guess_count}次。")
            break

if __name__ == "__main__":
    main()