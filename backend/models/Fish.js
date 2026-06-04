const mongoose = require("mongoose");

const FishSchema = new mongoose.Schema({
  fish: {
    type: String,
    required: true,
  },
  length: {
    type: Number,
    required: true,
  },
  weight: {
    type: Number,
    required: true,
  },
  location: {
    type: String,
    required: true,
  },
});

module.exports = mongoose.model("Fish", FishSchema);