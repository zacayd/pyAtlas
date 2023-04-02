import hashlib
import json
import os

from datetime import datetime

import pandas as pd
from AtlasApi import AtlasApi
from DataAccessLayer import DataAccessLayer


class ClassEntities:
  def __init__(self, entityName,url):
    #json_files = [f for f in os.listdir(dir_path) if f.endswith('.json')]
    self.entityName =entityName
    self.url=url
    self.readDictFromFile()

    with open('Config.json', 'r') as file:
        self.data = json.load(file)
        self.connectionString=self.data['CustomerDbConnectionString']
    # conn_string = f"mssql+pyodbc://{usr}:{pwd}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    self.dal=DataAccessLayer(self.connectionString)

  def compute_md5(self,txt):
      # encode the string as bytes before hashing
      encoded_string = txt.encode('utf-8')


      hash_object = hashlib.md5(encoded_string)

      # convert the hash to a hexadecimal string representation
      hash_hex = hash_object.hexdigest()

      return hash_hex


  def  Populate(self,connectionid):
        self.CreateEntities(connectionid)
        self.CreateRelations(connectionid)

  def CreateRelations(self, connectionid):
      relations = self.data["relations"]
      for k in relations:
          for y in k.items():
              try:
                  query = y[1]["Query"]
                  df = self.dal.execute_query(query, connectionid)
                  child = y[0].split('_')[0]
                  if len(y[0].split('_')) == 1:
                      parent = ""
                  else:
                      parent = y[0].split('_')[1]
                  print(f"load type{child}")
                  self.dfRelationToDict(df, parent, child)
                  print(f"end load type{child}")
              except Exception as e:
                  print(e)

  def CreateEntities(self, connectionid):
      entities = self.data["entities"]
      for k in entities:
          for y in k.items():
              try:
                  query = y[1]["Query"]
                  df = self.dal.execute_query(query, connectionid)

                  child = y[0].split('_')[0]
                  if len(y[0].split('_')) == 1:
                      parent = ""
                  else:
                      parent = y[0].split('_')[1]

                  print(f"load type{child}")

                  self.dfToDict(df, parent, child)
                  print(f"end load type{child}")


              except Exception as e:
                  print(e)

  def writeDictToFile(self):
      with open("dictGuidQualifiedName.json", "w") as file:
          file.write(json.dumps(self.dictGuidQualifiedName))

  def readDictFromFile(self):
      if os.path.isfile('dictGuidQualifiedName.json'):
          with open('dictGuidQualifiedName.json', 'r') as file:
              self.dictGuidQualifiedName = json.load(file)
      else:
          print('File does not exist')
          self.dictGuidQualifiedName = {}

  def dfRelationToDict(self,df):
          # create list of dictionaries for each row in the dataframe
          rows = []
          for i, row in df.iterrows():
              source_type = row["SourcetypeName"]
              source_qualified_name = row["SourcequalifiedName"]
              target_type = row["TargetTypeName"]
              target_qualified_name = row["TargetqulaifiedName"]
              row_dict = {
                  "end1": {
                      "typeName": source_type,
                      "uniqueAttributes": {
                          "qualifiedName": source_qualified_name
                      }
                  },
                  "end2": {
                      "typeName": target_type,
                      "uniqueAttributes": {
                          "qualifiedName": target_qualified_name
                      }
                  },

                  "propagateTags": "NONE",
                  "typeName": row["RelationtypeName"]
              }
              rows.append(row_dict)

          # create dictionary with list of row dictionaries
          result_dict = {
              "entities": rows
          }

          print(json.dumps(result_dict))
          try:
              payload = result_dict
              api = AtlasApi(self.url)
              txt = api.ApiAction(payload, "POST")
              print(txt)
          except Exception as e:
              print(e)


  def dfToDict(self,df,parentTypeName,typeName):

      result = {}

      try:
          for _, row in df.iterrows():
             typeName=row['typeName']
              # create dictionary for referred entity

             ref_ent = {


                      "typeName": typeName,
                      "displayText": row["name"]
             }

             attributes = {}
             try:
                      attributes["displayName"] = row["name"]
                      qualifiedName=row["qualifiedName"]
                      attributes["qualifiedName"] = qualifiedName
             except Exception as e:
                   print(e)

             try:
                  for col_name, col_value in row.items():
                          if col_name not in ["ParentQualifiedName","ParentType"]:
                            attributes[col_name] = col_value

                  ref_ent["attributes"] = attributes
                  parentTypeName=row["ParentType"]
                  parenQualifiedName = row['ParentQualifiedName']




                  if parenQualifiedName!="-1":
                        try:
                            parenQualifiedName=row['ParentQualifiedName']
                            guid=self.getGuidByName(parenQualifiedName,self.dictGuidQualifiedName)
                            if guid==None:
                                print("Check why")
                            ref_ent["attributes"][parentTypeName]={"guid":guid,
                                               "typeName": parentTypeName}
                        except Exception as e:
                            print(e)
             except Exception as e:
                print(e)



             result["entity"] = ref_ent

             print(json.dumps(result))
             try:
                  payload = result
                  api = AtlasApi(self.url)
                  txt = api.ApiAction(payload, "POST")
                  qualifiedName = payload["entity"]["attributes"]["qualifiedName"]
                  guidDict = json.loads(txt)
                  guid = self.CreateGuidFromResult(guidDict)
                  self.dictGuidQualifiedName[qualifiedName] = guid
                  self.writeDictToFile()
             except Exception as e:
                  print(e)

      except Exception as e:
         print(e)


  def getGuidByName(self,qualifiedName,guidDict):
      guid=""
      try:
          if qualifiedName in self.dictGuidQualifiedName:
            guid= self.dictGuidQualifiedName[qualifiedName]
          else:
              values = [value for value in guidDict["guidAssignments"].values()]
              guid= values[0]
          if guid==None:
              print("None")
          return guid
      except Exception as e:
       print(e)


  def CreateGuidFromResult(self,guidDict):
      guid=""
      try:
          values = [value for value in guidDict["guidAssignments"].values()]
          guid= values[0]
          return guid
      except Exception as e:
       print(e)

