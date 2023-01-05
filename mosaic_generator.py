import math
import cv2
import numpy as np
import argparse
import os
import sys
import time


class MosaicGenerator:

    def __init__(self, block_size, target_image, dataset_folder_path):
        self.block_size = block_size
        self.target_image = target_image
        self.target_image = self.make_image()
        self.dataset_folder_path = dataset_folder_path
        self.dataset = self.load_images_from_folder()
        self.resizedImgDts = self.setResize(self.block_size)
        self.h, self.w = self.target_image.shape[:2]
        self.d_type = self.target_image.dtype
        # self.img_resize_percent(percent=None, img=None)

    def make_image(self):
        made_image = cv2.imread(self.target_image)
        return made_image

    def load_images_from_folder(self):
        images = []
        for filename in os.listdir(self.dataset_folder_path):
            if filename.find(".png") != -1 or filename.find(".jpeg") != -1 or filename.find(".jpg") != -1:
                img = cv2.imread(os.path.join(self.dataset_folder_path, filename))
                if img is not None:
                    images.append(img)
        return images

    # def img_resize_percent(self, *args, **kwargs):
    #     h, w = self.target_image.shape[:2]
    #     try:
    #         width = int(w * kwargs["percent"] / 100)
    #         height = int(h * kwargs["percent"] / 100)
    #         dim = (width, height)
    #         resized_image = cv2.resize(kwargs["img"], dim, interpolation=cv2.INTER_AREA)
    #
    #         return resized_image
    #
    #     except KeyError and TypeError:
    #         pass

    # def image_Resize(self):
    #     dim = (self.h, self.w)
    #     resized_image = cv2.resize(self.target_image, dim, interpolation=cv2.INTER_AREA)
    #
    #     return resized_image

    def setResize(self, block_size):
        dim = (block_size, block_size)
        dest = []
        for i in range(len(self.dataset)):
            resized_image = cv2.resize(self.dataset[i], dim, interpolation=cv2.INTER_AREA)
            dest.append(resized_image)

        return dest

    def getAverage(self, img):
        avg_row = np.average(img, axis=0)
        avg_color = np.average(avg_row, axis=0)
        return (avg_color)

    def best_match_block(self, index, jindex):
        minimum = np.Infinity
        best_match = None
        avg_color_target = self.getAverage(
            self.target_image[index:index + self.block_size, jindex:jindex + self.block_size])
        # c = None

        for i in self.resizedImgDts:
            avg_color = self.getAverage(i)

            distance = np.linalg.norm(avg_color_target - avg_color)
            if distance < minimum:
                minimum = distance
                best_match = i
                # c = i
        return best_match

    def data_show(self):
        c = 0
        w = 440
        h = 370
        block_size = int(math.sqrt((w*h)/len(self.dataset)))
        resizedImgDts = self.setResize(block_size)
        output = np.zeros((h, w, 3), dtype=np.uint8)
        output = output-1
        for i in range(0, w, block_size):
            for j in range(0, h, block_size):
                try:
                    if c <= len(resizedImgDts)-1:
                        output[i:i + block_size, j:j + block_size] = resizedImgDts[c]
                        # cv2.namedWindow('output', cv2.WINDOW_NORMAL)
                        # cv2.imshow('output', output)
                        # cv2.waitKey(0)
                        c += 1
                except ValueError:
                    pass
        cv2.imwrite(f'dataShow-{block_size}-{w}x{h}.png', output)
        written_output = f'dataShow-{block_size}-{w}x{h}.png'
        return written_output

    def fit_size(self):
        w_crop = int((self.w % self.block_size))
        h_crop = int((self.h % self.block_size))
        if w_crop or h_crop:
            w_adjust = 1 if (w_crop % 2) else 0
            h_adjust = 1 if (h_crop % 2) else 0
            min_h, min_w = int(h_crop / 2), int(w_crop / 2)
            self.target_image = self.target_image[min_h:self.h - (min_h + h_adjust), min_w: self.w - (min_w + w_adjust)]

        return None

    def make_mosaic(self):
        start = time.time()
        c = 0
        cp = (self.h // self.block_size) - 1
        self.fit_size()
        output = np.zeros(self.target_image.shape, dtype=self.d_type)
        output = (output - 1)
        percent = 100 / cp

        for i in range(0, self.h-self.block_size, self.block_size):
            for j in range(0, self.w-self.block_size, self.block_size):
                output[i:i + self.block_size, j:j + self.block_size] = self.best_match_block(i, j)
            sys.stderr.write("Total complete: {}%\n".format(round(c)))
            c += percent
            self.flush_then_wait()

        sys.stderr.write('Elapsed time: {0:.2f}'.format(time.time() - start))
        # cv2.namedWindow('output', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('output', 720, 480)
        # cv2.imshow('output', output)
        # cv2.waitKey(0)
        cv2.imwrite('mosaic-{0}-{1}x{2}.png'.format(self.block_size, self.h, self.w), output)
        return output

    def flush_then_wait(self):
        sys.stderr.flush()
        sys.stderr.flush()
        time.sleep(.00000001)


def main():
    parser = argparse.ArgumentParser(description="Makes mosaic images out of a target and a dataset")
    parser.add_argument("block_size", help="Size of each mosaic")
    parser.add_argument("target", help="The target image path")
    parser.add_argument("dataset", help="The dataset directory")
    args = parser.parse_args()
    mg = MosaicGenerator(int(args.block_size), args.target, args.dataset)
    mg.make_mosaic()


if __name__ == "__main__":
    main()
    # img = cv2.imread('wci.jpg')
    # dataset = 'cars/'
    # block = 33
    # mg = MosaicGenerator(block, img, dataset)
    # # mosaic = mg.make_mosaic()
    # dataShow = mg.data_show()
    # # cv2.namedWindow('mosaic', cv2.WINDOW_NORMAL)
    # # cv2.imshow('mosaic', mosaic)
    # cv2.imshow('dataShow', dataShow)
    # # print(os.getcwd() + '/home')
    # # cv2.imwrite((os.getcwd() + '/output.jpg'), mosaic)
    #
    # if cv2.waitKey(0) & 0xff == 27:
    #     cv2.destroyAllWindows()
