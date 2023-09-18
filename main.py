import simplekml
import csv
from datetime import datetime, timedelta
import os
import subprocess
import gpxpy
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext  # Added for scrolled text widget
from tkinter import PhotoImage
from PIL import ImageTk, Image
from io import BytesIO
import base64


# Function to open Google Earth Pro with a KML file
def open_google_earth(kml_file):
    google_earth_path = r'C:\Program Files\Google\Google Earth Pro\client\googleearth.exe'
    subprocess.Popen([google_earth_path, kml_file])

# Function to find the closest GPS point based on timestamp
def find_closest_gps_point(gpx, target_timestamp):
    closest_point = None
    min_time_diff = float('inf')  # Initialize with positive infinity

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # Ensure both timestamps are offset-naive
                point_time_naive = point.time.replace(tzinfo=None)
                target_timestamp_naive = target_timestamp.replace(tzinfo=None)
                
                time_diff = abs((point_time_naive - target_timestamp_naive).total_seconds())
                
                if time_diff < min_time_diff:
                    min_time_diff = time_diff
                    closest_point = point

    return closest_point

# Function to handle the "Generate KML" button click
def generate_kml():
    # Get file paths, offset, and output file name from the GUI inputs
    gpx_file_path = gpx_file_entry.get()
    csv_file_path = csv_file_entry.get()
    offset_str = offset_entry.get()
    output_file_name = output_file_entry.get()  # Get the output file name

    # Check if the offset input is empty
    if not offset_str:
        offset = 0  # Default to no offset if input is empty
    else:
        try:
            offset = int(offset_str)  # Convert to integer if not empty
        except ValueError:
            # Handle invalid input (non-integer)
            offset = 0  # Default to no offset if input is not a valid integer

    # Load your music events from the CSV file
    music_events = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            music_events.append(row)

    # Initialize a KML document
    kml = simplekml.Kml()

    # Load and parse your .GPX data
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

        # Iterate through your music events
        for music_event in music_events:
            timestamp_str = music_event.get('timestamp', '')  # Get timestamp or empty string
            if not timestamp_str:
                continue  # Skip empty timestamps
            
            artist = music_event.get('artist', '')
            song_title = music_event.get('song_title', '')

            timestamp = datetime.strptime(timestamp_str, "%d %b %Y, %H:%M")

            # Offset the timestamp based on the provided offset (in seconds)
            offset_timestamp = timestamp + timedelta(seconds=offset)

            # Find the closest GPS data point in your .GPX data based on the offset timestamp
            closest_point = find_closest_gps_point(gpx, offset_timestamp)

            # Create a placemark at the matched GPS coordinates
            if closest_point:
                placemark = kml.newpoint(
                    name=f"{artist} - {song_title}",
                    coords=[(closest_point.longitude, closest_point.latitude)],
                )

    # Set the default output file name if left blank
    if not output_file_name:
        output_file_name = "music_events.kml"

    # Save the KML file with the specified output file name
    kml_file_path = output_file_name
    kml.save(kml_file_path)

    # Open Google Earth Pro with the generated KML file
    open_google_earth(kml_file_path)

# Function to display the About dialog
def show_about_dialog():
    about_text = "Mark's Strava Music Map Generator\nVersion 1.0\n\nCopyright (c) 2023 Mark Joudrey"
    tk.messagebox.showinfo("About", about_text)

# Function to display the "How to use" dialog
def show_how_to_use_dialog():
    how_to_use_text = "1. Select a .GPX file and a .CSV file using the Browse buttons.\n"
    how_to_use_text += "2. Enter an optional offset in seconds (e.g., -30 or 0).\n"
    how_to_use_text += "3. Click the 'Generate KML' button to create the KML file.\n"
    how_to_use_text += "4. Optionally, enter an output file name or leave it blank to use the default.\n"
    how_to_use_text += "5. Click 'Generate KML' to create the KML file and open it in Google Earth Pro."
    messagebox.showinfo("How to Use", how_to_use_text)

# Function to display the Photoshop Help message
def show_photoshop_help_dialog():
    photoshop_help_text = (
        "1) File > Save > Save Image (CTRL + ALT + S) in Google Earth of the following 3:\n\n"
        " - Plain map (no GPX/music data)\n"
        " - Music KML data (generated from this script) + green-screen overlay\n"
        " - GPX data only\n\n"
        "2) In Photoshop, use 'Select > Color Range,' and eye-drop the green color. "
        "Get closer to the text and use more eye-dropping to edge out the closer-to-font shades of green.\n\n"
        "3) Edit your privacy zone working with the multiple layers in Photoshop."
    )
    messagebox.showinfo("Photoshop Help", photoshop_help_text)

# Function to display the CSV formatting message
def show_csv_formatting_dialog():
    csv_formatting_text = "Required columns order: artist | song_title | timestamp"
    messagebox.showinfo("CSV Formatting", csv_formatting_text)

# Function to display information about the Last.FM Scrobble Recorder
def show_lastfm_scrobble_recorder_info():
    lastfm_info_text = (
        "By default, when using 'last.fm data export', it sorts music with your last played song at the top.\n\n"
        "When displaying this on your Strava, you would want chronological order.\n\nLast.FM Scrobble Recorder, "
        "reads the CSV file from 'last.fm data export' and sorts accordingly."
    )
    tk.messagebox.showinfo("Last.FM Scrobble Recorder", lastfm_info_text)

# Function to gracefully exit the application
def exit_application():
    # Clean up resources or perform any necessary tasks
    root.destroy()  # Close the main window


# Function to create and configure a new window with GUI elements
def create_new_window():
    new_window = tk.Tk()
    new_window.title("Mark's Strava Music Map Generator")
    
    # Add GUI elements for the new window (similar to your existing code)
    # For example, you can add labels, entry fields, buttons, etc.

    # Make sure to configure the new window's layout and functionality
    # based on your application's requirements.

    return new_window


# Create a global variable for the sorted list text widget
sorted_list_text = None

# Function to open the Last.FM Scrobble Recorder window
def open_scrobble_recorder():
    global sorted_list_text  # Make sorted_list_text accessible globally
    
    # Create a new window for the Last.FM Scrobble Recorder
    scrobble_window = tk.Toplevel(root)
    scrobble_window.title("Last.FM Scrobble Recorder")

    # Make the new window a child of the main window
    scrobble_window.transient(root)

    # Add a button to open the music .csv file in the Scrobble Recorder window
    open_csv_button = tk.Button(scrobble_window, text="Open Music .CSV File", command=open_music_csv)
    open_csv_button.pack()

    # Create a scrolled text widget to display the sorted list
    sorted_list_text = scrolledtext.ScrolledText(scrobble_window, width=50, height=20)
    sorted_list_text.pack()

    # Add a button to copy the sorted list to the clipboard
    copy_button = tk.Button(scrobble_window, text="Copy to Clipboard", command=lambda: copy_to_clipboard(scrobble_window, sorted_list_text))
    copy_button.pack()

# Function to handle opening the music .csv file
def open_music_csv():
    global sorted_list_text  # Make sorted_list_text accessible globally
    
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # Create a list to store the reversed "artist - song" entries
            reversed_entries = []

            for row in csv_reader:
                artist = row.get('artist', '')
                song_title = row.get('song_title', '')

                # Reversed "artist - song" entry
                reversed_entry = f"{song_title} - {artist}"
                reversed_entries.insert(0, reversed_entry)  # Insert at the beginning to reverse the order

            # Display the reversed entries in the scrolled text widget
            reversed_entries_text = '\n'.join(reversed_entries)
            sorted_list_text.insert('1.0', reversed_entries_text)  # Insert the reversed list into the scrolled text widget

# Function to copy the sorted list to the clipboard
def copy_to_clipboard(window, text_widget):
    # Get the content of the sorted list text widget
    sorted_list_content = text_widget.get("1.0", "end-1c")
    
    # Copy the content to the clipboard
    window.clipboard_clear()
    window.clipboard_append(sorted_list_content)
    window.update()  # Needed to ensure clipboard data is up to date

# Create the main GUI window
root = tk.Tk()
root.title("Mark's Strava Music Map Generator")  # Set the window title

# Add code to read the base64-encoded icon from a file
def read_base64_from_file(file_path):
    try:
        # Read the base64-encoded string from the file
        with open(file_path, "r") as file:
            icon_base64 = file.read()
        return icon_base64
    except FileNotFoundError:
        return None

# Read the base64 string from the file "base64_string.txt"
base64_file_path = "base64_string.txt"
icon_base64 = read_base64_from_file(base64_file_path)

# If the icon_base64 is not None, decode it and set the application icon
if icon_base64:
    # Decode the base64 string into image data
    icon_data = base64.b64decode(icon_base64)

    # Create a BytesIO object to work with the image data
    icon_stream = BytesIO(icon_data)

    # Create an Image object using PIL
    icon_image = Image.open(icon_stream)

    # Convert the PIL Image to a PhotoImage
    icon_photo = ImageTk.PhotoImage(image=icon_image)

    # For Tkinter:
    root.iconphoto(True, icon_photo)


# Get the screen dimensions using tkinter
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the window size as a percentage of the screen dimensions
window_width_fraction = 0.2  # Adjust this fraction as needed
window_height_fraction = 0.4  # Adjust this fraction as needed

# Set the window size
root.geometry(f"{int(screen_width * window_width_fraction)}x{int(screen_height * window_height_fraction)}")

# Configure the row and column weights for responsive layout
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_rowconfigure(7, weight=1)
root.grid_rowconfigure(8, weight=1)
root.grid_rowconfigure(9, weight=1)
root.grid_rowconfigure(10, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create and place GUI elements
gpx_file_label = tk.Label(root, text="Select .GPX file:")
gpx_file_label.grid(row=0, column=0, sticky="w")
gpx_file_entry = tk.Entry(root)
gpx_file_entry.grid(row=1, column=0, sticky="ew")
gpx_file_button = tk.Button(root, text="Browse", command=lambda: gpx_file_entry.insert(0, filedialog.askopenfilename()))
gpx_file_button.grid(row=1, column=1)

csv_file_label = tk.Label(root, text="Select .CSV file:")
csv_file_label.grid(row=2, column=0, sticky="w")
csv_file_entry = tk.Entry(root)
csv_file_entry.grid(row=3, column=0, sticky="ew")
csv_file_button = tk.Button(root, text="Browse", command=lambda: csv_file_entry.insert(0, filedialog.askopenfilename()))
csv_file_button.grid(row=3, column=1)

offset_label = tk.Label(root, text="Offset (seconds):")
offset_label.grid(row=4, column=0, sticky="w")
offset_entry = tk.Entry(root)
offset_entry.grid(row=5, column=0, sticky="ew")

# Add an input field for the output file name with a default value
output_file_label = tk.Label(root, text="Output File Name:")
output_file_label.grid(row=6, column=0, sticky="w")
output_file_entry = tk.Entry(root)
output_file_entry.grid(row=7, column=0, sticky="ew")
output_file_entry.insert(0, "music_events.kml")  # Set default value

generate_button = tk.Button(root, text="Generate KML", command=generate_kml)
generate_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Add padding to your widgets
gpx_file_label.grid(row=0, column=0, padx=10, pady=10)
csv_file_label.grid(row=2, column=0, padx=10, pady=10)
offset_label.grid(row=4, column=0, padx=10, pady=10)
output_file_label.grid(row=6, column=0, padx=10, pady=10)

gpx_file_entry.grid(row=1, column=0, padx=10, pady=10)
csv_file_entry.grid(row=3, column=0, padx=10, pady=10)
offset_entry.grid(row=5, column=0, padx=10, pady=10)
output_file_entry.grid(row=7, column=0, padx=10, pady=10)

generate_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Increase padding for some widgets
gpx_file_label.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="w")
csv_file_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky="w")
offset_label.grid(row=4, column=0, padx=(10, 0), pady=10, sticky="w")
output_file_label.grid(row=6, column=0, padx=(10, 0), pady=10, sticky="w")

# Adjust column weights to control expansion
root.grid_columnconfigure(0, weight=1)  # Increase weight for the leftmost column
root.grid_columnconfigure(1, weight=1)

# Make the browse buttons expand to fill their cells
gpx_file_button.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="ew")
csv_file_button.grid(row=3, column=1, padx=(0, 10), pady=10, sticky="ew")

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create a File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New Window", command=create_new_window)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)  # Exit the application

# Add the "Last.FM Scrobble Recorder" option that opens the window
menu_bar.add_command(label="Last.FM Scrobble Recorder", command=open_scrobble_recorder)

# Create a Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="How to use", command=show_how_to_use_dialog)
help_menu.add_command(label="CSV Formatting", command=show_csv_formatting_dialog)
help_menu.add_command(label="Last.FM Scrobble Recorder", command=show_lastfm_scrobble_recorder_info)
help_menu.add_command(label="Photoshop Help", command=show_photoshop_help_dialog)
help_menu.add_command(label="About", command=show_about_dialog)

# Use protocol to bind the exit_application function to the window's close button
root.protocol("WM_DELETE_WINDOW", exit_application)

# Start the GUI event loop
root.mainloop()
