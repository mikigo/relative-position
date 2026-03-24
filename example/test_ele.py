from relative_position import App

app = App("explorer.exe")

new_file_btn = app.Ele(
    direction="left_top",
    bbox=[20, 20, 50, 35]
)

# 或者使用 center 参数
save_btn = app.Ele(
    direction="left_top",
    center=[30, 30]
)
