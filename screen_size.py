from math import sqrt

widescreen = 16/9

def in_to_cm(inches):
    return inches*2.54

def height_from(diag, aspect_ratio=widescreen):
    return diag / sqrt(1 + aspect_ratio**2)

def width_from(diag, aspect_ratio=widescreen):
    return aspect_ratio * height_from(diag, aspect_ratio)

if __name__ == '__main__':
  s = input('TV size (inches): ')
  while s:
    diag_in = float(s)
    height_in = height_from(diag_in)
    width_in = width_from(diag_in)

    print(f'A {diag_in:.0f}-inch TV is about {in_to_cm(height_in):.1f}cm x {in_to_cm(width_in):.1f}cm')
    s = input('TV size (inches): ')

