/**
 * @file ./server/index.js
 * @author Camden Smith
 * @course CIS350
 * @assignment Assignment 1
 * @date 5/22/2026
 */

const express = require("express");
const app = express();
const mongoose = require("mongoose");
const FishModel = require('./models/Fish');

const cors = require("cors")
app.use(express.json());
app.use(cors());

mongoose.connect("mongodb+srv://Smitcamd:12345@cis350.bn4rxd8.mongodb.net/MERN?appName=CIS350");
app.listen(3001, () => {
console.log("Server is running......");
});

app.get("/getFish", (req, res) => {
    FishModel.find().then((data) => {
        console.log(data);
        res.json(data);
    });
});


app.post("/createFish", async (req, res) => {
    const fish = req.body;
    const newFish = new FishModel(fish);
    await newFish.save();
    res.json(fish);
});
