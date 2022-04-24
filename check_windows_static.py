windows_map = [ 
'binary_sensor.bathroomwindow',
'binary_sensor.bedroomwindow',
'binary_sensor.kitchenwindow',
'binary_sensor.livingroomwindow',
'binary_sensor.studiowindow',
'binary_sensor.studiowindowbalcony'
]

speaker_entity_id = "media_player.living_room_speaker"
tts_service = "google_translate_say"
open_windows=[]
closed_windows=[]


def check_windows():
    for window in windows_map:
        name = hass.states.get(window)
        if name.state == "on":
            open_windows.append(name.attributes.get('friendly_name'))
        else:
            closed_windows.append(name.attributes.get('friendly_name'))

def create_message():
    if len(open_windows) == 0:
        message = "All Windows are closed"
        logger.info(message)
    elif len(open_windows) == 1:
        message = f"{open_windows} is open"
        logger.info(message)
    else:
        message = f"{open_windows} are open"
        logger.info(message) 
    return message   

def send_message(message):
    service_data = {'message':message, 'entity_id': speaker_entity_id}
    hass.services.call('tts', tts_service, service_data)


def check_speaker_idle():
    finished = False
    loopcount = 0
    while not finished or loopcount > 3:
        state = hass.states.get(speaker_entity_id)
        if state.state == "idle" or state.state == "off":
            finished = True
            break
        else:
            time.sleep(.50)
            loopcount = loopcount + 1


check_speaker_idle()
check_windows()
message = create_message()
send_message(message)
check_speaker_idle()
