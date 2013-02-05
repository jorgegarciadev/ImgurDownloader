#!/usr/bin/env python
#encoding: utf-8

#<meta name="twitter:title" value="Prueba">

import os, sys, re, urllib, math

HELP_MESSAGE = '''
Script para descargar automáticamente albumes de Imgur.

Modo de uso:
~$ ./ImgurDownloader.py [URL del album] [Ruta a carpeta de destino]

Ejemplo:
~$ ./ImgurDownloader.py http://imgur.com/a/LXS9b /home/jorge/fotos

Si se omite la carpeta de destino se creará una carpeta con el mismo nombre
que el album, esto es, si la URL es http://imgur.com/a/LXS9b la carpeta
se llamará LXS9b.

'''

class DownloaderError(Exception):
    def __init__(self, msg=False):
        self.msg = msg

class ImgurDownloader():
    def __init__(self, albumUrl):
        self.albumUrl = albumUrl

        pattern = "http://(www\.)?imgur\.com/a/(\w+)(#\w+)?"

        match = re.match(pattern, albumUrl)
        if not match:
            raise DownloaderError('\nLa dirección no es correcta.')

        self.albumId = match.group(2)

        imgurAlbum = 'http://imgur.com/a/' + self.albumId + '/noscript'
        self.response = urllib.urlopen(imgurAlbum)

        if self.response.getcode() != 200:
            raise DownloaderError('\nError al conectar con Imgur: %d' % self.response.getcode())

    def SaveImages(self, destinationFolder = False):

        html = self.response.read()
        pattern = '<img src="(http://i\.imgur\.com/((\w+)\.(png|jpg|jpeg|gif)))"'
        self.images = re.findall(pattern, html)
        print '\n%d Imágenes encontradas.\n' % len(self.images)

        if destinationFolder:
            albumFolder = destinationFolder
        else:
            albumFolder = self.albumId

        if not os.path.exists(albumFolder):
            os.makedirs(albumFolder)

        for (index, image) in enumerate(self.images):
            print "Descargando imagen %d de %d: %s" % (index+1,len(self.images),image[0])
            prefix = "%s-" % (str(index).zfill(int(math.log(len(self.images),10))+1))
            path = os.path.join(albumFolder, prefix + image[1])
            try:
                urllib.urlretrieve(image[0], path)
            except IOError:
                print 'Error al descargar el archivo %s, probando de nuevo.\n' % (image[0])
                urllib.urlretrieve(image[0], path)
        print "\nAlbum %s descargado" % self.albumUrl


if __name__ == '__main__':
    args = sys.argv

    if len(args) == 1:
        
        print HELP_MESSAGE
        exit()

    try:
        downloader = ImgurDownloader(args[1])

        if len(args) == 3:
            albumFolder = args[2]
        else:
            albumFolder = False

        downloader.SaveImages(albumFolder)
        exit()
    except DownloaderError as error:
        print "\nError: %s\n" % error.msg
        exit(1)
