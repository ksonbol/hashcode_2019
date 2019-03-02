from slides import *
from random import shuffle, randint

in_a = "in/a_example.txt"
in_b = "in/b_lovely_landscapes.txt"
in_c = "in/c_memorable_moments.txt"
in_d = "in/d_pet_pictures.txt"
in_e = "in/e_shiny_selfies.txt"

out_a = "out/a.out"
out_b = "out/b.out"
out_c = "out/c.out"
out_d = "out/d.out"
out_e = "out/e.out"

def read(file_name):
    lines = []
    is_first = True
    first_line = ""
    with open(file_name, "r") as r:
        i = 0
        for line in r:
            if is_first:
                first_line = line
                is_first = False
            else:
                line = str(i) + " " + line
                lines.append(line)
                i = i + 1
    return (first_line, lines)

def preprocess(first_line, lines):
    out = []
    num_img = int(first_line.strip())
    for line in lines:
        line = line.strip()
        if not line:
            break
        out.append(line)
    return num_img, out

def create_slides(images):
    """
    Takes a list of images ordered according to the type
    """
    slides = []
    skip_next = False
    num_imgs = len(images)
    for i, im in enumerate(images):
        if skip_next:
            skip_next = False
            continue
        if im.is_horizontal():
            slides.append(Slide(im))
        elif (i+1) < num_imgs:
            next_im = images[i+1]
            slides.append(Slide(im, next_im))
            skip_next = True
        else: # last image
            continue
    return slides


def choose_order(slides):
    order = []
    if_total = 0
    num_slides = len(slides)
    num_compare = 1000 # change from 500 to 1000 doesn't have a big effect
    best = slides[0]
    next_s = 1
    order.append(slides[0])
    slides[0].set_used()
    count = 1
    num_iter = 0
    max_count = num_slides
    while count < max_count:
        num_iter += 1
        percentage = float(count) / num_slides * 100
        if (percentage % 10) == 0:
            print("Ordered {}% of a total {} slides.".format(percentage, num_slides))
        prev_s = best
        best_if = -1
        for i in range(num_compare):
            i = randint(0, num_slides-1)
            if not slides[i].is_used():
                s = slides[i]
                s_if = s.get_if(prev_s)
                if s_if > best_if:
                    best_if = s_if
                    best = slides[i]
        if best_if == -1:
             # all images in this round have been already used, try another round
            continue
        best.set_used()
        order.append(best)
        count += 1
        num_iter = 0
        if_total += order[-1].get_if(order[-2])
    return order, if_total

def check_out(out_file):
    seen = {}
    with open(out_file, 'r') as f:
        num_slides = int(f.readline().strip())
        count = 0
        for line in f:
            parts = line.strip().split()
            ids = list(map(lambda p: int(p), parts))
            if seen.get(ids[0]) or ((len(ids) > 1) and seen.get(ids[1])):
                print("Image " + str(ids[0]) + " is repeated")
                return False
            seen[ids[0]] = True
            if len(ids) > 1:
                seen[ids[1]] = True
    return True
    
def write(file_name, slides):
    with open(file_name, "w") as w:
        w.write(str(len(slides)) + "\n")
        for s in slides:
            l = s.get_ids()
            w.write(l + "\n")

def print_obj(objs):
    c = 10
    for i in objs:
        print(i)
        if c > 10:
            break
        c += 1

################
# Main Program #
################
def run(in_f, out_f):
    first_line, lines = read(in_f)
    num_img, im_descs = preprocess(first_line, lines)
    images = []
    for im in im_descs:
        im_obj = Image(im)
        images.append(im_obj)

    # order images by type: first horizontal ones then vertical ones
    images.sort(key=lambda i: i.get_type())
    slides = create_slides(images)
    order, if_total = choose_order(slides)
    # print("Slides")
    # print_obj(slides)
    print("Length of slides: {}, Length of ordered slides: {}\n".format(len(slides), len(order)))
    print("score = " + str(if_total))
    # print("Order")
    # print_obj(order)
    # print(str(num_img) + " processed")

    write(out_f, order)
    print(check_out(out_f))

# print("A dataset")
# run(in_a, out_a)

print("B dataset")
run(in_b, out_b)

# print("C dataset")
# run(in_c, out_c)

print("D dataset")
run(in_d, out_d)

print("E dataset")
run(in_e, out_e)
