class MainParams:
    def __init__(self, param):
        self.table_len = param.get(1)
        self.images_cnt = param.get(2)

    def __repr__(self):
        return f'MainParams(table_len={self.table_len}, images_cnt={self.images_cnt})'
