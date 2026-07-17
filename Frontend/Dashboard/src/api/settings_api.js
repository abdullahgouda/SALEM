import client from "./axios_client";

// ================= GET DEPARTMENTS =================
export const getDepartments = async () => {
  const response = await client.get(
    "/department/"
  );

  return response.data;
};

// ================= CREATE DEPARTMENT =================
export const createDepartment = async (
  formData
) => {
  const response = await client.post(
    "/department/create/",
    formData,
    {
      headers: {
        "Content-Type":
          "multipart/form-data",
      },
    }
  );

  return response.data;
};

// ================= UPDATE DEPARTMENT =================
export const updateDepartment = async (
  id,
  formData
) => {
  const response = await client.post(
    `/department/${id}/update/`,
    formData,
    {
      headers: {
        "Content-Type":
          "multipart/form-data",
      },
    }
  );

  return response.data;
};

// ================= DELETE DEPARTMENT =================
export const deleteDepartment = async (
  id
) => {
  const response = await client.delete(
    `/department/${id}/delete/`
  );

  return response.data;
};