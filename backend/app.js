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

// app.get("/attendance", async (req, res) => {
//   const attendaces = await db.all(
//     `SELECT ATTENDANCE.*, EMPLOYEES.name AS NAME
//     FROM ATTENDANCE
//     INNER JOIN EMPLOYEES ON ATTENDANCE.ID_NV = EMPLOYEES.id`,

//     (err, rows) => {
//       if (err) {
//         console.error(err.message);
//       }
//       res.send(rows);
//     }
//   );
// });
app.get("/attendance", async (req, res) => {
  try {
    const selectedMonth = req.query.month;
    const attendances = await db.all(
      `SELECT ID_NV, 
      COUNT(*) AS AttendanceCount,
      SUM(CASE WHEN TIME(CHECK_IN_TIME) > TIME('08:30') THEN 1 ELSE 0 END) AS lateCount,
      SUM(CASE WHEN TIME(CHECK_OUT_TIME) < TIME('17:30') THEN 1 ELSE 0 END) AS earlyCount
      FROM ATTENDANCE
      WHERE substr(DATE, 6, 2) = '${selectedMonth.padStart(2, "0")}'
      GROUP BY ID_NV;`,
      (err, rows) => {
        if (err) {
          console.error(err.message);
        }
        res.send(rows);
      }
    );
  } catch (error) {
    console.error(error.message);
    res.status(500).send("Internal Server Error");
  }
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
