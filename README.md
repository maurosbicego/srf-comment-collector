# SRF.ch Comment Collector
Collect comments from srf.ch. Tool can be used for research such as data science, political analysis or also (to some extent) OSINT.
IMPORTANT: Use at own risk, the data collected by this tool contains personal data that can be used to track the behaviour of specific people (as with all data from social media). Check rules / data ownership etc. and anonymise data before publishing anything.

## About
This tool can be used to periodically collect the comments available on different articles on srf.ch. SRF is a media plattform from Switzerland, content is in german and the topics with comments usually concern Switzerland. The comments are curated and users required to comment with their real name. This leads to a higher quality of comments compared to other plattforms.

## Structure

### Datebase models / tables

#### Article
Whenever we discover an article, we add an entry as "Article". We check if it has comments activated. If it does, we set "hascomments" to true. If the comment section is not closed yet, we don't fetch the comments yet. As long as "commentsfetched" is false, we check if the comment section is closed (upon next run).
If the comments close, we set "commentsfetched" to true and fetch all the comments.

#### User
Contains all the users that posted a comment with their username and full name

#### Comment
Definition for a comment. References the article for which it was written and references the User that wrote the comment. Can also reference another comment if it is a reply. Contains the amount of likes the comment received.

## Running the tool
The tool needs to be started once (ideally docker-compose or podman), it then reloads the data every hour. This time-period can be set in `settings.py` when running directly with python or `settings-docker.py` when using docker-compose, docker or podman
### Run with docker-compose

`sudo docker-compose up -d`

### Run with podman (no compose, no root)
1. Build: `podman build -f ./Dockerfile --tag srf-collector`
2. Make sure the directory `database` exists
3. Run with volume: `podman run -v $(pwd)/database:/collector/database srf-collector`

### Run directly with python3
1. Install requirements `pip3 install -r requirements.txt`
2. Run it `python3 main.py`

## Read the data
Data is saved into an sqlite-databse. It is located in the `database` directory where the tool is run. The database contains the tables mentioned above. Use SQL to perform your analysis. I might implement some functionality to analyse the data in the tool itself later.

## Citation
Should you use this tool for an academic publication, please cite it as outlined in the `CITATION.cff` file.