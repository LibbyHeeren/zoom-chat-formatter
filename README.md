# zoom-chat-formatter
These are some Python functions I use to re-format Zoom chat files for enhanced readability.  

PLEASE NOTE THAT THIS WORKS ON OFFICIAL CHAT FILES THAT ZOOM GIVES YOU AS THE HOST OF THE MEETING. The format of zoom chat files that you save as an attendee are, seemingly, different. It's been a frustrating journey realizing that.    

Input is a zoom chat .txt, output is also a .txt. It would be even better to turn them into markdown! This code is 500% a ChatGPT collaboration, so feel free to let me know if anything looks weird. This was created before Claude Code was really on the scene.  

```
# Example code processes a zoom chat file that lives in the project root
# process_zoom_chat("input.txt", "whatever you name your output.txt")

process_zoom_chat("RecordingnewChat.txt", "RecordingnewChat_reformatted.txt")

# The above line of code will read your chat file, reformat it, and save it
# in the root. Feel free to specify different file paths.
```
