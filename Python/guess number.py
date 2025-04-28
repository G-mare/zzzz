import random

def number_guessing_game():
    print("欢迎来到猜数字游戏！")
    print("我已经想好了一个1到100之间的数字，请开始猜吧！")
    
    while True:
        # 生成随机数
        secret_number = random.randint(1, 100)
        guess_count = 0
        
        while True:
            # 获取玩家输入
            guess_input = input("请输入你的猜测（1-100）：")
            
            # 验证输入
            try:
                guess = int(guess_input)
                if guess <= 0:
                    print("请输入正整数！")
                    continue
            except ValueError:
                print("请输入有效的数字！")
                continue
            
            guess_count += 1
            
            # 判断猜测结果
            if guess < secret_number:
                print("你猜的数字太小了！")
            elif guess > secret_number:
                print("你猜的数字太大了！")
            else:
                print(f"恭喜你！猜对了！你总共猜了{guess_count}次。")
                break
        
        # 询问是否再来一局
        play_again = input("是否再来一局？(输入y继续，其他退出)：")
        if play_again.lower() != 'y':
            print("游戏结束，谢谢游玩！")
            break

# 启动游戏
if __name__ == "__main__":
    number_guessing_game()