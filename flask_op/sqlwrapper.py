from flask_op.models import User

user_test = User("test_user")


class SQLWrapper(object):
    def authenticate(self, param):
        return True

    def find_by_login(self, login):
        return user_test

    def init_app(self, app):
        app.sql_backend= self

    """
    Fonctions de l'interface    
    """
    def __setitem__(self, key, value):
        #update db
        pass

    def __getitem__(self, key):
        #find by id
        return user_test

    def __delitem__(self, key):
        # delete by id
        pass

    def __contains__(self, key):
        # find if user exists
        return True

    def items(self):
        # get all users
        return [user_test]

    def pop(self, key, default=None):
        # ???
        pass