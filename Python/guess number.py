import random

def main():
    settings = {
        'min_range': 1,
        'max_range': 100,
        'dynamic_hint': False
    }
    
    while True:
        print("\n=== 猜数字游戏 ===")
        print("1. 开始游戏")
        print("2. 游戏设置")
        print("0. 退出游戏")
        
        choice = input("请选择（直接回车开始游戏）: ").strip()
        choice = '1' if choice == '' else choice
        
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
    
    while True:
        range_input = input(f"请输入数字范围（当前：{current_settings['min_range']}-{current_settings['max_range']}）: ").strip()
        
        # 解析输入逻辑
        if not range_input:
            min_val, max_val = current_settings['min_range'], current_settings['max_range']
        else:
            try:
                if '-' in range_input:
                    parts = list(map(int, range_input.replace(' ', '').split('-')))
                    min_val, max_val = sorted(parts)
                else:
                    m = int(range_input)
                    if m == 1:
                        min_val = max_val = 1
                    else:
                        min_val, max_val = (1, m) if m > 1 else (0, m)
            except:
                print("⚠ 输入格式错误，请使用数字格式（如'10-100'或'50'）")
                continue
        
        # 自动排序确保范围有效
        min_val, max_val = sorted((min_val, max_val))
        
        # 唯一数字验证
        if min_val == max_val:
            confirm = input(f"⚠ 数字已确定为 {min_val}，游戏将直接获胜！是否继续？（y/n）").lower()
            if confirm != 'y':
                continue
        elif max_val - min_val < 7:
            confirm = input(f"⚠ 数字范围较小（差值{max_val-min_val}），游戏会非常简单！是否继续？（y/n）").lower()
            if confirm != 'y':
                continue
        
        # 保存并显示新设置
        current_settings['min_range'] = min_val
        current_settings['max_range'] = max_val
        print(f"✅ 游戏范围已更新为 {min_val}-{max_val}！")
        break
    
    # 动态提示设置
    current_status = '启用' if current_settings['dynamic_hint'] else '禁用'
    dynamic = input(f"启用动态范围提示？（当前：{current_status}）（y/n）").lower()
    current_settings['dynamic_hint'] = dynamic == 'y'
    
    print("✅ 设置已保存！")
    return current_settings

def play_game(settings):
    min_val = settings['min_range']
    max_val = settings['max_range']
    
    # 处理唯一数字情况
    if min_val == max_val:
        print(f"\n⚠ 注意：数字已确定为 {min_val}")
        input("按回车键提交答案...")  # 戏剧性暂停
        print(f"🎉 恭喜你！猜对了！你总共猜了 1 次。")
        return
    
    # 正常游戏流程
    secret_number = random.randint(min_val, max_val)
    guess_count = 0
    current_min, current_max = min_val, max_val
    
    print(f"\n✅ 游戏开始！我已经想好了一个{min_val}到{max_val}之间的数字。")
    
    while True:
        hint_range = f"（{current_min}-{current_max}）" if settings['dynamic_hint'] else f"（{min_val}-{max_val}）"
        
        try:
            guess = int(input(f"请输入你的猜测{hint_range}: "))
            if guess < 0:
                print("⚠ 请输入非负整数！")
                continue
        except:
            print("⚠ 请输入有效数字！")
            continue
        
        guess_count += 1
        
        if guess < secret_number:
            print("你猜的数字太小了！")
            if settings['dynamic_hint'] and guess > current_min:
                current_min = guess + 1
        elif guess > secret_number:
            print("你猜的数字太大了！")
            if settings['dynamic_hint'] and guess < current_max:
                current_max = guess - 1
        else:
            print(f"🎉 恭喜你！猜对了！你总共猜了 {guess_count} 次。")
            break

if __name__ == "__main__":
    main()