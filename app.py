import requests
import subprocess
import os
import logging
from icalendar import Calendar
from datetime import datetime, date, time, timedelta

# Logging setup. You must input a log file location.

log_file = "/dir/location/app.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Here are where the file locations will be input. It is recommended to use absolute paths instead of relative ones.

ffmpegLoc = "" # Location of ffmpeg binary
textFile = "/dir/location/upcoming.txt" # Location to save the intermediate text file
inputFile = "/dir/location/ComingSoonTemplate.mp4" # Input file. This is the video you want to use as the background.
outputFile = "/dir/location/ComingSoon.mp4" # This is the location where the final video is saved.
iCalURL = "http://..." # This is the URL to retrieve Radarr ical file.
fontFile = "/dir/location/arial.ttf" # This is the location of the font file.

# Here are the parameters for the text overlayed onto the video. The defaults are what works in my setup.
# fontsize: fontsize in pixels
# fontcolor: Usable strings can be found here: https://ffmpeg.org/ffmpeg-utils.html#color-syntax
# x: The x coordinate for the top-left of the text area
# y: The y coordinate for the top-left of the text area
# startTime: The time of the video (in seconds) the text appears
# endTime: The time of the video (in seconds) the text disappears

fontSize = 70
fontColor = "white"
x = 300
y = 150
startTime = 5
endTime = 13
lineSpacing = 10
centerText = False

if centerText:
    x = "(w-text_w)/2"
    y = "(h-text_h)/2"

# Fetching of ical file

def fetch_ical_data(url):
    response = requests.get(url)
    response.raise_for_status()
    logging.info("Fetched iCal data successfully")
    return response.text

# Checking if just a date and makes the object a datetime object for downsteam operations

def normalize_dt(dt):
    if isinstance(dt, date) and not isinstance(dt, datetime):
        return datetime.combine(dt, time.min)
    return dt

# Parsing of the ical file to create a filtered list of upcoming digital releases

def ical_to_filtered_list(ical_data):
    calendar = Calendar.from_ical(ical_data)
    events = []
    today = datetime.now()

    for component in calendar.walk():
        if component.name == "VEVENT":
            dtstart = normalize_dt(component.get('dtstart').dt)
            if dtstart > today:
                summary = str(component.get('summary'))
                logging.info(f"Analyzing: {summary} {dtstart}")
                if "Digital Release" in summary:
                    cleaned_summary = summary.replace(" (Digital Release)", "")
                    dtstart_str = dtstart.strftime("%m/%d/%Y")
                    events.append((cleaned_summary, dtstart_str))
                    logging.info(f"Processing {cleaned_summary}")
                else:
                    logging.info("Not a digital release")
    
    events.sort(key=lambda x: datetime.strptime(x[1], "%m/%d/%Y"))
    return events

# Writes the list to the intermediate file.

def write_to_file(events, filename):
    with open(filename, "w") as file:
        for summary, dtstart in events:
            file.write(f"{dtstart} - {summary}\n") # You can edit this line to format how you desire. {dtstart} is the release date and {summary} is the movie title.
    logging.info(f"Wrote {len(events)} events to {filename}")

# This is the running of the ffmpeg command. It takes in the intermediate file and overlays the text onto the video.

def run_ffmpeg_command():
    command = (
        f"{ffmpegLoc}ffmpeg -y -i {inputFile} -vf "
        f"\"drawtext=textfile={textFile}:fontfile={fontFile}:fontsize={fontSize}:fontcolor={fontColor}:x={x}:y={y}:line_spacing={lineSpacing}:enable='between(t,{startTime},{endTime})'\" "
        f"-c:a copy {outputFile}"
    )
    subprocess.run(command, shell=True, check=True)
    logging.info("FFmpeg command executed successfully")

# If there are no upcoming movies the Coming Soon video will not be made and the existing one will be deleted. This is because software (ex: Plex) will not show anything
# if the file doesn't exist. Delete lines 121 thru 123 if you do not want this function to run.

def delete_file_if_no_events(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        logging.info(f"Deleted file {filepath} because there were no events")

# The main function

def main():
    try:
        ical_data = fetch_ical_data(iCalURL)
        events = ical_to_filtered_list(ical_data)
        
        write_to_file(events, textFile)
        
        if events:
            run_ffmpeg_command()
        else:
            delete_file_if_no_events(outputFile)
            logging.info("There are no upcoming movies to process")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

