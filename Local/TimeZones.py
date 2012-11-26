# TODO integrate time zones with geoip
# TODO handle DST changes (there is a list somewhere)


# Atlantic Standard Time (Puerto Rico)
class AST(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours = -4)

    def dst(self, dt):
        return datetime.timedelta(0)

# Eastern Standard Tribe
class EST(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours = -5)

    def dst(self, dt):
        return datetime.timedelta(0)

# Central Standard
class CST(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours = -6)

    def dst(self, dt):
        return datetime.timedelta(0)

# Mountain Time
class MT(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours = -7)

    def dst(self, dt):
        return datetime.timedelta(0)

# Mountain Standard Time (Fucking Arizona only. Bad as Pike County)
class MST(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours = -7)

    def dst(self, dt):
        return datetime.timedelta(0)

# Pacific Standard Time
class PST(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours = -8)

    def dst(self, dt):
        return datetime.timedelta(0)

# Alaska Standard Time
class AKST(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours = -9)

    def dst(self, dt):
        return datetime.timedelta(0)

# Hawaii Standard Time
class HST(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours = -10)

    def dst(self, dt):
        return datetime.timedelta(0)

# Pu Muli Time Zone (American Samoa)
class STZ(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours = -11)

    def dst(self, dt):
        return datetime.timedelta(0)

