# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

from edgetpuvision import svg

CSS_STYLES = str(svg.CssStyle({'.back': svg.Style(fill='black',
                                                  stroke='black',
                                                  stroke_width='0.5em')}))

def size_em(length):
    return '%sem' % str(0.6 * length)

def overlay(title, results, inference_time, layout):
    x0, y0, width, height = layout.window
    font_size = 0.03 * height

    defs = svg.Defs()
    defs += CSS_STYLES

    doc = svg.Svg(width=width, height=height,
                  viewBox='%s %s %s %s' % layout.window,
                  font_size=font_size, font_family='monospace', font_weight=500)
    doc += defs

    ox1, ox2 = x0 + 20, x0 + width - 20
    oy1, oy2 = y0 + 20 + font_size, y0 + height - 20

    # Classes
    lines = ['%s (%.2f)' % pair for pair in results]
    for i, line in enumerate(lines):
        y = oy2 - i * 1.7 * font_size

        doc += svg.Rect(x=0, y=0, width=size_em(len(line)), height='1em',
                        transform='translate(%s, %s) scale(-1,-1)' % (ox2, y),
                        _class='back')

        doc += svg.Text(line, text_anchor='end', x=ox2, y=y, fill='white')

    # Title
    if title:
        doc += svg.Rect(x=0, y=0, width=size_em(len(title)), height='1em',
                        transform='translate(%s, %s) scale(1,-1)' % (ox1, oy1), _class='back')
        doc += svg.Text(title, x=ox1, y=oy1, fill='white')

    # Info
    lines = [
        'Inference time: %.2f ms (%.2f fps)' % (inference_time, 1000.0 / inference_time)
    ]

    for i, line in enumerate(reversed(lines)):
        y = oy2 - i * 1.7 * font_size
        doc += svg.Rect(x=0, y=0, width=size_em(len(line)), height='1em',
                       transform='translate(%s, %s) scale(1,-1)' % (ox1, y), _class='back')
        doc += svg.Text(line, x=ox1, y=y, fill='white')

    return str(doc)
