# OmniCinema 🎬

OmniCinema is a full-stack, polyglot movie ticketing and seat reservation platform. Built with a microservices-inspired architecture, it integrates multiple programming languages to handle specific domain tasks, demonstrating cross-platform process communication, state management, and containerized deployment.

## 🎥 Project Demo
**https://drive.google.com/drive/folders/1gSl_43ss-4rlehfuHZLnsDaHotTIC5A5?usp=sharing**
> *Note: This video demonstrates the complete user journey, backend API interactions, and cross-language process execution in real-time.*

## 🏗️ Architecture & Tech Stack

This project deliberately utilizes a polyglot backend to demonstrate systems integration and language-specific strengths:
* **Frontend:** HTML, CSS, JavaScript (Responsive UI, async API calls)
* **Backend Core:** Python (Flask) - Handles REST API routing, HTTP requests, and database orchestration.
* **Seat Validation Engine:** Java - Executes strict business logic to validate seat availability and prevent race conditions.
* **Payment Microservice:** C# (.NET) - Processes transaction calculations, age verification, and change dispensing.
* **Database:** SQLite - Relational data storage for movies, schedules, seating arrays, and sales records.
* **Deployment:** Docker, Herza Cloud VPS (Linux)

## ⚙️ Local Development Setup (Windows)

To run this project locally for development or testing, ensure you have **Python 3**, **Java (JDK)**, and the **.NET SDK** installed.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/omnicinema.git
   cd omnicinema
   ```

2. **Configure the environment for Local Testing:**
   In `main.py`, ensure the C# execution command is set to use the local .NET SDK rather than the compiled Linux production binary.

   *Uncomment this section (Lines 77-80):*
   ```python
   cs_project = os.path.join(BASE_DIR, "payment-service", "PaymentService")
   cs_result = subprocess.run(
       ["dotnet", "run", "--project", cs_project, "--", str(ticket_price), str(age), str(amount_paid)],
       capture_output=True, text=True, cwd=BASE_DIR
   )
   ```

   *Ensure the production binary command is commented out (Lines 81-84):*
   ```python
   # cs_result = subprocess.run(
   # ["./PaymentService", str(ticket_price), str(age), str(amount_paid)],
   # ...
   ```

3. **Start the Flask Server:**
   ```bash
   python main.py
   ```

4. **Access the application:** 
   Open `http://127.0.0.1:5000` in your web browser.

## 🐳 Production Deployment (Docker/Linux)

The production environment is containerized via Docker to run seamlessly on a Linux VPS. It utilizes a pre-compiled standalone Linux binary for the C# payment service, removing the need for the full .NET SDK in production.

1. **Prepare for Production:** Revert the toggles in `main.py` to use the `./PaymentService` binary.
2. **Build the image:**
   ```bash
   docker build -t omnicinema .
   ```
3. **Run the container (Detached):**
   ```bash
   docker run -d -p 80:5000 --name my-omnicinema omnicinema
   ```

## 👨‍💻 Author
**Michael Joseph Salusu**
*Undergraduate Computer Science Student @ BINUS University*
* [LinkedIn](https://linkedin.com/in/yourprofile)
* [GitHub](https://github.com/yourusername)
