import random

def generate_number():
    """生成一个由0-9中不重复的4个数字组成的字符串"""
    digits = random.sample(range(10), 4)
    return ''.join(map(str, digits))

def get_hint(secret, guess, advanced=False):
    """根据猜测返回提示信息"""
    correct_positions = sum(s == g for s, g in zip(secret, guess))
    correct_digits = sum(min(secret.count(d), guess.count(d)) for d in set(guess))
    correct_digits_only = correct_digits - correct_positions
    
    if advanced:
        # 高级提示
        position_info = []
        digit_info = []
        
        # 检查每个位置
        for i, (s, g) in enumerate(zip(secret, guess)):
            if s == g:
                position_info.append(f"第{i+1}位数字位置正确")
        
        # 检查数字是否正确但位置不对
        secret_counts = {}
        guess_counts = {}
        for d in set(guess):
            secret_counts[d] = secret.count(d)
            guess_counts[d] = guess.count(d)
        
        for d in set(guess):
            if secret_counts.get(d, 0) > 0 and d not in [secret[i] for i in range(4) if secret[i] == guess[i]]:
                digit_info.append(f"数字{d}正确")
        
        # 构建高级提示信息
        if not position_info and not digit_info:
            return "没有数字位置正确，没有数字正确"
        elif not position_info and digit_info:
            return f"没有数字位置正确，{', '.join(digit_info)}"
        elif position_info and not digit_info:
            return f"{', '.join(position_info)}，没有其他数字正确"
        else:
            return f"{', '.join(position_info)}，{', '.join(digit_info)}"
    else:
        # 基础提示
        return f"{correct_positions}个数字位置正确，{correct_digits}个数字正确"

def play_game():
    """主游戏函数"""
    secret_number = generate_number()
    attempts = 0
    
    print("游戏开始！请猜一个由0-9中不重复的4个数字组成的数字。")
    
    while True:
        guess = input("请输入你的猜测（4位数字）：").strip()
        attempts += 1
        
        # 验证输入
        if len(guess) != 4 or not guess.isdigit() or len(set(guess)) != 4:
            print("请输入4个不重复的数字！")
            attempts -= 1
            continue
        
        if guess == secret_number:
            print(f"恭喜你猜对了，一共用了{attempts}次")
            break
        
        # 根据尝试次数决定提示级别
        if attempts > 10:
            hint = get_hint(secret_number, guess, advanced=True)
            print(f"程序提示（高级）：{hint}")
        else:
            hint = get_hint(secret_number, guess, advanced=False)
            print(f"程序提示（基础）：{hint}")

def main():
    """主程序"""
    print("欢迎来到数字猜谜游戏！")
    
    while True:
        play_game()
        play_again = input("再来一局吗？（Y/N）").strip().upper()
        if play_again != 'Y':
            print("游戏结束，谢谢游玩！")
            break

if __name__ == "__main__":
    main()