def read(filename):
    image = []
    with open(filename) as file:
        enhancement = file.readline().strip()
        file.readline()

        for line in file:
            image.append(".." + line.strip() + "..")
    assert(len(enhancement) == 512)
    blank = [len(image[0]) * "."]
    return blank + blank + image + blank + blank, enhancement

def pp(im):
    for row in im:
        print(row)

def toDec(pix):
    assert(len(pix) == 9)
    result = 0
    worth = 256
    for c in pix:
        if c == '#':
            result += worth
        worth = worth >> 1
    return result

assert(toDec("...#...#.") == 34)

# step 0 ...iii...   ..iii..  (i = the actual image)
# step 1 ##iiiii##  ##iiiii##
# step 2 .iiiiiii. ..iiiiiii..

def enhance(image, enhancement, step):
    assert(step > 0)
    new_edge = '.'
    if enhancement[0] == '#' and step % 2 == 1:
        new_edge = '#'
    blank = [(len(image[0]) + 2) * new_edge]
    new_image = blank + blank
    for r in range(len(image))[1:-1]:
        new_row = new_edge*2
        for c in range(len(image[0]))[1:-1]:
            pix = image[r-1][c-1:c+2]
            pix += image[r][c-1:c+2]
            pix += image[r+1][c-1:c+2]
            new_row += enhancement[toDec(pix)]
        new_row += new_edge*2
        new_image.append(new_row)
    new_image += blank + blank

    return new_image

def pixCount(image):
    result = 0
    for row in image:
        for c in row:
            if c == '#':
                result += 1
    return result

image, enhancement = read("2021_20_testcase")
for n in range(1, 51): # Start counting at 1
    image = enhance(image, enhancement, n) 
    if n == 2:
        assert(pixCount(image) == 35)
assert(pixCount(image) == 3351)

# image = enhance(image, enhancement, 1)
# image = enhance(image, enhancement, 2)
# print(pixCount(image))
image, enhancement = read("2021_20_input")
for n in range(1, 51): # Start counting at 1
    image = enhance(image, enhancement, n) 
    if n == 2:
        print("Answer part 1: " + str(pixCount(image)))
print("Answer part 2: " + str(pixCount(image)))
