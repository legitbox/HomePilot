from locale import currency
from pathlib import Path

from endstone.plugin import Plugin
from endstone.event import event_handler, PlayerJoinEvent
from endstone.event import PlayerTeleportEvent
from endstone.command import Command, CommandSender
from endstone import ColorFormat, Player
from datetime import datetime
import math

from endstone_home_pilot.config import load_config, check_config, load_config_eco
from endstone_home_pilot.database_controller import check_main_table, set_home, get_home, get_last_home_usage, \
    delete_home, server_balance_fetch, get_home_no_cooldown
from endstone_home_pilot.database_controller import check_user_data, check_player_username_for_change
version = "0.0.1"

check_config()
config = load_config()
home_timeout = config[0]
economy_enabled = config[1]
min_home_teleport_price = config[2]
home_teleport_price_multiplier = config[3]
currency = load_config_eco()

class Main(Plugin):
    api_version = "0.5"

    commands = {
        "sethome": {
            "description": "This command sets the home of the user",
            "usages": ["/sethome"],
            "permissions": ["home_pilot.command.sethome"]
        },
        "home": {
            "description": "This command teleports the user to his home",
            "usages": ["/home"],
            "permissions": ["home_pilot.command.home"]
        },
        "tprice": {
            "description": "This command tells the user how much money will his teleportation cost",
            "usages": ["/tprice"],
            "permissions": ["home_pilot.command.tprice"]
        },
        "delhome": {
            "description" : "This command removes the home, meant for administrator use",
            "usages": ["/delhome <username: str>"],
            "permissions": ["home_pilot.command.delhome"]
        }
    }
    permissions = {
        "home_pilot.command.sethome": {
            "description": "Allows the users to use the sethome command",
            "default": True
        },
        "home_pilot.command.home": {
            "description": "Allows the users to use the home command",
            "default": True
        },
        "home_pilot.command.delhome": {
            "description": "Allows the users to use the delhome command",
            "default": "op"
        },
        "home_pilot.command.tprice": {
            "description": "Allows the users to use the tprice command",
            "default": True
        }
    }

    def on_enable(self):
        self.register_events(self)

    def  on_load(self):
        self.logger.info(f"""
        {ColorFormat.GOLD}
         ╱|、
        (` - 7
        |、⁻〵
        じしˍ,)ノ
        HOME PILOT, version - {version} 
        By Lunatechnika studios
        {ColorFormat.RESET}
        """)
        self.logger.info(f"{ColorFormat.GOLD}Home Pilot has been loaded :3{ColorFormat.RESET}")
        self.logger.info(f"{ColorFormat.GOLD}Checking Database...{ColorFormat.RESET}")
        data_location = self.data_folder

        check_main_table()

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent):
        player = event.player
        self.logger.info(f"{ColorFormat.GOLD}Home Pilot is checking user's {ColorFormat.GREEN}{player.name}{ColorFormat.RESET} {ColorFormat.GOLD}records on the database{ColorFormat.RESET}")
        check_user_data(player.unique_id, player.name)
        check_player_username_for_change(player.unique_id, player.name)

    def on_command(self, sender: Player, command: Command, args: list[str]):
        match command.name:
            case "sethome":
                if sender.name == "Server":
                    sender.send_message(f"{ColorFormat.RED}This command can only be ran by a player{ColorFormat.RESET}")
                else:
                    player = sender.name
                    player_location_x = sender.location.x
                    player_location_y = sender.location.y
                    player_location_z = sender.location.z
                    sender.send_message(f"{set_home(player, player_location_x, player_location_y, player_location_z)}")
            case "home":
                if sender.name == "Server":
                    sender.send_message(f"{ColorFormat.RED}This command can only be ran by a player{ColorFormat.RESET}")
                else:
                    player = sender.name

                    dateof2000 = datetime(2000, 1, 1, 0, 0, 0)
                    dateofnow = datetime.now()
                    time_difference = dateofnow - dateof2000
                    time_seconds_now = time_difference.total_seconds()

                    last_used_seconds = get_last_home_usage(player)

                    if int(time_seconds_now - last_used_seconds) < home_timeout:
                        sender.send_message(f"{ColorFormat.GOLD}You still have to wait for {ColorFormat.LIGHT_PURPLE}{home_timeout - int(time_seconds_now - last_used_seconds)}{ColorFormat.GOLD} seconds until you can use this command again{ColorFormat.RESET}")

                    else:
                        home_location = get_home(player)
                        if home_location[0] == "''" or home_location[1] == "''" or home_location[2] == "''":
                            sender.send_message(f"{ColorFormat.RED}You haven't set your home yet! do that by using /sethome{ColorFormat.RESET}")
                        else:
                            if economy_enabled == False:
                                self.server.dispatch_command(self.server.command_sender,f"effect {player} blindness 3 100 true")
                                self.server.dispatch_command(self.server.command_sender, f"teleport {player} {int(home_location[0])} {int(home_location[1])} {int(home_location[2])}")
                                sender.send_message(f"{ColorFormat.GOLD}You have been teleported to home{ColorFormat.RESET}")
                            if economy_enabled == True:
                                location_x = int(sender.location.x)
                                location_z = int(sender.location.z)

                                home_location = get_home_no_cooldown(sender.name)
                                home_location_x = int(home_location[0])
                                home_location_z = int(home_location[2])

                                distance = int(math.sqrt(math.pow(location_x - home_location_x, 2)+ pow(location_z - home_location_z, 2)))

                                player_balance = int(server_balance_fetch(sender.name))
                                if player_balance >= int(min_home_teleport_price + distance * home_teleport_price_multiplier):
                                    self.server.dispatch_command(self.server.command_sender,f"serverdeduct {player} {int(min_home_teleport_price + distance * home_teleport_price_multiplier)}")
                                    self.server.dispatch_command(self.server.command_sender,f"effect {player} blindness 3 100 true")
                                    self.server.dispatch_command(self.server.command_sender,f"teleport {player} {int(home_location[0])} {int(home_location[1])} {int(home_location[2])}")
                                    sender.send_message(f"{ColorFormat.GOLD}You have been teleported to home for {ColorFormat.AQUA}{int(min_home_teleport_price + distance * home_teleport_price_multiplier)}{currency}{ColorFormat.RESET}")
                                else:
                                    sender.send_message(f"{ColorFormat.RED}You need at least {ColorFormat.AQUA}{int(min_home_teleport_price + distance * home_teleport_price_multiplier)}{currency}{ColorFormat.RESET} to teleport back to home!{ColorFormat.RESET}")
            case "delhome":
                sender.send_message(f"{delete_home(str(args[0]))}")
            case "tprice":
                if economy_enabled:
                    location_x = int(sender.location.x)
                    location_z = int(sender.location.z)

                    home_location = get_home_no_cooldown(sender.name)
                    home_location_x = int(home_location[0])
                    home_location_z = int(home_location[2])

                    if home_location[0] == "''" or home_location[1] == "''" or home_location[2] == "''":
                        sender.send_message(f"{ColorFormat.RED}You haven't set your home yet! do that by using /sethome{ColorFormat.RESET}")
                    else:
                        distance = int(math.sqrt(math.pow(location_x - home_location_x, 2)+ pow(location_z - home_location_z, 2)))
                        sender.send_message(f"{ColorFormat.GOLD}You can be teleported home for {ColorFormat.AQUA}{int(min_home_teleport_price + distance * home_teleport_price_multiplier)}{currency}{ColorFormat.RESET}")
                else:
                    sender.send_message(f"{ColorFormat.RED}You cannot use this feature until Economy Pilot support is enabled!{ColorFormat.RESET}")



