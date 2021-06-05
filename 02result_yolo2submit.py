# funcs: convert result from yolo to submit
# notice: use for 14belt only


import json
import os
import copy



with open('best_predictions_for02.json') as f:
    yolo_dict = json.load(f)

with open('link_image_fn_id.json') as f:
    map = json.load(f)



yolo_dict_debug = copy.deepcopy(yolo_dict)

for i,val in enumerate(yolo_dict):

    fn_no_ext = yolo_dict[i]['image_id']
    yolo_dict[i]['image_id'] = map[fn_no_ext] # fn_no_ext > int_id

    yolo_dict_debug[i]['image_id'] = (map[fn_no_ext], fn_no_ext)   # denug


    print(val)




with open('submit.json', 'w') as fp:
    json.dump(yolo_dict, fp )
    # json.dump(to_submit, fp, indent=4)

with open('submit_debug.json', 'w') as fp:
    json.dump(yolo_dict_debug, fp )
    # json.dump(to_submit, fp, indent=4)