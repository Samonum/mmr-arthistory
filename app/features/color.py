import unittest

################################################################################
# FUNCTIONS
################################################################################

def rgbToHsv(rgb):
	"""
	Converts an array with RGB values to HSV values
	"""
	rgb = [c/255.0 for c in rgb]
	
	maxi = 0 if rgb[0] > rgb[1] else 1
	maxi = maxi if rgb[maxi] > rgb[2] else 2
	
	mini = 0 if rgb[0] < rgb[1] else 1
	mini = mini if rgb[maxi] < rgb[2] else 2
	
	d = rgb[maxi] - rgb[mini]
	hsv = [0] * 3
	
	#Black means all 0 even in HSV
	if rgb[maxi] == 0:
		return hsv
		
	hsv[2] = rgb[maxi]
	
	#Gray means no hue or saturation
	if d == 0:
		return hsv
		
	if maxi == 0:
		hsv[0] = 60 * (((rgb[1] - rgb[2]) / d) % 6)
	elif maxi == 1:
		hsv[0] = 60 * ((rgb[2] - rgb[0]) / d + 2)
	else:
		hsv[0] = 60 * ((rgb[0] - rgb[1]) / d + 4)
	
	hsv[1] = d/rgb[maxi]
	return hsv

def huecount(num):
    """
    This is a docstring, it tells something about the function when you
    execute help(huecount). Three quotation marks enable multiline strings.

    Currently this is a nonsense function for illustration purposes.

    To calculate actual hue you can use the Pillow package (image I/O, calcs).
    I googled a bit and there seems to be a 'posterize' function that reduces
    the number of colors, then you'll only have to count the number of colors
    remaining, possibly with a minimum treshold (e.g. at least 3 pixels of this
    color).
    http://pillow.readthedocs.io/en/3.1.x/reference/ImageOps.html#PIL.ImageOps.posterize
    """
    return num+8

################################################################################
# TESTS
################################################################################

# The unittest module provides nice utilities for testing
# Check out docs at https://docs.python.org/3/library/unittest.html !!!
class TestColorFeatures(unittest.TestCase):

    def test_hue(self):
        # Put in this test's docstring what this tested function should do
        "Should output correct hue count"
        # You should load the image here
        # Then pass it to function...
        self.assertEqual(huecount(34), 42)
        # ... and then evaluate the output

# This if statement gets executed when you run this file, so > python color.py
if __name__ == '__main__':
    # It's a convenient way of running unittests!
    unittest.main()
