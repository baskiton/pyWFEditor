class WFError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg

    def __repr__(self):
        return self.message


class WFFileFormatError(WFError):
    def __init__(self):
        super().__init__(f'Not a Watchface file')


class WFImageFormatError(WFError):
    def __init__(self, sign):
        super().__init__(f'Unknown image signature: {sign}')
