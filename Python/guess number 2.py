import random
import time

def generate_number(difficulty):
    """根据难度生成数字"""
    if difficulty == "极难":
        # 允许重复数字
        return ''.join(str(random.randint(0, 9)) for _ in range(4))
    else:
        # 不重复数字
        return ''.join(map(str, random.sample(range(10), 4)))

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

def show_help():
    """显示帮助信息"""
    print("\n可用命令：")
    print("/hint - 基于上次猜测获取高级提示")
    print("/home - 返回主菜单（难度选择页面）")
    print("/exit或/quit - 显示答案并退出游戏")
    print("/answer - 显示答案并询问是否再来一局")
    print("/help - 显示此帮助信息")
    print("/ra - 显示剩余尝试次数")
    print("/restart - 以当前难度重新开始游戏")
    print("/rule - 显示当前难度游戏规则")

def show_rules(difficulty):
    """显示当前难度规则"""
    print(f"\n当前难度【{difficulty}】游戏规则：")
    
    if difficulty == "简单":
        print("- 数字由0-9中不重复的4个数字组成")
        print("- 不限尝试次数")
        print("- 始终提供高级提示")
    elif difficulty == "普通":
        print("- 数字由0-9中不重复的4个数字组成")
        print("- 最多尝试16次")
        print("- 前8次提供基础提示，之后提供高级提示")
    elif difficulty == "困难":
        print("- 数字由0-9中不重复的4个数字组成")
        print("- 最多尝试8次")
        print("- 仅提供基础提示（可使用/hint获取高级提示）")
    elif difficulty == "极难":
        print("- 数字由0-9中4个数字组成（可能重复）")
        print("- 最多尝试32次")
        print("- 仅提供基础提示（可使用/hint获取高级提示）")
    
    print("\n提示说明：")
    print("- 基础提示：显示数字位置正确数量和数字正确数量")
    print("- 高级提示：显示具体哪些位置正确，哪些数字正确但位置不对")

def play_game(difficulty):
    """主游戏函数"""
    while True:  # 用于/restart命令
        secret_number = generate_number(difficulty)
        attempts = 0
        max_attempts = {
            "简单": float('inf'),
            "普通": 16,
            "困难": 8,
            "极难": 32
        }[difficulty]
        last_guess = None
        
        print(f"\n游戏开始！难度：{difficulty}")
        print("请猜一个由0-9组成的4位数字" + ("（数字可能重复）" if difficulty == "极难" else "（数字不重复）"))
        print("输入 /help 查看可用命令")
        
        while True:
            remaining = max_attempts - attempts if max_attempts != float('inf') else '无限'
            prompt = f"\n请输入你的猜测（4位数字" + (f"，剩余尝试次数：{remaining}" if remaining != '无限' and remaining <= 3 else "") + "）："
            guess = input(prompt).strip()
            
            # 检查是否是命令
            if guess.startswith('/'):
                if guess.lower() in ['/exit', '/quit']:
                    print(f"\n本局正确答案是：{secret_number}")
                    print("游戏结束，谢谢游玩！")
                    exit()
                elif guess.lower() == '/home':
                    print("\n返回主菜单...")
                    return True
                elif guess.lower() == '/answer':
                    print(f"\n本局正确答案是：{secret_number}")
                    play_again = input("再来一局吗？（Y/N）").strip().upper()
                    return play_again == 'Y'
                elif guess.lower() == '/hint':
                    if last_guess:
                        print("\n高级提示：" + get_hint(secret_number, last_guess, advanced=True))
                    else:
                        print("\n请先进行一次猜测后再使用此命令")
                    continue
                elif guess.lower() == '/help':
                    show_help()
                    continue
                elif guess.lower() == '/ra':
                    print(f"\n剩余尝试次数：{remaining}")
                    continue
                elif guess.lower() == '/restart':
                    print(f"\n本局正确答案是：{secret_number}")
                    print("3秒后重新开始游戏...")
                    time.sleep(3)
                    break  # 跳出内部循环，重新开始游戏
                elif guess.lower() == '/rule':
                    show_rules(difficulty)
                    continue
                else:
                    print("\n未知命令，输入 /help 查看可用命令")
                    continue
            
            attempts += 1
            last_guess = guess
            
            # 验证输入
            if len(guess) != 4 or not guess.isdigit():
                print("\n请输入4位数字！")
                attempts -= 1
                last_guess = None
                continue
            
            if difficulty != "极难" and len(set(guess)) != 4:
                print("\n请输入4个不重复的数字！")
                attempts -= 1
                last_guess = None
                continue
            
            if guess == secret_number:
                print(f"\n恭喜你猜对了，一共用了{attempts}次")
                play_again = input("再来一局吗？（Y/N）").strip().upper()
                return play_again == 'Y'
            
            # 检查是否超过最大尝试次数
            if attempts >= max_attempts:
                print(f"\n很遗憾，你没有在{max_attempts}次内猜出正确答案：{secret_number}")
                play_again = input("再来一局吗？（Y/N）").strip().upper()
                return play_again == 'Y'
            
            # 根据难度决定提示级别
            if difficulty == "简单":
                hint = get_hint(secret_number, guess, advanced=True)
                print(f"\n高级提示：{hint}")
            elif difficulty == "普通":
                if attempts > 8:
                    hint = get_hint(secret_number, guess, advanced=True)
                    print(f"\n高级提示：{hint}")
                else:
                    hint = get_hint(secret_number, guess, advanced=False)
                    print(f"\n提示：{hint}")
            else:  # 困难和极难模式
                hint = get_hint(secret_number, guess, advanced=False)
                print(f"\n提示：{hint}")

def select_difficulty():
    """选择难度"""
    print("\n请选择游戏难度：")
    print("1. 简单 - 不限次数，始终提供高级提示")
    print("2. 普通 - 16次限制，8次后提供高级提示")
    print("3. 困难 - 8次限制，仅基础提示（可输入/hint获取高级提示）")
    print("4. 极难 - 32次限制，数字可重复，仅基础提示（可输入/hint获取高级提示）")
    
    while True:
        choice = input("请输入难度编号(1-4)：").strip()
        if choice in ['1', '2', '3', '4']:
            return ["简单", "普通", "困难", "极难"][int(choice)-1]
        print("无效输入，请输入1-4的数字")

def main():
    """主程序"""
    print("""
欢迎来到数字猜谜游戏！

游戏规则：
1. 程序会随机生成一个4位数字（根据难度可能允许重复数字）
2. 你需要猜测这个数字是什么
3. 每次猜测后会得到提示：
   - 基础提示：显示数字位置正确数量和数字正确数量
   - 高级提示：显示具体哪些位置正确，哪些数字正确但位置不对
4. 不同难度有不同的尝试次数限制和提示规则
5. 游戏过程中可以输入各种命令获取帮助或控制游戏

输入 /help 可以查看所有可用命令
""")
    
    while True:
        difficulty = select_difficulty()
        while play_game(difficulty):
            pass  # 继续游戏
        
        # 询问是否完全退出
        if input("\n是否完全退出游戏？（Y/N）").strip().upper() == 'Y':
            print("\n游戏结束，谢谢游玩！")
            break

if __name__ == "__main__":
    main()