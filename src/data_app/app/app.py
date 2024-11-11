from utils.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from models.user_model import db
from sqlalchemy import text
from controllers.pipeline_controller import pipeline_blueprint
from controllers.margin_controller import margin_blueprint
from controllers.view_controller import view_blueprint
from services.clickhouse_client_service import execute_sql_script
from services.cron_service import start_cron_job 
from controllers.substitutes_controller import substitute_blueprint
from controllers.cross_sell_controller import cross_sell_blueprint
from controllers.users_controller import user_blueprint
from controllers.auth_controller import auth_blueprint
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
JWTManager(app)


app.register_blueprint(pipeline_blueprint, url_prefix='/pipeline')
app.register_blueprint(margin_blueprint, url_prefix='/margin')
app.register_blueprint(view_blueprint, url_prefix='/view')
app.register_blueprint(substitute_blueprint, url_prefix='/substitute')
app.register_blueprint(cross_sell_blueprint)
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(user_blueprint, url_prefix='/users')

with app.app_context():
    with open('app/sql/create_user_table.sql', 'r') as f:
        sql_script = f.read()
        db.session.execute(text(sql_script))
    db.session.commit()
    print("Tabela 'user' criada com sucesso!")

if __name__ == '__main__':
    execute_sql_script('app/sql/create_working_table.sql')
    execute_sql_script('app/sql/create_view_margin.sql')
    execute_sql_script('app/sql/create_view_store_regions.sql')
    execute_sql_script('app/sql/create_view_product.sql')
    execute_sql_script('app/sql/create_view_remuneracao_gerente.sql')
    execute_sql_script('app/sql/create_view_stock.sql')
    execute_sql_script('app/sql/create_view_sku_dataset.sql')
    
    start_cron_job()
    app.run(host='0.0.0.0', port=5000)
    