# Change your speaker entity_id and exclude_entities
# In order for this to work you windows must have window device_class set and a friendly name

exclude_entities = ['binary_sensor.all_windows']
speaker_entity_id = "media_player.living_room_speaker"
tts_service = "google_translate_say"
open_windows=[]
closed_windows=[]


def check_windows_dynamic():
    for entity_id in hass.states.entity_ids('binary_sensor'):
        state = hass.states.get(entity_id)
        if state.attributes.get('device_class') == 'window' and entity_id not in exclude_entities:    
            entity_status = state.state
            entity_friendly_name = state.attributes.get('friendly_name')
            if entity_status == "on":
                open_windows.append(entity_friendly_name)
            else:
                closed_windows.append(entity_friendly_name)


def create_message():
    if len(open_windows) == 0:
        message = "All Windows are closed"
    elif len(open_windows) == 1:
        message = f"{open_windows} is open"
    else:
        message = f"{open_windows} are open"
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
check_windows_dynamic()
message = create_message()
send_message(message)
check_speaker_idle()
