import cv2 as cv
import csv
import numpy as np
import matplotlib.pyplot as plt
import datetime

IMAGE_DIR = ('images\\')
INFO = {
    "description": "China Street Vehicle Dataset",
    "url": "https://github.com/andytung2019",
    "version": "0.1.0",
    "year": 2018,
    "contributor": "andy tung",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

CATEGORIES = [
    {
        'id': 3,
        'name': 'car',
        'supercategory': 'vehicle',
    },
    {
        'id': 6,
        'name': 'bus',
        'supercategory': 'vehicle',
    },
    {
        'id': 8,
        'name': 'truck',
        'supercategory': 'vehicle',
    },
]



class Rect:
    idx = -1
    x = None
    y = None
    w = None
    h = None

    def str2float(self, s):
        def char2num(s):
            return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]
             #这事实上是一个字典
        index_point=s.find('.')
        if index_point==-1:
            daichu=1
        else:
            daichu=0.1**(len(s)-1-index_point)
            s=s[0:index_point]+s[index_point+1:]#这里是除去小数点
        from functools import reduce
        result1=reduce(lambda x,y:x*10+y,map(char2num,s))
        return result1*daichu

    def __init__(self,idx, str):
        self.idx = idx
        l = str.split('_')
        print(l)
        self.x = int(self.str2float(l[0]))
        self.y = int(self.str2float(l[1]))
        self.w = int(self.str2float(l[2]))
        self.h = int(self.str2float(l[3]))

    def draw_me(self, image):
        cv.rectangle(image, (self.x,self.y),(self.x+self.w, self.y+self.h), (0, 255,0) )

        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(image, str(self.idx), (self.x + int(self.w/2), self.y+int(self.h/2)), font, 1, (0, 255, 0), 1, cv.LINE_AA)

    def print_me(self):
        print("x,y, w, h: %d, %d, %d, %d"%(self.x,self.y,self.w,self.h))



class VehicleLabel:



    def __init__(self):
        self.obj_list = []
        self.out_list = []

    def load_csv(self, path):
        with open(path) as csv_file:
            fields=['name', 'objs']
            reader = csv.DictReader(csv_file, fieldnames=fields)
            for row in reader:
                tp_img = (row['name'], row['objs'])
                self.obj_list.append(tp_img)

    def check_label(self):
        if len(self.obj_list) == 0:
            return
        for item in self.obj_list:
            print(item[0])
            img = cv.imread("images//"+item[0])
            cv.namedWindow('image')
            cv.imshow("image", img)

            l_objs = item[1].split(';')
            for i in range(len(l_objs)):
                rect = Rect(i, l_objs[i])
                rect.draw_me(img)
                cv.imshow("image", img)
            cv.waitKey(0)

        cv.destroyAllWindows()

    def create_coco(self):

        coco_output = {
            "info": INFO,
            "licenses": LICENSES,
            "categories": CATEGORIES,
            "images": [],
            "annotations": []
        }

        image_id = 1
        segmentation_id = 1

        # filter for jpeg images
        for root, _, files in os.walk(IMAGE_DIR):
            image_files = filter_for_jpeg(root, files)

            # go through each image
            for image_filename in image_files:
                image = Image.open(image_filename)
                image_info = pycococreatortools.create_image_info(
                    image_id, os.path.basename(image_filename), image.size)
                coco_output["images"].append(image_info)

                # filter for associated png annotations
                for root, _, files in os.walk(ANNOTATION_DIR):
                    annotation_files = filter_for_annotations(root, files, image_filename)

                    # go through each associated annotation
                    for annotation_filename in annotation_files:

                        print(annotation_filename)
                        if 'square' in annotation_filename:
                            class_id = 1
                        elif 'circle' in annotation_filename:
                            class_id = 2
                        else:
                            class_id = 3

                        category_info = {'id': class_id, 'is_crowd': 'crowd' in image_filename}
                        binary_mask = np.asarray(Image.open(annotation_filename)
                                                 .convert('1')).astype(np.uint8)

                        annotation_info = pycococreatortools.create_annotation_info(
                            segmentation_id, image_id, category_info, binary_mask,
                            image.size, tolerance=2)

                        if annotation_info is not None:
                            coco_output["annotations"].append(annotation_info)

                        segmentation_id = segmentation_id + 1

                image_id = image_id + 1

        with open('{}/instances_hulu_train2018.json'.format(ROOT_DIR), 'w') as output_json_file:
            json.dump(coco_output, output_json_file)


vecl = VehicleLabel()
vecl.load_csv('book1.csv')
vecl.check_label()
