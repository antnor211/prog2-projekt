mutate = {
    "create_user": """
    insert into users(username, password)
        values ({username}, {password});
    """,
    "delete_user": """
    delete from users
    where username = {username};
    """    
}


add = {
    "add_game": """
    insert into games(gameSession, playerCards, dealerCards)
        values ({player}, {player_cards}, {dealer_cards});
    """
}


update = {
    "update_password": """
    update users
    set password = {password}
    where username is {username};
    """
}


fetch = {
    "fetch_user": """
    select * from users 
    where username is {username};
    """,
    "fetch_game": """
    select * from games
    where id is {game_id}
    """
}