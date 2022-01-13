import pkg_resources

from .. import __version__, __name__ as pkg_name


APP_ICON = pkg_resources.resource_filename(__name__, 'app_icon.ico')
PREV_TEST = pkg_resources.resource_filename(__name__, 'prev_test.png')
PREV_TEST_8 = pkg_resources.resource_filename(__name__, 'prev_test_8.png')

ST_NAME = 'Watch Face Editor'
ST_PKG_NAME = pkg_name
ST_VERSION = __version__
ST_DESCRIPTION = 'Watch Face Editor'
ST_COPYRIGHT = 'Copyright (c) 2022 Alexander Baskikh'
ST_HOMEPAGE = f'https://github.com/baskiton/{pkg_name}'
ST_LICENSE_LINK = f'https://github.com/baskiton/{pkg_name}/blob/main/LICENSE'
ST_LICENSE = (
        'MIT License\n\n'
        'Copyright (c) 2022 Alexander Baskikh\n\n'
        'Permission is hereby granted, free of charge, to any person obtaining a copy '
        'of this software and associated documentation files (the "Software"), to deal '
        'in the Software without restriction, including without limitation the rights to '
        'use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies '
        'of the Software, and to permit persons to whom the Software is furnished to do '
        'so, subject to the following conditions:\n\n'
        'The above copyright notice and this permission notice shall be included in all '
        'copies or substantial portions of the Software.\n\n'
        'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR '
        'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, '
        'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE '
        'AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, '
        'WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN '
        'CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'
)
