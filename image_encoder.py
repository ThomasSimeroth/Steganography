from PIL import Image
import random


'''
ImageEncoder
    a class to load, encode, and save an image file using random spacing of 
    the set of 3 pixels needed to encode a character
Attributes:
    filename: the filename of the image to encode
'''
class ImageEncoder:
    def __init__( self, filename ):
        self.image_file = filename

        try:
            self.original_image = Image.open( self.image_file )
        except:
            print("File could not be opened.")
            sys.exit(1)

        self.image_format = self.original_image.format

        self.encoded_image = self.original_image.copy()
        self.pixel_matrix = self.encoded_image.load()

        self.image_width = self.encoded_image.size[0]
        self.image_height = self.encoded_image.size[1]
        self.pixel_num = self.image_width * self.image_height

        self.stored_data = ""
        self.encoded = False

    def encode( self, data ):
        '''
        encode
            encodes the data passed to the image using least significant 
            bit steganography
        Parameters:
            data: a string of characters to hide within the image
        Returns:
            True: on success
            False: if the image has already been encoded or if the data
            string is too long to be stored in the image
        '''
        NUM_PIXELS_FOR_CHAR = 3

        if self.encoded:
            print( "Image has already been encoded with data." )
            return False

        if len(data) * NUM_PIXELS_FOR_CHAR > self.pixel_num:
            print( "Size of input is too large for image to store." )
            return False

        self.stored_data = data

        pixels_used = len( data ) * NUM_PIXELS_FOR_CHAR
        max_index = ( ( self.pixel_num - pixels_used ) / pixels_used )
        section_size = max_index + NUM_PIXELS_FOR_CHAR
        section_num = self.pixel_num / section_size

        current_col = 0
        current_row = 0

        for i in range( section_num ):
            random_index = random.randint( 0, max_index )

            for j in range( random_index ):
                self.pixel_matrix[current_col, current_row] = self.zero_pixel( self.pixel_matrix[current_col, current_row] )
                current_col += 1
                if current_col > self.image_width:
                    current_col = 0
                    current_row += 1

            pixel_set = []
            pixel_set_coordinates = []
            for j in range( NUM_PIXELS_FOR_CHAR ):
                pixel_set.append( self.pixel_matrix[current_col, current_row] )
                pixel_set_coordinates.append( ( current_col, current_row ) )
                current_col += 1
                if current_col > self.image_width:
                    current_col = 0
                    current_row += 1

            new_pixel_set = self.store_char( data[0], pixel_set )
            data = data[1:]

            for new_pixel in new_pixel_set:
                self.pixel_matrix[pixel_set_coordinates[0][0], pixel_set_coordinates[0][1]] == new_pixel
                pixel_set_coordinates = pixel_set_coordinates[1:]

            for j in range( section_size - ( random_index + NUM_PIXELS_FOR_CHAR ) ):
                self.pixel_matrix[current_col, current_row] = self.zero_pixel( self.pixel_matrix[current_col, current_row] )
                current_col += 1
                if current_col > self.image_width:
                    current_col = 0
                    current_row += 1

        self.encoded = True

        return True

    def reset_image( self ):
        '''
        reset_image
            resets the encoded image back to the original image
        '''
        self.encoded_image = self.original_image.copy()
        self.encoded = False

    def bin_to_pixel( bin_pixel ):
        '''
        bin_to_pixel
            converts a tuple with three binary values into a tuple containing
            the integer representations of those values
        Parameters:
            bin_pixel: a tuple with three binary values
        Returns
            a tuple with the binary values converted to integers
        '''
        return ( int( bin_pixel[0], 2 ), int( bin_pixel[1], 2 ), int( bin_pixel[2], 2 ) )

    def zero_pixel( self, pixel ):
        '''
        zero_pixel
            sets the least significant bit of the first value in the pixel
            tuple to zero
        Parameters:
            pixel: the pixel tuple to zero the first value for
        Returns:
            zeroed_pixel: the zeroed pixel tuple
        '''
        bin_pixel = self.pixel_to_bin( pixel )
        zeroed_position = bin_pixel[0][:-1] + "0"
        zeroed_pixel = ( zeroed_position, bin_pixel[1], bin_pixel[2] )
        zeroed_pixel = self.bin_to_pixel( zeroed_pixel )
        return zeroed_pixel

    def pixel_to_bin( rgb_tuple ):
        '''
        pixel_to_bin
            converts a tuple with three integer values into a tuple containing
            the binary representations of those values
        Parameters:
            rgb_tuple: a pixel tuple of three integers 0-255
        Returns
            a tuple with the integer values converted to binary
        '''
        return ( bin( rgb_tuple[0] ), bin( rgb_tuple[1] ), bin( rgb_tuple[2] ) )

    def store_char( self, char, pixel_list ):
        '''
        store_char
            stores a single character into a set of three pixels, setting the
            first of the nine least significant bits to 1 to designate the 
            start of an encoded pixel block
        Parameters:
            char: the single character to store in the pixel set

            pixel_list: a list containing three pixel tuples to store the 
            character in
        Returns:
            new_pixel_list: a list containing the three pixel tuples encoded
            with the character in their least significant bits
        '''
        char_value = ord( char )
        char_bin = bin( char_value )

        bin_pixel_list = []
        for pixel in pixel_list:
            bin_pixel_list.append( self.pixel_to_bin( pixel ) )

        new_pixel_list = []

        first_bin_val = True
        for pixel in bin_pixel_list:
            new_bin_values = []
            for bin_val in pixel:
                if !first_bin_val:
                    new_bin_values.append( bin_val[:-1] + char_bin[0] )
                    char_bin = char_bin[1:]
                else:
                    new_bin_values.append( bin_val[:-1] + "1" )
                    first_bin_val = False
            new_pixel_list.append( tuple( new_bin_values ) )

        for i in range( len( new_pixel_list ) ):
            new_pixel_list[i] = self.bin_to_pixel( new_pixel_list[i] )

        return new_pixel_list

    def save_image( self, filename, new_format = None ):
        '''
        save_image
            saves the encoded image to a file using the passed filename, and
            format if one is specified
        Parameters:
            filename: the new image filename as a string, without the .format 
            on the end

            new_format: a standard image format to use as a string, defaulting
            to the original format if no format parameter is passed
                ex. "png", "JPEG", etc.
        Returns:
            True: on success

            False: if the image could not be saved, or if a file with that
            name already exists (to prevent loss of the original image)
        '''
        if new_format is None:
            new_format = self.image_format

        if filename + "." + new_format == self.image_file:
            print( "File already exists." )
            return False

        try:
            self.encoded_image.save( filename, new_format )
            return True
        except:
            print( "Incorrect filename or format specified." )
            return False