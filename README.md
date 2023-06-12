# Flask-docker (Server)

---

### 📌 Introduction

**The Flask-based Workout Video Analysis Server** is designed to analyze users' workout videos and provide insightful results. Built upon the Flask framework, this server offers a seamless and user-friendly experience, enabling fitness enthusiasts to gain valuable insights into their exercise routines.

Our servers leverage **computer vision technology** to help users extract key metrics and information from workout videos. Whether you're an individual who wants to optimize training or a fitness professional who wants to provide customized guidance.

---

### 📌 Features

- **Video analysis**
    
    The server leverages computer vision algorithms to analyze workout videos, extracting valuable information such as body movements, exercise form, and posture. This enables users to gain insights into their technique and make necessary adjustments to optimize their workouts.
    
- **Form Correction**
    
    The server offers feedback on exercise form, helping users maintain proper technique and prevent injuries. It identifies deviations from correct posture and provides recommendations for correcting and aligning movements, ensuring safe and effective workouts.
    
- **Scalability & Performance**
    
    Flask-based servers are designed to efficiently handle large amounts of video processing requests. Multi-threading technology ensures reliable performance during peak periods, allowing users to quickly access analysis results without delay.
    
- **Stability using Docker volume**
    
    Create a Docker volume to be used as a temporary DB. Data is not stored locally on the computer where the server runs, stored in Docker volume. This is because if all user videos received while the server is running are assigned to variables and managed, there is a risk of taking up a large amount of capacity in RAM, which may burden the server, and if the server fails to fully store data in Firebase and shuts down, all data stored as local variable disappears. By placing the volume separately like this, the stability was enhanced.
    

### 📌 Server Architecture

**The flowchart of the client's video analysis through the server and database is shown below.**

![Untitled](https://github.com/CHOHYUNSIK/Flask-docker/assets/69946205/0029b116-16cf-4602-9834-3f8e3228de8f)

**[Explanation]**

1. The client uploads exercise video to the database.
2. After the upload is completed, send the upload completion message to the server.
3. The server accesses the database and loads your video into the server for analysis.
4. Analyze exercise posture and generate feedback on the server.
5. Upload the results of the exercise posture analysis (image, feedback content, statistical figures) to the database.
6. Inform the client that the results analysis and feedback generation have been completed.
7. Access the database from the client and get analysis results and feedback.

---

### 📌 API Documentation

**This request allows you to request analysis from the server.**

| HTTP Method | POST |
| --- | --- |
| Url (request) | http://[serverIP]:[PORT]/download_and_analyze |
| Query param
(data) | ?data=[path_your_video] |
| Output | RESULT(if success), HTTP error(505,504.. etc) |
- **[serverIP] :** The external IP address that can connect to the server.
- **[PORT] :** Port number that can connect to the server. (5000 used)
- **[path_your_video] :** Path to user-uploaded images

**ex) `http://12.345.678.90:5000/download_and_analyze?data=temp/video/user/drj9802@gmail.com/exercise_Squat_2305092259`**

**If the RESULT string is received, the analysis results are stored in the DB's own account folder.**

---

### 📌 Installation and Setup

You have to download and install **Docker**

[Download Docker Desktop | Docker](https://www.docker.com/products/docker-desktop/)

**[Case 1] Using dockerhub**

You can easily download the server image through the **docker Hub.**

[Docker](https://hub.docker.com/repository/docker/chohyunsik/dothis/general)

Alternatively, you can **download the image** using **the following command.**

**→ `docker pull chohyunsik/dothis:latest`**

<aside>
💡 You can use this image with **Linux, Window OS**

</aside>

**After you download the image, you can run it using the following command.**

→ **`docker container run -d -p5000:5000 chohyunsik/dothis`**

**[Case 2] Using github**

You can easily download the server file through the **GitHub.**

→ **`git clone https://github.com/CHOHYUNSIK/Flask-docker.git`**

After downloading, change directory 

→ **`cd [YOUR_DOWNLOADED_PATH]\Flask-docker\Flask-Docker\app\api`**

Run server with **docker-compose.yml**

→ **`docker-compose up`**

---

### 📌 Support

If there is a problem or if you have any questions, please contact us by **email.**

📧 **whgustlr0326@gmail.com**

---
