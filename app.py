import random
import os
from flask import Flask, request

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
    chapter_links = ''.join([f'<li><a href="/xs/{chapter}" onclick="loadChapter(\'{chapter}\'); return false;">{chapter}</a></li>' for chapter in chapters])
    
    return f'''
    <h1>小说章节</h1>
    <div style="display: flex;">
        <ul style="margin-right: 20px;">
            {chapter_links}
        </ul>
        <div id="content" style="border: 1px solid #ccc; padding: 10px; width: 300px;"></div>
    </div>
    <script>
        function loadChapter(chapter) {{
            fetch('/xs/' + chapter)
                .then(response => response.text())
                .then(data => document.getElementById('content').innerHTML = data);
        }}
    </script>
    '''

@app.route('/xs/<chapter>')
def read_chapter(chapter):
    # 读取指定章节的内容
    try:
        with open(os.path.join('XS', chapter), 'r', encoding='utf-8') as f:
            content = f.read()
        return f'<h1>章节 {chapter}</h1><p>{content}</p>'
    except FileNotFoundError:
        return '<h1>章节未找到</h1> <a href="/xs">返回章节列表</a>'

if __name__ == '__main__':
    app.run()
