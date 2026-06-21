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

The user needs to run the frontend and the backend at the same time. In the frontend folder the user runs `npm start` to launch the React app, and in the backend folder runs `py -m uvicorn main:app --reload --port 3001` to start the server. Once both are running, the user can open the app in their browser.

## 4.2 Home Screen

<p align="center">
  <img width="850" alt="Home screen" src="https://github.com/user-attachments/assets/dbdc7124-b0d8-45e9-b810-fdee81e4792a" />
  <br>
  The landing page lists your saved recipes and links out to the recipe planner.
</p>

## 4.3 Creating a Recipe

<p align="center">
  <img width="800" alt="Recipe planner" src="https://github.com/user-attachments/assets/63a07e9d-90c2-41d8-8d76-838df8378373" />
  <br>
  The recipe planner, where you set the name, summary, ingredients, instructions, and cook time. Added ingredients show in the panel on the right.
</p>

<p align="center">
  <img width="620" alt="Adding a volume ingredient" src="https://github.com/user-attachments/assets/4ab67f7d-f8f3-474b-983b-46d69f12baca" />
  <br>
  Adding an ingredient measured by volume, like 2 cups of flour.
</p>

<p align="center">
  <img width="620" alt="Adding a mass ingredient" src="https://github.com/user-attachments/assets/f9437eaf-fd35-4a95-8588-0610ef8cdac3" />
  <br>
  Adding an ingredient measured by mass, with a name, unit, and amount.
</p>

## 4.4 Viewing Saved Recipes

<p align="center">
  <img width="850" alt="Recipe details" src="https://github.com/user-attachments/assets/c63e0932-e1e8-4a11-893e-9a7219d60696" />
  <br>
  Picking a saved recipe shows its full details, ingredients, and instructions.
</p>

## 4.5 Add to Grocery List

<p align="center">
  <img width="850" alt="Add to grocery list" src="https://github.com/user-attachments/assets/2e1e29c6-f975-4a09-a3e8-a55d784382e0" />
  <br>
  Recipes you add land in the Selected panel, and the button downloads the grocery list for them.
</p>

## 4.6 Grocery List

<p align="center">
  <img width="250" alt="Downloaded grocery list" src="https://github.com/user-attachments/assets/f8bfe42a-1f47-40ca-b1dc-68eb7d8defda" />
  <br>
  The downloaded list combines ingredients across the recipes and keeps volume and mass separate when they cannot be merged.
</p>


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
  - The database holds no personal, private, or sensitive data, so a leak would not expose anything important.
  - The hardcoded password is not a real or reused password, so it does not actually put anything at risk.
  - The app's functionality has been tested extensively by hand.
- **Operational Risks:**
  - The MongoDB cluster runs on AWS, which has around 99.99% uptime, so downtime should be rare.
  - User accounts are planned as a future addition. (If the project were to be continued past this course)
- **Market Risks:**
  - AI features are planned. (If the project were to be continued past this course)
  - The architecture makes it easy to add new features as needs change.

---

# 6 Retrospective

### What Went Well

- We are happy with the frontend UI. It is intuitive and looks good.
- The Python backend is organized well for creating recipes and parsing them into grocery lists. The logic is split across clear files: the API endpoints live in `main.py`, the ingredient combining and unit conversion lives in `ingredient.py`, and the output formatting lives in `format_output.py`. The code is easy to follow and build on.
- The unit tests and integration tests run successfully through CI/CD with GitHub Actions.

### Areas for Improvement

- We need to use Jira more consistently and actually keep up with it during the week.
- The frontend uses Bootstrap, which is nice and looks good, but it would be nicer to write the styling in plain CSS and HTML for more control over the look instead of leaning premade UI.
- We should offload more of the work to the backend instead of relying so heavily on frontend JavaScript.

### Lessons Learned

- Start the frontend UI early.
- Start the backend GET and POST endpoints early.
  - The frontend cannot do much without data to show, and the backend is hard to work on without something calling it.
- Start writing tests early instead of saving them all for the end.
- Put more effort into getting the diagrams right up front.

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

- Let the user tune the grocery list before downloading it. If you already have eggs, remove them; if you still need bbq sauce, add it.
- Export the grocery list directly as a PDF instead of a text file.
- Add pictures to recipes. We were limited here by the storage caps on the free database tier.
- AI powered features:
  - Use a low cost LLM to combine amounts that are in different units, like 2 lbs of flour plus 2 cups of flour.
  - Recipe generation. A button that pulls up new recipe ideas right inside the app.

### Technical Enhancements

- Host the web app on a server. Right now the app only runs locally: the frontend on `localhost:3000` and the backend on `localhost:3001`, so only the person running it can use it. 
- More database capacity, since the current setup is on the free tier.
- Logins and personal recipes for each user.

---

# 9 Conclusion

Grocery Studio does what we set out to build. You can save your recipes, keep them in one place, and turn the ones you plan to cook into a single grocery list that combines repeated ingrediants and sorts out the units for you. It runs on a React frontend, a FastAPI backend, and a MongoDB database, with the work split cleanly across those three parts. There is still plenty we would add, like editing the list before downloading, user logins, and hosting the app online, but as a first version it covers the core idea well and gives us a good foundation and proof of concept.
