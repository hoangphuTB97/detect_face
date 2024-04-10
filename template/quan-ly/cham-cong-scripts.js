const getEmployees = async () => {
    try {
        // Gửi yêu cầu lấy dữ liệu nhân viên từ API endpoint
        const res = await fetch("http://localhost:3000/employees", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        // Chuyển đổi dữ liệu nhận được thành định dạng JSON
        const data = await res.json();

        // Lấy thẻ tbody của bảng
        const tbody = document.getElementById("employeeTableBody");

        // Xóa dữ liệu cũ trong tbody
        tbody.innerHTML = "";

        // Duyệt qua mỗi nhân viên và thêm thông tin vào bảng
        for (const employee of data) {
            var row = document.createElement("tr");
            var idCell = document.createElement("td");
            idCell.textContent = employee.ID;
            row.appendChild(idCell);

            var nameCell = document.createElement("td");
            nameCell.textContent = employee.NAME;
            row.appendChild(nameCell);

            var departmentCell = document.createElement("td");
            departmentCell.textContent = employee.DEPARTMENT;
            row.appendChild(departmentCell);

            var positionCell = document.createElement("td");
            positionCell.textContent = employee.POSITION;
            row.appendChild(positionCell);

            var attendanceCell = document.createElement("td");
            // Sử dụng await khi gọi hàm calculateAttendance
            const selectedMonth = document.getElementById("monthSelect").value;
            const attendanceDays = await calculateAttendance(employee.ID, selectedMonth);
            attendanceCell.textContent = attendanceDays.totalWorkingDays;
            row.appendChild(attendanceCell);

            var lateCell = document.createElement("td");
            lateCell.textContent = attendanceDays.lateCount;
            row.appendChild(lateCell);

            var earlyCell = document.createElement("td");
            earlyCell.textContent = attendanceDays.earlyCount;
            row.appendChild(earlyCell);

            tbody.appendChild(row); // Thêm dòng vào tbody
        }
    } catch (error) {
        console.log("Error:", error);
    }
};

// Hàm tính toán số ngày công trong tháng cho một nhân viên dựa trên ID của nhân viên
const calculateAttendance = async (employeeId, selectedMonth) => {
    try {
        // Gửi yêu cầu lấy dữ liệu chấm công từ API endpoint, truyền vào ID của nhân viên và tháng được chọn
        const res = await fetch(`http://localhost:3000/attendance?employeeId=${employeeId}&month=${selectedMonth}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        // Chuyển đổi dữ liệu nhận được thành định dạng JSON
        const attendanceData = await res.json();

        // Khởi tạo biến để tính tổng số ngày công trong tháng
        let totalWorkingDays = 0;
        let lateCount = 0;
        let earlyCount = 0;

        // Duyệt qua mỗi bản ghi trong dữ liệu chấm công
        for (const record of attendanceData) {
            // Lấy ngày từ cột 'DATE' của dữ liệu chấm công
            const date = new Date(record.DATE);

            // Lấy tháng từ ngày
            const month = date.getMonth() + 1;

            // Kiểm tra xem tháng có bằng tháng được chọn không
            if (month === parseInt(selectedMonth)) {
                // Nếu có, tăng biến totalWorkingDays lên 1
                totalWorkingDays++;

                // Lấy giờ check-in và check-out từ dữ liệu
                const checkInTime = record.CHECK_IN;
                const checkOutTime = record.CHECK_OUT;

                // Xử lý số lần đi muộn và về sớm
                const { late, early } = handleLateAndEarly(checkInTime, checkOutTime);
                lateCount += late;
                earlyCount += early;
            }
        }

        // Trả về tổng số ngày công trong tháng và số lần đi muộn, về sớm
        return { totalWorkingDays, lateCount, earlyCount };
    } catch (error) {
        console.log("Error:", error);
        return { totalWorkingDays: 0, lateCount: 0, earlyCount: 0 };
    }
};

// Hàm xử lý số lần đi muộn và về sớm
const handleLateAndEarly = (checkInTime, checkOutTime) => {
    const standardCheckInTime = new Date(`1970-01-01T08:30:00Z`);
    const standardCheckOutTime = new Date(`1970-01-01T17:30:00Z`);

    // Chuyển đổi thời gian check-in và check-out thành đối tượng Date
    const actualCheckInTime = new Date(`1970-01-01T${checkInTime}Z`);
    const actualCheckOutTime = new Date(`1970-01-01T${checkOutTime}Z`);

    // Khởi tạo biến late và early
    let late = 0;
    let early = 0;

    // Kiểm tra xem nhân viên có đi muộn hay về sớm không
    if (actualCheckInTime > standardCheckInTime) {
        late = 1;
    }
    if (actualCheckOutTime < standardCheckOutTime) {
        early = 1;
    }

    return { late, early };
};


getEmployees();
