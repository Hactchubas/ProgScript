from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

def init_db():
    """Inicializa o banco de dados"""
    conn = sqlite3.connect('counter.db')
    c = conn.cursor()
    
    # Cria tabela para armazenar valores e suas contagens
    c.execute('''
        CREATE TABLE IF NOT EXISTS value_counts (
            value TEXT PRIMARY KEY,
            count INTEGER,
            last_updated TIMESTAMP
        )
    ''')
    
    # Cria tabela para log de histórico
    c.execute('''
        CREATE TABLE IF NOT EXISTS value_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT,
            timestamp TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_count(value):
    """Obtém a contagem atual para um valor"""
    conn = sqlite3.connect('counter.db')
    c = conn.cursor()
    
    c.execute('SELECT count FROM value_counts WHERE value = ?', (value,))
    result = c.fetchone()
    
    conn.close()
    return result[0] if result else 0

def update_count(value):
    """Atualiza a contagem para um valor"""
    conn = sqlite3.connect('counter.db')
    c = conn.cursor()
    
    current_time = datetime.now().isoformat()
    
    # Atualiza ou insere na tabela de contagens
    c.execute('''
        INSERT INTO value_counts (value, count, last_updated)
        VALUES (?, 1, ?)
        ON CONFLICT(value) DO UPDATE SET
            count = count + 1,
            last_updated = ?
    ''', (value, current_time, current_time))
    
    # Adiciona entrada no histórico
    c.execute('''
        INSERT INTO value_history (value, timestamp)
        VALUES (?, ?)
    ''', (value, current_time))
    
    conn.commit()
    
    # Obtém a contagem atualizada
    count = get_count(value)
    
    conn.close()
    return count

@app.route('/count', methods=['POST'])
def count_value():
    try:
        data = request.get_json()
        value = str(data.get('value'))
        
        if not value:
            return jsonify({
                'status': 'error',
                'message': 'Valor não pode ser vazio'
            }), 400
        
        count = update_count(value)
        
        return jsonify({
            'status': 'success',
            'count': count,
            'message': f'Valor "{value}" recebido com sucesso'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# Novo endpoint para obter histórico
@app.route('/history/<value>', methods=['GET'])
def get_value_history(value):
    try:
        conn = sqlite3.connect('counter.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT timestamp
            FROM value_history
            WHERE value = ?
            ORDER BY timestamp DESC
            LIMIT 10
        ''', (value,))
        
        history = [row[0] for row in c.fetchall()]
        conn.close()
        
        return jsonify({
            'status': 'success',
            'value': value,
            'history': history
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# Inicializa o banco de dados quando o servidor iniciar
init_db()

if __name__ == '__main__':
    app.run(debug=True)