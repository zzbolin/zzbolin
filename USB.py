from flask import Flask, request, render_template
from gtts import gTTS
import speech_recognition as sr
import subprocess

app = Flask(__name__)

# 创建语音识别器对象
recognizer = sr.Recognizer()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/imitation', methods=['POST'])
def imitation_game():
    if request.method == 'POST':
        audio_text = request.form['audio_text']
        
        # 将语音文本传递给语音合成程序
        tts = gTTS(text=audio_text, lang='en')
        tts.save('output.mp3')

        # 使用subprocess播放合成的语音文件
        subprocess.call(['afplay', 'output.mp3'])

        return render_template('imitation.html')

if __name__ == '__main__':
    app.run(debug=True)
