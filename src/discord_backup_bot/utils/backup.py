from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

import discord

PKG_DIR = Path(__file__).parent.parent.parent
CHANNEL_ATTRIBUTE_NAMES = [
    "name",
    "id",
    "nsfw",
    "position",
    "type",
    "overwrites",
    "category_id",
    "permissions_synced",
    "default_auto_archive_duration",
    "default_thread_slowmode_delay",
    "slowmode_delay",
    "bitrate",
    "user_limit",
    "rtc_region",
    "video_quality_mode",
]

ROLE_ATTRIBUTE_NAMES = [
    "name",
    "id",
    "permissions",
    "colour",
    "hoist",
    "display_icon",
    "mentionable",
    "position",
]


def generate_unique_id() -> str:
    """Generates a unique id based off of the current timestamp.

    Returns
    -------
    str
        The unique id.
    """

    return hex(
        int(
            datetime.now().timestamp() * 1000
            - datetime.fromisoformat("2020-01-01").timestamp() * 1000
        )
    )[2:].upper()


class Backup:
    """A class containing a backup.

    Attributes
    ----------
    _id: str
        The unique backup id.
    channels: list of dict, optional
        An optional list of all guild channels in a backup.
    rules_channel: int, optional
        Optional rules channel id of community servers.
    public_updates_channel: int, optional
        Optional updates channel id of community servers.
    roles: list of dict, optional
        An optional list of all guild roles in a backup.
    """

    def __init__(
        self,
        _id: str | None = None,
        channels: list[dict] | None = None,
        rules_channel: int | None = None,
        public_updates_channel: int | None = None,
        roles: list[dict] | None = None,
    ) -> None:

        self._id: str = _id or generate_unique_id()
        self.channels: list[dict] | None = channels
        self.rules_channel: int | None = rules_channel
        self.public_updates_channel: int | None = public_updates_channel
        self.roles: list[dict] | None = roles

    @property
    def id(self) -> str:
        """Returns the backup id."""
        return self._id

    @classmethod
    async def create(cls, guild: discord.Guild) -> "Backup":
        """Creates a backup of a guild

        Parameters
        ----------
        guild : discord.Guild
            The discord server to backup.

        Returns
        -------
        Backup
            The backup.
        """

        roles = [
            await convert_guild_role_to_json(role)
            for role in guild.roles
            if not role.is_bot_managed()
        ]

        for i, role in enumerate(sorted(roles, key=lambda r: r.get("position"))):
            role.update({"position": i})

        return cls(
            channels=[
                convert_guild_channel_to_json(channel) for channel in guild.channels
            ],
            rules_channel=guild.rules_channel.id if guild.rules_channel else None,
            public_updates_channel=guild.public_updates_channel.id
            if guild.public_updates_channel
            else None,
            roles=roles,
        )

    def to_json(self) -> dict[str, Any]:
        """Converts self into a dict object"""
        return self.__dict__


class BackupChannel:
    def __init__(self, **kwargs) -> None:
        self.name = kwargs.get("name")
        self.id = kwargs.get("id")
        self.nsfw = kwargs.get("nsfw")
        self.position = kwargs.get("position")
        self.type = kwargs.get("type")
        self.overwrites = kwargs.get("overwrites")

        self.category_id = kwargs.get("category_id")
        self.permissions_synced = kwargs.get("permissions_synced")

        self.default_auto_archive_duration = kwargs.get("default_auto_archive_duration")
        self.default_thread_slowmode_delay = kwargs.get("default_thread_slowmode_delay")
        self.slowmode_delay = kwargs.get("slowmode_delay")

        self.bitrate = kwargs.get("bitrate")
        self.user_limit = kwargs.get("user_limit")
        self.rtc_region = kwargs.get("rtc_region")
        self.video_quality_mode = kwargs.get("video_quality_mode")

    def to_json(self) -> dict[str, Any]:
        """Converts the class attributes into JSON format."""
        data = {
            "name": self.name,
            "id": self.id,
            "nsfw": self.nsfw,
            "position": self.position,
            "type": self.type,
            "overwrites": self.overwrites,
            "permissions_synced": self.permissions_synced,
        }

        if self.type in [0, 5, 10, 11, 12, 15]:
            data.update(
                {
                    "category_id": self.category_id,
                    "default_auto_archive_duration": self.default_auto_archive_duration,
                    "default_thread_slowmode_delay": self.default_thread_slowmode_delay,
                    "slowmode_delay": self.slowmode_delay,
                }
            )

        elif self.type in [2, 13]:
            data.update(
                {
                    "category_id": self.category_id,
                    "slowmode_delay": self.slowmode_delay,
                    "bitrate": self.bitrate,
                    "user_limit": self.user_limit,
                    "rtc_region": self.rtc_region,
                    "video_quality_mode": self.video_quality_mode,
                }
            )

        return data


def convert_permissionoverwrite_to_list(
    overwrites: dict[
        discord.Role | discord.Member | discord.Object, discord.PermissionOverwrite
    ],
) -> list[dict]:
    """Converts a PermissionOverwrite object to a list.

    Parameters
    ----------
    overwrites: dict of Role, Member, or Object keys and PermissionOverwrite values
        The overwrites which should be converted.

    Returns
    -------
    list
        A list containing dicts for each overwrite.
    """

    return [
        {
            "target_id": target.id,
            "overwrites": overwrite._values,
        }
        for target, overwrite in overwrites.items()
    ]


def extract_attributes_from_class(
    attributes: list[str], _class: Any, convert: dict[str, Callable] | None = None
) -> dict[str, Any]:
    """Extracts the values of the attributes given in `attributes` from the `_class` object.

    Parameters
    ----------
    attributes: list of str
        The list of attribute names you want to extract.
    _class: Any
        The class instance of which the attributes should be extracted.
    convert: dict of str keys and callable values
        Allows to convert the attribute value to something else e.g. {"attribute1": lambda value: value + 1}.

    Returns
    -------
    dict of str keys and any values
        The attributes with their values.
    """

    result = {}

    if _class is None:
        return result

    for attribute in dir(_class):
        if str(attribute) not in attributes:
            continue

        value = getattr(_class, attribute)

        if convert:
            attribute_converter = convert.get(attribute)

            if callable(attribute_converter):
                value = attribute_converter(value)

        result.update({attribute: value})

    return result


def convert_guild_channel_to_json(guild_channel: discord.abc.GuildChannel) -> dict:
    """Converts a server channel to JSON."""
    return extract_attributes_from_class(
        attributes=CHANNEL_ATTRIBUTE_NAMES,
        _class=guild_channel,
        convert={
            "type": lambda type_value: type_value[1],
            "overwrites": lambda overwrites: convert_permissionoverwrite_to_list(
                overwrites
            ),
            "video_quality_mode": lambda video_quality_mode: video_quality_mode[1],
        },
    )


async def convert_guild_role_to_json(guild_role: discord.Role) -> dict:
    """Converts a server role to JSON."""
    raw_guild_role = extract_attributes_from_class(
        attributes=ROLE_ATTRIBUTE_NAMES,
        _class=guild_role,
        convert={
            "colour": lambda colour: list(colour.to_rgb()),
            "permissions": lambda permissions: permissions.value,
        },
    )

    # FIXME: Poor implementation of image saving, but it works (somehow).
    if (dis_icon := raw_guild_role.get("display_icon")) is not None:
        dis_icon_file = PKG_DIR / "assets" / f"{dis_icon.key}.png"
        dis_icon_file.parent.mkdir(exist_ok=True, parents=True)
        with open(dis_icon_file, "wb") as role_image_file:
            role_image_file.write(await dis_icon.read())

        raw_guild_role.update({"display_icon": dis_icon.key})

    return raw_guild_role
