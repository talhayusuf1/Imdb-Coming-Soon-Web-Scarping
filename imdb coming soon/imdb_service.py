from time import time
import requests
import html5lib
import json
from bs4 import BeautifulSoup


def time(str2):
    if(len(str2)>2):
        num=int(str2.strip(" min"))
        if(num<60):
            return '0h '+ str(num)
        else:
         h = num / 60
         m = int(num) - (int(h)*60)
        return str(int(h)) +'h '+ str(m)+'m'

def getAll():
    movies = {}
    
    for month in range(6,13):
        for x in range(1,5):
            getMovies(month, movies)
            print(movies)
            f = open("movies.json", "w")
            f.write(str(movies))
    

def getMovies(m, movies):
    moviemonth={}

    m=str(m)
    if(len(m)<2):
        month = '0'+str(m)
    else:
        month=str(m)
    
    Url = "https://www.imdb.com/movies-coming-soon/2022-{}/".format(month)
    print(Url)
    response = requests.get(Url)
    parsedResponse = BeautifulSoup(response.text,"html5lib")
    q_response = parsedResponse.find_all("td",{"class":"overview-top"})
    index =0
    for film in q_response:
      movie_name=film.find("a").text 
      movie_genre= film.find("p",{"class":"cert-runtime-genre"}).find_all("span")
      movie_description= film.find("div",{"class":"outline"}).text
      staff = film.find_all("div",{"class":"txt-block"})
      try:
        runtime = film.find("p",{"class":"cert-runtime-genre"}).time.text

      except :
          runtime="0 min"

      duration = time(runtime)
      genres=[]
      for i in movie_genre:
        if(i.text !='|'):
          genres.append(i.text)
      stars= []
      directors=[]

      for i in staff:
        header = i.find("h5",{"class":"inline"}).text
        if(header == "Director:" ): 
          yonetmen = i.find_all("a")
          for k in yonetmen:
            directors.append(k.text.strip("\n").strip("  ") )
        if(header == "Stars:" ): 
          star = i.find_all("a")
          for k in star:
            stars.append(k.text.strip("\n").strip("  ") )

      movie = {
        "movie_name" : movie_name,
        "genres": genres ,
        "directors": directors,
        "stars": stars, 
        "duration" : duration,
        "description" : movie_description
      }
      moviemonth[index] = movie
      index+=1

    movies[month]=moviemonth

