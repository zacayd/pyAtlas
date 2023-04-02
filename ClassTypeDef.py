import json

import requests
import  os

from AtlasApi import AtlasApi


class TypeDef:
  def __init__(self, dir_path,url):
    #json_files = [f for f in os.listdir(dir_path) if f.endswith('.json')]

    self.file_data = {}
    self.dir_path=dir_path
    self.url=url



  def runTypeDefs(self, dir_path):
    try:
      json_files = self.get_json_files(dir_path)
      for file_name in json_files:
        with open(os.path.join(dir_path, file_name)) as f:
          payload = json.load(f)
          fname = os.path.basename(file_name)
          self.file_data[fname] = payload
          print(fname)

          api=AtlasApi(self.url+'types/typedefs')
          result = api.ApiAction (payload,"POST")
          if 'errorCode' in json.loads(result):
            print(json.loads(result)['errorMessage'])

    except Exception as e:
      print(e)



  def get_json_files(self,dir_path):
      json_files = []
      for filename in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, filename)):
          if filename.endswith('.json'):
            json_files.append( filename)
      return json_files








  def print_value(self):
    print(self.value)




