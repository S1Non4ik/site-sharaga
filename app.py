from flask import Flask, render_template, jsonify, send_from_directory, request, redirect, url_for
from psycopg2 import Error
import psycopg2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'static/man_photo'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def get_db_connection():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="g,adfgi9hm",  
            host="localhost",
            port="5432",
            database="user_counter",
            client_encoding='UTF-8'  
        )
        return connection
    except (Exception, Error) as error:
        print("Ошибка при подключении к PostgreSQL:", error)
        return None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/<path:path>')
def send_file(path):
    return send_from_directory(app.static_folder, path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/add_sneaker', methods=['POST'])
def add_sneaker():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        category = request.form['category']
        price = request.form['price']
        description = request.form['description']
        
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400
            
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f'man_photo/{filename}'
            
            connection = get_db_connection()
            if connection is None:
                return jsonify({'error': 'Не удалось подключиться к базе данных'}), 500
                
            try:
                cur = connection.cursor()
                cur.execute(
                    "INSERT INTO sneakers (brand, model, category, price, image_path, description) VALUES (%s, %s, %s, %s, %s, %s)",
                    (brand, model, category, price, image_path, description)
                )
                connection.commit()
                cur.close()
                return jsonify({'message': 'Товар успешно добавлен'}), 201
            except (Exception, Error) as error:
                print("Ошибка при добавлении товара:", error)
                return jsonify({'error': 'Не удалось добавить товар'}), 500
            finally:
                connection.close()
        else:
            return jsonify({'error': 'Недопустимый формат файла'}), 400

@app.route('/api/sneakers')
def get_sneakers():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Не удалось подключиться к базе данных'}), 500
        
    try:
        cur = connection.cursor()
        cur.execute("SELECT * FROM sneakers ORDER BY created_at DESC")
        sneakers = cur.fetchall()
        cur.close()
        
        sneakers_list = []
        for sneaker in sneakers:
            sneakers_list.append({
                'id': sneaker[0],
                'brand': sneaker[1],
                'model': sneaker[2],
                'category': sneaker[3],
                'price': float(sneaker[4]),
                'image_path': sneaker[5],
                'description': sneaker[6],
                'created_at': sneaker[7].strftime('%Y-%m-%d %H:%M:%S')
            })
            
        return jsonify(sneakers_list)
    except (Exception, Error) as error:
        print("Ошибка при получении товаров:", error)
        return jsonify({'error': 'Не удалось получить список товаров'}), 500
    finally:
        connection.close()

@app.route('/api/visit', methods=['POST'])
def visit():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Не удалось подключиться к базе данных'}), 500
    try:
        cur = connection.cursor()
        cur.execute("UPDATE user_count SET count = count + 1;")
        connection.commit()
        cur.close()
        return jsonify({'message': 'Пользователь учтен'})
    except (Exception, Error):
        return jsonify({'error': 'Не удалось обновить счетчик пользователей'}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)