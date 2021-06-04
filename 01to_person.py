
import json


# Check for boxA and boxB intersection, xywh
def checkIntersection(boxA, boxB):
    # print(boxA,boxB)
    x = max(boxA[0], boxB[0])
    y = max(boxA[1], boxB[1])
    w = min(boxA[0] + boxA[2], boxB[0] + boxB[2]) - x
    h = min(boxA[1] + boxA[3], boxB[1] + boxB[3]) - y

    foundIntersect = True
    if w < 0 or h < 0:
        foundIntersect = False

    return foundIntersect

    # return (foundIntersect, [x, y, w, h])


def check_overlap(crop_info,crops_list):
    found = 0
    overlaps_list = []

    for crop_b in crops_list:
        if crop_b['category_id'] in [0,3] : # is_person: 0ground, 3fly
            # boxA = [crop_info["bbox"],crop_info["bbox"],crop_info["bbox"],crop_info["bbox"]]
            # boxB = [crop_b["bbox"],crop_b["bbox"],crop_b["bbox"],crop_b["bbox"]]
            if checkIntersection(crop_info["bbox"],crop_b["bbox"]):
                overlaps_list += [crop_b]
                found += 1

    if found != 0:
        # print('founded:' )
        # print(overlaps_list)


        return True, overlaps_list
    else:
        print("warning! no overlaps found , image_id is " + str(crop_info["image_id"]) )
        return False, overlaps_list


def get_iou(box1, box2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x, y) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner

    Returns
    -------
    float
        in [0, 1]
    """
    bb1={'x1':box1[0],'y1':box1[1],'x2':box1[2],'y2':box1[3],}
    bb2={'x1':box2[0],'y1':box2[1],'x2':box2[2],'y2':box2[3],}


    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou












with open('best_predictions.json') as f:
    submit_list = json.load(f)

# make stacked_dict
stacked_dict = {}
for i,val in enumerate(submit_list):
    if val['image_id'] in stacked_dict:
        stacked_dict[val['image_id']] += [val]
    else:
        stacked_dict[val['image_id']] = [val]

# print(json.dumps(stacked_dict, indent=4))

for key, crops_list in stacked_dict.items():
    for i, crop_info in enumerate(crops_list):
        # print(crop_info)
        if crop_info["category_id"] in [1, 2]:  # no_preson: 1guard, 2safebelt

            is_overlap,overlaps_list = check_overlap(crop_info,crops_list)
            if is_overlap:
                origin = stacked_dict[key][i]['bbox']
                # select max IOU
                stacked_dict[key][i]['bbox'] = overlaps_list[0]['bbox']

                crop_dict1 = stacked_dict[key][i]
                bb1 = [crop_dict1['bbox'][0],
                       crop_dict1['bbox'][1],
                       crop_dict1['bbox'][2]+crop_dict1['bbox'][0],
                       crop_dict1['bbox'][3]+crop_dict1['bbox'][1]]

                for crop_dict2 in overlaps_list:
                    bb2 = [crop_dict2['bbox'][0],
                           crop_dict2['bbox'][1],
                           crop_dict2['bbox'][2]+crop_dict2['bbox'][0],
                           crop_dict2['bbox'][3]+crop_dict2['bbox'][1]]

                    iou=get_iou(bb1, bb2)
                    print(iou)

                # print(crop_info["category_id"],origin, stacked_dict[key][i]['bbox'])


            if len(overlaps_list) > 1:
                # print("this is image_id " + crop_info['image_id'],
                #       "overlaps greater than 1: "+ str(len(overlaps_list)))
                # print(crop_info['bbox'] )
                # print([overlap_crop['category_id'] for overlap_crop in overlaps_list])
                # print( [overlap_crop['bbox'] for overlap_crop in overlaps_list])
                # print('')
                pass




# rebuild best_predictions from stacked list
final_list = []
for key, crops_list in stacked_dict.items():
    for i, crop_info in enumerate(crops_list):
        final_list += [crop_info]


# xywh > xyxy
for i,val in enumerate(final_list):
    x,y,w,h = final_list[i]['bbox']
    x2,y2 = x+w,y+h
    final_list[i]['bbox'] = [x,y,x2,y2]



# # remove score that <= 0.5
# final_list2 = [val for i, val in enumerate(final_list) if val['score'] >= 0.5]
# print(len(final_list),len(final_list2))


# make file
with open('best_predictions_for02.json', 'w') as fp:
    json.dump(final_list, fp )
    # json.dump(to_submit, fp, indent=4)



# print(final_list2)


