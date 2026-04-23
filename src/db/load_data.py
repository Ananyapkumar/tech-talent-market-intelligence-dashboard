import psycopg2
import pandas as pd

# connecting to database
conn = psycopg2.connect(
    dbname="talent_db",
    user="postgres",
    password="5432",  # add your password if needed
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# read csv
df = pd.read_csv("data/jobs.csv")

# insert data
for _, row in df.iterrows():

    # insert job
    cur.execute("""
        INSERT INTO jobs (title, company, location, salary, skills)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (row['title'], row['company'], row['location'], row['salary'], row['skills']))

    job_id = cur.fetchone()[0]

    # split skills (NOW INSIDE LOOP ✅)
    skill_list = str(row['skills']).split(",")

    for skill in skill_list:
        skill = skill.strip()

        # insert skill if not exists
        cur.execute("""
            INSERT INTO skills (skill_name)
            VALUES (%s)
            ON CONFLICT (skill_name) DO NOTHING
            RETURNING id
        """, (skill,))

        result = cur.fetchone()

        if result:
            skill_id = result[0]
        else:
            cur.execute("SELECT id FROM skills WHERE skill_name = %s", (skill,))
            skill_id = cur.fetchone()[0]

        # insert into bridge (FIXED NAME ✅)
        cur.execute("""
            INSERT INTO job_skills (job_id, skill_id)
            VALUES (%s, %s)
        """, (job_id, skill_id))


conn.commit()
cur.close()
conn.close()

print("✅ Data loaded into PostgreSQL")