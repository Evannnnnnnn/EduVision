from __future__ import print_function

import webbrowser
from tkinter import *
from PIL import Image, ImageDraw
from PIL import ImageTk
import threading
import datetime
import imutils
import cv2
import os
from imutils.video import VideoStream, FPS
import argparse
import time
from googlesearch import search
import webbrowser

class application():
    def __init__(self, vs, outputPath):
        self.vs = vs
        self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.framenumber = 0
        self.allboundingboxes = None
        self.mostrecentlylookedat = None
        self.seen_words = {}
        self.watch_timer = {}

        self.root = Tk()
        self.panel = None
        self.paused = None

        btn = Button(self.root, text='Pause')  # command=self.pause)
        # btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        self.stopEvent = threading.Event()
        self.t1 = threading.Thread(target=self.videoLoop, args=())


        self.root.wm_title("Video Viewer Demo")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)
        self.curr_bboxes = None

        #-----------------------------------------------------------------------------------------------

        self.img_list = ['Images/1.png', 'Images/2.png', 'Images/3.png', 'Images/4.png', 'Images/5.png']

        self.display_padx = (20, 10)
        self.display_pady = (20, 10)

        self.row_offset = 6
        self.buttonheight = 120
        self.buttonwidth = 210
        #
        self.button_padx = (0, 10)
        self.button_pady = (0, 10)

        self.search_padx = (0, 20)
        self.search_pady = 10

        self.search_padx = (0, 20)
        self.search_pady = 10

        img = Image.open(self.img_list[0])
        img = ImageTk.PhotoImage(img)

        self.Button1 = Button(self.root, height=self.buttonheight, width=self.buttonwidth, image=img, command=lambda: self.changevid(0))
        self.Button1.grid(column=0, row=1 + self.row_offset, padx=self.button_padx, pady=self.button_pady)
        self.Button1.image = img

        img = Image.open(self.img_list[1])
        img = ImageTk.PhotoImage(img)

        self.Button2 = Button(self.root, height=self.buttonheight, width=self.buttonwidth, image=img, command=lambda: self.changevid(1))
        self.Button2.grid(column=1, row=1 + self.row_offset, padx=self.button_padx, pady=self.button_pady)
        self.Button2.image = img

        img = Image.open(self.img_list[2])
        img = ImageTk.PhotoImage(img)

        self.Button3 = Button(self.root, height=self.buttonheight, width=self.buttonwidth, image=img, command=lambda: self.changevid(2))
        self.Button3.grid(column=2, row=1 + self.row_offset, padx=self.button_padx, pady=self.button_pady)
        self.Button3.image = img

        img = Image.open(self.img_list[3])
        img = ImageTk.PhotoImage(img)

        self.Button4 = Button(self.root, height=self.buttonheight, width=self.buttonwidth, image=img, command=lambda: self.changevid(3))
        self.Button4.grid(column=3, row=1 + self.row_offset, padx=self.button_padx, pady=self.button_pady)
        self.Button4.image = img

        img = Image.open(self.img_list[4])
        img = ImageTk.PhotoImage(img)

        self.Button5 = Button(self.root, height=self.buttonheight, width=self.buttonwidth, image=img, command=lambda: self.changevid(4))
        self.Button5.grid(column=4, row=1 + self.row_offset, padx=self.button_padx, pady=self.button_pady)
        self.Button5.image = img

        self.stats_button = Button(self.root, width=21, height=7, text='Viewing Statistics', command=self.see_stats)
        self.stats_button.grid(row=1 + self.row_offset, column=5, padx=self.button_padx, pady=self.button_pady)

        self.search_label = Label(self.root, width=50, borderwidth=10, text="No Recommendation Yet")
        self.search_label.grid(column=5, row=1, padx=self.search_padx, pady=self.search_pady)

        self.rec_column = Label(self.root, text='Recommended topics here')
        self.rec_column.grid(column=5, row=0)

        self.search_button = Button(self.root, text='Search', command=self.search_web)
        self.search_button.grid(column=5, row=2, padx=self.search_padx, pady=self.search_pady)



    def start_thread(self):
        self.t1.start()

    def update_curr_bboxes(self, framenumber):
        self.curr_bboxes = []
        self.curr_bboxes = self.allboundingboxes[framenumber]

    def videoLoop(self):
        try:
            timer = FPS().start()
            while not self.stopEvent.is_set() and not self.paused:


                self.grabed, self.frame = self.vs.read()

                if self.frame is None:
                    break
                self.frame = imutils.resize(self.frame, width=1080)

                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                #Update the bounding boxes for said image
                self.update_curr_bboxes(self.framenumber)
                for bbox in self.curr_bboxes:
                    min_x = bbox[0]
                    min_y = bbox[1]
                    max_x = bbox[2]
                    max_y = bbox[3]
                    draw = ImageDraw.Draw(image)
                    draw.line((min_x, max_y, max_x, max_y))
                    draw.line((min_x, min_y, max_x, min_y))
                    draw.line((max_x, min_y, max_x, max_y))
                    draw.line((min_x, min_y, min_x, max_y))

                image = ImageTk.PhotoImage(image)
                self.framenumber += 1
                if self.panel is None:
                    self.panel = Label(image=image)
                    self.panel.image = image
                    self.panel.grid(column=0, row=0, columnspan=5, rowspan=7, padx=self.display_padx, pady=self.display_pady)

                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

            # timer.stop()
            # print(timer.fps())
            # print(timer.elapsed())

        except RuntimeError as e:
            print(e)


    def onClose(self):
        print("Closing window!")
        self.stopEvent.set()
        self.vs.release()
        self.root.quit()

    def pause(self):
        if not self.paused:
            self.paused = True
            self.vs.stop()
        else:
            self.paused = False
            self.vs.start()


    def changevid(self, num):
        # self.vs.stop()
        # self.stopEvent.set()
        # vid_change = self.img_list[num]
        # self.vs = VideoStream(src=vid_change, framerate=24).start()
        #
        # self.stopEvent = threading.Event()
        # self.t1 = threading.Thread(target=self.videoLoop, args=())
        # self.t1.start()

        img = Image.open(self.img_list[num])
        img = ImageTk.PhotoImage(img)
        display = Label(self.root, height=810, width=1440, image=img)
        display.image = img
        display.grid(column=0, row=0, columnspan=5, rowspan=7, padx=self.display_padx, pady=self.display_pady)

    def motion(self, event):

        x = event.x - 5
        y = event.y - 5
        for bbox in self.curr_bboxes:
            min_x = bbox[0]
            min_y = bbox[1]
            max_x = bbox[2]
            max_y = bbox[3]

            if x >= min_x and x <= max_x and y >= min_y and y <= max_y:
                print("Currently looking at {}".format(bbox[4]))
                if self.watch_timer.get(bbox[4]):
                    self.watch_timer[bbox[4]] += 1
                else:
                    self.watch_timer[bbox[4]] = 1
                if bbox[4] != self.mostrecentlylookedat:
                    print(self.seen_words)
                    if self.seen_words.get(bbox[4]):
                        self.search_label.configure(text=str(bbox[4]))
                        numlink = 5
                        links = []
                        eval_link = lambda x: (lambda p: webbrowser.open_new(x))
                        for i in range(numlink):
                            links.append(Label(self.root, text=self.seen_words[bbox[4]][i]))
                            links[i].grid(row=i + 3, column=5)
                            links[i].bind('<Button-1>', eval_link(self.seen_words[bbox[4]][i]))
                        print(links)

                    else:
                        self.mostrecentlylookedat = bbox[4]
                        self.search_label.configure(text=str(bbox[4]))
                        data = str(self.mostrecentlylookedat)
                        results = search(data)
                        self.seen_words[bbox[4]] = results
                        numlink = 5
                        links = []
                        eval_link = lambda x: (lambda p: webbrowser.open_new(x))
                        for i in range(numlink):
                            links.append(Label(self.root, text=results[i]))
                            links[i].grid(row=i + 3, column=5)
                            links[i].bind('<Button-1>', eval_link(results[i]))



    def see_stats(self):
        new_window = Tk()
        for item in self.watch_timer:
            stats_label = Label(new_window, text=item + " : " + str(self.watch_timer[item] / 24) + " Seconds.")
            stats_label.pack()



    def search_web(self):
        data = str(self.mostrecentlylookedat)
        results = search(data)
        numlink = 5
        links = []
        for i in range(2, numlink + 1):
            links.append(Label(self.root, text=results[i - 2]))

        i = 2
        for label in links:
            label.grid(row=i + 1, column=5)
            label.bind('<Button-1>', lambda e: webbrowser.open_new(results[i - 2]))
            i += 1

    def setup_bboxes(self):
        f = open("Boundingboxes/{path}.txt".format(path=name), 'r')

        lines = f.readlines()  # A list of each individual line
        frames = []
        index = 0
        for i in range(len(lines)):
            line = lines[i]
            if line[0] != '[':
                # We have a new instance of a potential frame
                # Once we have our grame, go and grab the extra data
                # Go backwards through the lines until we find the previous frame, everything in between us our data
                index += 1
                j = i - 1
                frame = []
                while j >= 0 and lines[j][0] == '[':
                    frame.append(lines[j])
                    j = j - 1

                frames.append(frame)
        for i in range(len(frames)):
            if frames[i] != []:
                for j in range(len(frames[i])):
                    # Pull out the numbers so that it is the minx miny maxx maxy

                    bboxes = frames[i][j].strip("[")
                    bboxes = bboxes.replace("]", "")
                    bboxes = bboxes.replace(" -", ",")
                    bboxes = bboxes.split(", ")

                    string = ""
                    for l in bboxes[4]:

                        if l != " ":
                            string += l
                        else:
                            break
                    bboxes[4] = string
                    for k in range(4):
                        bboxes[k] = float(bboxes[k])
                    frames[i][j] = bboxes
        self.allboundingboxes = frames

fps = 24
name = "OctoberSky"
src = "C:/Users/Evanl/Test Sample/{path}.mov".format(path=name)
vs = cv2.VideoCapture(src)



vidView = application(vs, "")
vidView.setup_bboxes()
vidView.root.bind('<Motion>', vidView.motion)
vidView.start_thread()

vidView.root.mainloop()