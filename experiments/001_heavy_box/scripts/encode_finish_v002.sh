#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
/opt/homebrew/bin/ffmpeg -n -hide_banner -loglevel error -framerate 24 -start_number 1 -i artifacts/finish-v002/frames/frame-%04d.png -i artifacts/finish-v002/audio/soundtrack.wav -t 10 -map 0:v:0 -map 1:a:0 -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart artifacts/finish-v002/preview-with-sound.mp4
/opt/homebrew/bin/ffprobe -v error -show_entries stream=codec_name,codec_type,width,height,r_frame_rate,nb_frames,sample_rate,channels,duration:format=duration,size -of json artifacts/finish-v002/preview-with-sound.mp4 > artifacts/finish-v002/verified-video.json
/opt/homebrew/bin/ffmpeg -n -hide_banner -loglevel error -i artifacts/finish-v002/preview-with-sound.mp4 -vf "select='not(mod(n,12))',scale=320:-1,tile=5x4" -frames:v 1 artifacts/finish-v002/contact-sheet.png
/opt/homebrew/bin/ffmpeg -hide_banner -i artifacts/finish-v002/preview-with-sound.mp4 -vn -af loudnorm=I=-18:TP=-1.5:LRA=9:print_format=json -f null - > artifacts/finish-v002/audio/final-loudness.log 2>&1
