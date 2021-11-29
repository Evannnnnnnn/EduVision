def setup_bboxes():
    f = open("boundingboxes.txt", 'r')

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
                        string +=  l
                    else:
                        break
                bboxes[4] = string
                for k in range(4):
                    bboxes[k] = float(bboxes[k])
                frames[i][j] = bboxes

if __name__ == '__main__':
    setup_bboxes()