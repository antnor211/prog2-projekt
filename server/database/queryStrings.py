mutate = {
    "create_user": """
    insert into users(firstname, lastname, username, password),
        ({firstname}, {lastname}, {username}, {password});
    """,
    "delete_user": """
    delete from users
    where id = {user_id}
    """
}