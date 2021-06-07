# funcs: convert result from yolo to submit
# notice: use for 14belt only


import json
import os
import copy


# load coco_list
with open('best_predictions_for02.json') as f:
    yolo_list = json.load(f)

# load fn-id map
with open('link_image_fn_id.json') as f:
    map = json.load(f)

# xywh > xyxy
for i,val in enumerate(yolo_list):
    x,y,w,h = yolo_list[i]['bbox']
    x2,y2 = x+w,y+h
    yolo_list[i]['bbox'] = [x,y,x2,y2]

# # remove score that <= 0.5
# yolo_list2 = [val for i, val in enumerate(yolo_list) if val['score'] >= 0.5]
# print(len(yolo_list),len(yolo_list2))

# remove cls_id=0
yolo_list = [ ele for ele in  yolo_list if ele['category_id'] != 0 ]


# image_id  fn2int
yolo_list_debug = copy.deepcopy(yolo_list)
for i,val in enumerate(yolo_list):
    fn_no_ext = yolo_list[i]['image_id']
    yolo_list[i]['image_id'] = map[fn_no_ext] # fn_no_ext > int_id
    yolo_list_debug[i]['image_id'] = (map[fn_no_ext], fn_no_ext)   # denug


with open('submit.json', 'w') as fp:
    json.dump(yolo_list, fp )
    # json.dump(to_submit, fp, indent=4)

with open('submit_debug.json', 'w') as fp:
    json.dump(yolo_list_debug, fp )
    # json.dump(to_submit, fp, indent=4)