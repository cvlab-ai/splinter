from asyncore import write
from cmath import rect
from cairosvg import svg2png
from consts import *
from constructs import *

svg_code = [page_top(PAGE_WIDTH, PAGE_HEIGHT), 
            page(),                                             # empty page
            black_squares_rows((245, 240), (245, 3130), 3),     # left vertical squares
            black_squares_rows((2015, 240), (2015, 3130), 2),   # right vertical squares
            full_black_squares(1130, 3010),                     # bottom middle square
            writing_rectangle((630, 335), (1350, 150)),         # exam title box
            multiline_text((630, 345), ['Exam   ', 'title']),      # exam title text
            writing_rectangle((630, 510), (1350, 150)),         # student name box
            multiline_text((630, 520), ['Student', 'name']),    # student name text
            writing_rectangle((630, 690), (530, 150)),          # date box
            multiline_text((630, 750), ['Date   ']),               # date text
            answer_column((1550, 740), (4, 1)),                 # exam key
            multiline_text((1530, 750), ['Exam key']),       # exam key text
            answer_column((485, 1185), (4, 10)),                # 1-10 questions boxes
            number_column((415, 1185), [1, 10]),                # 1-10 questions numbers
            answer_column((485, 2050), (4, 10)),                # 11-20 boxes
            number_column((415, 2050), [21, 30]),               # 11-20 numbers
            answer_column((1010, 1185), (4, 10)),               # 21-30 boxes
            number_column((940, 1185), [11, 20]),               # 21-30 numbers
            answer_column((1010, 2050), (4, 10)),               # 31-40 boxes
            number_column((940, 2050), [31, 40]),               # 31-40 numbers
            answer_column((1540, 2050), (4, 10)),               # 41-50 boxes
            number_column((1470, 2050), [41, 50]),              # 41-50 numbers
            answer_column((1460, 1185), (6, 10), is_index=True),# index fields
            number_column((1390, 1185), [0, 9]),                # index numbers
            typing_boxes((1460, 1065), (80, 120), 6),           # index fill in boxes
            text(1560, 1020, 60, 'black', 'Student ID'),        # index student id text
            answer_column((745, 3015), (4, 2), bounding_boxes=False),
            bounding_box((405, 2980), (685, 230)),
            answer_column((1630, 3015), (4, 2), bounding_boxes=False),
            bounding_box((1290, 2980), (685, 230)),
            f'<image href="tutorialmask.png" height="{PAGE_HEIGHT}" width="{PAGE_WIDTH}"/>',
            page_bottom]
svg_code = ''.join(svg_code)
svg2png(bytestring=svg_code, write_to='research/svg/svgtest.png')