from ctypes import c_void_p
import requests
from bs4 import BeautifulSoup
from os import path, makedirs
import csv

base_url = "https://realpython.github.io/fake-jobs/"

url = base_url

response_page = requests.get(url)

soup = BeautifulSoup(response_page.content, "html.parser")

results = soup.find(id="ResultsContainer")

jobs_elements = results.find_all("div", class_="card-content")

python_jobs = results.find_all("h2", string=lambda text:"python" in text.lower())
python_jobs_elements = [ job_element.parent.parent.parent for job_element in python_jobs]

def get_jobs_description(job_element):
    links = job_element.find_all("a")
    link_url = links[1]["href"]
    job_desciptions = requests.get(link_url)
    soup = BeautifulSoup(job_desciptions.content, "html.parser")
    job_content = soup.find("div", class_="content")
    job_informations = job_content.find_all("p")
    job_desc = job_informations[0]
    return job_desc.text


def get_jobs_data(list_of_jobs):   
    job_list_of_datas = []

    for  job_element in list_of_jobs:
        job_data = {}
        title_element = job_element.find("h2", class_="title")
        company_element = job_element.find("h3", class_="company")
        location_element  = job_element.find("p", class_="location")
        date_posted = job_element.find("time")
        job_description = get_jobs_description(job_element)

        job_data["name"] = title_element.text
        job_data["date"] = date_posted.text
        job_data["company"] = company_element.text.strip()
        job_data["location"] = location_element.text.strip()
        job_data["description"] = job_description
        job_list_of_datas.append(job_data)

    return job_list_of_datas
    



jobs_datas = get_jobs_data(jobs_elements)


directory = "data"
if not path.exists(directory):
    makedirs(directory)

columns = [
            "name",
            "date",
            "company",
            "location",
            "description"
        ]

def get_columns_data(data, columns):
    list_of_columns = []
    for item in columns:
        list_of_columns.append(data[item])
    
    return list_of_columns

with open("data/jobs_datas.csv", "w", newline="", encoding="utf-8") as csv_file:
    csv_write = csv.writer(csv_file)
    csv_write.writerow(columns)

    for row in jobs_datas:
        for column in columns:
            csv_write.writerow(get_columns_data(data=row, columns=columns))




