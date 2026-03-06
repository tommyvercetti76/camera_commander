import os

# Helper function to print colored text
def color_text(text, color):
    colors = {"green": '\033[92m', "cyan": '\033[96m', "yellow": '\033[93m', "reset": '\033[0m', "magenta": '\033[95m'}
    return colors.get(color, colors["reset"]) + text + colors["reset"]

# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Show menu and get selection
def show_menu(options, title, selected_item=None):
    clear_screen()
    print(color_text(f"✨📸 Welcome to Kamera Quest CLI 📸✨", "magenta"))
    if selected_item:
        print(color_text(f"\n✅ Selected: {selected_item}", "green"))
    print(color_text(f"\n📸 {title}", "cyan"))
    print(color_text('-'*60, 'yellow'))
    for idx, option in enumerate(options, 1):
        print(f"[{idx}] {option}")
    print(f"[0] Go Back")
    print(color_text('-'*60, 'yellow'))

    choice = input("Enter your choice: ")
    return int(choice)

# Conditions selection
def select_conditions():
    conditions = {
        'Lighting': ['Golden Hour', 'Midday', 'Night', 'Indoor'],
        'Weather': ['Clear', 'Cloudy', 'Rain', 'Snow'],
        'Stability': ['Handheld', 'Tripod']
    }
    selected_conditions = {}

    for condition, options in conditions.items():
        while True:
            clear_screen()
            print(color_text(f"Select condition for {condition}", "cyan"))
            print(color_text('-'*40, 'yellow'))
            for idx, opt in enumerate(options, 1):
                print(f"[{idx}] {opt}")
            choice = int(input(f"Select {condition} (0 to go back): "))

            if choice == 0:
                return None
            if 1 <= choice <= len(options):
                selected_conditions[condition] = options[choice-1]
                break

    return selected_conditions

# Main CLI Flow
def main(cameras, lenses_for_camera):
    selected_camera, selected_lens = None, None

    # Camera Selection
    while True:
        camera_choice = show_menu(cameras, "Choose Your Camera", selected_camera)
        if camera_choice == 0:
            print("Exiting Kamera Quest CLI.")
            return
        if 1 <= camera_choice <= len(cameras):
            selected_camera = cameras[camera_choice - 1]
            break

    # Lens Selection
    compatible_lenses = lenses_for_camera.get(selected_camera, [])
    while True:
        lens_choice = show_menu(compatible_lenses, "Compatible Lenses", selected_lens)
        if lens_choice == 0:
            selected_camera = None
            return main(cameras, lenses_for_camera)
        if 1 <= lens_choice <= len(compatible_lenses):
            selected_lens = compatible_lenses[lens_choice - 1]
            break

    # Condition Selection
    conditions = select_conditions()
    if conditions is None:
        return main(cameras, lenses_for_camera)

    # Display Final Selection
    clear_screen()
    print(color_text("✨📸 Kamera Quest Summary 📸✨", "magenta"))
    print(color_text('-'*40, 'yellow'))
    print(color_text(f"Camera: {selected_camera}", "green"))
    print(color_text(f"Lens: {selected_lens}", "green"))
    for cond, value in conditions.items():
        print(color_text(f"{cond}: {value}", "cyan"))
    print(color_text('-'*40, 'yellow'))

    input("\nPress any key to confirm and exit...")


# Example usage
cameras = ["Canon EOS-1D X Mark II", "Canon EOS 5D Mark IV", "Canon EOS 80D"]
lenses_for_camera = {
    "Canon EOS-1D X Mark II": ["Canon EF 16-35mm f/2.8L III USM", "Canon EF 24-105mm f/4L IS II USM"],
    "Canon EOS 5D Mark IV": ["Canon EF 24-105mm f/4L IS II USM"],
    "Canon EOS 80D": ["Canon EF-S 18-135mm f/3.5-5.6 IS USM"]
}

main(cameras, lenses_for_camera)