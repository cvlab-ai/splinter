page_top = lambda x, y: f'<svg xmlns="http://www.w3.org/2000/svg" width="{x}" height="{y}" fill="white" stroke="#000" stroke-width="2" version="1.1">'

page_bottom = "</svg>"

rectangle = lambda x_pos, y_pos, w, h, fill_color, border_color, border_width: f'<rect x="{x_pos}" y="{y_pos}" width="{w}" height="{h}" style="fill:{fill_color};stroke:{border_color};stroke-width:{border_width}" />'

text = lambda x_pos, y_pos, font_size, color, content: f'<text x="{x_pos}" y="{y_pos}" font-size="{font_size}" font-family="sans-serif" style="fill: {color}; stroke: {color}"> {content} </text>'

PAGE_HEIGHT = 3367
PAGE_WIDTH = 2380