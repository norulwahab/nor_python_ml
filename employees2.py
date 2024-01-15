import numpy as np
import pandas as pd
import psycopg2
from datetime import datetime
import random
import string

VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))

"""This method generate a name mixing consonants and vowels lower alphabets"""


def generate_name(length):
    name = ""
    for i in range(length):
        if i % 2 == 0:
            name += random.choice(CONSONANTS)
        else:
            name += random.choice(VOWELS)
    return name

# Create a Connection


def create_connection():
    conn = psycopg2.connect(dbname='norul', user='norul', password='**************',
                           host='******.postgres.database.azure.com', port=5432)
    return conn

# Task 1: Generate job data


def insert_data(conn):
    with conn.cursor() as cursor:
        # Step 1: Create 10000 persons with random first_name and random last_name
        for i in range(10000):
            cursor.execute("INSERT INTO person (first_name, last_name) VALUES (%s, %s);",
                           (generate_name(np.random.choice(np.arange(2, 10))),
                            generate_name(np.random.choice(np.arange(2, 10)))))

        # Step 2: Create 5000 companies with a random fictional name
        for i in range(5000):
            cursor.execute("INSERT INTO company (name) VALUES (%s);",
                           (generate_name(np.random.choice(np.arange(2, 10)))+' AB',))

        # Step 3: Generate jobs data
        cursor.execute("SELECT * FROM person")
        rows = cursor.fetchall()
        # for getting person_id from person table, which is returned in row[0]
        for row in rows:
            start_date1 = datetime(np.random.randint(2012, 2022), np.random.randint(1, 13), 1)
            end_date1 = datetime(np.random.randint(start_date1.year, 2022), np.random.randint(start_date1.month, 13),28)
            cursor.execute(
                "INSERT INTO person_job (title, start_date, end_date, person_id, company_id) "
                "VALUES (%s, %s, %s, %s, %s);",
                ('junior', start_date1, end_date1, row[0], random.randint(1, 5000)))

            start_date2 = datetime(np.random.randint(end_date1.year, 2022), np.random.randint(1, 13), 1)
            end_date2 = datetime(np.random.randint(start_date2.year, 2022), np.random.randint(start_date2.month, 13),28)
            cursor.execute(
                "INSERT INTO person_job (title, start_date, end_date, person_id, company_id) "
                "VALUES (%s, %s, %s, %s, %s);",
                ('senior', start_date2, end_date2, row[0], random.randint(1, 5000)))

            start_date3 = datetime(np.random.randint(end_date2.year, 2022), np.random.randint(1, 13), 1)
            # for avoiding the not null constraint, min datetime is entered
            end_date3 = datetime.min
            cursor.execute(
                "INSERT INTO person_job (title, start_date, end_date, person_id, company_id) "
                "VALUES (%s, %s, %s,%s, %s);",
                ('lead', start_date3, end_date3, row[0], random.randint(1, 5000)))

# Task 2: Show some metrics


def show_results(conn):
    with conn.cursor() as cur:
        # 1. Most common first name
        cur.execute('SELECT first_name, COUNT(*) as count FROM person '
                    'GROUP BY first_name ORDER BY count DESC LIMIT 1;')
        most_common_first_name = cur.fetchone()
        print(f'1. Most common first_name: {most_common_first_name[0]} ({most_common_first_name[1]} persons)')

        # 2. Company with the most number of employees
        cur.execute('SELECT c.name, COUNT(*) as count FROM company c '
                    'JOIN person_job j ON c.id = j.company_id '
                    'WHERE j.end_date = (%s) '
                    'GROUP BY c.name '
                    'ORDER BY count DESC LIMIT 1;', (datetime.min,))
        most_employees_company = cur.fetchone()
        print(f'2. Company with the most number of employees: '
              f'{most_employees_company[0]} ({most_employees_company[1]} employees)')

        # 3. Who has the longest years of work experience
        cur.execute('SELECT person_id, start_date, CASE WHEN end_date = (%s) THEN (%s) '
                    'ELSE end_date END as end_date '
                    ' FROM person_job;', (datetime.min, datetime(2022, 12, 28)))
        person_exp = pd.DataFrame(columns=['person_id', 'experience'])
        p_id = []
        exp = []
        for row in cur.fetchall():
            p_id.append(row[0])
            diff = row[2].date() - row[1]
            exp.append(diff.days)
        person_exp['person_id'] = p_id
        person_exp['experience'] = exp
        longest_experience_person = person_exp.groupby('person_id')['experience'].sum().idxmax()
        longest_experience = person_exp.loc[person_exp['person_id'] ==
                                            longest_experience_person, 'experience'].sum()
        print(f'3. Who has the longest years of work experience: Person with ID '
              f'{longest_experience_person} ({round(longest_experience/365,2)} years)')

        # 4. Who has the shortest years of work experience
        shortest_experience_person = person_exp.groupby('person_id')['experience'].sum().idxmin()
        shortest_experience = person_exp.loc[person_exp['person_id'] ==
                                             shortest_experience_person, 'experience'].sum()
        print(f'3. Who has the longest years of work experience: Person with ID '
              f'{shortest_experience_person} ({round(shortest_experience/365,2)} years)')

        # 5. Average years of work experience
        average_experience_person = person_exp.groupby('person_id')['experience'].sum()/3
        total = 0
        for row in average_experience_person:
            total += row

        print(f'5. Average years of work experience: {round((total/10000)/365, 0)} years')

# Main execution


try:
    connection = create_connection()
#    insert_data(connection)
#    connection.commit()
#    print("Data is inserted in all tables successfully.")
    show_results(connection)
except Exception as e:
    print(f"Error: {e}")
finally:
    if connection:
        connection.close()
