mutate = {
    "create_user": """
    insert into users(firstname, lastname, username, password),
        ({firstname}, {lastname}, {username}, {password});
    """,
    "delete_user": """
    delete from users
    where username = {username};
    """    
}

update = {
    "update_password": """
    update users
    set password = {password}
    where username is {username};
    """,
    "update_name": """
    update users
    set firstname = {firstname},
        lastname = {lastname}
    where username is {username};
    """
}

fetch = {
    "fetch_user": """
    select * from users 
    where username is {username};
    """
}