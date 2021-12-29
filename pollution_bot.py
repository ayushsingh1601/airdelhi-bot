from apscheduler.schedulers.blocking import BlockingScheduler
import praw
import collections
import time
import urllib.request, json
from praw.models import Message
from praw.models import Comment
from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.events import EVENT_JOB_EXECUTED


print("INITIALIZING.....")
def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')


def pollution():
  try:
      with urllib.request.urlopen("https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69?api-key=API_KEY&format=json&offset=0&limit=500") as url:
        data = json.loads(url.read().decode())
              
      json_string = json.dumps(data)
      python_obj = json.loads(json_string)

      pol_data = {}

      covid_string = ""
      sample = {
        "PM2.5":-1,
        "PM10":-1,
        "NO2":-1,
        "NH3":-1,
        "SO2":-1,
        "CO":-1,
        "OZONE":-1
      }
      timeofupdate = ""
      cou = 0
      for item in python_obj["records"]:
        station = item["station"]
        last_update = item["last_update"]
        timeofupdate = last_update
        station = station[:-14]
        if station == "Lodhi Roa":
          station = "Lodhi Road IMD"
        if station == "North Campus, D":
          station = "North Campus, DU"
        if station == "Pus":
            station = "Pusa IMD"
        if station == "Aya Naga":
            station = "Aya Nagar"
        if station == "IGI Airport (T3":
            station = "IGI Airport (T3)"
        if station == "CRRI Mathura Roa":
            station = "CRRI Mathura Road"

        pollutant_name = item["pollutant_id"]
        pollutant_min = "NA"
        pollutant_max = "NA"
        pollutant_avg = "NA"
        if "pollutant_min" in item:
            pollutant_min = item["pollutant_min"]
            pollutant_max = item["pollutant_max"]
            pollutant_avg = item["pollutant_avg"]

        city = item["city"]
        if(city == "Delhi"):
            new_dict = sample.copy()
            new_dict[pollutant_name] = pollutant_avg

            if station not in pol_data.keys():
              pol_data.update({station : new_dict})
            else:
              pol_data[station][pollutant_name] = new_dict[pollutant_name]
        else :
            cou = cou + 1
    ##            print("Delhi Exceeded and others excluded")
            
      print("Not Delhi : ",cou)
      string = "*DELHI POLLUTION*\n"
      string += "\n"
      string += "**Area**^[AQIs-pollutant-wise]|**PM2.5**|**PM10**|**NO2**|**NH3**|**SO2**|**CO**|**OZONE**\n-|-|-|-|-|-|-|-\n"
      print(pol_data)
      for station in pol_data:
          if station == "Pusa IMD" or "Punjabi Bagh":
            string += station
            string += "|"
            for keys,value in pol_data[station].items():
                if(value==-1):
                    string += "NA"
                else:
                    string += str(value)
                string += "|"
            string = string[:-1]
            string += "\n"
      string += "-\n"
      string += "Last updated at: "
      string += timeofupdate

      string += ".Data from -- Ministry of Environment and Forests , Central Pollution Control Board and covid19india.org.\n"
      string += ('^(Beep Boop! I am a Bot.Mention me in comments.) [ ^(My Creator )](https://www.reddit.com/message/compose/?to=Pollution_Hater)')
      return string
  except Exception as e:
      print("ERROR WITH POLLUTION API",e)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
def covid():
      try:
          with urllib.request.urlopen("https://api.covid19tracker.in/data/static/data.min.json") as url:
            cdata = json.loads(url.read().decode())
          cjson_string = json.dumps(cdata)
          covid_data = json.loads(cjson_string)
          
          covid_string = "*DELHI COVID STATUS*\n"
          covid_string += "\n"
          covid_string += "**Confirmed**|**Deceased**|**Recovered**|**1st Dose**|**2nd Dose**|**Tested**\n-|-|-|-|-|-\n"
          population = covid_data["DL"]["meta"]["population"]
          update = str(covid_data["DL"]["meta"]["last_updated"])
          for key,value in covid_data["DL"]["total"].items():
                      
            if value == -1:
              covid_string += "NA"
            elif key == "vaccinated1" or key == "vaccinated2":
              vax = value/population
              covid_string += str(vax)[2:4]
              covid_string += "%"
            elif value != 0:
              covid_string += str(value)
            covid_string += "|"
          covid_string = covid_string[:-1]
          covid_string += "\n"
          covid_string += "\n"

          covid_string += "Last updated at:"
          covid_string += update[:-1]
          covid_string += "\nFrom covid19tracker.in "
          covid_string += ('^(Beep Boop! I am a Bot.Mention me in comments.) [ ^(My Creator )](https://www.reddit.com/message/compose/?to=Pollution_Hater)')
          return covid_string
      except Exception as e:
          print("ERROR WITH COVID API",e)

def noida_pollution():
  try:
      with urllib.request.urlopen("https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69?api-key=API_KEY&format=json&offset=1400&limit=400") as url:
        data = json.loads(url.read().decode())
              
      json_string = json.dumps(data)
      python_obj = json.loads(json_string)

      pol_data = {}

      covid_string = ""
      sample = {
        "PM2.5":-1,
        "PM10":-1,
        "NO2":-1,
        "NH3":-1,
        "SO2":-1,
        "CO":-1,
        "OZONE":-1
      }
      timeofupdate = ""
      cou = 0
      for item in python_obj["records"]:
        station = item["station"]
        last_update = item["last_update"]
        timeofupdate = last_update
        station = station[:-14]
        if "Greater" in station:
          station = station[:-8]
        if station != "Sector - 6":
          station = station[:-1]

        pollutant_name = item["pollutant_id"]
        pollutant_min = "NA"
        pollutant_max = "NA"
        pollutant_avg = "NA"
        if "pollutant_min" in item:
            pollutant_min = item["pollutant_min"]
            pollutant_max = item["pollutant_max"]
            pollutant_avg = item["pollutant_avg"]

        city = item["city"]
        if(city == "Noida" or city == "Greater Noida"):
            new_dict = sample.copy()
            new_dict[pollutant_name] = pollutant_avg

            if station not in pol_data.keys():
              pol_data.update({station : new_dict})
            else:
              pol_data[station][pollutant_name] = new_dict[pollutant_name]
        else :
            cou = cou + 1
    ##            print("Noida Exceeded and others excluded")
            
      print("Not Noida : ",cou)
      string = "*NOIDA POLLUTION*\n"
      string += "\n"
      string += "**Area**^[AQIs-pollutant-wise]|**PM2.5**|**PM10**|**NO2**|**NH3**|**SO2**|**CO**|**OZONE**\n-|-|-|-|-|-|-|-\n"
      print(pol_data)
      for station in pol_data:
          if station == "Pusa IMD" or "Punjabi Bagh":
            string += station
            string += "|"
            for keys,value in pol_data[station].items():
                if(value==-1):
                    string += "NA"
                else:
                    string += str(value)
                string += "|"
            string = string[:-1]
            string += "\n"
      string += "-\n"
      string += "Last updated at: "
      string += timeofupdate

      string += ".Data from -- Ministry of Environment and Forests , Central Pollution Control Board  and covid19india.org.\n"
      string += ('^(Beep Boop! I am a Bot.Mention me in comments.) [ ^(My Creator )](https://www.reddit.com/message/compose/?to=Pollution_Hater)')
      return string
  except Exception as e:
      print("ERROR WITH NOIDA POLLUTION API",e)
    
def killpoll():
  
  while True:
      time.sleep(70)
      reddit = praw.Reddit(client_id='CLIENT_ID',
               client_secret='CLIENT_SECRET',
               user_agent='airdelhi v1.0 by /u/Pollution_Hater',
               username='airdelhi',
               password='PASSWORD'
           )
      
      string = pollution()
      covid_string = covid()
      noida_string = noida_pollution()
      print("Checking for unread messages ")        
      for item in reddit.inbox.unread(limit=2):
       
        if isinstance(item, Comment) or isinstance(item,Message):
          if hasattr(item,"body"):
            print(item.body)
            parent = item.parent()
            print("parent",parent)
            try:
              print("FOUND unread MESSAGE !")
              if(False):
                print("No Ho Ho !")
              else:
                print("REPLYING !")
                try:
                  item.mark_read()
                  item.body=item.body.lower()
                  if "u/airdelhi" in item.body or "aqi" in item.body:
                    if "covid" in item.body or "corona" in item.body:
                        try:
                          item.reply(covid_string)
                        except Exception as er:
                          print("COVID EXCEPTION : %s"%(er))
                          item.mark_unread()
                    elif "noida" in item.body:
                        try:
                          item.reply(noida_string)
                        except Exception as er:
                          print("NOIDA COVID EXCEPTION : %s"%(er))
                          item.mark_unread()
                    else:
                        try:
                          item.reply(string)
                      
                        except Exception as e:
                          print("REPLY EXCEPTION:%s"%(e))
                          item.mark_unread()
                          
                  else:
                      print("Not related comment")
                except Exception as e:
                  print("REPLY FAILED:-- %s"%(e))
                  
              
            except Exception as e:
              print("MESSAGE SEARCH FAILED: %s"%(e))
        print("Exiting Search")
      print("killpoll finish")   
try:   
  sched = BlockingScheduler()
  sched.add_listener(my_listener, EVENT_JOB_ERROR | EVENT_JOB_EXECUTED)
  @sched.scheduled_job('interval', minutes=5)
  def timed_job():
      print("Scheduler Start")
      time.sleep(5)
      killpoll()
      
  
  sched.start()
except Exception as e:
  print("Scheduler went wrong: %s"%(e))

