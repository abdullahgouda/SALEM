import client from "./axios_client";

/* ================= GET USERS ================= */
export const getUsers = async () => {
    const res = await client.get("/employee/");

    return res.data.employees.map((u) => ({
        id: u.id,
        name: u.Name,
        email: u.Email,
        role: u.Role,
        status: u.Account_Status,
    }));
};

/* ================= CREATE USER ================= */
export const createUser = async (data) => {
    const payload = {
        Name: data.name,
        National_Id: data.nationalId,
        Phone_Number: data.phoneNumber,
        Email: data.email,
        Password: data.password,
        User_Type: "employee",
        Role: data.role,
        Region: data.region,
        Department: data.department,
        Account_Status: data.accountStatus || "نشط",
    };

    const res = await client.post("/employee/signup/", payload);

    return res.data;
};

/* ================= UPDATE USER ================= */
export const updateUser = async (id, data) => {
    const payload = {
        Name: data.name,
        Phone_Number: data.phoneNumber,
        Email: data.email,
        Role: data.role,
        Region: data.region,
        Department: data.department,
        Account_Status: data.accountStatus,
    };

    const res = await client.put(
        `/employee/${id}/update/`,
        payload
    );

    return res.data;
};

/* ================= DELETE USER ================= */
export const deleteUser = async (id) => {
    await client.delete(`/employee/${id}/delete/`);
};