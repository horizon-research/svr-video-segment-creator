import cv2
import json
import constants
import os
import sys
import container
import pprint


def crop(video_path, trace_list, width, height, output_path):
    print(video_path)
    filename = video_path.split('.')
    videocap = cv2.VideoCapture(video_path)
    success, image = videocap.read()
    fps = videocap.get(cv2.CAP_PROP_FPS)
    print('output_path', output_path)
    output = cv2.VideoWriter(output_path,
                             cv2.VideoWriter_fourcc(*'XVID'),
                             fps,
                             (width, height))
    for trace in trace_list:
        print(trace)
        success, image = videocap.read()
        if success:
            print(trace)
            crop_img = image[trace.y:trace.y + height, trace.x:trace.x + width]
            output.write(crop_img)
    output.release()


# Usage:
#  python3 <full-size-video-dir> <filename of full size video> <predict file> <json detection file> <width> <height>
if __name__ == '__main__':
    storage_path = sys.argv[1]
    video_filename = sys.argv[2]
    pred_filename = sys.argv[3]
    object_det_filename = sys.argv[4]
    fov_width = int(sys.argv[5])
    fov_height = int(sys.argv[6])
    frame_list = []
    pp = pprint.PrettyPrinter(indent=4)

    with open(pred_filename) as f:
        obj_list = []
        for line in f:
            line_split = line.split()
            fid, object_id = int(line_split[0]), int(line_split[1])
            extract_coord = line_split[-1].split(',')
            point = container.Trace(100, extract_coord[0], extract_coord[1], extract_coord[2], extract_coord[3])
            point.update_coord_with_dimension(fov_width, fov_height)
            if object_id == 0:
                if fid != 1:
                    frame_list.append(obj_list)
                obj_list = []
            obj_list.append(point)
        frame_list.append(obj_list)

    with open(object_det_filename) as f:
        json_obj = json.load(f)
    segment_index = 1
    for _, video_block in enumerate(json_obj):
        start = video_block['frame_start']
        end = video_block['frame_end']
        cluster = video_block['cluster']
        for local_start in range(start, end, constants.SEGMENT_NUM):
            print('SEG#', segment_index, 'crop from', local_start, 'to', local_start + constants.SEGMENT_NUM)
            fov_filename = os.path.join(storage_path, video_filename + '_' + str(segment_index) + '.mp4')
            # crop and save video segments from an original segment
            for j in cluster:
                output_dir = os.path.join(os.path.join(storage_path, str(segment_index)))
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_path = os.path.join(output_dir, str(j) + '.mp4')
                trace_list = []
                for i in range(local_start, local_start + constants.SEGMENT_NUM):
                    trace_list.append(frame_list[i][j])
                print('process index', segment_index, 'path_id', j)
                crop(fov_filename, trace_list, fov_width, fov_height, output_path)
            segment_index = segment_index + 1
