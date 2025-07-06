# 🌸 Flower Shop – Scalable AWS Architecture

A simple online flower shop to demonstrate a scalable backend architecture on AWS, using EC2, Auto Scaling, CloudFront, and S3.

## 📦 Project Overview

**Architecture Components:**

- **Frontend** – hosted in **Amazon S3** (static website) and served via **CloudFront**
- **Backend** – Flask app running on **EC2** instances behind an **Application Load Balancer (ALB)**, managed by an **Auto Scaling Group (ASG)**
- **Order Storage** – orders are saved to **S3** as JSON files
- **Monitoring** – custom CloudWatch metric `OrderCount` is published every time an order is placed
- **Auto Scaling** – automatically adjusts number of backend instances based on order traffic

## 🔧 Technologies Used

- AWS EC2 + Launch Templates
- Auto Scaling Group (1–3 instances)
- Application Load Balancer (ALB)
- CloudFront + S3 static website hosting
- Python + Flask + Boto3
- CloudWatch Custom Metrics and Alarms
- IAM Roles and Policies
- Security Groups allowing inbound from CloudFront only

## 🛠️ Backend Logic

`app.py` handles the `/order` endpoint:

- Accepts `POST` requests with order data (name, address, flower type)
- Saves each order to S3 under the `orders/` folder
- Sends a custom metric to CloudWatch: `OrderCount = 1`

## 📈 Auto Scaling Logic

| Condition                    | Action            |
|-----------------------------|-------------------|
| OrderCount > 30 per minute  | Add 2 instances   |
| OrderCount ≤ 15 per minute  | Remove 2 instances|

Alarms are based on CloudWatch metrics with 1-minute granularity.

## 🚀 Load Testing

Use `load_test.py` to simulate real-time traffic with randomized flower orders:

```bash
python3 load_test.py
```

Modify `orders_to_send` and `delay` inside the script to increase load.

## 🔐 Security Notes

- ALB security group only allows inbound traffic from **CloudFront** IP ranges.
- Backend EC2 instances use an **IAM role** that allows:
  - `s3:PutObject` on the `orders/` path
  - `cloudwatch:PutMetricData` for custom metrics

## 📂 Project Files

- `app.py` – Flask backend
- `load_test.py` – Traffic generator for load testing
- `FlowerShopS3WriteAccess_AWS_Policy` – IAM policy for EC2 role
- `flower-backend.service` – Systemd unit file for running Flask app
- `index.html` – HTML code of main page

## 🎬 Screenshots and demonstration

**Scenario:** The online flower shop works well, but a peak in demand affects the business.

On busy days like March 8th, the backend slows down, and orders are not created properly. Customers can't wait and leave for other flower shops.  
The DevOps Engineer decided to use an Auto Scaling Group to handle high demand properly, increasing backend capacity from 1 to 3 instances.

---

### 🌐 Website Overview

Let's start with the main page of my website:  
![Main page](./screenshots/Index1.JPG)  
As you can see, I'm using the domain: https://shoppng.online

This domain is added in Route 53:  
![Route53](./screenshots/Route53.JPG)

Then I received an SSL certificate via ACM:  
![ACM](./screenshots/ACM.JPG)

The website is served worldwide using CloudFront distribution:  
![CloudFront](./screenshots/CloudFront1.JPG)

It has 2 behaviors - one for the main page, and one for the /order route:  
![Behaviors](./screenshots/CloudFront2.JPG)

There are 2 origins: ALB and S3:  
![Origins](./screenshots/CloudFront3.JPG)

The main page is a static website hosted in an S3 bucket:  
![S3 static](./screenshots/S3_1.JPG)

At the bottom of the page, you'll see the order form:  
![Form](./screenshots/Index2.JPG)

This form submits data to the backend (`app.py`) running on my EC2 instances.  
The backend receives the order and saves it as an object in the same S3 bucket (used for testing instead of a real database):  
![S3 object](./screenshots/S3_2.JPG)  
![S3 object detail](./screenshots/S3_3.JPG)

An Auto Scaling Group (ASG) handles instance creation and termination based on load:  
![ASG](./screenshots/ASG.JPG)

Instances are launched using a custom AMI:  
![AMI](./screenshots/AMI.JPG)

Launch template includes an IAM role for permissions:  
![Launch Template](./screenshots/LaunchTemplate.JPG)

---

### 📉 Normal Load

Let's simulate a normal day with ~1 order every 8 seconds.  
I run `load_test.py`:  
![Normal load GIF](./screenshots/low.gif)

Check the CloudWatch dashboard:  
![CloudWatch](./screenshots/CloudWatch1.JPG)

It has 2 graphs. The right one shows an alarm used by ASG to scale in when orders are less than 15 per minute.  
Only 1 EC2 instance is active:  
![EC2](./screenshots/EC2_1.JPG)

ALB under normal conditions:  
![ALB normal](./screenshots/ALB1.JPG)

---

### 📈 High Load (Celebration Day)

Now imagine a celebration day with more than 200 orders per minute:  
![High load GIF](./screenshots/high.gif)

CloudWatch metrics spike:  
![CloudWatch spike](./screenshots/CloudWatch2.JPG)

ASG scales out from 1 to 3 EC2 instances:  
![ASG scale out](./screenshots/ASG_2.JPG)  
![ASG scale out](./screenshots/ASG_3.JPG)  
![EC2](./screenshots/EC2_2.JPG)

After a few minutes, ALB balances traffic across all 3 instances:  
![ALB scaled](./screenshots/ALB2.JPG)

---

### 📉 Back to Normal

As the celebration ends, orders slow down again to one every 8 seconds:  
![CloudWatch back](./screenshots/CloudWatch3.JPG)

ASG scales in:  
![ASG scale in](./screenshots/ASG_4.JPG)  
![ASG scale in](./screenshots/ASG_5.JPG)  
![ASG scale in](./screenshots/ASG_6.JPG)  
![EC2 downscaled](./screenshots/EC2_3.JPG)

---

## ✅ Conclusion

I hope this demonstration helps you better understand how Auto Scaling works in response to traffic changes in a real-world scenario.

---

🛠️ **Built by**: Nikita Butakov

---

This project was built as part of a DevOps learning journey to practice AWS scalability, monitoring, and automation.

