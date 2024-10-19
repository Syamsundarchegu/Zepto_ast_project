from flask import Flask, request, jsonify, render_template
import sqlite3
import traceback

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('rules.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the database schema
def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS rules (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        rule_string TEXT NOT NULL
                        )''')
    conn.close()



class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

    def to_dict(self):
        return {
            'type': self.type,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None,
            'value': self.value
        }

def create_rule(rule_string):
    import re
    precedence = {'AND': 2, 'OR': 1}
    tokens = re.findall(r'\w+|\(|\)|>|<|==|!=|\'[^\']+\'', rule_string)

    def parse_expression(tokens):
        stack = []
        op_stack = []

        def apply_operator():
            operator = op_stack.pop()
            right = stack.pop()
            left = stack.pop()
            stack.append(Node(node_type='operator', left=left, right=right, value=operator))

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '(':
                op_stack.append(token)
            elif token == ')':
                while op_stack and op_stack[-1] != '(':
                    apply_operator()
                op_stack.pop()
            elif token in precedence:
                while (op_stack and op_stack[-1] in precedence and
                       precedence[op_stack[-1]] >= precedence[token]):
                    apply_operator()
                op_stack.append(token)
            else:
                if i + 2 < len(tokens) and tokens[i + 1] in ['>', '<', '==', '!=']:
                    operand = token
                    operator = tokens[i + 1]
                    value = tokens[i + 2]
                    i += 2
                    node = Node(node_type='operand', value=f'{operand} {operator} {value}')
                    stack.append(node)
                else:
                    stack.append(Node(node_type='operand', value=token))
            i += 1
        while op_stack:
            apply_operator()
        return stack[0]

    return parse_expression(tokens)

def evaluate_rule(node, data):
    if node.type == 'operator':
        left_value = evaluate_rule(node.left, data)
        right_value = evaluate_rule(node.right, data)
        if node.value == 'AND':
            return left_value and right_value
        elif node.value == 'OR':
            return left_value or right_value
    elif node.type == 'operand':
        attribute, operator, value = node.value.split(maxsplit=2)
        attribute_value = data.get(attribute)
        if attribute_value is None:
            return False
        if operator == '>':
            return float(attribute_value) > float(value)
        elif operator == '<':
            return float(attribute_value) < float(value)
        elif operator == '==':
            return str(attribute_value) == value.strip("'")
        elif operator == '!=':
            return str(attribute_value) != value.strip("'")
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def api_create_rule():
    rule_string = request.json.get('rule_string')
    ast = create_rule(rule_string)
    conn = get_db_connection()
    try:
        print(f'Inserting rule: {rule_string}')

        conn.execute('INSERT INTO rules (rule_string) VALUES (?)', (rule_string,))
        conn.commit()

        rule_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        print(f'Rule ID {rule_id} inserted successfully')
        
        return jsonify({'id': rule_id, 'ast': ast.to_dict()})
    
    except Exception as e:
        print('Error during rule insertion:')
        traceback.print_exc()  # Log the full traceback of the error
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    
    finally:
        conn.close()


@app.route('/get_rule/<int:id>', methods=['GET'])
def get_rule(id):
    conn = get_db_connection()
    rule = conn.execute('SELECT * FROM rules WHERE id = ?', (id,)).fetchone()
    conn.close()
    if rule is None:
        return jsonify({'error': 'Rule not found'}), 404
    ast = create_rule(rule['rule_string'])
    print(f'Rule ID {id} retrieved successfully')
    return jsonify({'id': rule['id'], 'rule_string': rule['rule_string'], 'ast': ast.to_dict()})

@app.route('/evaluate_rule', methods=['POST'])
def api_evaluate_rule():
    rule_string = request.json.get('rule_string')
    print(rule_string)
    data = request.json.get('data')
    ast = create_rule(rule_string)
    result = evaluate_rule(ast, data)
    return jsonify({'result': result})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=3000, host='0.0.0.0')

