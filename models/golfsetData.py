from app import db
from models.users import User
import datetime as dt

class ClubHead(db.Document):
    meta = {'abstract': True, 'allow_inheritance': True}
    loft = db.IntField()
    weight = db.FloatField()

class WoodHead(ClubHead):
    meta={'collection': 'woodHeads'}
    size = db.StringField()

    @staticmethod
    def createWoodHead(loft, weight, size):
        woodHead = WoodHead.objects(loft=loft, weight=weight).first()
        if not woodHead:
            woodHead = WoodHead(loft=loft, weight=weight, size=size).save()
        return woodHead

    def getClubHeight():
        return float(size/400)

class IronHead(ClubHead):
    meta={'collection': 'ironHeads'}
    material = db.StringField()

    @staticmethod
    def createIronHead(loft, weight, material):
        ironHead = IronHead.objects(loft=loft, weight=weight).first()
        if not ironHead:
            ironHead = IronHead(loft=loft, weight=weight, material=material).save()
        return ironHead

    def getClubHeight():
        return 1

class PutterHead(ClubHead):
    meta={'collection': 'putterHeads'}
    style = db.StringField()

    @staticmethod
    def createPutterHead(loft, weight, style):
        putterHead = PutterHead.objects(loft=loft, weight=weight).first()
        if not putterHead:
            putterHead = PutterHead(loft=loft, weight=weight, style=style).save()
        return putterHead

    def getClubHeight(self):
        return float(1 if self.style == "Blade" else 0.5)

class Shaft(db.Document):
    meta = {'collection': 'shafts'}
    material = db.StringField()
    length = db.FloatField()
    weight = db.IntField()
    flex = db.StringField()
    height = db.FloatField()

    @staticmethod
    def createShaft(length, weight, material, flex):
        shaft = Shaft.objects(length=length, weight=weight, material=material, flex=flex).first()
        if not shaft:
            shaft = Shaft(length=length, weight=weight, material=material, flex=flex).save()
        return shaft

    def getShaftHeight(self):
        return self.height

        
class Grip(db.Document):
    meta = {'collection': 'manufacturers'}
    diameter = db.FloatField()
    weight = db.IntField()
    material = db.StringField()

    @staticmethod
    def createGrip(diameter, weight, material):
        grip = Grip.objects(diameter=diameter, weight=weight, material=material).first()
        if not grip:
            grip = Grip(diameter=diameter, weight=weight, material=material).save()
        return grip

class Club(db.Document):
    meta = {'collection': 'Golfset'} 
    email = db.StringField() 
 
    label = db.StringField() 
    clubtype = db.StringField() 
    clubheadloft = db.FloatField() 
    clubheadweight = db.IntField() 
    clubheadsize_material_style = db.StringField() 
    shaftlength = db.FloatField() 
    shaftweight = db.IntField() 
    shaftmaterial = db.StringField() 
    shaftflex = db.StringField() 
    gripdiameter = db.FloatField() 
    gripweight = db.IntField() 
    gripmaterial = db.StringField()

    @staticmethod
    def createClub(dataString):
        parts = dataString.split(",")
        club = Club.objects(label=parts[0]).first()
    
        if not club:
            if parts[1].strip() == "Wood":
                clubhead = WoodHead.createWoodHead(float(parts[2]), int(parts[3]), (parts[4]))
            if parts[1].strip() == "Iron":
                clubhead = WoodHead.createWoodHead(float(parts[2]), int(parts[3]), (parts[4]))
            if parts[1].strip() == "Putter":
                clubhead = WoodHead.createWoodHead(float(parts[2]), int(parts[3]), (parts[4]))

            shaft = Shaft.createShaft(float(parts[5]), int(parts[6]), parts[7], parts[8])
            grip = Grip.createGrip(float(parts[9]), int(parts[10]), parts[11])
            club = Club(label=parts[0], head=clubhead, shaft=shaft, grip=grip).save()
        
        return club

    def geteadClubHeadHeight(self):
        return self.shaft.getShaftHeight() + self.head.getClubHeadHeight()

    def getDistance(self, speed):
        club_head_height = self.geteadClubHeadHeight()
        club_length = club_head_height + self.shaftlength
 
        if self.clubtype == "Wood":
            club.clubheadsize_material_style = int(self.clubheadsize_material_style.split("-")[0])
            club_head_height = club_head_size / 400

            estimated_distance = (280 - abs(48 - club_length) * 10 - abs(self.clubheadloft - 10) * 1.25) * float(speed) / 96
        elif self.clubtype == "Iron":
            club_head_height = 1
            estimated_distance = (280 - abs(48 - club_length) * 10 - abs(self.clubheadloft - 10) * 1.25) * float(speed) / 96
        else:
            if self.clubtype == "Putter":
                club_head_height = 0.5
                estimated_distance = (280 - abs(48 - club_length) * 10 - abs(self.clubheadloft - 10) * 1.25) * float(speed) / 96   

        return estimated_distance

class GolfSet(db.Document):
    meta = {'collection': 'golfsets'}
    golfer = db.ReferenceField(User)
    clubs = db.DictField()
    
    @staticmethod
    def createGolfSet(email, label, clubtype, clubheadloft, clubheadweight, clubheadsize_material_style, shaftlength, shaftweight, shaftmaterial, shaftflex, gripdiameter, gripweight, gripmaterial): 
        club = Club.objects(email=email, label=label, clubtype=clubtype, clubheadloft=clubheadloft, clubheadweight=clubheadweight, clubheadsize_material_style=clubheadsize_material_style, shaftlength=shaftlength, shaftweight=shaftweight, shaftmaterial=shaftmaterial, shaftflex=shaftflex, gripdiameter=gripdiameter, gripweight=gripweight, gripmaterial=gripmaterial).first()

        if not club:
            club = Club(email=email, label=label, clubtype=clubtype, clubheadloft=clubheadloft, clubheadweight=clubheadweight, clubheadsize_material_style=clubheadsize_material_style, shaftlength=shaftlength, shaftweight=shaftweight, shaftmaterial=shaftmaterial, shaftflex=shaftflex, gripdiameter=gripdiameter, gripweight=gripweight, gripmaterial=gripmaterial)
            club.save()
        return club

    @staticmethod
    def addClub(self, club):
        if club.label in self.clubs:
            return False
        club.label = parts[0]
        self.save()
        return True

    @staticmethod
    def getGolfSetByEmail(email):
        golfer = User.getUser(email)
        if golfer:
            return GolfSet.objects(golfer=golfer).first()
        else:
            return None

    def getClubs(self):
        return self.clubs
    
    def getClub(self, label):
        return self.clubs.get(label)

class Swing(db.Document):
    meta = {'collection': 'swings'}
    golfer = db.StringField()
    club = db.StringField()
    swingSpeed = db.FloatField()
    swing_datetime = db.DateTimeField()
    distance = db.FloatField()

    @staticmethod
    def createSwingDistance(email, club, swingSpeed, datetime_str, distance):
        swing_datetime_obj = dt.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")
        swing = Swing.objects(golfer=email, club=club, swingSpeed=swingSpeed, swing_datetime=swing_datetime_obj,distance=distance).first()
        if not swing:
            swing = Swing(golfer=email, club=club, swingSpeed=swingSpeed, swing_datetime=swing_datetime_obj,distance=distance)
            swing.save()
        return swing

    @staticmethod
    def getAllOwnersWhoSwings():
        golfers = [] # list of emails
        swings = Swing.objects()
        for swing in swings:
            if not (swing.golfer in golfers):
                golfers.append(swing.golfer)
        return golfers

    @staticmethod
    def getDateTimeDistanceList(email):
        datetime_distance_list = []

        golfer = User.getUser(email)
        if golfer:
            swings = Swing.objects(golfer=email)
            for d in swings:
                datetime_str = dt.datetime.strftime(d.swing_datetime, "%Y-%m-%d %H:%M:%S")
                datetime_distance_list.append([datetime_str, d.distance])

            datetime_distance_list.sort(key=lambda x: x[0])
            
        return datetime_distance_list


    def getDistance(email,label, speed):

        club = Club.objects(email=email,label=label).first()

        if club.clubtype == "Wood":
            distance = (280 - abs(48 - ((float(club.clubheadsize_material_style)/400) + club.shaftlength))*10 - abs(club.clubheadloft - 10)*1.25) * float(speed)/float(96) 
            return float(distance)
        elif club.clubtype == "Iron":
            distance = (280 - abs(48-(1+club.shaftlength)) * 10 - abs(club.clubheadloft - 10) * 1.25) * float(speed)/float(96) 
            return float(distance)
        elif club.clubtype == "Putter":
            distance = (280 - abs(48-(0.5+club.shaftlength))*10 - abs(club.clubheadloft - 10)*1.25) * float(speed)/float(96)
            return float(distance)