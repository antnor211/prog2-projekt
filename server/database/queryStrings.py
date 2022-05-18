class queryStrings:
    def __init__(self) -> None:
        self.querys = {
        "get_password": "SELECT password FROM users WHERE username=?;",
        "get_balance": "SELECT balance FROM users WHERE session=?;",
        "get_user_by_username": "SELECT * FROM users WHERE username=?;",
        "get_user_by_session": "SELECT * FROM users WHERE session=?;",
        "fetch_game": "SELECT * FROM games WHERE gameSession=?"
        }
        
        self.mutations = {
            "create_user": "INSERT INTO users(username, password, session, balance) VALUES(?, ?, ?, ?);",
            "blackjack_create_game": "INSERT INTO games(gameSession, playerCards, dealerCards, bet) VALUES(?,?,?,?);",
        }
        self.updates = {
            "update_password": "UPDATE users SET password = ? WHERE username=?;",
            "update_session": "UPDATE users SET session=? WHERE username=?;",
            "update_player_cards": "UPDATE games SET playerCards=? WHERE gameSession=?;",
            "update_player_balance": "UPDATE users SET balance=? WHERE session=?;"
        }
        self.deletes = {
            "delete_user": "DELETE FROM users WHERE username=?;",
            "delete_game": "DELETE FROM games WHERE gameSession=?"

        }
    def query(self, command) -> str:
        return self.querys[command]