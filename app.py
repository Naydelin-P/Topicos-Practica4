from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"  

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="control_lista"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        return None

@app.route('/')
def home():
    conn = get_db_connection()
    if conn is None:
        flash("Error al conectar a la base de datos", "danger")
        return render_template('index.html', alumnos=[])

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM lista")
        alumnos = cursor.fetchall()
        cursor.close()
    except mysql.connector.Error as e:
        flash(f"Error en la consulta: {e}", "danger")
        alumnos = []
    finally:
        conn.close()

    return render_template('index.html', alumnos=alumnos)


@app.route('/add', methods=['POST'])
def add():
    nombres = request.form['nombres'].strip()
    apellidos = request.form['apellidos'].strip()
    edad = request.form['edad'].strip()

    if not nombres or not apellidos or not edad:
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for('home'))

    if not edad.isdigit():
        flash("La edad debe ser un número", "danger")
        return redirect(url_for('home'))

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO lista (nombres, apellidos, edad) VALUES (%s, %s, %s)", (nombres, apellidos, edad))
            conn.commit()
            cursor.close()
            flash("✅ Alumno agregado exitosamente", "success")
        except mysql.connector.Error as e:
            flash(f"Error al agregar alumno: {e}", "danger")
        finally:
            conn.close()

    return redirect(url_for('home'))
    
    @app.route('/update/<int:id>', methods=['POST'])
def update(id):
    nombres = request.form['nombres'].strip()
    apellidos = request.form['apellidos'].strip()
    edad = request.form['edad'].strip()

    if not nombres or not apellidos or not edad:
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for('home'))

    if not edad.isdigit():
        flash("La edad debe ser un número", "danger")
        return redirect(url_for('home'))

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE lista SET nombres=%s, apellidos=%s, edad=%s WHERE id=%s", 
                           (nombres, apellidos, edad, id))
            conn.commit()
            cursor.close()
            flash("🔄 Alumno actualizado exitosamente", "info")
        except mysql.connector.Error as e:
            flash(f"Error al actualizar alumno: {e}", "danger")
        finally:
            conn.close()

    return redirect(url_for('home'))


@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM lista WHERE id=%s", (id,))
            conn.commit()
            cursor.close()
            flash("🗑️ Alumno eliminado exitosamente", "warning")
        except mysql.connector.Error as e:
            flash(f"Error al eliminar alumno: {e}", "danger")
        finally:
            conn.close()
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
