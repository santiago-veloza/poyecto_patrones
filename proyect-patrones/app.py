from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from db_singleton import DatabaseSingleton
from models import User
from strategies import TrabajadorStrategy, JefeStrategy, ClienteStrategy, RoleContext

# Singleton para base de datos
db = DatabaseSingleton.get_db()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Configurar LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)
            # Aplicar estrategia según el rol
            if user.role == 'trabajador':
                context = RoleContext(TrabajadorStrategy())
            elif user.role == 'jefe':
                context = RoleContext(JefeStrategy())
            elif user.role == 'cliente':
                context = RoleContext(ClienteStrategy())
            else:
                return "⚠️ Rol no reconocido"

            return context.redirect_user(user)
        else:
            return "❌ Usuario o contraseña incorrectos"

    return render_template('login.html')

@app.route('/trabajador')
@login_required
def trabajador_dashboard():
    return render_template('trabajador.html', user=current_user)

@app.route('/jefe')
@login_required
def jefe_dashboard():
    return render_template('jefe.html', user=current_user)

@app.route('/cliente')
@login_required
def cliente_dashboard():
    return render_template('cliente.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Inicializar base de datos
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.first():
            db.session.add(User(username='juan', password='123', role='trabajador'))
            db.session.add(User(username='ana', password='123', role='jefe'))
            db.session.add(User(username='mario', password='123', role='cliente'))
            db.session.commit()
    app.run(debug=True)
