import json
import random
import serial
import time

def generate_random_json():
    """Generates random values and returns a JSON-like dictionary."""
    humidities = [random.randint(0, 99) for _ in range(16)]
    temperatures =  [random.randint(0, 99) for _ in range(144)]
    voltages =  [random.randint(0, 99) for _ in range(144)]
    pec_errors = [random.randint(0, 15) for _ in range(16)]
    balancing = [random.randint(0, 1) for _ in range(144)]
    accumulator_info = { # Example data
        "Ams_Error": str(random.choice([0, 1])),
        "Imd_Error": str(random.choice([0, 1])),
        "AIR_P_Supp": str(random.choice([0, 1])),
        "AIR_M_Supp": str(random.choice([0, 1])),
        "AIR_P_State": str(random.choice([0, 1])),
        "AIR_M_State": str(random.choice([0, 1])),
        "over60_dclink": str(random.choice([0, 1])),
        "dc_dc_temp": "{:.4f}".format(random.uniform(0, 100)),
        "HVroom_humidity": str(random.randint(0, 100)),
        "precharge_voltage": "{:.4f}".format(random.uniform(0, 800)),
        "AIR_P_State_Int": str(random.choice([0, 1]))
    }

    isabelle_info = {
        "V_Side_Voltage": "{:.1f}".format(random.uniform(0, 800)),
        "Current": "{:.2f}".format(random.uniform(0, 100)),
        "Ah_consumed": "{:.3f}".format(random.uniform(0, 50)),
        "Energy Consumed": str(random.randint(0, 500))
    }

    elcon_info = {
        "Target_Voltage": "{:.1f}".format(random.uniform(0, 800)),
        "Output_Voltage": "{:.1f}".format(random.uniform(0, 800)),
        "Target_Current": "{:.1f}".format(random.uniform(0, 100)),
        "Output_Current": "{:.1f}".format(random.uniform(0, 100)),
        "Elcon_connected": str(random.choice([0, 1])),
        "Elcon_AC_input_OK": str(random.choice([0, 1])),
        "CANBUS_Error": str(random.choice([0, 1])),
        "Target_charge_state": str(random.choice([0, 1])),
        "Elcon_charge_status": str(random.choice([0, 1])),
        "Elcon_overtemp": str(random.choice([0, 1]))
    }
    w = random.randint(0, 7)
    if(w == 0): data = {"AccumulatorInfo": accumulator_info}
    if(w == 1): data = {"Isabelle Info": isabelle_info}
    if(w == 2): data = {"Elcon Info": elcon_info}
    if(w == 3): data = {"Humidities": humidities}
    if(w == 4): data = {"Temperatures": temperatures}
    if(w == 5): data = {"Voltages": voltages}
    if(w == 6): data = {"PEC_Errors": pec_errors}
    if(w == 7): data = {"Balancing": balancing}

    return data

def send_json_via_serial(data, port, baudrate=9600):
    """Sends the JSON data via serial port."""
    try:
        ser = serial.Serial(port, baudrate, timeout=1)  # Adjust timeout as needed
        json_string = json.dumps(data) + '\n'  # Add newline for easy parsing
        ser.write(json_string.encode('utf-8'))
        time.sleep(0.1)  # Small delay to ensure all data is sent
        ser.close()
        print(f"JSON data sent to {port}")

    except serial.SerialException as e:
        print(f"Error: Could not open serial port {port}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    serial_port = "COM2"  # Example: Adjust to your Android's COM port
    while(True):
        random_data = generate_random_json()
        # You might need to use /dev/ttyACM0, /dev/ttyS0, etc.
        # Check your android device to find the correct port.
        send_json_via_serial(random_data, serial_port)