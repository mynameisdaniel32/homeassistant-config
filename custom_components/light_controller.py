import homeassistant.loader as loader
from homeassistant.components import toggle, light
from homeassistant.helpers.event import track_state_change
#from homeassistant.const import STATE_ON, STATE_OFF

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "light_controller"

# List of component names (string) your component depends upon.
DEPENDENCIES = ['mqtt']


CONF_TOPIC = 'topic'
DEFAULT_TOPIC = 'home-assistant/light_controller'


def setup(homeassistant, config):
#    mqtt = loader.get_component('mqtt')
    mqtt = homeassistant.components.mqtt
    sub_topic = config[DOMAIN].get('topic', DEFAULT_TOPIC)
    #pub_topic = 'node/light_switch/test'
    #pub_test = 'testing'
    entity_id = 'light_controller.last_message'
    light_assign = {}
    button_assign = {}
    button_assign['000-1'] = 'light.study'
    button_assign['000-2'] = 'light.living_1'
    button_assign['000-3'] = 'light.living_2'
    button_assign['000-4'] = 'light.living_3'
    button_assign['000-5'] = 'light.laundry'
    button_assign['000-6'] = 'light.wardrobe'
    button_assign['000-7'] = 'light.bedroom'
    button_assign['000-8'] = 'light.front_door'
    button_assign['001-1'] = 'light.bedroom'
    button_assign['002-1'] = 'light.study'

    brightness_table = {}
    brightness_table[1] = 1
    brightness_table[2] = 0
    brightness_table[3] = 2
    brightness_table[4] = 0
    brightness_table[5] = 3
    brightness_table[6] = 0
    brightness_table[7] = 4
    brightness_table[8] = 0
    brightness_table[9] = 0
    brightness_table[0] = 0
    
    
    # Listener to be called when we receive a message.
    def message_received(topic, payload, qos):
        """MQTT message received"""
#        if 'light_switch' in topic:
        node = topic[-3:]
        button = payload[:1]
        switch_button = node + '-' + button
        homeassistant.states.set(entity_id, node + '-' + payload)
        if 'toggle' in payload:
            toggle(homeassistant, button_assign[switch_button])
        if 'hold' in payload:
            brightness_level = int(payload[-1:])
            if brightness_table[brightness_level] > 0:
                light.turn_on(homeassistant, button_assign[switch_button], brightness = (brightness_table[brightness_level] * 255 / 4))
            
        

    # Function for creating the light assignments dictionary
    def get_light_assignments(d):
        newdict = {}
        for k, v in d.items():
            newdict.setdefault(v, []).append(k)
        return newdict

    def state_change(button_id, old_state, new_state):
        for light_id in light_assign[button_id]:
            if '=on' in str(new_state): 
#                mqtt.publish(homeassistant, sub_topic + light_id[:3], light_id[-1:] + '_led_on')
                mqtt.publish(sub_topic + light_id[:3], light_id[-1:] + '_led_on')
            if '=off' in str(new_state):
#                mqtt.publish(homeassistant, sub_topic + light_id[:3], light_id[-1:] + '_led_off')
                mqtt.publish(sub_topic + light_id[:3], light_id[-1:] + '_led_off')

    # Set the initial state
    homeassistant.states.set(entity_id, 'No messages')

    # Invert the button dictionary to create one for lights
    light_assign = get_light_assignments(button_assign)

    # Subscribe our listener to a topic.
#    mqtt.subscribe(homeassistant, sub_topic + '+', message_received)
    mqtt.subscribe(sub_topic + '+', message_received)

    # Track state changes for all button controlled lights
    track_state_change(homeassistant, list(button_assign.values()), state_change)
    
    # Return boolean to indicate that initialization was successfully.
    return True