import requests
import pandas as pd

def fetch_jobs():
    url="https://remoteok.com/api"
    response = requests.get(url)

    data = response.json()

    jobs=[]

    for job in data[1:]: #skip metadata
        jobs.append({
            "title": job.get("position"),
            "company":job.get("company"),
            "location": job.get("location"),
            "salary": job.get("salary"),
            "skills":",".join(job.get("tags",[]))
        })
    
    df = pd.DataFrame(jobs)
    df.to_csv("data/jobs.csv", index=False)

    print("Jobs data saved to data/jobs.csv")

# run function 
if __name__ == "__main__":
    fetch_jobs()
    