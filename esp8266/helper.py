import machine
trigger_type = {}
trigger_type['on'] = machine.Pin.IRQ_RISING
trigger_type['off'] = machine.Pin.IRQ_FALLING
trigger_type['any'] = machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING

state_changed = ''
