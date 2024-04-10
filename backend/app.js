// file app.js
const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const sqlite3 = require("sqlite3").verbose();
port = 3000;
var cors = require("cors");
const allowCrossDomain = (req, res, next) => {
  res.header(`Access-Control-Allow-Origin`, `example.com`);
  res.header(`Access-Control-Allow-Methods`, `GET,PUT,POST,DELETE`);
  res.header(`Access-Control-Allow-Headers`, `Content-Type`);
  next();
};
app.use(function (req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept"
  );
  next();
});
app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded
app.use(allowCrossDomain);
app.use(cors());

let db = new sqlite3.Database(
  "../database/databases.db",
  sqlite3.OPEN_READWRITE,
  (err) => {
    if (err) {
      console.error(err.message);
    }
    console.log("Connected to the database.");
  }
);
// Thêm một endpoint mới để lấy thông tin tất cả nhân viên
app.get("/employees", async (req, res) => {
    const employees = await db.all("SELECT * FROM EMPLOYEES", (err, rows) => {
      if (err) {
        console.error(err.message);
      }
      res.send(rows);
    });
  });
  
app.get("/attendance", async (req, res) => {
  const attendaces = await db.all(
    `SELECT ATTENDANCE.*, EMPLOYEES.name AS NAME
    FROM ATTENDANCE
    INNER JOIN EMPLOYEES ON ATTENDANCE.ID_NV = EMPLOYEES.id`,
    
    (err, rows) => {
      if (err) {
        console.error(err.message);
      }
      res.send(rows);
    }
  );
});
app.get("/attendance", async (req, res) => {
  try {
    const selectedMonth = req.query.month;
    const attendances = await db.all(
      `SELECT ATTENDANCE.ID_NV, 
              COUNT(*) AS total_working_days,
              SUM(ATTENDANCE.LATE) AS total_late,
              SUM(ATTENDANCE.EARLY) AS total_early
      FROM ATTENDANCE 
      INNER JOIN EMPLOYEES ON ATTENDANCE.ID_NV = EMPLOYEES.id
      WHERE strftime('%m', ATTENDANCE.DATE) = ?
      GROUP BY ATTENDANCE.ID_NV`,
      [selectedMonth]
    );
    
    res.send(attendances);
  } catch (error) {
    console.error(error.message);
    res.status(500).send("Internal Server Error");
  }
});


app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
