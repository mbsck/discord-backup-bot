<h1 align="center" style="margin-top: 20px;">Discord Backup Bot</h1>

<p align="center">
<a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.8_|_3.9_|_3.10_|_3.11-3776AB"/>
</a>
<a href="https://opensource.org/license/mit/">
    <img src="https://img.shields.io/badge/license-MIT-yellow"/>
</a>
<a href="https://opensource.org/license/mit/">
    <img src="https://img.shields.io/badge/PRs-welcome-green"/>
</a>
</p>

## Overview
This is an easy to use backup bot to save the state of your discord server and load it at any time.
The bot uses SQLite as its db which makes the install as easy as possible.

## Features
|       Status       |            Feature             |
|--------------------|:-------------------------------|
| :heavy_check_mark: | Cross Server Backups           |
| :heavy_check_mark: | Channel / Category backups     |
|         :x:        | Automatic backups in intervals |
| :heavy_check_mark: | Role backups                   |
|         :x:        | Message backups                |

## Setup
1. Clone the repository
    ```
    git clone https://github.com/icudev/discord-backup-bot.git
    ```
2. Install [`pixi`](https://pixi.prefix.dev/latest/installation/)
3. Install Python and its dependencies into a virtual environment
    ```
    pixi install
    ```
4. Copy `.env.template` to `.env` and insert your discord bot token or
export it in the shell you are`.env` running the bot from with export `DISCORD_BOT_TOKEN=<token>`
5. Run the bot
    ```
    pixi run backup-bot
    ```

    If no database directory is passed with `-o <dir>/--output <dir>`, one
    will be created within the top level of the repository.

## Usage
|   Command name   |         Command description         |
|------------------|-------------------------------------|
| `/backup create` |   Creates a backup of your server   |
| `/backup load`   |    Loads a backup to your server    |
| `/backup delete` | Deletes a backup to save disk space |

## FAQ
> Why is the bot not doing anything when loading a backup?

Make sure that the bot role is above every other and has the following permission:
* Administrator

If that doesn't help it could be because your bot got ratelimited. This happens when
you load a lot of backups in a short amount of time. In that case you just have to wait.
