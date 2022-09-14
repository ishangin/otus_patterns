import jwt
import db
from models import User, Game


class Auth:
    def __init__(self, user: User):
        self.user = user

    def check_pass(self) -> None:
        db_user = self.get_user()
        if self.user.password == db_user.password:
            self.user = db_user
            self.user.authenticated = True

    def get_user(self) -> User:
        try:
            return User(**list(filter(lambda x: x['login'] == self.user.login, db.USERS))[0])
        except IndexError:
            raise ValueError('User not found')

    def get_jwt(self, game: Game) -> str:
        if not self.user.authenticated:
            raise ValueError('user was not authenticated')
        if self.user.id not in game.players:
            raise ValueError('user is not member of this game')

        token = jwt.encode({self.user.id: self.user.login, game.id: str(game.players)},
                           self.user.password, algorithm="HS256")
        db.GAMES[game.id]['tokens'].append(token)
        return token


if __name__ == '__main__':
    u = User('user0', 'pass0')
    auth = Auth(u)
    auth.check_pass()
    print(u)
