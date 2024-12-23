import random
import os
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

target_number = None  # 全局变量，用于存储猜数字游戏的目标数字

def generate_target_number():
    # 生成一个随机目标数字
    global target_number
    target_number = random.randint(1, 100)

def play_rps(player_choice):
    choices = ["石头", "剪刀", "布"]
    computer_choice = random.choice(choices)

    if player_choice == computer_choice:
        result = "平局"
    elif (player_choice == "石头" and computer_choice == "剪刀") or \
         (player_choice == "剪刀" and computer_choice == "布") or \
         (player_choice == "布" and computer_choice == "石头"):
        result = "恭喜您，您赢了！"
    else:
        result = "很遗憾，计算机赢了。"

    return f"您选择了 {player_choice}，计算机选择了 {computer_choice}。<br>{result}"

@app.route('/')
def hello_world():
    # 主页路由，包含图片、文本和链接
    return '''
    <h1>张柏林的网站正在搭建中...</h1>
    <h2>^ - ^</h2>
    <a href="/start_game">进入游戏</a>
    <br>
    <a href="/nb"><img src="/static/dinosaur.gif" /></a>
    '''

@app.route('/start_game')
def start_game():
    # 进入游戏页面的路由，提供欢迎消息和链接开始游戏
    return '''
    <h1>欢迎进入游戏！</h1>
    <a href="/nn">猜数字游戏</a>
    <br>
    <a href="/rps">石头-剪刀-布游戏</a>
    '''

@app.route('/nn', methods=['GET', 'POST'])
def play_game():
    global target_number

    if request.method == 'POST':
        try:
            # 处理用户提交的猜测
            guess = int(request.form['guess'])
        except ValueError:
            return '<h1>请输入一个有效的整数。</h1> <a href="/">返回主页</a> <a href="/nn">继续游戏</a>'

        message = ""

        if guess < target_number:
            message = "太小了，请再试一次。"
        elif guess > target_number:
            message = "太大了，请再试一次。"
        else:
            message = f"恭喜，您猜中了！答案是{target_number}。"
            generate_target_number()  # 重新生成随机数

        return f'<h1>{message}</h1>  <h2>^ - ^</h2> <a href="/">返回主页</a> <a href="/nn">继续游戏</a>'

    else:
        if target_number is None:
            # 游戏开始，生成随机目标数字
            generate_target_number()
            return '<h1>猜一个1到100之间的数字：</h1>' \
                   '<form method="post">' \
                   '<input type="text" name="guess">' \
                   '<input type="submit" value="提交">' \
                   '</form>'
        else:
            # 游戏进行中，允许用户继续猜测
            return '<h1>游戏进行中...</h1>' \
                   '<form method="post">' \
                   '<input type="text" name="guess">' \
                   '<input type="submit" value="提交">' \
                   '</form> <a href="/">返回主页</a> <a href="/nn">继续游戏</a>'

@app.route('/nb')
def hello_world2():
    # 第二个页面，包含图片、消息和返回主页的链接
    return '<h1>牛比不?</h1>  <h2>^ - ^</h2> <a href="/"><img src="/static/dinosaur.gif" /></a> <a href="/">返回主页</a>'

@app.route('/rps', methods=['GET', 'POST'])
def play_rps_game():
    if request.method == 'POST':
        player_choice = request.form.get('choice')
        if player_choice not in ["石头", "剪刀", "布"]:
            return '<h1>请选择石头、剪刀或布。</h1> <a href="/">返回主页</a> <a href="/rps">继续游戏</a>'

        result = play_rps(player_choice)
        return f'<h1>{result}</h1> <a href="/">返回主页</a> <a href="/rps">继续游戏</a>'
    else:
        return '''
        <h1>石头-剪刀-布游戏</h1>
        <form method="post">
        <input type="radio" name="choice" value="石头"> 石头
        <input type="radio" name="choice" value="剪刀"> 剪刀
        <input type="radio" name="choice" value="布"> 布
        <br>
        <input type="submit" value="提交">
        </form>
        <a href="/">返回主页</a> <a href="/rps">继续游戏</a>
        '''

@app.errorhandler(Exception)
def handle_error(e):
    return f'<h1>发生错误: {str(e)}</h1> <a href="/">返回主页</a>', 500

@app.route('/xs')
def novel_index():
    # 获取小说章节列表并按数字排序
    chapters = sorted(os.listdir('XS'), key=lambda x: int(x))  # 假设章节文件在XS文件夹中
    chapter_links = ''
    
    for index, chapter in enumerate(chapters, start=1):  # 从1开始计数
        with open(os.path.join('XS', chapter), 'r', encoding='utf-8') as f:
            title = f.readline().strip()  # 读取第一行作为章节标题
        chapter_links += f'<li><a href="/xs/{chapter}" onclick="loadChapter(\'{chapter}\', this); return false;">第{index}章: {title}</a></li>'
    
    return f'''
    <h1>ASNIWATW</h1>
    <div style="display: flex; gap: 20px; align-items: flex-start;">
        <ul style="width: 200px; list-style-type: none; padding: 0; margin: 0;">
            {chapter_links}
        </ul>
        <div id="content" style="border: 1px solid #ccc; padding: 10px; max-width: 600px; flex-grow: 1;"></div>
    </div>
    <h2>添加/修改章节</h2>
    <form method="POST" action="/add_chapter">
        <input type="text" name="chapter_name" placeholder="章节文件名（数字）" required>
        <input type="text" name="chapter_title" placeholder="章节标题" required>
        <textarea name="chapter_content" placeholder="章节内容" required></textarea>
        <input type="submit" value="添加/修改章节">
    </form>
    <script>
        function loadChapter(chapter, element) {{
            fetch('/xs/' + chapter)
                .then(response => response.text())
                .then(data => {{
                    document.getElementById('content').innerHTML = data;
                    // 清除所有按钮的红色样式
                    const links = document.querySelectorAll('ul a');
                    links.forEach(link => link.style.color = '');  // 恢复默认颜色
                    element.style.color = 'red';  // 设置当前按钮为红色
                }});
        }}
    </script>
    <style>
        @media (max-width: 600px) {{
            div {{
                flex-direction: column;  /* 小屏幕时改为垂直方向 */
            }}
            ul {{
                width: auto;  /* 小屏幕上宽度自适应 */
                margin-right: 0;
                margin-bottom: 10px;
            }}
            #content {{
                margin-top: 20px;  /* 在小屏幕上增加顶部间距 */
                max-width: 100%;  /* 确保在小屏幕上内容宽度自适应 */
            }}
        }}
    </style>
    '''

@app.route('/add_chapter', methods=['POST'])
def add_chapter():
    chapter_name = request.form['chapter_name']
    chapter_title = request.form['chapter_title']
    chapter_content = request.form['chapter_content']
    
    # 保存章节内容到文件
    with open(os.path.join('XS', chapter_name), 'w', encoding='utf-8') as f:
        f.write(f"{chapter_title}\n{chapter_content}")
    
    return redirect(url_for('novel_index'))

@app.route('/xs/<chapter>')
def read_chapter(chapter):
    # 读取指定章节的内容
    try:
        with open(os.path.join('XS', chapter), 'r', encoding='utf-8') as f:
            lines = f.readlines()
            content = ''.join(lines[1:]).strip()  # 只获取从第二行开始的内容
        return f'<p>{content}</p>'  # 只返回内容，不再显示标题
    except FileNotFoundError:
        return '<h1>章节未找到</h1> <a href="/xs">返回章节列表</a>'

if __name__ == '__main__':
    app.run()
