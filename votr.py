from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(votr, name='Dashboard')
admin.add_view(ModelView(Users, db.session))