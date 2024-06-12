import asyncio

import pyrcrack

from rich.console import Console
from rich.prompt import Prompt


async def scan_for_targets():
    """Scan for targets, return json."""
    console = Console(record=True)
    console.clear()
    console.show_cursor(False)
    airmon = pyrcrack.AirmonNg()

    interface = [a.interface for a in await airmon.interfaces][0]


    async with airmon(interface) as mon:
        async with pyrcrack.AirodumpNg() as pdump:
            async for result in pdump(mon.monitor_interface):
                console.clear()
                console.print(result.table)
                console.save_html("asd.html")
                await asyncio.sleep(2)


asyncio.run(scan_for_targets())
