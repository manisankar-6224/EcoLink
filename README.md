# 🌱 EcoLink: Community Asset Exchange and Waste-Reduction Network

## 1. About the Project

**EcoLink** is a community-based web application designed to connect people who have unused items with others who need them. It encourages sharing, exchanging, and reusing useful resources instead of throwing them away.

The platform is intended for the wider community, including individuals, families, students, working professionals, local groups, and organizations.

The main goal of EcoLink is to reduce unnecessary waste, improve resource utilization, and promote sustainable consumption.

## 2. Problem Statement

Many people have reusable items they no longer need, while others may be searching for those same items. Information about available items is often scattered across social media groups, donation platforms, and online marketplaces.

This makes it difficult to discover reusable resources and organize requests efficiently.

EcoLink addresses this problem by providing a centralized platform for listing, discovering, and requesting reusable items.

## 3. Objectives

- Encourage the sharing and reuse of useful items.
- Reduce the unnecessary disposal of reusable resources.
- Provide a centralized platform for item listings.
- Allow users to search for items using keywords and categories.
- Enable users to submit requests for listed items.
- Help manage requests through status updates.
- Display basic statistics about items and requests.
- Promote responsible consumption and sustainable living.

## 4. Key Features

### 📦 Item Listings
Users can list items by providing details such as title, category, condition, area, and description.

### 🔎 Search and Filter
Users can search for items using keywords and filter listings by category.

### 📨 Item Requests
Users can request an available item by entering their name and an optional message.

### 📋 Request Management
Submitted requests can be viewed and their statuses can be updated to Pending, Accepted, or Rejected.

### 📊 Dashboard
The dashboard displays basic statistics, including the total number of listed items and request counts by status.

### ♻️ Waste-Reduction Estimate
The application displays an illustrative estimate of potential waste avoided based on the number of listed items. This is an approximate demonstration, not a measurement of actual waste reduction.

## 5. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application framework |
| HTML | Web page structure |
| CSS | Styling and layout |
| SQLite | Database for storing items and requests |
| Web Browser | Accessing the application |

## 6. System Architecture

EcoLink follows a simple three-layer architecture.

1. **Presentation Layer:** HTML and CSS display the user interface.
2. **Application Layer:** Python and Flask process user actions, search requests, item requests, and status updates.
3. **Database Layer:** SQLite stores item listings and request information.

### Application Workflow

1. The user opens the EcoLink website.
2. The application displays available item listings and dashboard statistics.
3. The user searches for items or filters them by category.
4. The user can submit a request for an item.
5. The application stores the request in the SQLite database.
6. Requests can be viewed and their statuses updated.
7. The dashboard displays updated statistics.

## 7. Database

EcoLink uses SQLite to store application data.

The main database tables are:

- **Items:** Stores item details such as title, category, condition, area, and description.
- **Requests:** Stores item requests, requester information, optional messages, and request statuses.

SQLite provides lightweight, local database storage suitable for this project prototype.

## 8. Installation and Setup

### Prerequisites

Install Python on your computer. A modern Python 3 version compatible with your installed Flask version is recommended.

### Step 1: Open the project folder

Open Command Prompt or PowerShell and navigate to your EcoLink project directory.

```bash
cd path/to/EcoLink
```

Replace `path/to/EcoLink` with your actual project folder path.

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate the virtual environment

**Windows:**

```powershell
venv\Scripts\activate
```

### Step 4: Install Flask

```bash
pip install flask
```

If your project includes a `requirements.txt` file, you can install its dependencies using:

```bash
pip install -r requirements.txt
```

### Step 5: Run the application

```bash
python app.py
```

### Step 6: Open the website

Open your browser and visit:

http://127.0.0.1:5000/

The EcoLink application should now be available locally on your computer.

## 9. Project Structure

A typical project structure is shown below. Your actual filenames may differ.

```text
EcoLink/
│
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── requirements.txt
├── README.md
└── instance/
    └── ecolink.db
```

The database location depends on how the SQLite connection is configured in your application. The structure above is illustrative; keep the paths consistent with your actual code.

## 10. Expected Outcomes

- A centralized interface for listing and discovering reusable items.
- Easier searching and filtering of item listings.
- Organized submission and management of item requests.
- Basic visibility into item and request statistics.
- Increased awareness of sharing, reuse, and responsible consumption.

These are intended project outcomes; actual environmental impact would need to be measured separately.

## 11. Limitations

- The current application is a learning prototype.
- User registration and secure login are not included in the current feature set.
- Item image uploads and real-time notifications are not included.
- Item exchange and delivery arrangements are not automated.
- The waste-reduction estimate is illustrative rather than based on measured item weights.
- The application has not been hardened for production use.

## 12. Future Enhancements

- Secure user registration and login.
- Item image uploads.
- Location-based item discovery.
- Real-time notifications for requests.
- Improved search and filtering options.
- User ratings and feedback.
- Secure communication between users.
- More accurate environmental impact tracking.
- Mobile-friendly improvements or a dedicated mobile application.

## 13. Sustainable Development Goal

EcoLink supports **United Nations Sustainable Development Goal 12: Responsible Consumption and Production**.

By encouraging people to reuse and share useful items, the project aims to support more responsible resource consumption and reduce unnecessary waste.

## 14. Conclusion

EcoLink demonstrates how a simple web application can support community resource sharing and sustainable practices. By combining item listings, search and filtering, request management, and dashboard statistics, the project provides a starting point for a more organized community exchange system.

Future improvements can make the platform more secure, accessible, and scalable while helping communities make better use of existing resources.

---

**Project Name:** EcoLink: Community Asset Exchange and Waste-Reduction Network  
**Project Type:** Web Application  
**Backend:** Python and Flask  
**Database:** SQLite  
**Frontend:** HTML and CSS
