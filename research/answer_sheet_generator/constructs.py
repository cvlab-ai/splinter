from consts import *

def page(width=PAGE_WIDTH, height=PAGE_HEIGHT):
    return rectangle(0, 0, width, height, 'white', 'black', 0)

def full_black_squares(x, y, length=120):
    return rectangle(x, y, length, length, 'black', 'black', 0)

def black_squares_rows(xy_start, xy_end, amount_of_squares = 3, length=120):
    pos_calc = lambda pos_start, pos_end: [int(pos_start + idx * (pos_end - pos_start - length) / (amount_of_squares - 1)) for idx in range(amount_of_squares)]
    x_start, y_start = xy_start
    x_end, y_end = xy_end
    if x_start == x_end:
        x_pos = [x_start] * amount_of_squares
        y_pos = pos_calc(y_start, y_end)
    if y_start == y_end:
        x_pos = pos_calc(x_start, y_end)
        y_pos = [y_start] * amount_of_squares
    return ''.join([full_black_squares(x, y) for x, y in zip(x_pos, y_pos)])

def writing_rectangle(xy_pos, wh):
    x, y = xy_pos
    w, h = wh
    return rectangle(x, y, w, h, 'white', 'black', 5)

def bounding_box(xy_pos, wh):
    x, y = xy_pos
    w, h = wh
    return rectangle(x, y, w, h, 'none', 'black', 8)

def answer_box(xy_pos, letter=None, length=80, inner_length=40, font_size=40):
    x, y = xy_pos
    return rectangle(x, y, length, length, 'white', 'black', 2) + \
           rectangle(x + inner_length//2, y + inner_length//2, inner_length, inner_length, 'white', 'black', 3) + \
           text(x + inner_length // 2 + 5, y + length - inner_length // 2 - 5, font_size, 'darkgray', letter)

def answer_row(xy_start, amount_of_boxes = 4, outer_length=80, inner_length=40, font_size=40, force_letter=None):
    if force_letter is None:
        letter_function = lambda idx: chr(ord('A') + idx)
    else:
        letter_function = lambda _ : force_letter
    x, y = xy_start
    return ''.join([answer_box((x + outer_length * idx, y), letter_function(idx), outer_length, inner_length, font_size) for idx in range(amount_of_boxes)])

def answer_column(xy_start, wh_boxes, outer_length=80, inner_length=40, font_size=40, is_index=False, bounding_boxes=True):
    x, y = xy_start
    num_cols, num_rows = wh_boxes
    if is_index:
        answer_boxes =  ''.join([answer_row((x, y + outer_length * idx), num_cols, outer_length, inner_length, font_size, str(idx)) 
        for idx in range(num_rows)])
    else:
        answer_boxes =  ''.join([answer_row((x, y + outer_length * idx), num_cols, outer_length, inner_length, font_size) 
        for idx in range(num_rows)])
    if bounding_boxes:
        return answer_boxes + bounding_box(xy_start, (num_cols*outer_length, num_rows*outer_length))
    else: 
        return answer_boxes

def typing_boxes(xy_start, wh, amount_of_boxes):
    x, y = xy_start
    w, h = wh
    return ''.join([rectangle(x + idx * w, y, w, h, 'none', 'black', 5) for idx in range(amount_of_boxes)]) + \
            bounding_box(xy_start, (amount_of_boxes * w, h))

def number_column(xy_start, numbers_range, box_size=80, font_size=40):
    x, y = xy_start
    numbers_range[1] += 1
    return ''.join([text(x, y + (idx - numbers_range[0]) * box_size + box_size * 3/4, font_size, 'black', str(idx)) for idx in range(*numbers_range) ])



def multiline_text(xy_start, multiline_content, font_size=45, interline=20):
    x, y = xy_start
    max_length = max([len(x) for x in multiline_content])
    x -= max_length * font_size * 3/4
    y += font_size
    return ''.join([text(x, y + idx * (font_size + interline), font_size, 'black', content) for idx, content in enumerate(multiline_content)])
