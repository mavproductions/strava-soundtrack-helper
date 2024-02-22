## strava-soundtrack-helper
With the use of Strava GPX and Last.FM scrobble history, you can make your own music map and share your music listening history from your workout!

Inside the app will give you tips with the manual work required inside Adobe Photoshop or GIMP to make your own privacy zones of your music map.

### Requirements
* GPS Fitness tracking Smartwatch with LTE or Smartphone with Mobile Data (Hoping to eliminate Mobile Data during runs requirement on future updates)
* Strava on either devices
* Spotify account
* Last.FM account with proper Spotify Scrobbling capabilities (I use [PanoScrobbler](https://play.google.com/store/apps/details?id=com.arn.scrobble&hl=en&gl=US))
* Something to edit/eliminate CSV row titles from [Last.FM Data Exporter](https://mainstream.ghan.nl/export.html)
* Google Earth Pro for your Desktop/Laptop OS (I've only tested on Windows)
* Python 3.10 (Will hopefully eliminate this requirement when I have the time)
* Photoshop, GIMP, or [PhotoPea](https://www.photopea.com/) - For music map layer editing to clean up your map, and replicate "privacy zones" on Strava

### Usage
1) Go for a run while tracking with Strava app or an app that supports Strava data syncing
2) Listen to your spotify music from your wearOS watch, or use any app on your smartphone - with mobile data enabled and scrobbling live.
3) After your run download the GPX using Strava's ["Export GPX"](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#h_01GDP2JB35R4ECM0E6YAH316B9) feature
4) Go to [Last.FM Data Exporter](https://mainstream.ghan.nl/export.html) and use strava-soundtrack-helper's Time Converter to convert to UNIX Timestamp
5) If you just want the listening history from your you'll need to edit the CSV and make the first row "artist" and second row "song_title" and save.
   * Select "Last.FM Scrobble Recorder" in the file menu at the top and open the modified CSV and click "copy to clipboard"
   * Paste to your Strava activity 😁
8) (**Currently convoluted**) If you want to make a "Music Map" of your run and music listened to, import a modified version of the CSV with "artist" and "song_title", but everything
   else as well.
9) Output the music_events.kml and import it into Google Earth Pro if strava-soundtrack-helper doesn't do it automatically for you.
11) Import the Strava GPX if you haven't already
12) Save 3 images with the data now in Google Earth Pro (DON'T ADJUST THE CAMERA ANGLE OF THE PHOTO)
    * An image with an alpha-channel or greenscreen `(0,255,0)` with the scrobbled music pinpoints
    * An image with the strava gpx track lines on the map
    * An image of the map alone
13) Import these layers into photoshop. When you're done editing your privacy zones and using magic erase on the greenscreen layer,
    your layers top-bottom should be: music-pinpoints+text, strava gps running lines, blank map photo
14) Save this Photoshop document and upload as a picture to your run!😃
15) Done - finally!

### Notes
* Without Panoscrobbler, Spotify uses Recently Played for tracking music and pushing to your Last.FM account. There are a lot of inconsistencies with the
  Spotify API, which is why I recommend a present LTE device for the time being.

### Offsets
With offset timing, it is app/scrobbler-dependent. With tests from [Panscrobbler for Android](https://play.google.com/store/apps/details?id=com.arn.scrobble&hl=en&gl=US), I get pinpoint accuracy for GPS scrobbles, where as [Last.FM's Spotify Scrobbling](https://www.last.fm/settings/applications), doesn't set the scrobble point to when the song started.

### GUI Elements
![GUI Preview](https://i.imgur.com/bTU2TjO.png)

### Google Earth Music Map Preview
![Preview of Google Earth Music Map](https://i.imgur.com/cebEp8w.png)
