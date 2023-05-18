import os
from flask import Flask, render_template, request
from google.cloud import vision

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # アップロードされた画像の保存先フォルダ

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\Users\t-miy\Downloads\rapid-stage-380007-621ecdc46c1c.json'

@app.route('/')
def index():
    # 画像読み込み
    with open('./static/uploads/image.jpg', 'rb') as image_file:
        content = image_file.read()
    
    # Vision APIへのリクエスト
    image = vision.Image(content=content)
    annotator_client = vision.ImageAnnotatorClient()
    response_data = annotator_client.label_detection(image=image)
    labels = response_data.label_annotations
    
    # ラベルとスコアのリストを作成
    result = []
    for label in labels:
        result.append((label.description, round(label.score * 100, 2)))
    
    # テンプレートに結果を渡して表示
    return render_template('index.html', image_path='/static/image.jpg', result=result)

@app.route('/analyze', methods=['POST'])
def analyze():
    # アップロードされた画像を取得
    uploaded_file = request.files['image']
    if uploaded_file.filename != '':
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(image_path)
        
        # Vision APIへのリクエスト
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        annotator_client = vision.ImageAnnotatorClient()
        response_data = annotator_client.label_detection(image=image)
        labels = response_data.label_annotations
        
        # ラベルとスコアのリストを作成
        result = []
        for label in labels:
            result.append((label.description, round(label.score * 100, 2)))
        
        return render_template('index.html', image_path=image_path, result=result)
    
    return 'No image selected.'

if __name__ == '__main__':
    app.run()



