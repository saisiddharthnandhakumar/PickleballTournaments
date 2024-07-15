# Pickleball Tournament Data

## Context : I am a new pickleball player who has been playing for nearly two months now, and in my first tournament in the 3.5 rating, me and my partner had won a bronze medal. Playing tennis for nearly 13 years has definitely translated to pickleball. If you haven't started playing yet I'd highly suggest it. It's fun.

## Problem: Me and my partner have a very busy work schedule and we wanted to know the nearest tournaments from our home which we could go to without any scheduling conflicts.

## Solution: Created a dashboard with a map including all pickleball tournaments listed in the country. With information on each tournament from rating, events, and which day each event is played on

## Methodology:

### Technologies Used: Python, Tableau, SQL, Selenium Chrome Driver, Google BigQuery, Google Cloud Storage Bucket, Google DataFlow, Google Cloud Function, Apache Airflow,

### Extract:

I got is from pickleballbrackets.com. I used a python script(extract_test.py) with the Selenium Webdriver to be able to scrape all the website data.

## Transform:

(transform.py) Another python script was used to convert the raw .csv file from extract_test.py into a cleaner dataset.

## Load:

(bracket_data.csv) The cleaned .csv file is then uploaded to a google cloud storage bucket.

From here a cloud function is triggered which then sets off a data flow job sending the data into a Big Query Table with a specified simple schema (bq.json)

## Visualization:

The Bigquery table is then connected to Tableau Desktop, in which the visualizations are seen.

## Caveats/Updates to be made:

- This workflow is yet to be automated and scheduled using an orchestrator like Apache Airflow or Mage.ai.
- ETL Logic is yet to be fine-tuned and some of the Event Details are still messy or missing.
- A staging table is to be made in BigQuery to handle deduplication.
- Existing Schema is too simple and doesn't yet have all the tournament info.
- A better data model is required to be created.
