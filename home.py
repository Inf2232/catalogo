from flask import Flask, render_template, url_for, redirect, request, flash
from peewee import *
import base64
# Configuración

db = SqliteDatabase("catalogo.db")

# Modelos
class Media(db.Model):
    id = IntegerField(primary_key=True)
    tipo = CharField()
    titulo =CharField()
    fecha_salida = IntegerField()
    descripcion = CharField()
    foto = BlobField()
class Meta:
    database = db
#crear tablas
db.create_tables([Media])

def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

app = Flask(__name__, template_folder="template", static_folder="static")
app.config['UPLOAD_FOLDER'] = 'static/imagenes'
app.jinja_env.filters['b64encode'] = b64encode_filter

# Rutas
@app.route('/')
def home():
    return render_template("index.html")
@app.route("/admin/")
def admin():
    peliculas = Media.select().where(Media.tipo == 'Pelicula')
    series = Media.select().where(Media.tipo == 'Serie')
    novelas = Media.select().where(Media.tipo == "Novela")
    return render_template("admin.html" ,peliculas=peliculas , series=series,novelas=novelas)
@app.route("/agregar")
def agregar():
    return render_template ("agregar.html")

@app.route("/append", methods=['GET','POST'])
def agregar_catalogo():
    if request.method == 'POST':
        foto = request.files["foto_media"]
        if foto and allowed_file(foto.filename):
            # Lee los datos del archivo de imagen
            foto_data=foto.read()
            media = Media(
                tipo=request.form["tipo_media"],
                titulo=request.form["nombre_media"],
                fecha_salida=request.form["anio_media"],
                descripcion=request.form["descripcion_media"],
                foto=foto_data
            )
            media.save()
            
            return redirect(url_for("admin"))
    return render_template("agregar.html")
# Asegúrate de tener una función para verificar el tipo de archivo subido
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Asegúrate de tener una función para manejar nombres de archivo seguros
def secure_filename(filename):
    from werkzeug.utils import secure_filename
    return secure_filename(filename)
    return render_template("agregar.html")
@app.route('/eliminar/<int:id>', methods=["GET"])
def eliminar(id):
    try:
        
        media = Media.get(Media.id == id)
        # Eliminar la película de la base de datos
        media.delete_instance()
        # Redirigir al usuario de vuelta a la página de inicio
        return redirect(url_for("admin"))
    except media.DoesNotExist:
        # Si la película no existe, devolver un mensaje de error
        return 'La Media no existe'
@app.route("/exportar/")
    

@app.route('/peliculas/')
def peliculas():
    peliculas = Media.select().where(Media.tipo == 'Pelicula')
    return render_template("peliculas.html", peliculas=peliculas) 
@app.route('/series/')
def series():
    series = Media.select().where(Media.tipo == 'Serie')
    return render_template("series.html", series=series)
@app.route('/novelas/')
def novelas():
    novelas = Media.select().where(Media.tipo == "Novela")
    return render_template("novelas.html" , novelas=novelas)
@app.route('/other/')
def otros():
    return render_template ("other.html")
@app.route('/detalles/<int:id>')
def detalles(id):
    media= Media.get_or_none(Media.id == id)
    if media is None:
        return "Media no encontrada", 404
    return render_template("detalles.html", media=media)

if __name__ == '__main__':
   app.run(debug=True)
    
