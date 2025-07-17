# Shamzam-Microservices

### Overview

A microservice-based music recognition MVP inspired by Shazam. It allows users to upload audio fragments and matches them to known music tracks using the Audd.io API. Built in Python with RESTful microservices and SQLite.

### Features

- RESTful services for track management and audio recognition
- Audio fragments matched via Audd.io API and cross-referenced with local catalogue
- SQLite-based metadata store and local file system audio archive
- Clean REST interface with full status code coverage and JSON I/O
- End-to-end tests for all user stories, including failure scenarios

### How to run
1. Clone the repository
   ```bash
   git clone https://github.com/sharpegeorge/Shamzam-Microservices.git
   cd Shamzam-Microservices
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

5. Run one of the available test suites
   ```bash
   python "tests/test_add.py"
   python "tests/test_list.py"
   python "tests/test_remove.py"
   python "tests/test_request.py"
   ```
### Files Included
- `audd_api.py`
- `database.py`
- `track_add.py`
- `track_list.py`
- `track_remove.py`
- `track_request.py`
- `tests/`
    - `test_add.py`
    - `test_list.py`
    - `test_remove.py`
    - `test_request.py`
- `requirements.txt`
