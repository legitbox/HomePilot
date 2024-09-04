![logo](https://github.com/legitbox/HomePilot/blob/main/home_pilot_128.png?raw=true)
# Home Pilot<br>
A simple Home plugin for Endstone servers with Economy Pilot integration<br>

### Features<br>
- multithreaded SQLite database for fast and simple operations<br>
- Economy Pilot integration<br>
- home teleport prices based on distance from home<br>
- customisable home command timeout<br>

### Installation<br>
Drag and drop the .whl file that you can get from releases and put it in your endstone's plugin folder<br>

### File Structure<br>
```
config/
├─ home-pilot.toml
databases/
├─ home-pilot/
│  ├─ home_database.db
```
<br>
- Configuration file `home-pilot.toml`<br>
- Database file `home_database.db`<br>

### Configuration
```toml
# DO NOT TOUCH
config_version = "0.0.1"

# [MAIN]
# sets the home command timeout in seconds
home_timeout = 10

# [ECONOMY]

# if you have the Economy Pilot plugin, you can enable it here
economy_enabled = false

# sets the minimum warp price, before the distance calculation, 0 to disable
min_home_teleport_price = 100
# sets the distance calculation price multiplier, set to 0.0 to disable
home_teleport_price_multiplier = 1.0
```

### Command usage<br>
- Player commands<br><br>
`/sethome` - if executed by the player it will give the players current balance
<br><br>
`/home` - if executed by the player, this command will teleport the user home (it will also deduct some balance from the player if the economy mode is set to true in the config)
<br><br>
`/tprice` - if executed by the player, it will give the user the amount of balance it will cost to teleport back home (only works when the economy mode is set to true in the config)

- Administrator/Server commands [needs op]<br>

  `/delhome <player: str>` - if executed by the server or an administrator, it will remove a players home, <br>for example `/delhome legitbox7811`
<br><br>
