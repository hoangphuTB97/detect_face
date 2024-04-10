const getEmployees = async () => {
    try {
        const res = await fetch("http://localhost:3000/employees", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        const data = await res.json();
        console.log(data);
        const table = document.querySelector("table");
        console.log(table);
        data.forEach(function (item) {
            var row = document.createElement("tr");

            var idCell = document.createElement("td");
            idCell.textContent = item.ID;
            row.appendChild(idCell);

            var nameCell = document.createElement("td");
            nameCell.textContent = item.NAME;
            row.appendChild(nameCell);

            var genderCell = document.createElement("td");
            genderCell.textContent = item.GENDER;
            row.appendChild(genderCell);

            var dateCell = document.createElement("td");
            dateCell.textContent = item.BIRTH_YEAR;
            row.appendChild(dateCell);

            var checkInCell = document.createElement("td");
            checkInCell.textContent = item.POSITION;
            row.appendChild(checkInCell);

            var checkOutCell = document.createElement("td");
            checkOutCell.textContent = item.DEPARTMENT;
            row.appendChild(checkOutCell);

            table.appendChild(row);
        });
    } catch (error) {
        console.log("err", error);
    }
};

getEmployees()
// Thêm sự kiện click cho mục "Quản lý nhân viên" trong menu
document
  .getElementById("employeeManagement")
  .addEventListener("click", async function () {
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
  document.getElementById("employeeTableBody").addEventListener("click", async function (event) {
    // Kiểm tra xem người dùng đã nhấp vào nút "Sửa" hay không
    if (event.target.classList.contains("edit-btn")) {
        // Lấy ID của nhân viên được sửa từ thuộc tính data-id của nút "Sửa"
        const employeeId = event.target.dataset.id;

        // Gửi yêu cầu GET để lấy thông tin chi tiết của nhân viên cần sửa
        const res = await fetch(`http://localhost:3000/employees/${employeeId}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        const employeeData = await res.json();

        // Hiển thị modal sửa thông tin
        const editEmployeeModal = document.getElementById("editEmployeeModal");
        editEmployeeModal.style.display = "block";

        // Điền thông tin của nhân viên vào các trường nhập liệu trong modal
        document.getElementById("nameInput").value = employeeData.NAME;
        document.getElementById("genderInput").value = employeeData.GENDER;
        document.getElementById("birthYearInput").value = employeeData.BIRTH_YEAR;
        document.getElementById("positionInput").value = employeeData.POSITION;
        document.getElementById("departmentInput").value = employeeData.DEPARTMENT;

        // Gắn ID của nhân viên đang được sửa vào một thuộc tính data của modal để sử dụng sau này
        editEmployeeModal.dataset.id = employeeId;
    }
});

// Thêm sự kiện submit cho form trong modal sửa thông tin
document.getElementById("editEmployeeForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    // Lấy thông tin mới của nhân viên từ các trường nhập liệu trong modal
    const updatedEmployeeData = {
        name: document.getElementById("nameInput").value,
        gender: document.getElementById("genderInput").value,
        birthYear: document.getElementById("birthYearInput").value,
        position: document.getElementById("positionInput").value,
        department: document.getElementById("departmentInput").value,
    };

    // Lấy ID của nhân viên đang được sửa từ thuộc tính data của modal
    const employeeId = document.getElementById("editEmployeeModal").dataset.id;

    // Gửi yêu cầu PUT để cập nhật thông tin của nhân viên
    const res = await fetch(`http://localhost:3000/employees/${employeeId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedEmployeeData),
    });

    // Đóng modal sau khi cập nhật thành công
    document.getElementById("editEmployeeModal").style.display = "none";

    // Tải lại trang để cập nhật lại dữ liệu
    location.reload();
});

// Đóng modal khi người dùng nhấp vào nút đóng hoặc vùng xung quanh modal
document.getElementById("editEmployeeModal").addEventListener("click", function (event) {
    if (event.target === this || event.target.classList.contains("close")) {
        this.style.display = "none";
    }
});

