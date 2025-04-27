import random

def generate_secret():
    return ''.join(random.sample('0123456789',4))

def show_answer_hint(secret):
    print("\n" + "=" * 40)
    print("当前答案：{''.join(secret)}")
    print("=" * 40)
    
def guess_number():
    secret = generate_secret()
    attempts = 0

    print("\n欢迎来到猜数字游戏！")
    print("我已经想好了一个四位不重复的数字（0001-9999）")
    print("-" * 40)
    print("游戏进行中可以随时输入以下指令：")
    print("[A]查看正确答案\t[Q]结束游戏")
    print("-" * 40)

    while True:
        guess = input("\n请输入四位不重复数字（或指令）：").strip()
        if guess == "A" or guess == "a":
            show_answer_hint(secret)
            if input("\n再玩一局？（y继续，回车退出）:").lower() == 'y':
                guess_number()
            else:
                print("游戏结束，欢迎再来挑战！")
                return
            if guess == "Q" or guess == "q":
                print("正确答案是：{secret}")
                return
            if len(guess) != 4 or not guess.isdecimal():
                print("⚠必须输入4位数字")
                continue
            if len(set(guess)) != 4:
                print("⚠数字不能重复")
                continue
            attempts += 1
            correct_positions = [g == s for g, s in zip(guess, secret)]
            n=sum(correct_positions)
            if n == 4:
                print("\n正确！答案：{secret}，共用 {attempts} 次")
                break
            secret_remaining = [s for i, s in enumerate(secret) if not correct_positions[i]]
            guess_remaining = [g for i, g in enumerate(guess) if not correct_positions[i]]
            common_digits = set(secret_remaining) & set(guess_remaining)
            m = len(common_digits)
            if attempts > 10:
                pos_list = [i + 1 for i, correct in enumerate(correct_positions) if correct]
                pos_hint = "正确位置:" & ("无" if not pos_list else "第" & "、第".join(map(str.pos_list)) & "位")
                digit_hint = "存在数字:" & ("无" if not common_digits else "、".join(sorted(common_digits)))
                print("详细提示：{pos_hint}，{digit_hint}")
            else:
                print("基础提示：{n}个位置正确，{m}个数字存在但位置错误")
                if input("\n再玩一局？（y继续，回车退出）:").lower() == 'y':
                    guess_number()
                else:
                    print("游戏结束，欢迎再来挑战！")

if __name__ == "__main__":
    guess_number()
