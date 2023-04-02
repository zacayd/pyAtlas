import json

from ClassEntities import ClassEntities
from ClassTypeDef import TypeDef
class Program:
    def __init__(self):
        dir_path="Entities"
        with open('Config.json', 'r') as file:
            self.myDic = json.load(file)
            self.url=self.myDic["baseUrl"]






    def CreateTypeDef(self):
        dir_path="Entities"
        typeDefEntities = TypeDef(dir_path, self.url)
        print("run entities:")
        typeDefEntities.runTypeDefs(dir_path)
        print("end run entities")
        dir_path = "RelationShips"
        print("run relationships ...")
        relationShipEntities = TypeDef(dir_path, self.url)
        relationShipEntities.runTypeDefs(dir_path)
        print("end relationships")

    def run(self,connectionID):
        en = ClassEntities("SSIS", self.url+ 'entity')
        en.Populate(connectionID)


    def GetDictFromJson(self,ky):
        with open('Config.json', 'r') as file:
            myDic=json.load(file)
            if ky in myDic:
                return myDic[ky]

pg=Program()
connectionID=pg.GetDictFromJson('connectionid')
#pg.CreateTypeDef()
pg.run(connectionID)


