# Asteria
A custom discord bot :D

 - Forked from Pandora to separate CTFtime functionality


## Usage
Use `help` (with prefix) to see commands in Discord.

 - `help`: shows this command
 - `ping`: ping the bot
 - `ctftime` (or `ctf`): grab some information about a CTF from CTFtime
 - `ctfnow`: grab some information about current ongoing CTFs
 

The bot owner is also able to use the following commands:
 - `list`: list all the guilds that the bot is part of
 - `bail`: leave a guild
 - `sleep`: shut down the bot
This allows the bot to be removed from a server without the owner being part of said server.



## Setup
To run your own instance of Asteria, you will need some extra files in the project's `src/` directory.

### Files

`src/env` with
```env
DISCORD_TOKEN=[Discord token here]
```

`src/variables.py` with
```py
class botVars:
    prefix = [prefix]
    owner = [numerical Discord ID]
```
The prefix should be a single character used as the prefix for bot commands.

Then, run `docker build -t asteria .` to build the docker image, and `docker run asteria` to run pandora.

Alternatively, to run without docker, install dependences 

### Program Dependencies

Install `screen`
```bash
sudo apt install screen
```

#### Python Dependencies

If you don't have python3 and pip already, install them
```bash
sudo apt install python-is-python3 python3-pip
```

Install python dependencies
```bash
pip install discord.py python-dotenv feedparser
```

Then run `run.sh`
```bash
chmod +x run.sh
./run.sh
```

Generate a discord bot invite URL on the applications page and invite to a server. 
