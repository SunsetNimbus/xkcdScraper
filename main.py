import requests
from bs4 import BeautifulSoup


contador = 405
response = True
while response:
    if contador != 404:
        response = requests.get(f"https://xkcd.com/{contador}/")
    
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    if response.status_code == 200:

        image = soup.find_all('img', style=True)
        image_link = f"https://xkcd.com{image[0]['src'].replace('//', '/')}"
        
        response_image = requests.get(image_link)

        with open(f"comics/{contador} - {image_link.split('/')[-1]}", "wb") as file:
            file.write(response_image.content)
        
    elif response.status_code == 404:
        print("Fin")
    contador += 1
