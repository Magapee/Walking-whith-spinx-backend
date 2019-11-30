from FlaskTemplate import main_db


class User(main_db.Model):
    id = main_db.Column(main_db.Integer,
                        primary_key=True,
                        index=True,
                        nullable=False)
    username = main_db.Column(main_db.String(64),
                              index=True,
                              unique=True,
                              nullable=False)
    email = main_db.Column(main_db.String(512),
                           index=True,
                           unique=True,
                           nullable=False)
    password_hash = main_db.Column(main_db.String(128),
                                   nullable=False)
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"