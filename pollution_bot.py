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

def killpoll():
  
  while True:
      time.sleep(45)
      reddit = praw.Reddit(client_id='CLIENT_ID',
               client_secret='CLIENT_SECRET',
               user_agent='USER_AGENT',
               username='airdelhi',
               password='PASSWORD'
           )
      
      with urllib.request.urlopen("https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69?api-key=API_KEY&format=json&offset=191&limit=180") as url:
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

        pollutant_name = item["pollutant_id"]
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
            print("Delhi Exceeded and others excluded")
            break;

      string = "**Area**^[AQIs-pollutant-wise]|**PM2.5**|**PM10**|**NO2**|**NH3**|**SO2**|**CO**|**OZONE**\n-|-|-|-|-|-|-|-\n"

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

      string += ".Data from -- Ministry of Environment and Forests , Central Pollution Control Board.\n"
      string += ('^(Beep Boop! I am a Bot.Mention me in comments.)[^(My Creator)](https://www.reddit.com/message/compose/?to=Pollution_Hater).')
      with urllib.request.urlopen("https://api.covid19india.org/v4/data.json") as url: #https://github.com/covid19india/api
        cdata = json.loads(url.read().decode())
      cjson_string = json.dumps(cdata)
      covid_data = json.loads(cjson_string)
      covid_string = "*DELHI COVID STATUS*\n"
      covid_string += "\n"
      covid_string += "**Confirmed**|**Deceased**|**Recovered**|**Tested**\n-|-|-|-\n"

  

      for key,value in covid_data["DL"]["total"].items():
                  
        if value == -1:
          covid_string += "NA"
        else:
          covid_string += str(value)
        covid_string += "|"
      covid_string = covid_string[:-1]
      covid_string += "\n"
      covid_string += "-\n"
      update = str(covid_data["DL"]["districts"]["Delhi"]["meta"]["tested"]["last_updated"])
      covid_string += "Last updated at:"
      covid_string += update
      covid_string += "\n"
      covid_string += ('^(Beep Boop! I am a Bot,Please be nice.Mention me in comments.)[^(My Creator)](https://www.reddit.com/message/compose/?to=Pollution_Hater).')

      print("Checking for unread messages ")     
          
      for item in reddit.inbox.unread(limit=2):
        
        
        if isinstance(item, Comment):
          if hasattr(item,"body"):
            print(item.body)
            parent = item.parent()
            print("parent",parent)
            try:
                print("FOUND unread MESSAGE !")
              
                try:
                  item.mark_read()
                  if "u/airdelhi" in item.body:
                    if "covid" in item.body or "corona" in item.body:
                        try:
                          item.reply(covid_string)
                        except Exception as er:
                          print("COVID EXCEPTION : %s"%(er))
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
  @sched.scheduled_job('interval', minutes=3)
  def timed_job():
      print("Scheduler Start")
      time.sleep(5)
      killpoll()
      
  
  sched.start()
except Exception as e:
  print("Scheduler went wrong: %s"%(e))

