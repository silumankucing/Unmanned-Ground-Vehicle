from machine import Pin, PWM, ADC
from time import sleep

# --- Motor Setup ---
ENA = PWM(Pin(12), freq=15000)  # Left Motor PWM
IN1 = Pin(14, Pin.OUT)
IN2 = Pin(27, Pin.OUT)

ENB = PWM(Pin(13), freq=15000)  # Right Motor PWM
IN3 = Pin(26, Pin.OUT)
IN4 = Pin(25, Pin.OUT)

# --- Sensor Setup ---
vibration_sensor = Pin(32, Pin.IN)  # SW-420 Vibration Sensor (Digital)
sound_sensor = ADC(Pin(34))         # KY-038 Sound Sensor (Analog)
sound_sensor.atten(ADC.ATTN_11DB)   # Full range (0-3.3V)

# --- Thresholds ---
SOUND_THRESHOLD = 2500  # Adjust based on testing
VIBRATION_THRESHOLD = 1  # 1 = Detected, 0 = Not Detected

def motor_control(motor, direction, speed=100):
    """Control motor direction and speed."""
    speed = min(max(speed, 0), 100)
    pwm_duty = int(speed * 10.23)  # 0-100 → 0-1023
    
    if motor == 'A':
        ENA.duty(pwm_duty)
        if direction == 'forward':
            IN1.on()
            IN2.off()
        elif direction == 'backward':
            IN1.off()
            IN2.on()
        else:  # stop
            IN1.off()
            IN2.off()
    
    elif motor == 'B':
        ENB.duty(pwm_duty)
        if direction == 'forward':
            IN3.on()
            IN4.off()
        elif direction == 'backward':
            IN3.off()
            IN4.on()
        else:  # stop
            IN3.off()
            IN4.off()

# --- Main Loop ---
while True:
    # Read sensors
    vibration = vibration_sensor.value()
    sound_level = sound_sensor.read()  # 0-4095
    
    print(f"Vibration: {vibration}, Sound: {sound_level}")
    
    # Trigger motors based on sensors
    if vibration == VIBRATION_THRESHOLD:
        print("Vibration detected! Motors forward at 80% speed.")
        motor_control('A', 'forward', 80)
        motor_control('B', 'forward', 80)
        sleep(2)  # Run for 2 seconds
        motor_control('A', 'stop')
        motor_control('B', 'stop')
    
    elif sound_level > SOUND_THRESHOLD:
        print("Loud sound detected! Motors backward at 60% speed.")
        motor_control('A', 'backward', 60)
        motor_control('B', 'backward', 60)
        sleep(1)  # Run for 1 second
        motor_control('A', 'stop')
        motor_control('B', 'stop')
    
    sleep(0.1)  # Small delay to avoid flooding serial monitor