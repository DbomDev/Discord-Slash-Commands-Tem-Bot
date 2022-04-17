# Disocrd Slash Commands Bot Template
Here you go guys. A standard slash commands bot template which I use regularly to start new Bots.

## MUST HAVE STANDARD LISTS & FUNCTIONS
### Standard Lists
```python
colors_list = {
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_NAVY': 0x2C3E50
}

option_types={
    "SUB_COMMAND":1,
    "SUB_COMMAND_GROUP":2,
    "STRING":3,
    "INTEGER":4,
    "BOOLEAN":5,
    "USER":6,
    "CHANEL":7,
    "ROLE":8
}
```

### Standard Functions & Events
```python

# Standard Functions & Events
async def all_guilds_func():
    for guild in client.guilds:
        id = guild.id
        guild_ids.append(id)

@client.event
async def on_ready():
    await all_guilds_func()
    print(f"ALl Guild Id's\n{guild_ids}")

    print("\n---------\n")
    print(f"Logged in as {client.user}")
    print("\n---------\n")
```

## Credits
Credits are required because I have invested much time in making this Standard Bot.
```md
[ Credits ]( DbomDev )
```
