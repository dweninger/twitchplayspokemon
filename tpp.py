import time
import os
from dotenv import load_dotenv
from twitchio.ext import commands
import win32api
import win32con

load_dotenv()
token = os.getenv('TWITCH_OAUTH_TOKEN')
channel = os.getenv('CHANNEL_NAME')

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=token, prefix='!',
                         initial_channels=[channel],
                         case_insensitive=True)
        self.create_directional_commands()

    async def event_ready(self):
        print(f'Logged in as {self.nick}')

    async def event_message(self, message):
        # Check for command with or without "!"
        if message.content.startswith('!'):
            await self.handle_commands(message)
        else:
            # If command does not have "!" prefix, trigger anyway
            message.content = f'!{message.content}'
            await self.handle_commands(message)

    def press_key(self, key):
        key_map = {
            'up': 0x57,     # W
            'down': 0x53,   # S
            'left': 0x41,   # A
            'right': 0x44,  # D
            'a': 0x58,      # X
            'b': 0x43,      # C
            'l': 0x4C,      # L
            'r': 0x52,      # R
            'select': 0xBC, # ','
            'start': 0xBE   # '.'
        }
        
        if key in key_map:
            vk_key = key_map[key]
            win32api.keybd_event(vk_key, 0, 0, 0)  # Key down
            time.sleep(0.1)  # Key press duration
            win32api.keybd_event(vk_key, 0, win32con.KEYEVENTF_KEYUP, 0)  # Key up
        else:
            raise ValueError(f"Invalid key: {key}")
        
    def repeat_key_press(self, key, times):
        try:
            for _ in range(times):
                self.press_key(key)
                time.sleep(0.1)
        except ValueError as e:
            print(e)

    def create_directional_commands(self):
        directions = ['up', 'down', 'left', 'right']
        for direction in directions:
            command_name = f'{direction}'
            self.create_command(command_name, direction, 1)
            # Allow commands of <direction>[number] from 1-4
            for i in range(1, 5):
                command_name = f'{direction}{i}'
                self.create_command(command_name, direction, i)

    def create_command(self, command_name, direction, repeat_count):
        async def command_func(ctx):
            self.repeat_key_press(direction, repeat_count)

        command_func.__name__ = f'{command_name}_command'
        self.add_command(commands.Command(name=command_name, func=command_func))
   
    # Non-directional commands
    @commands.command(name='a')
    async def a_command(self, ctx):
        self.press_key('a')

    @commands.command(name='b')
    async def b_command(self, ctx):
        self.press_key('b')

    @commands.command(name='l')
    async def l_command(self, ctx):
        self.press_key('l')

    @commands.command(name='r')
    async def r_command(self, ctx):
        self.press_key('r')

    @commands.command(name='select')
    async def select_command(self, ctx):
        self.press_key('select')

    @commands.command(name='start')
    async def start_command(self, ctx):
        self.press_key('start')
        
    @commands.command(name='help')
    async def help_command(self, ctx):
        commands_list = """
        Available commands:  up[1-4], down[1-4], left[1-4], right[1-4], a, b, l, r, select, start   [optional]
        """
        await ctx.send(commands_list)

    @commands.command(name='howto')
    async def howto_command(self, ctx):
        message = """
        Check out my blog post where I explain how I made this Twitch Plays Pokemon script: https://daniel-weninger.com/blog/simple-tpp-script/
        """
        await ctx.send(message)

bot = Bot()
bot.run()
