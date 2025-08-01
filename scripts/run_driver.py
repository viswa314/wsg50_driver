import sys
from wsg50110_driver import WSG50110Driver

def main():
    args = sys.argv[1:]

    if not args:
        print("Usage:")
        print("  python run_driver.py home")
        print("  python run_driver.py calibrate")
        print("  python run_driver.py move <width> <speed>")
        print("  python run_driver.py get_pos")
        print("  python run_driver.py simulate \"COMMAND\"")
        return

    driver = WSG50110Driver()
    command = args[0].lower()

    if command == "home":
        driver.home()

    elif command == "calibrate":
        driver.home()
        driver.calibrate()

    elif command == "move" and len(args) == 3:
        width = float(args[1])
        speed = float(args[2])
        driver.home()
        driver.calibrate()
        driver.move_to_width(width, speed)

    elif command == "get_pos":
        print("Current width:", driver.get_status()["current_width"])

    elif command == "simulate" and len(args) >= 2:
        full_command = " ".join(args[1:])
        response = driver.simulate_gcl_command(full_command)
        print("Response:", response)

    else:
        print("[ERROR] Invalid command or missing arguments.")


if __name__ == "__main__":
    main()
