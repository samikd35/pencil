#!/bin/sh
# Preserve existing exports; FFmpeg refuses to overwrite them.
set -eu
cd "$(dirname "$0")/.."
/opt/homebrew/bin/ffmpeg -n -hide_banner -loglevel error -framerate 24 -start_number 1 -i artifacts/rough-v005/frames/frame-%04d.png -frames:v 240 -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart -an artifacts/rough-v005/preview.mp4
/opt/homebrew/bin/ffprobe -v error -show_entries stream=codec_name,codec_type,width,height,r_frame_rate,nb_frames:format=duration,size -of json artifacts/rough-v005/preview.mp4 > artifacts/rough-v005/verified-video.json
/opt/homebrew/bin/ffmpeg -n -hide_banner -loglevel error -i artifacts/rough-v003/preview.mp4 -i artifacts/rough-v005/preview.mp4 -filter_complex "[0:v]trim=start_frame=88:end_frame=192,setpts=PTS-STARTPTS,scale=640:360,drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial.ttf:text='Before':x=24:y=18:fontsize=24:fontcolor=0x20252c[a];[1:v]trim=start_frame=88:end_frame=192,setpts=PTS-STARTPTS,scale=640:360,drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial.ttf:text='Revised':x=24:y=18:fontsize=24:fontcolor=0x20252c[b];[a][b]hstack=inputs=2[v]" -map '[v]' -an -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart artifacts/rough-v005/before-after.mp4
/opt/homebrew/bin/ffmpeg -n -hide_banner -loglevel error -i artifacts/rough-v005/preview.mp4 -vf "select='not(mod(n,12))',scale=320:-1,tile=5x4" -frames:v 1 artifacts/rough-v005/contact-sheet.png
/opt/homebrew/bin/ffmpeg -n -hide_banner -loglevel error -i artifacts/rough-v005/preview.mp4 -vf "select='between(n,151,178)*not(mod(n-151,2))',scale=320:-1,tile=7x2" -frames:v 1 artifacts/rough-v005/recovery-sequence.png
