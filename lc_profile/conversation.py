from leancloud import LeanCloudError, Object


LC_STORE_ROW_NOT_FOUND = 101
LC_STORE_ROW_NOT_UNIQUE = 137


class Conversation(Object):

    @classmethod
    def get_by_name(cls, name):
        return cls.query.equal_to('name', name).first()

    @classmethod
    def create(cls, name, members=None, unique=True):
        if members is None:
            members = []

        if unique:
            conv = cls(name=name, uniqueId=name, m=members)
        else:
            conv = cls(name=name, m=members)

        try:
            conv.save()
            return conv
        except LeanCloudError as error:
            if error.code == LC_STORE_ROW_NOT_UNIQUE:
                conv = cls.get_by_name(name)
                conv.ensure_members(members)
                return conv
            raise

    @classmethod
    def get_or_create(cls, name, members=None, unique=True):
        try:
            conv = cls.get_by_name(name)
            conv.ensure_members(members)
            return conv
        except LeanCloudError as error:
            if error.code == LC_STORE_ROW_NOT_FOUND:
                return cls.create(name, members, unique)
            raise

    def ensure_members(self, members):
        if set(self.get('m')) == set(members):
            return
        self.set('m', members)
        self.save()


Conversation._class_name = '_Conversation'  # LeanCloud 内部类
