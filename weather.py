import requests
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import WeatherResponse, UserDefaultCity, Unit
from oauth import allow_access
from database_models import User, Weather

router = APIRouter(tags=["Weather"])

# saving snapshots of users historic searches 
@router.post("/weather", response_model=WeatherResponse)
def add_weather_in_db(city_name:str, db:Session = Depends(get_db), user_credentials:User = Depends(allow_access)):

    api_key = "add_private_weatherapi_key"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    response = requests.get(url)

    data = response.json()
    
    if str(data.get("cod")) != "200":
        raise HTTPException(status_code= int(data["cod"]) , detail=data)


    weather_info = Weather(
        city= city_name,
        current_temp=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        minimum_temp=data["main"]["temp_min"],
        maximum_temp=data["main"]["temp_max"],
        user_id=user_credentials.id
    )

    db.add(weather_info)
    db.commit()
    db.refresh(weather_info)
    return weather_info



##############################################################################################################
##############################################################################################################
##############################################################################################################



# ask user for default city 
@router.post("/default_city")
def add_default_city(dc:UserDefaultCity, db:Session = Depends(get_db), uc:User = Depends(allow_access)):

    db_user = db.query(User).filter(User.id== uc.id).first()

    api_key = "add_private_weatherapi_key"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={dc.default_city}&appid={api_key}&units=metric"

    response = requests.get(url)

    data = response.json()
    
    if str(data.get("cod")) != "200":
        raise HTTPException(status_code= int(data["cod"]) , detail=data)
    
    db_user.default_city = dc.default_city
    db.commit()
    db.refresh(db_user)
    return {"message": f"Default city set to {db_user.default_city}"}



##############################################################################################################
##############################################################################################################
##############################################################################################################



#show user weather of its default city
@router.get("/user/default_city")
def show_default_city_weather(db:Session = Depends(get_db), uc:User = Depends(allow_access)):
    db_user = db.query(User).filter(User.id == uc.id).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Default city not set")

    api_key = "add_private_weatherapi_key"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={uc.default_city}&appid={api_key}&units=metric"

    response = requests.get(url)

    data = response.json()

    if str(data.get("cod")) != "200":
        raise HTTPException(status_code= int(data["cod"]) , detail=data)

    weather_info = Weather(
        city= uc.default_city,
        current_temp=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        minimum_temp=data["main"]["temp_min"],
        maximum_temp=data["main"]["temp_max"]
    )

    return weather_info


##############################################################################################################
##############################################################################################################
##############################################################################################################

    
# live weather search for everyone. 
@router.get("/city/weather")
def check_weather(city:str, units:Unit):    

    api_key = "add_private_weatherapi_key"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units.value}"

    response = requests.get(url)

    data = response.json()
    
    if str(data.get("cod")) != "200":
        raise HTTPException(status_code= int(data["cod"]) , detail='Invalid city name')

    weather_info = Weather(
        city= city,
        current_temp=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        minimum_temp=data["main"]["temp_min"],
        maximum_temp=data["main"]["temp_max"]
    )

    return weather_info




##############################################################################################################
##############################################################################################################
##############################################################################################################


# get 5 recent searches content 
@router.get("/recent/city")
def historical_checks(db:Session = Depends(get_db), uc:User = Depends(allow_access)):
    db_user = db.query(Weather.city).filter(User.id == uc.id).order_by(Weather.id.desc()) .limit(3).all() # limit will limit the result with desc making sure its descending order in id.
    
    recent_cities = [c[0] for c in db_user]
    return {"history": recent_cities}




##############################################################################################################
##############################################################################################################
##############################################################################################################


# delete user account and its all the data stored. 

@router.delete("/delete")
def delete_user(db:Session = Depends(get_db), uc:User = Depends(allow_access)):
    db_user = db.query(User).filter(User.id == uc.id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="user does not exist")
    
    db.delete(db_user)
    db.commit()
    return {"message":"user and its history deleted."}


















