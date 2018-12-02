from PIL import Image
import random

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
        NUM_PIXELS_FOR_CHAR = 3

        if encoded:
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
                self.pixel_matrix[current_col, current_row] = zero_pixel( self.pixel_matrix[current_col, current_row] )
                current_col += 1
                if current_col > image_width:
                    current_col = 0
                    current_row += 1

            pixel_set = []
            for j in range( NUM_PIXELS_FOR_CHAR ):
                pixel_set.append( self.pixel_matrix[current_col, current_row] )
                current_col += 1
                if current_col > image_width:
                    current_col = 0
                    current_row += 1

            for j in range( section_size - ( random_index + NUM_PIXELS_FOR_CHAR ) ):
                self.pixel_matrix[current_col, current_row] = zero_pixel( self.pixel_matrix[current_col, current_row] )
                current_col += 1
                if current_col > image_width:
                    current_col = 0
                    current_row += 1

            new_pixel_set = store_char( data[0], pixel_set )
            data = data[1:]

        self.encoded = True

        return True

    def reset_image( self ):
        self.encoded_image = self.original_image.copy()

    def bin_to_pixel( bin_pixel ):
        return ( int( bin_pixel[0], 2 ), int( bin_pixel[1], 2 ), int( bin_pixel[2], 2 ) )

    def zero_pixel( pixel ):
        bin_pixel = pixel_to_bin( pixel )
        zeroed_position = bin_pixel[0][:-1] + "0"
        new_pixel = ( zeroed_position, bin_pixel[1], bin_pixel[2] )
        new_pixel = bin_to_pixel( new_pixel )
        return new_pixel

    def pixel_to_bin( rgb_tuple ):
        return ( bin( rgb_tuple[0] ), bin( rgb_tuple[1] ), bin( rgb_tuple[2] ) )

    def store_char( char, pixel_list ):
        char_value = ord( char )
        char_bin = bin( char_value )

        bin_pixel_list = []
        for pixel in pixel_list:
            bin_pixel_list.append( pixel_to_bin( pixel ) )

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
            new_pixel_list[i] = bin_to_pixel( new_pixel_list[i] )

        return new_pixel_list

    def save_image( self, filename, format = None ):
        if format is None:
            format = self.image_format

        try:
            self.encoded_image.save( filename, format )
        except:
            print("Incorrect filename or format specified.")