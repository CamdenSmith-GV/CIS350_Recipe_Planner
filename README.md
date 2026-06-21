# Grocery Studio

## A tool for saving recipes and turning them into grocery lists

**Authors:** Camden Smith, Jasper Gugino, William Calihan

**Date:** June 22, 2026

**Course:** CIS 350

**Institution:** Grand Valley State University

---

## Links

### [GitHub Repository](https://github.com/CamdenSmith-GV/CIS350_Recipe_Planner)

---

# 1 Abstract
Grocery Studio is a web app for keeping recipes in one place and turning them into a grocery list. A user can add a recipe with its name, a summary, instructions, a cook time, and a list of ingredients, and it gets saved to a database so it stays there between visits. From the saved recipes, the user picks the ones they plan to cook and the app builds a single grocery list from them. It combines the same ingredient across recipes and converts the units so the amounts add up, which makes the list shorter and easier to shop from. The app is built with a React frontend, a FastAPI backend, and a MongoDB database.

---

# 2 Introduction
Planning meals takes a lot of time, just ask my mother, and one of the more annoying parts is figuring out everything you need to buy once you have picked your recipes. Cook a few things in a week and you end up with the same ingredient written down in different spots and amounts, which makes it easy to miss something at the store. Grocery Studio was built to handle that part for you.

You save your recipes in the app, and each one holds its ingredients with an amount, a unit, and a type (volume, mass, or count). When you are ready to shop, you pick the recipes you are making and the app pulls all of their ingredients into one list, combining anything that repeats and converting the units so the totals make sense.

The app is split into three parts. The React frontend is where you create recipes, browse the ones you have saved, and build the grocery list. The FastAPI backend handles saving and loading recipes and does the math for the list. The recipes live in a MongoDB database so they can be loaded back any time.

---

# 3 Architectural Design

## 3.1 Class Diagram

## 3.2 Use Case Diagram

## 3.3 Sequence Diagram


---

# 4 User Guide / Implementation

## 4.1 Starting the Application

## 4.2 Home Screen

## 4.3 Creating a Recipe

## 4.4 Viewing Saved Recipes

## 4.5 Recipe Details

## 4.6 Grocery List


---

# 5 Risk Analysis

### Risk Identification

- **Technical Risks:**
  - The app runs as three separate pieces (React, FastAPI, MongoDB), so there are more places for something to break than a single self contained app.
  - The database login is hardcoded in the backend instead of being kept in a config file, which is a security risk on a public repo.
  - Testing on the frontend and backend integration is limited, so some of that behavior is not covered.
- **Operational Risks:**
  -  The app depends on a hosted MongoDB cluster, so it stops working if the database is down or unreachable.
  -  There are no user accounts, so every recipe is shared from one collection with no separation between people.
- **Market Risks:**
  - Other of recipe and meal planning apps already exist that cover similar behaviors.
  - What people want out of a meal planning tool can shift over time.
    - People may want certain features such as an AI meal planner etc...  

### Risk Mitigation Strategies

- **Technical Risks:**
- **Operational Risks:**
- **Market Risks:**

---

# 6 Retrospective

### What Went Well

### Areas for Improvement

### Lessons Learned

---

# 7 Project Management

We used Jira to plan and track the project throughout development. The work was split into three sprints, with tasks assigned to each member and moved across the board as they were started, worked on, and finished. Each sprint held smaller, manageable pieces of work such as building the sequence diagram or adding unit tests, which broke the project down into clear steps. This kept a large project feeling approachable and easy to divide among the team.


<img width="1890" height="1416" alt="image" src="https://github.com/user-attachments/assets/69ef5c7a-c512-4ea2-b06d-906694215915" />
<img width="3158" height="784" alt="image" src="https://github.com/user-attachments/assets/8bfd8914-9264-452a-a477-ca3916888196" />

<p align="center">
  <img width="800" alt="Jira task overview" src="https://github.com/user-attachments/assets/69ef5c7a-c512-4ea2-b06d-906694215915" />
  <br>
  Figure 1: Full task list in Jira across all three sprints.
</p>

<p align="center">
  <img width="1000" alt="Jira sprint board" src="https://github.com/user-attachments/assets/8bfd8914-9264-452a-a477-ca3916888196" />
  <br>
  Figure 2: Jira board for the third sprint.
</p>
---

# 8 Future Scope

### Expansion of Features

### Technical Enhancements

---

# 9 Conclusion
