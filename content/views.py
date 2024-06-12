import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
import asyncio
from pyrcrack import AirmonNg, AirodumpNg
from rich.console import Console
import pandas as pd
from django.views.decorators.csrf import csrf_exempt

from content.models import DeviceData






def index(request):
    devices = DeviceData.objects.all()
    print(devices)
    devices = sorted([{
            "mac": device.mac,
            "dbms": device.dbms,
            "location": device.location,
            "under_attack": device.under_attack,
            "timestamp": device.timestamp,
            # extra can be added
        }
        for device in devices
    ], key=lambda x: x['timestamp'], reverse=True)

    info = {
        "numof_attacked_devices": DeviceData.objects.filter(under_attack=1).count(),
        "current_time": datetime.datetime.now(),
    }
    
    return render(request, 'index.html', {'devices': devices, 'info': info})

        

@csrf_exempt # disabling the security mechanism to avoid (CSRF cookie not set.) error.
def update_output_info(request):
    # print(request)
    if request.method == 'POST':
        # Deserialize the JSON data received from the request
        data = json.loads(request.body)
        print(data)
        data = eval(data)
        # Extract necessary fields
        mac = data.get('mac')
        dbms = data.get('dbms')
        location = data.get('location')
        timestamp = data.get('timestamp')
        under_attack = data.get('under_attack')
    
        # Check if a record with the same MAC address already exists
        try:
            device = DeviceData.objects.get(mac=mac)
            # Update the existing record
            device.dbms = dbms
            device.location = location
            device.timestamp = timestamp
            device.under_attack = under_attack
            device.save()
        except DeviceData.DoesNotExist:
            # Create a new record
            DeviceData.objects.create(mac=mac, dbms=dbms, location=location, under_attack=under_attack, timestamp=timestamp)

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


async def start_scan(request):
    # await scan_for_targets()
    
    return redirect(index)

def update_table(request):
    ...
    # with open("asd.html", "r") as f:
    #     content = f.readlines()
    # return JsonResponse({'content': content})


async def scan_for_targets():
    console = Console(record=True)
    console.clear()
    console.show_cursor(False)
    airmon = AirmonNg()

    # interface = Prompt.ask(
    #     'Select an interface',
    #     choices=[a.interface for a in await airmon.interfaces])
    interface = [a.interface for a in await airmon.interfaces][0]

    async with airmon(interface) as mon:
        async with AirodumpNg() as pdump:
            async for result in pdump(mon.monitor_interface):
                console.clear()
                content = result.table
                console.print(content)
                console.save_html("asd.html", inline_styles=True)
                await asyncio.sleep(3)
