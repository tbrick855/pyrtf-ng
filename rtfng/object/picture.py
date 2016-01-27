from binascii import hexlify

from rtfng.document.base import RawCode

from PIL import Image as PIL_Image

class Image( RawCode ) :

    #  Need to add in the width and height in twips as it crashes
    #  word xp with these values.  Still working out the most
    #  efficient way of getting these values.
    # \picscalex100\picscaley100\piccropl0\piccropr0\piccropt0\piccropb0
    # picwgoal900\pichgoal281

    PICT_TYPES = { 'png' : 'pngblip',
                   'jpeg' : 'jpegblip',
                 }

    def __init__( self, file_name, **kwargs ) :

        im = PIL_Image.open(file_name)
        im.thumbnail((500,500), PIL_Image.ANTIALIAS)
        pict_type = self.PICT_TYPES[im.format.lower()]
        width = im.width
        height = im.height
        im.save(file_name)
        im.close()

        codes = [ pict_type,
                  'picwgoal%s' % (width  * 20),
                  'pichgoal%s' % (height * 20) ]
        for kwarg, code, default in [ ( 'scale_x',     'scalex', '100' ),
                                      ( 'scale_y',     'scaley', '100' ),
                                      ( 'crop_left',   'cropl',    '0' ),
                                      ( 'crop_right',  'cropr',    '0' ),
                                      ( 'crop_top',    'cropt',    '0' ),
                                      ( 'crop_bottom', 'cropb',    '0' ) ] :
            codes.append( 'pic%s%s' % ( code, kwargs.pop( kwarg, default ) ) )


        #  reset back to the start of the file to get all of it and now
        #  turn it into hex.
        fin = open(file_name, 'rb')
        data = []
        image = hexlify( fin.read() )
        for i in range( 0, len( image ), 128 ) :
            data.append( image[ i : i + 128 ] )

        data = r'{\pict{\%s}%s}' % ( '\\'.join( codes ), '\n'.join([x.decode('UTF-8') for x in data]))
        RawCode.__init__( self, data )

    def ToRawCode( self, var_name ) :
        return '%s = RawCode( """%s""" )' % ( var_name, self.Data )

