import requests
from bs4 import BeautifulSoup
import threading

def download_comic(contador):
    response = requests.get(f"https://xkcd.com/{contador}/")
    
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        
        image = soup.find_all('img', style=True)
        image_link = f"https://xkcd.com{image[0]['src'].replace('//', '/')}"
        
        response_image = requests.get(image_link)
        
        with open(f"comics/{contador} - {image_link.split('/')[-1]}", "wb") as file:
            file.write(response_image.content)
        print(f"Comic {contador} downloaded")
    
    elif response.status_code == 404:
        print(f"Finished")
        
def create_threads():
    threads = []
    contador = 3014
    while True:
        # It checks if the comic is 404 bcs xkcd made it so it gave an error as joke
        if contador == 404:
            contador += 1
        thread = threading.Thread(target=download_comic, args=(contador,))
        threads.append(thread)
        thread.start()
        
        response = requests.get(f"https://xkcd.com/{contador}/")
        if response.status_code == 404:
            print("Reached the end of available comics.")
            break
        
        contador += 1

    for thread in threads:
        thread.join()

create_threads()
