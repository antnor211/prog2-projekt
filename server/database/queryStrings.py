class queryStrings:
    def __init__(self) -> None:
        self.querys = {
        "create_user": "INSERT INTO users(username, password, session, balance) VALUES({username}, {password}, {session}, {balance});",
        "delete_user": "delete from users where username = {username};",
        "get_password": "select password from users where username is {username};",
        "update_session": "UPDATE users SET session={session} WHERE username={username};",
        "get_balance": "SELECT balance FROM users WHERE username is {username};",
        "blackjack_create_game": "INSERT INTO games(gameSession, playerCards, dealerCards) VALUES({session},{playerCards},{dealerCards});",
        "update_password": "update users set password = {password} where username is {username};",
        "get_user_by_username": "select * from users where username is {username};",
        "get_user_by_session": "select * from users where session is {session};",
        "fetch_game": "select * from games where id is {game_id}"
        }
    def query(self, command) -> str:
        return self.querys[command]