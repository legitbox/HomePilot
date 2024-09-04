import sqlite3

from endstone_home_pilot.config import check_config, load_config
from endstone import ColorFormat
from pathlib import Path
from datetime import datetime

check_config()


directory_path = Path('databases/home-pilot/')

if not directory_path.exists():
    directory_path.mkdir(parents=True, exist_ok=True)

def check_main_table():
    connection = sqlite3.connect(f'{directory_path}/home_database.db')
    cursor = connection.cursor()
    command = """
    CREATE TABLE IF NOT EXISTS database(
    uuid TEXT PRIMARY KEY,
    username TEXT,
    coordinate_x INTEGER,
    coordinate_y INTEGER,
    coordinate_z INTEGER,
    last_used INTEGER
    );
    """
    cursor.execute(command)
    connection.commit()
    connection.close()

def check_user_data(uuid, username):
    connection = sqlite3.connect(f'{directory_path}/home_database.db')
    cursor = connection.cursor()
    command = """
    INSERT OR IGNORE INTO database (uuid, username)
    VALUES (?, ?);
    """
    cursor.execute(command, (str(uuid), str(username)))
    connection.commit()
    connection.close()

def check_player_username_for_change(uuid, unchecked_username):
    connection = sqlite3.connect(f'{directory_path}/home_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM database WHERE uuid = ?;", (str(uuid),))

    database_username = str(cursor.fetchone()).replace("(", "").replace(")", "").replace(",", "")
    if database_username != unchecked_username:
        cursor.execute("""
        UPDATE database
        SET username = ?
        WHERE uuid = ?;
        """, (str(unchecked_username), str(uuid)))

    connection.commit()
    connection.close()

def set_home(username, coordinate_x, coordinate_y, coordinate_z) -> str:
    connection = sqlite3.connect(f'{directory_path}/home_database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT EXISTS(SELECT 1 FROM database WHERE username = ?)", (str(username),))
    reciever_exists = int(cursor.fetchone()[0])
    if reciever_exists == 0:
        return_string = f"{ColorFormat.RED}This user isnt logged in the database{ColorFormat.RESET}"
        connection.close()
        return return_string

    return_message = f"{ColorFormat.GOLD}your home coordinates were set to {ColorFormat.AQUA}x:{coordinate_x} y:{coordinate_y} z:{coordinate_z}{ColorFormat.RESET}"

    dateof2000 = datetime(2000, 1, 1, 0, 0, 0)
    dateofnow = datetime.now()

    time_difference = dateofnow - dateof2000
    total_seconds = time_difference.total_seconds()

    cursor.execute("UPDATE database SET coordinate_x = ? WHERE username = ?;", (int(coordinate_x), str(username)))
    cursor.execute("UPDATE database SET coordinate_y = ? WHERE username = ?;", (int(coordinate_y), str(username)))
    cursor.execute("UPDATE database SET coordinate_z = ? WHERE username = ?;", (int(coordinate_z), str(username)))
    cursor.execute("UPDATE database SET last_used = ? WHERE username = ?;", (int(total_seconds), str(username)))

    return_message = f"{ColorFormat.GOLD}Your home coordinates were set to {ColorFormat.AQUA}x:{int(coordinate_x)} y:{int(coordinate_y)} z:{int(coordinate_z)}{ColorFormat.RESET}"


    connection.commit()
    connection.close()
    return return_message

def get_home(username):
    connection = sqlite3.connect(f'{directory_path}/home_database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT coordinate_x FROM database WHERE username = ?;", (str(username),))
    coordinate_x = str(cursor.fetchone()).replace("(", "").replace(")", "").replace(",", "")
    cursor.execute("SELECT coordinate_y FROM database WHERE username = ?;", (str(username),))
    coordinate_y = str(cursor.fetchone()).replace("(", "").replace(")", "").replace(",", "")
    cursor.execute("SELECT coordinate_z FROM database WHERE username = ?;", (str(username),))
    coordinate_z = str(cursor.fetchone()).replace("(", "").replace(")", "").replace(",", "")

    dateof2000 = datetime(2000, 1, 1, 0, 0, 0)
    dateofnow = datetime.now()

    time_difference = dateofnow - dateof2000
    total_seconds = time_difference.total_seconds()

    cursor.execute("UPDATE database SET last_used = ? WHERE username = ?;", (int(total_seconds), str(username)))


    connection.commit()
    connection.close()

    return coordinate_x, coordinate_y,  coordinate_z

def get_home_no_cooldown(username):
    connection = sqlite3.connect(f'{directory_path}/home_database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT coordinate_x FROM database WHERE username = ?;", (str(username),))
    coordinate_x = str(cursor.fetchone()).replace("(", "").replace(")", "").replace(",", "")
    cursor.execute("SELECT coordinate_y FROM database WHERE username = ?;", (str(username),))
    coordinate_y = str(cursor.fetchone()).replace("(", "").replace(")", "").replace(",", "")
    cursor.execute("SELECT coordinate_z FROM database WHERE username = ?;", (str(username),))
    coordinate_z = str(cursor.fetchone()).replace("(", "").replace(")", "").replace(",", "")

    connection.commit()
    connection.close()

    return coordinate_x, coordinate_y,  coordinate_z

def get_last_home_usage(username):
    connection = sqlite3.connect(f'{directory_path}/home_database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT last_used FROM database WHERE username = ?;", (str(username),))
    last_time_used = int(str(cursor.fetchone()).replace("(", "").replace(")", "").replace(",", ""))

    connection.commit()
    connection.close()
    return last_time_used

def delete_home(username):
    connection = sqlite3.connect(f'{directory_path}/home_database.db')
    cursor = connection.cursor()

    return_message = f"{ColorFormat.GOLD}home of the player {ColorFormat.GREEN}{username}{ColorFormat.RESET}{ColorFormat.GOLD} has been removed from the database{ColorFormat.RESET}"

    cursor.execute("SELECT EXISTS(SELECT 1 FROM database WHERE username = ?)", (str(username),))
    reciever_exists = int(cursor.fetchone()[0])
    if reciever_exists == 0:
        return_string = f"{ColorFormat.RED}This user isnt logged in the database{ColorFormat.RESET}"
        connection.close()
        return return_string

    cursor.execute("UPDATE database SET coordinate_x = '' WHERE username = ?;", (str(username),))
    cursor.execute("UPDATE database SET coordinate_y = '' WHERE username = ?;", (str(username),))
    cursor.execute("UPDATE database SET coordinate_z = '' WHERE username = ?;", (str(username),))

    connection.commit()
    connection.close()
    return return_message


### ECONOMY PILOT FUNCTIONS

directory_path_eco = Path('databases/economy-pilot/')
def server_balance_fetch(username) -> str:
    connection = sqlite3.connect(f'{directory_path_eco}/database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT EXISTS(SELECT 1 FROM database WHERE username = ?)", (str(username),))
    reciever_exists = int(cursor.fetchone()[0])
    if reciever_exists == 0:
        return_string = f"{ColorFormat.RED}This user isnt logged in the database{ColorFormat.RESET}"
        connection.close()
        return return_string

    cursor.execute("SELECT money FROM database WHERE username = ?;", (str(username),))
    return_string = str(cursor.fetchone()).replace("(", "").replace(")", "").replace(",", "")
    connection.commit()
    connection.close()

    return return_string