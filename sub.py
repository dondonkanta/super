import random
import string
import os

def generate_password(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def save_password(password, name, folder="passwords"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    # ファイル名は名前.txt（安全のため拡張子や特殊文字除去は要検討）
    filename = os.path.join(folder, f"{name}.txt")
    with open(filename, "w") as f:
        f.write(password)
    print(f"パスワードを {filename} に保存しました。")

def main():
    while True:
        name = input("名前を入力してください（終了するなら空Enter）: ").strip()
        if not name:
            break
        length = input("パスワードの長さを入力してください（デフォルト8）: ").strip()
        length = int(length) if length.isdigit() and int(length) > 0 else 8

        password = generate_password(length)
        print(f"生成されたパスワード: {password}")

        save_password(password, name)

    print("終了します。")

if __name__ == "__main__":
    main()
