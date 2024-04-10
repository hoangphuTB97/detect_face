
const getAttendance = async () => {
  try {
    // const res = await axios({
    //   method: "get",
    //   url: "localhost:3000/attendance",
    // });

    const res = await fetch("http://localhost:3000/attendance", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await res.json();
    nhanvien = data;
    console.log(data);
    const table = document.querySelector("tbody");

    data.forEach(function (item) {
      var row = document.createElement("tr");

      var idCell = document.createElement("td");
      idCell.textContent = item.ID_NV;
      row.appendChild(idCell);

      var nameCell = document.createElement("td");
      nameCell.textContent = item.NAME;
      row.appendChild(nameCell);

      var dateCell = document.createElement("td");
    dateCell.textContent = item.DATE; // Sử dụng dữ liệu ngày từ máy chủ
    row.appendChild(dateCell);

      var checkInCell = document.createElement("td");
      checkInCell.textContent = item.CHECK_IN_TIME;
      row.appendChild(checkInCell);

      var checkOutCell = document.createElement("td");
      checkOutCell.textContent = item.CHECK_OUT_TIME;
      row.appendChild(checkOutCell);

      table.appendChild(row);
    });
  } catch (error) {
    console.log("err", error);
  }
};
getAttendance();
// Thêm sự kiện click cho mục "Quản lý nhân viên" trong menu
document.getElementById("employeeManagement").addEventListener("click", async function() {
    try {
        const res = await fetch("http://localhost:3000/employees", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        const data = await res.json();
        console.log(data);
        const table = document.querySelector("tbody");

        // Xóa dữ liệu cũ trong bảng
        table.innerHTML = "";

        // Tạo các dòng mới trong bảng với thông tin nhân viên
        data.forEach(function (employee) {
            var row = document.createElement("tr");

            var idCell = document.createElement("td");
            idCell.textContent = employee.ID;
            row.appendChild(idCell);

            var nameCell = document.createElement("td");
            nameCell.textContent = employee.NAME;
            row.appendChild(nameCell);

            var genderCell = document.createElement("td");
            genderCell.textContent = employee.GENDER;
            row.appendChild(genderCell);

            var birthYearCell = document.createElement("td");
            birthYearCell.textContent = employee.BIRTH_YEAR;
            row.appendChild(birthYearCell);

            var positionCell = document.createElement("td");
            positionCell.textContent = employee.POSITION;
            row.appendChild(positionCell);

            var departmentCell = document.createElement("td");
            departmentCell.textContent = employee.DEPARTMENT;
            row.appendChild(departmentCell);

            table.appendChild(row);
        });
    } catch (error) {
        console.log("err", error);
    }
});


