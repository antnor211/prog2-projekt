class DBStrings:
    def __init__(self) -> None:
        self.querys = {
            "getPassword": "SELECT password FROM users WHERE username=?;",
            "getBalance": "SELECT balance FROM users WHERE session=?;",
            "getUserByUsername": "SELECT * FROM users WHERE username=?;",
            "getUserBySession": "SELECT * FROM users WHERE session=?;",
            "fetchGame": "SELECT * FROM games WHERE gameSession=?",
        }
        
        self.mutations = {
            "createUser": "INSERT INTO users(username, password, session, balance) VALUES(?, ?, ?, ?);",
            "blackjackCreateGame": "INSERT INTO games(gameSession, playerCards, dealerCards, bet) VALUES(?,?,?,?);",
        }
        self.updates = {
            "updatePassword": "UPDATE users SET password = ? WHERE username=?;",
            "updateSession": "UPDATE users SET session=? WHERE username=?;",
            "updatePlayerCards": "UPDATE games SET playerCards=? WHERE gameSession=?;",
            "updatePlayerBalance": "UPDATE users SET balance=? WHERE session=?;",
        }
        self.deletes = {
            "deleteUser": "DELETE FROM users WHERE username=?;",
            "deleteGame": "DELETE FROM games WHERE gameSession=?",

        }
    def query(self, command) -> str:
        return self.querys[command]