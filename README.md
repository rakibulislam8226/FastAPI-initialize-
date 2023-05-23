### Installation guidelines

* `Python 3.9` 
* `PostgreSQL` 

---
**Create virtual environment based on your operating system**
 ```shell
python3.9 -m venv venv
  ```

  ###### Activate the virtual environment
 ```shell
source venv/bin/activate
  ```
---

**Install the requirements.txt file**

```shell
pip3 install -r requirements.txt
```

---
**Copy .env.defaults file to .env:**

  * For linux
    ```shell
    cp .env.defaults .env
    ```
  * For windows
    ```shell
    copy .env.defaults .env
    ```
  ###### Fill up the .env with proper credentials.

---

**Run the project**
  ```shell 
  uvicorn app:app --reload
  ```
  OR
  ```shell 
  python app.py
  ```
---


**Project Structure**