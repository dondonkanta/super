import tkinter as tk
import random
import string
import os
import itertools

# ----------------------------
# グローバル変数
# ----------------------------

password_data = {}
daikichi_count = 0
daikichi_count_file = "daikichi_count.txt"
is_daikichi_rush = False
is_next_omikuji_daikichi = False  # ネガポジ後の大吉確定フラグ

# ----------------------------
# パスワード処理関数
# ----------------------------

def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def save_all_passwords(folder="passwords"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for name, password in password_data.items():
        with open(os.path.join(folder, f"{name}.txt"), "w") as f:
            f.write(password)

def load_passwords_from_file(folder="passwords"):
    if not os.path.exists(folder):
        return
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            name = filename[:-4]
            with open(os.path.join(folder, filename), "r") as f:
                password_data[name] = f.read().strip()

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    label_result.config(text=f"✅ コピーしました: {text}", fg="green")

def on_generate():
    name = entry_name.get().strip()
    length_str = length_var.get()

    if not name:
        label_result.config(text="⚠ 名前を入力してください", fg="red")
        return

    if name in password_data:
        label_result.config(text="⚠ この名前はすでに使われています", fg="red")
        return

    try:
        length = int(length_str)
    except ValueError:
        label_result.config(text="⚠ パスワードの長さが無効です", fg="red")
        return

    password = generate_password(length)
    password_data[name] = password
    save_all_passwords()

    label_result.config(text=f"{name} : {password}", fg="blue")
    copy_button.config(command=lambda p=password: copy_to_clipboard(p))
    copy_button.pack()

def on_check_all():
    if not password_data:
        label_result.config(text="まだデータがありません。", fg="black")
        return

    result_window = tk.Toplevel(root)
    result_window.title("保存された名前とパスワード")
    result_window.geometry("600x600")

    search_var = tk.StringVar()

    def update_list():
        search_text = search_var.get().strip().lower()
        for widget in frame_display.winfo_children():
            widget.destroy()
        found = False
        for name, pw in password_data.items():
            if search_text in name.lower():
                row = tk.Frame(frame_display)
                row.pack(fill="x", pady=4)
                tk.Label(row, text=f"{name} : {pw}", font=("Arial", 14), anchor="w").pack(side="left", padx=10)

                def copy(p=pw):
                    root.clipboard_clear()
                    root.clipboard_append(p)
                    root.update()
                    label_result.config(text=f"✅ コピーしました: {p}", fg="green")

                tk.Button(row, text="📋 コピー", command=copy, font=("Arial", 10)).pack(side="right", padx=10)
                found = True
        if not found:
            tk.Label(frame_display, text="一致するデータがありません", fg="gray").pack()

    tk.Label(result_window, text="名前で検索:", font=("Arial", 12)).pack(pady=5)
    search_entry = tk.Entry(result_window, textvariable=search_var, font=("Arial", 12), width=30)
    search_entry.pack(pady=5)
    tk.Button(result_window, text="検索", command=update_list, font=("Arial", 12)).pack(pady=5)

    frame_display = tk.Frame(result_window)
    frame_display.pack(pady=10, fill="both", expand=True)

    update_list()

# ----------------------------
# daikichi_count の保存・読み込み
# ----------------------------

def save_daikichi_count():
    try:
        with open(daikichi_count_file, "w") as f:
            f.write(str(daikichi_count))
    except Exception as e:
        print("daikichi_count保存失敗:", e)

def load_daikichi_count():
    global daikichi_count
    try:
        with open(daikichi_count_file, "r") as f:
            daikichi_count = int(f.read())
    except Exception:
        daikichi_count = 0

# ----------------------------
# タイトルの文字色を左から順に金色に変える演出
# ----------------------------

def highlight_title():
    global daikichi_count
    daikichi_count += 1
    if daikichi_count > len(title_labels):
        daikichi_count = len(title_labels)
    for i, lbl in enumerate(title_labels):
        if i < daikichi_count:
            lbl.config(fg="gold")
        else:
            lbl.config(fg="black")
    save_daikichi_count()

# ----------------------------
# 大吉ラッシュ突入演出
# ----------------------------

def show_daikichi_rush_message():
    global is_daikichi_rush
    is_daikichi_rush = True
    omikuji_button.config(text="🎉 大吉ラッシュ中！")

    rush_window = tk.Toplevel(root)
    rush_window.attributes('-fullscreen', True)
    rush_window.configure(bg="black")

    label = tk.Label(rush_window, text="大吉ラッシュ突入！", font=("Arial", 72, "bold"), bg="black", fg="white")
    label.pack(expand=True)

    rainbow_colors = itertools.cycle(["red", "orange", "yellow", "green", "blue", "indigo", "violet"])

    def flash(count=0):
        if count >= 14:
            rush_window.destroy()
            return
        label.config(fg=next(rainbow_colors))
        rush_window.after(200, flash, count + 1)

    flash()

# ----------------------------
# 777演出
# ----------------------------

def start_777_fall_animation():
    anim_win = tk.Toplevel(root)
    anim_win.attributes('-fullscreen', True)
    anim_win.configure(bg="black")

    canvas = tk.Canvas(anim_win, bg="black")
    canvas.pack(fill="both", expand=True)

    width = anim_win.winfo_screenwidth()
    height = anim_win.winfo_screenheight()

    x_positions = [width // 2 - 150, width // 2, width // 2 + 150]
    y_target = height // 2

    rainbow_colors = itertools.cycle(["red", "orange", "yellow", "green", "blue", "indigo", "violet"])

    sevens = []
    for i in range(3):
        seven = canvas.create_text(x_positions[i], -100, text="7", font=("Arial", 80, "bold"),
                                   fill=next(rainbow_colors))
        sevens.append(seven)

    speed = 20
    delays = [0, 500, 1000]
    finished = [False, False, False]

    def move_seven(index):
        def animate():
            x, y = canvas.coords(sevens[index])
            if y < y_target:
                canvas.move(sevens[index], 0, speed)
                canvas.after(50, animate)
            else:
                canvas.coords(sevens[index], x, y_target)
                finished[index] = True
                if all(finished):
                    show_right_guide_and_wait()
        animate()

    for i, delay in enumerate(delays):
        anim_win.after(delay, move_seven, i)

    def show_right_guide_and_wait():
        guide = canvas.create_text(
            width - 50, height - 50,
            text="右を狙え",
            font=("Arial", 48, "bold"),
            fill="white",
            anchor="se"
        )
        canvas.move(guide, -100, -150)
        canvas.after(2000, show_omedetou)

    def show_omedetou():
        for widget in anim_win.winfo_children():
            widget.destroy()
        anim_win.configure(bg="white")
        label = tk.Label(anim_win, text="おめでとう", fg="black", bg="white", font=("Arial", 72, "bold"))
        label.pack(expand=True)
        anim_win.after(3000, lambda: [anim_win.destroy(), show_daikichi_rush_message()])

# ----------------------------
# レインボー背景
# ----------------------------

def start_rainbow_background():
    colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    idx = 0

    def change_bg():
        nonlocal idx
        root.configure(bg=colors[idx])
        label_omikuji.config(bg=colors[idx])
        omikuji_button.config(bg=colors[idx])
        label_result.config(bg=colors[idx])
        idx = (idx + 1) % len(colors)
        root.after(100, change_bg)

    change_bg()

# ----------------------------
# おみくじ処理
# ----------------------------

def draw_omikuji():
    global is_daikichi_rush, daikichi_count, is_next_omikuji_daikichi

    if is_next_omikuji_daikichi:
        result = "大吉"
        is_next_omikuji_daikichi = False
        if not is_daikichi_rush:
            start_rainbow_background()

        entry_name.config(bg="white")
        dropdown_length.config(bg="white")
    else:
        root.configure(bg="SystemButtonFace")
        label_omikuji.config(bg=root.cget("bg"))
        omikuji_button.config(bg=root.cget("bg"))
        label_result.config(bg=root.cget("bg"))
        entry_name.config(bg="white")
        dropdown_length.config(bg="SystemButtonFace")

        if is_daikichi_rush:
            result = random.choices(
                population=["大吉", "中吉", "小吉", "吉", "末吉", "凶", "大凶"],
                weights=[77, 5, 5, 5, 4, 2, 2],
                k=1
            )[0]
        else:
            result = random.choice(["大吉", "中吉", "小吉", "吉", "末吉", "凶", "大凶"])

    if result == "大吉":
        if is_daikichi_rush:
            daikichi_count += 1
            save_daikichi_count()

            anim_window = tk.Toplevel(root)
            anim_window.attributes('-fullscreen', True)
            anim_window.configure(bg="white")

            label = tk.Label(anim_window, text="大吉", font=("Arial", 100, "bold"), bg="white")
            label.pack(expand=True)

            rainbow_colors = itertools.cycle(["red", "orange", "yellow", "green", "blue", "indigo", "violet"])

            scale_min = 1.0
            scale_max = 7.0
            scale_step = 0.8
            current_scale = scale_min
            growing = True

            stop_animation = False

            def animate(count=0):
                nonlocal current_scale, growing, stop_animation

                if stop_animation:
                    return

                label.config(fg=next(rainbow_colors))

                base_size = 100
                size = int(base_size * current_scale)
                label.config(font=("Arial", size, "bold"))

                if growing:
                    current_scale += scale_step
                    if current_scale >= scale_max:
                        current_scale = scale_max
                        growing = False
                else:
                    if random.random() < 0.02:
                        stop_animation = True
                        anim_window.configure(bg="black")
                        label.config(bg="black", fg="white")

                        def go_to_renchu():
                            anim_window.destroy()
                            show_renchu_window()

                        anim_window.after(2000, go_to_renchu)
                        global is_next_omikuji_daikichi
                        is_next_omikuji_daikichi = True
                        return

                    current_scale -= scale_step
                    if current_scale <= scale_min:
                        current_scale = scale_min
                        growing = True

                if count < 60:
                    anim_window.after(50, animate, count + 1)
                else:
                    anim_window.destroy()
                    show_renchu_window()

            def show_renchu_window():
                ren_window = tk.Toplevel(root)
                ren_window.attributes('-fullscreen', True)
                ren_window.configure(bg="white")

                text = f"{daikichi_count}連"
                lbl = tk.Label(ren_window, text=text, font=("Arial", 800, "bold"), fg="black", bg="white")
                lbl.pack(expand=True)

                ren_window.after(3000, ren_window.destroy)

            animate()
            return

        else:
            daikichi_count = 1
            save_daikichi_count()

            pre_window = tk.Toplevel(root)
            pre_window.attributes('-fullscreen', True)
            pre_window.configure(bg="white")

            label = tk.Label(pre_window, text="予告", fg="black", bg="white", font=("Arial", 72, "bold"))
            label.pack(expand=True)

            def show_next_hint():
                label.config(text="次回大吉確定")
                rainbow_colors = itertools.cycle(["red", "orange", "yellow", "green", "blue", "indigo", "violet"])

                def flash_color(count=0):
                    if count >= 12:
                        pre_window.destroy()
                        start_777_fall_animation()
                        return
                    label.config(fg=next(rainbow_colors))
                    pre_window.after(150, flash_color, count + 1)

                flash_color()

            pre_window.after(3000, show_next_hint)

    else:
        if is_daikichi_rush:
            # 🎉 大吉ラッシュ終了演出
            rush_end_window = tk.Toplevel(root)
            rush_end_window.attributes('-fullscreen', True)
            rush_end_window.configure(bg="white")

            label_end = tk.Label(rush_end_window, text="大吉ラッシュ終了", font=("Arial", 72, "bold"), fg="black", bg="white")
            label_end.pack(pady=100)

            label_count = tk.Label(rush_end_window, text=f"大吉 × {daikichi_count}連", font=("Arial", 64, "bold"), fg="red", bg="white")
            label_count.pack()

            def close_and_reset():
                global is_daikichi_rush, daikichi_count
                rush_end_window.destroy()
                is_daikichi_rush = False
                daikichi_count = 0
                save_daikichi_count()
                omikuji_button.config(text="おみくじを引く")

            rush_end_window.after(3000, close_and_reset)

        else:
            label_omikuji.config(text=f"おみくじの結果: {result}", fg="purple", font=("Arial", 20))


# ----------------------------
# メインGUIレイアウト
# ----------------------------

root = tk.Tk()
root.title("パスワード生成＆保存アプリ")
root.attributes("-fullscreen", True)

title_text = "パスワード生成 ＆ 保存 アプリ"
title_frame = tk.Frame(root)
title_frame.pack(pady=30)

title_labels = []
for ch in title_text:
    lbl = tk.Label(title_frame, text=ch, font=("Arial", 32, "bold"), fg="black")
    lbl.pack(side="left")
    title_labels.append(lbl)

load_daikichi_count()
for i, lbl in enumerate(title_labels):
    if i < daikichi_count:
        lbl.config(fg="gold")
    else:
        lbl.config(fg="black")

tk.Label(root, text="名前を入力してください:", font=("Arial", 16)).pack(pady=10)
entry_name = tk.Entry(root, font=("Arial", 16), width=30)
entry_name.pack(pady=10)

tk.Label(root, text="パスワードの長さを選んでください:", font=("Arial", 16)).pack(pady=10)
length_var = tk.StringVar(root)
length_var.set("8")
length_options = [str(i) for i in range(1, 16)]
dropdown_length = tk.OptionMenu(root, length_var, *length_options)
dropdown_length.config(font=("Arial", 14))
dropdown_length.pack(pady=10)

tk.Button(root, text="パスワード生成", command=on_generate, font=("Arial", 16), width=20).pack(pady=10)
tk.Button(root, text="保存済みを確認", command=on_check_all, font=("Arial", 16), width=20).pack(pady=10)

label_result = tk.Label(root, text="", font=("Arial", 18))
label_result.pack(pady=10)

copy_button = tk.Button(root, text="📋 コピー", font=("Arial", 14), command=lambda: copy_to_clipboard(""))
copy_button.pack(pady=5)
copy_button.pack_forget()

omikuji_button = tk.Button(root, text="おみくじを引く", command=draw_omikuji, font=("Arial", 16), width=20)
omikuji_button.pack(pady=10)
label_omikuji = tk.Label(root, text="", font=("Arial", 16))
label_omikuji.pack(pady=10)

tk.Button(root, text="アプリを終了", command=root.quit, font=("Arial", 14)).pack(pady=30)

load_passwords_from_file()
root.mainloop()
