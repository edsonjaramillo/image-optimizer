# Image Optimizer

This is a program made with python that I created to help my clients optimize a large number of images at once. This ultimately helped reduce the amount of size taken for storage on their CMS and decreased load times. The images are also converted to `.webp` format for even more storage saving while still keeping the image quality.

## Technologies used:

- [Python 3.10](https://www.python.org/)
- [Tkinter GUI Library](https://docs.python.org/3/library/tkinter.html)
- [PIL Library](https://pillow.readthedocs.io/en/stable/)

## Preview

![Program screenshot](https://media.graphassets.com/gQF1YUL9S1qDjqTbexGn)

## Process

If let's say two images with dimensions of `4096x2730` with a size of `430kb` and `4928x3264` with a size of `1689kb` and the settings are set to a `600px` minimum the two images will be reduced down to `897x597` and `901x597` respectively. The images were then compressed to `15kb` and `11kb` respectively.

![Screenshot showing an alert with 98% reduction size](https://media.graphassets.com/qXNUFfsnQLKaZfcXvFIb)
