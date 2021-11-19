import time
from bs4 import BeautifulSoup
from requests_html import HTMLSession

def scrape(node_id):
    url = f'https://stats.golem.network/node/{node_id}'
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    page = r.html.html

    cpu_p_h = None
    glm_p_h = None
    start_glm = None
    
    while (cpu_p_h == None or glm_p_h == None or start_glm == None):
        bs = BeautifulSoup(page, 'html.parser')
        bs_r = bs.find_all('div', {'class':'ml-1'})
        a = []
        for e in bs_r:
            a.append(e.find('h5', class_='mb-0').text.strip())
        cpu_p_h = a[3]
        glm_p_h = a[4]
        start_glm = a[5]
        if (cpu_p_h == '' or glm_p_h == '' or start_glm == ''):
            cpu_p_h = None
            time.sleep(5)
            print(f'pulled blank values for {node_id}, retrying...')
    return[cpu_p_h,glm_p_h,start_glm]
    #print(f'cpu/h = {a[3]} glm/h = {a[4]} start/h = {a[5]} | sleep = {seconds[i]} seconds')