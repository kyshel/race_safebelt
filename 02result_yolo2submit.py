# funcs: convert result from yolo to submit
# notice: use for 14belt only


import json
import os


with open('best_predictions_for02.json') as f:
    yolo_dict = json.load(f)

with open('link_image_fn_id.json') as f:
    map = json.load(f)

# # build link dict
#
# map = {}
# to_submit_images_list = []
#
# for index,item in enumerate(link_list['images']):
#     filename = item['file_name']
#     image_id =  os.path.splitext(filename)[0]
#     map[image_id]= int(item['id'])
#
#     image = {}
#     image['file_name'] = filename
#     image['id'] = int(item['id'])
#     to_submit_images_list += [image]

# print(map)
# print(to_submit_images_list)


for i,val in enumerate(yolo_dict):

    fn_no_ext = yolo_dict[i]['image_id']
    yolo_dict[i]['image_id'] = map[fn_no_ext] # fn_no_ext > int_id

    print(val)




with open('submit.json', 'w') as fp:
    json.dump(yolo_dict, fp )
    # json.dump(to_submit, fp, indent=4)