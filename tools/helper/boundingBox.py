def mergeBoundingBoxes(bbs):
    """
    Combine multiple bounding boxes into one that covers all the provided bounding boxes.
    Args:
        bbs (array of bounding box): A list where each element is a bounding box represented as 
                             [x, y, width, height].
    Returns:
        A single bounding box [x, y, width, height] that covers the area of all input bounding boxes.

    Example:
        >>> bbs = [[10, 20, 30, 40], [15, 25, 50, 60]]
        >>> mergeBoundingBox(bbs)
        [10, 20, 55, 65]
    """
    if (len(bbs)==1):
        return bbs[0]
    minX = 10000
    minY = 10000
    maxX = 0
    maxY = 0
    for b in bbs:
        if b[0]<=minX:
            minX=b[0]
        if b[0]+b[2]>=maxX:
            maxX=b[0]+b[2]
        if b[1]<=minY:
            minY=b[1]
        if b[1]+b[3]>=maxY:
            maxY=b[1]+b[3]
    return [minX,minY,maxX-minX,maxY-minY]
    
# Scan list of bounding boxes then merge bounding box that are relate to each other
# for example, a big bounding box follow by 4 small bounding box\
# imply that it is a question follow by 4 choices.
# return new list of bounding box

# the widest bounding are assume to be a question (IRL this is not always true)
# All question assume to be starting at the same x position
# Any line starting at that position indicate the start of a new question
def mergeRelatedBoundingBoxes(bounding_boxes,page_width,offset):
    min_x_bb = max(bounding_boxes,key= lambda x:x[2])[0]
    #max_w_bb = max(bounding_boxes,key= lambda x:x[2])[2]
    new_bb = []
    curr_bb = []
    pass_header_yet = False
    for bb in bounding_boxes:
        #if (not pass_header_yet):
           # if abs((bb[2]-max_w_bb)/page_width)< 
        if (bb[0]-min_x_bb)/(page_width)<= offset and curr_bb:
            new_bb.append(mergeBoundingBoxes(curr_bb))
            curr_bb = []
        curr_bb.append(bb)
    if (curr_bb):
        new_bb.append(mergeBoundingBoxes(curr_bb))
    return new_bb

def combineTwoHalf(bbs_l,bbs_r,cut_position):
    for bb in bbs_r:
        bbs_l.append([bb[0]+cut_position,bb[1],bb[2],bb[3]])
    return bbs_l