import subprocess

def get_cpu_temperature_windows():
    command = "wmic /namespace:\\\\root\\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature"
    output = subprocess.check_output(command, shell=True).decode('utf-8').strip()
    temperature = int(output.split('=')[1].strip()) / 10.0 - 273.15
    return temperature

try:
    cpu_temp = get_cpu_temperature_windows()
    print(f"CPU Temperature: {cpu_temp} °C")
except Exception as e:
    print(f"Failed to retrieve CPU temperature: {e}")
