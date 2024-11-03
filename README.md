# coming-soon

## Notes

This is a Python script for generating a "Coming Soon" pre-roll using data from Radarr (Radarr must be in use to use this script).

The way it works is it grabs the current iCal calendar from Radarr, then parses through the data to find upcoming digital releases and creates an intermediate text file listing the releases. It then overlays the text file onto an input video of your choice using ffmpeg and outputs the final file for your use.

The script is commented to help guide you through the setup.

It is recommended to automate the running of the script at least once a day to keep the pre-roll up to date. This can be done through a cronjob or any other scheduling method of your choice.

The version of ffmpeg included in this repo is a verison that has been compiled with the necessary libraries to work with adding overlays to video files. Other versions may not work for you. You can substitute the font file with anything you want, you just need to make the filename change accordingly in the script.

## Radarr

To obtain the link for iCal, go to the Calendar tab from the left menu bar, then click on the "iCal Link" button on the top of the page. Keep "Show as All-Day Event" unchecked, but you can choose if you want "Include Unmonitored" checked or not. Leave the Tags blank and copy the text from the iCal Feed box into the string in the Python script.

## Example

An example template: [Template](https://www.youtube.com/watch?v=kKc8jydRlzc)
Example of processed final video: [Final](https://www.youtube.com/watch?v=IJHpwps4DYM)

## Important

This Python script uses the library "icalendar" to parse the iCal information received from Radarr. You will need to install the library onto your system using pip. This may also require you to install the pip package on your system. I won't go into any Python or Linux usage details here. Google or ChatGPT is a good resource for helping in these situations.

Typical install for the library would be:

    python3 -m pip install icalendar

Note: This package serves as a starting template and I will not be entertaining any pull requests or issues. This comes as-is and it is up to you to modify and use it however you please and have a somewhat working knowledge of Python and Linux.
