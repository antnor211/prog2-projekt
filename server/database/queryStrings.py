class queryStrings:
    def __init__(self) -> None:
        self.querys = {
        "create_user": "INSERT INTO users(username, password, session) VALUES({username}, {password}, {session});",
        "delete_user": "delete from users where username = {username};",
        "get_password": "select password from users where username is {username};",
        "update_session": "update users set session = {session} where username is {username};",
        "get_balance": "select balance from users where username is {username};",
        "add_game": """
        insert into games(gameSession, playerCards, dealerCards)
            values ({player}, {player_cards}, {dealer_cards});
        """,        "update_password": """
        update users
        set password = {password}
        where username is {username};
        """,
        "get_user_by_username": """
        select * from users where username is {username};
        """,
        "fetch_game": """
        select * from games
        where id is {game_id}
        """
        }

    def query(self, command) -> str:
        return self.querys[command]