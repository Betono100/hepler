class UserLogin():

    def fromDataBase(self, self_id, db):
        self.__user = db.query.filter_by(login=self_id).first()
        return self

    def create(self, user):
        self.__user = user
        print(user)
        return self

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.__user