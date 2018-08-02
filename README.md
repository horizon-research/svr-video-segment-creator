# svr-video-segment-creator
Create video segments for the svr-streaming-system.

## Prerequisite
- python3
- ffmpeg
- opencv

## Usage
- Create full-size videos
    - `python3 <mp4-file> <segment-num> <output-path/name-of-video>`
- Create fov videos
    - `python3 <path-of-full-size-videos> <name-of-video> <object-detection-file> <cluster-file> <width> <height>`
- Example:
```bash
# create full size video segment
$ python3 rhino-no-prefix.mp4 100 rhino/output

# create fov video segment
$ python3 storage/rhino-full output rhinos-pred.txt rhinos.json 1800 1800
```