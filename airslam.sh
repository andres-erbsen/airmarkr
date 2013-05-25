#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DEMO_SLAM=${DEMO_SLAM-"demo_slam"}

if test $# -lt 1 ; then
    echo "Usage: $0 VIDEO_WITHOUT_EXT" >&2
    exit 1
fi

batchname=$(echo "$1" | sed 's:.mp4$::')
batchname=$(echo "$batchname" | sed 's:.dat$::')

if [ ! -f "$batchname.mp4" ]; then
    echo "File $batchname.mp4 not found!" >&2
    exit 1
fi
video=$(realpath "$batchname.mp4")

if [ ! -f "$batchname.dat" ]; then
    echo "File $batchname.dat not found!" >&2
    exit 1
fi
sensors=$(realpath "$batchname.dat")
datapath=$(dirname "$sensors")

mkdir -p "$batchname"
cd "$batchname"

if [ ! -f PREPPED ]; then
    ffmpeg -i "$video" image_%07d.png 1>&2
    duration=$(ffprobe -loglevel error -show_streams "$video" | grep duration | cut -f2 -d= | tail -1)
    N=$(ls image*.png | tail -1 | cut -d_ -f2 | cut -d. -f1)
    
    for n in $(seq 1 90); do rm "$(ls image*.png | head -1)"; done
    
    for f in image*.png; do
        n=$(echo $f | cut -d_ -f2 | cut -d. -f1)
        echo "scale=9; $duration*$n/$N" | bc > "$(echo $f | cut -d. -f1).time" # assume frames occur regularly
    done
   
    cp "$(ls *.time | head -1)" sdate.log
    python2 "$DIR/accconverter.py" "$sensors" MTI.log
    touch PREPPED
fi

"$DEMO_SLAM" --robot=1 --replay=1 --data-path=. --config-setup="$DIR/setup.cfg" --config-estimation="$DIR/estimation.cfg" --log=1

python3 "$DIR/trace2csv.py" "$sensors" "rtslam.log" > "$datapath/$batchname.csv"

( python3 "$DIR/plot.py" "$datapath/$batchname.csv" || true ) &
