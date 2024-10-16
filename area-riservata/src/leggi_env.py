import os
from dotenv import load_dotenv

load_dotenv()

class Endpoint:
  def __init__(self, users_url, users2_url,institutions_url, onboardingusers_url,quee_url,api_url):
    if not users_url or not users2_url or not institutions_url or not onboardingusers_url or not quee_url or not api_url:
      raise ValueError("Uno o più ENDPOINT di chiamata non è stato configurato correttamente")
    else:
      self.users_url = users_url
      self.users2_url = users2_url
      self.institutions_url = institutions_url
      self.onboardingusers_url = onboardingusers_url
      self.quee_url=quee_url
      self.api_url=api_url

class ApiKey:
  def __init__(self, delete, adduser,get_user_info_key):
    if not delete   or not adduser or not get_user_info_key:
      raise ValueError("Una o più KEY di chiamata non è stata configurata correttamente")
    else:
      self.delete = delete
      self.adduser = adduser
      self.get_user_info_key=get_user_info_key

class ProductsKey:
  def __init__(self, pagopa, interop, io):
    if not pagopa or not interop or not io:
      raise ValueError("Una o più KEY di prodotto non è stata configurata correttamente")
    else:
      self.pagopa = pagopa
      self.interop = interop
      self.io = io

class MongoSettings: #aggiornato 
  def __init__(self,mongokey,mongourl):
    if not mongokey or not mongourl:
      raise ValueError("Una o più KEY di prodotto non è stata configurata correttamente")
    else:
      self.mongokey = mongokey
      self.mongourl=mongourl
      
    

class ConfigObj:
    def __init__(self, apikey, endpoint, productkey, mongokey):
        self.apikey = apikey
        self.endpoints = endpoint
        self.productkey = productkey
        self.mongokey = mongokey 
         


class ConfigEnv:
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(ConfigEnv, cls).__new__(cls)
    return cls.instance

  def loadConfig(self):
    obj = ConfigObj(
      ApiKey(os.getenv('delete_key'), os.getenv('add_user_key'), os.getenv('get_user_info_key')), 
      Endpoint(os.getenv('users_url'), os.getenv('users2_url'), os.getenv('institutions_url'), os.getenv('onboardingusers_url'), os.getenv("queue_url"),os.getenv("api_url")),
      ProductsKey(os.getenv('prod_pagopa'), os.getenv('prod_interop'), os.getenv('prod_io')),
      MongoSettings(os.getenv("mongokey"), os.getenv("mongourl"))    )
    
    return obj


