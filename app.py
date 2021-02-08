from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#configuracion base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD']='NO'
app.config['MYSQL_DB'] = 'flask_contacts'
myssql = MySQL(app)

#session
app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    cur = myssql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', miscontactos=data)


@app.route('/add_contacto', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = myssql.connection.cursor()
        cur.execute(
            'INSERT INTO contacts (fullname,phone,email) VALUES (%s,%s,%s)',
            (fullname, phone, email))
        myssql.connection.commit()
        message = flash('Contacto agregado correctamente')
        return redirect(url_for('index'))


@app.route('/edit_contact/<id>')
def get_contact(id):
    cur = myssql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id ={0}'.format(id))
    data = cur.fetchall()
    # message=flash('Contacto editado correctamente')
    return render_template('edit_contact.html', contact=data[0])


@app.route('/delete_contact/<string:id>')
def delete_contact(id):
    cur = myssql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id={0}'.format(id))
    myssql.connection.commit()
    message = flash('Contacto eliminado correctamente')
    return redirect(url_for('index'))


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
    cur = myssql.connection.cursor()
    cur.execute(
        """
    UPDATE contacts
    SET fullname=%s,
    phone=%s,
    email=%s
    WHERE id=%s
    """, (fullname, phone, email, id))
    myssql.connection.commit()
    message = flash('Contacto actualizado correctamente')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(port=3000, debug=True)
