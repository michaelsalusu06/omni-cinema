# OmniCinema 🎬

A polyglot cinema ticket booking system integrated with **Python (Flask)**, **Java**, and **C# (.NET)**. The project demonstrates multi-language microservice communication via process execution, using SQLite for transaction persistence and an interactive web interface for seat selection and payment processing.

---

## 🌟 Key Features

* **Multi-Language Architecture**: Seamless coordination between Python (web orchestration & API), Java (seat validation logic), and C# (payment processing & discount logic).
* **Dynamic Movie & Schedule Selection**: Browse movies, showtimes, base prices, and halls with live updating seating maps.
* **Interactive 3x3 Seating Grid**: Visual seat map (A1 through C3) displaying availability in real-time (Green = Available, Blue = Selected, Red = Booked).
* **Live Pricing & Discount Calculation**: Automatic 10% Youth Discount applied for customers under age 18.
* **Transaction Persistence**: Sales ledger and updated seat availability saved to an underlying SQLite database.

---

## 🛠️ Tech Stack & Roles

| Language / Framework | Module | Role |
| :--- | :--- | :--- |
| **Python (Flask)** | `main.py` | Web server, REST API provider, SQLite ORM manager, and subprocess coordinator. |
| **Java** | `seats.java` | CLI seat validation service enforcing occupancy constraints. |
| **C# (.NET)** | `PaymentService` | Financial calculation engine handling age discounts, invariant currency parsing, and change calculations. |
| **JavaScript / HTML / CSS** | `index.html`, `script.js` | Single-page application UI handling DOM updates and API calls. |
| **SQLite** | `omnicinema.db` | Relational database initialized via `schema.sql`. |

---

## 🔄 System Workflow
```text
[ Web Frontend ] 
       │ (HTTP POST /api/buy-ticket)
       ▼
[ Python Flask Backend ] 
       │
       ├── 1. Invokes Java Engine ──► [ seats.java ]
       │                              └─ Validates if seat is occupied
       │
       ├── 2. Invokes C# Engine ────► [ PaymentService (C#) ]
       │                              └─ Applies 10% youth discount (age < 18)
       │                              └─ Validates funds & calculates change
       │
       └── 3. Commits to DB ────────► [ SQLite (omnicinema.db) ]
                                      └─ Updates seat state to booked (1)
                                      └─ Records sale entry in ledger
```

## 📁 Repository Structure
```text
OmniCinema/
├── main.py                          # Flask web server & backend controller
├── schema.sql                       # Database schema & initial seeding data
├── index.html                       # Frontend web view
├── script.js                        # Frontend UI logic & API fetch requests
├── seats.java                       # Java seat occupancy validation service
├── omnicinema.db                    # SQLite database file (generated on launch)
└── payment-service/
    └── PaymentService/
        ├── Class1.cs                # C# payment & discount calculation logic
        └── PaymentService.csproj    # .NET executable project file
```
## ⚙️ Prerequisites
Ensure you have the following installed on your machine:

- Python 3.8+
- Java Development Kit (JDK 11+)
- .NET SDK (6.0 / 8.0 / 10.0)

## 🚀 Getting Started
1. Clone the Repository
git clone [https://github.com/your-username/OmniCinema.git](https://github.com/your-username/OmniCinema.git)
cd OmniCinema

2. Install Dependencies
Install Flask using pip:
pip install flask

3.Target Framework Check (Optional)
Ensure the <TargetFramework> inside payment-service/PaymentService/PaymentService.csproj matches your installed .NET version (e.g., net6.0, net8.0, or net10.0). You can verify your installed version with:
dotnet --version

4. Run the Application
Start the Flask application:
python main.py

Open your browser and navigate to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)
