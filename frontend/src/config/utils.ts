import axios from "axios";
import { error } from "console";
import axiosInstance from "./axiosInstance";

const API_URL = 'http://127.0.0.1:8000/api'

// refresh token
// utils.ts
export const refreshAccessToken = async () => {
    const refresh_token = localStorage.getItem('refresh_token');
  
    if (!refresh_token) {
      // No refresh token available, redirect to login
      localStorage.clear();
      window.location.href = '/Components/Login';
      return { success: false, error: 'No refresh token' };
    }
  
    try {
      const response = await axios.post(`${API_URL}/token/refresh/`, {
        refresh: refresh_token,
      });
  
      const newAccessToken = response.data.access;
      localStorage.setItem('access_token', newAccessToken);
      return { success: true, access_token: newAccessToken };
    } catch (error: any) {
      console.error("Refresh token failed:", error.response?.data || error.message);
      // Clear storage and redirect on refresh failure
      localStorage.clear();
      window.location.href = '/Components/Login';
      return { success: false, error: 'Token refresh failed' };
    }
  };

// function to handle login and get a token
export const loginUser = async (
    email: string,
    password: string
) => {
    try {
        const response = await axiosInstance.post(`${API_URL}/user_login/`, {
            email: email,
            password: password
        });

        const {
            access_token,
            refresh_token,
            user_id,
            user_email,
            first_letter,
            is_admin,
            is_teacher,
            is_student,
            is_parent,
            teacher_profile_picture,
            parent_profile_picture,
        } = response.data;

        // save tokens and user info in localStorage
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        localStorage.setItem('user_id', user_id);
        localStorage.setItem('user_email', user_email);
        localStorage.setItem('first_letter', first_letter);
        localStorage.setItem('is_admin', is_admin);
        localStorage.setItem('is_teacher', is_teacher);
        localStorage.setItem('is_student', is_student);
        localStorage.setItem('is_parent', is_parent);
        localStorage.setItem('teacher_profile_picture', teacher_profile_picture);
        localStorage.setItem('parent_profile_picture', parent_profile_picture);

        return {success: true, data: response.data};

    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            return {
                success: false,
                error: error.response?.data || 'Login Failed',
            };
        }
        return {success: false, error: 'An unknown error occurred'};
    }
};

// LOGOUT FUNCTION
export const logoutUser = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_email');
    localStorage.removeItem('first_letter');
    localStorage.removeItem('is_admin');
    localStorage.removeItem('is_teacher');
    localStorage.removeItem('is_student');
    localStorage.removeItem('is_parent');
    localStorage.removeItem('teacher_profile_picture');
    localStorage.removeItem('parent_profile_picture');

    return {success: true, message: 'Logged Out Successfully'}
}

// Admin API Service

// function to create an admin
export const createAdmin = async (
    first_name: string,
    last_name: string,
    username: string,
    email: string,
    password: string, 
    confirm_password: string, 
    token: string,
) => {
    try {
        const response = await axiosInstance.post(`${API_URL}/create_admin/`, {
            first_name: first_name,
            last_name: last_name,
            username: username,
            email: email,
            password: password,
            confirm_password: confirm_password
        });
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error Creating Admin", error.response?.data || error.message);
            return error.response?.data || {error: "Error Creating Admin"}
        } else {
            console.error("Unknown Error", error);
            return {error: "Unknown Error"}
        }
    }
}

// function  to retreive all admins
export const fetchAdmins = async () => {
    try {
        const response = await axiosInstance.get(`${API_URL}/create_admin/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error fetching admins", error.response?.data || error.message);
            return error.response?.data || {error: "Error fetching admins"}; 
        } else {
            console.error("Unknown error", error);
            return {error: "Unknown error"};
        }
    }
}

// function to fetch a single admin
export const singleAdmin = async (id: string) => {
    try {
        const response = await axiosInstance.get(`${API_URL}/admin_info/${id}/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error retreiving Admin", error.response?.data || error.message);
            return error.response?.data || {error: 'Error retreiveng admin'};
        } else {
            console.error("Unknown error", error);
            return {error: "Unknown error"};
        }
    }
}

// function to update an admin
export const updateAdmin = async (
    id: string,
    first_name: string,
    last_name: string,
    username: string,
    email: string,
    password: string,
    confirm_password: string,
    token: string
) => {
    try {
        const response = await axiosInstance.patch(`${API_URL}/admin_info/${id}/`, {
            first_name: first_name,
            last_name: last_name,
            username: username,
            email: email,
            password: password,
            confirm_password: confirm_password
        });
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error updating Admin", error.response?.data || error.message);
            return error.response?.data || {error: "Error updating Admin"}
        } else {
            console.error("Unknown Error", error);
            return {error: "Unknown Error"};
        }
    }
}

// function to delete an admin
export const deleteAdmin = async (id: string) => {
    try {
        const response = await axiosInstance.delete(`${API_URL}/admin_info/${id}/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error deleting Admin", error.response?.data || error.message);
            return error.response?.data || {error: "Error deleting Admin"}
        } else {
            console.error("Unknown Error", error);
            return {error: "Unknown Error"}
        }
    }
}

// Teacher API Service

// function to fetch all teachers
export const fetchTeachers = async () => {
    const token = localStorage.getItem('access_token');
    
    try {
      const response = await axiosInstance.get(`${API_URL}/fetch_all_teachers/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      
      // Ensure the response data is an array
      const teachersData = Array.isArray(response.data) ? response.data : [];
      return { data: teachersData, error: null };
      
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 400) {
          return { data: [], error: error.response.data };
        }
        return { data: [], error: error.message || 'An Error Occurred' };
      }
      return { data: [], error: 'An Unknown Error Occurred' };
    }
  };

//   function to create a teacher
export const createTeacher = async (
    first_name: string,
    last_name: string,
    username: string,
    email: string,
    phone: string,
    profile_picture: File,
    address: string,
    password: string,
    confirm_password: string,
    token: string
) => {
    try {
        const formData = new FormData();
        
        // Append user data as nested object
        formData.append('user.first_name', first_name);
        formData.append('user.last_name', last_name);
        formData.append('user.username', username);
        formData.append('user.email', email);
        formData.append('user.password', password);
        formData.append('user.confirm_password', confirm_password);
        formData.append('user.role.name', 'teacher');
        
        // Append teacher-specific fields
        formData.append('phone', phone);
        formData.append('profile_picture', profile_picture);
        formData.append('address', address);

        const response = await axiosInstance.post(`${API_URL}/create_teacher/`, formData, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error: any) {
        if (error.response) {
            console.error("Server Error:", error.response.data);
            throw error.response.data;
        } else if (error.request) {
            console.error("No Response:", error.request);
            throw new Error("No Response from Server");
        } else {
            console.error("Error:", error.message);
            throw new Error(error.message);
        }
    }
};

// function to retreive a single teacher
export const singleTeacher = async (id: string) => {
    try {
      const response = await axiosInstance.get(`${API_URL}/teacher_info/${id}/`);
      return { data: response.data, error: null };
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        const errorMessage = error.response?.data.detail || error.message || 'An error occurred while fetching the teacher';
        return { data: null, error: errorMessage };
      } else {
        return { data: null, error: 'An unexpected error occurred' };
      }
    }
  };

// Function to update a teacher
export const updateTeacher = async (id: string, formData: FormData, token: string) => {
    try {
        const response = await axiosInstance.patch(`${API_URL}/teacher_info/${id}/`, formData, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            const errorMessage = error.response?.data || error.message;
            console.error("Error updating teacher:", errorMessage);
            throw new Error(
                typeof errorMessage === 'object' 
                ? JSON.stringify(errorMessage)
                : errorMessage
            );
        } else {
            console.error("Unknown error while updating:", error);
            throw new Error("Unknown error occurred while updating teacher");
        }
    }
}

// function to delete a teacher
export const deleteTeacher = async (id: string) => {
    try {
        const response = await axiosInstance.delete(`${API_URL}/teacher_info/${id}/`);
        return response.data
    } catch (error: any) {
        console.error('Delete error: ', error);
        throw error;
    }
};

// function to create a parent
export const createParent = async (
    first_name: string,
    last_name: string,
    username: string, 
    email: string,
    password: string,
    confirm_password: string,
    phone: string,
    profile_picture: File | null,
    address: string,
    token: string
) => {
    try {
        const formData = new FormData()
        formData.append('user.first_name', first_name);
        formData.append('user.last_name', last_name);
        formData.append('user.username', username);
        formData.append('user.email', email);
        formData.append('user.password', password);
        formData.append('user.confirm_password', confirm_password);
        formData.append('phone', phone);
        if (profile_picture) {
            formData.append('profile_picture', profile_picture)
        }
        formData.append('address', address);
    
        const response = await axiosInstance.post(`${API_URL}/create_parent/`, formData, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'multipart/form-data',
            }
        })
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error Creating Parent", error.response?.data || error.message)
            return error.response?.data || {error: "Somethig went wrong. Please try again..."}
        } else {
            console.error("Unknown error", error)
            return {error: "Unexpected error occurred!"}
        }
    }
}

// function to retreive all parents
export const fetchParents = async () => {
    try {
        const response = await axiosInstance.get(`${API_URL}/fetch_all_parents/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error fetching parents", error.response?.data || error.message)
            return error.response?.data || {error: "Something went wrong.Please try again..."}
        } else {
            console.error("Unknown error", error)
            return {error: "Unexpected error occurred!"}
        }      
    }
}

// function to retreive a single parent
export const singleParent = async (id: string) => {
    try {
        const response = await axiosInstance.get(`${API_URL}/parent_info/${id}/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error retreivin Teacher", error.response?.data || error.message)
            return error.response?.data || {error: "Something went wrong.Please retry..."}
        } else {
            console.error("Unknown error", error)
            return {error: "Unexpected error occurred!"}
        }
    }
}

// function to update a parent
export const updateParent = async (
    id: string,
    formData: FormData,
    token: string
) => {
    try {
        const response = await axiosInstance.patch(
            `${API_URL}/parent_info/${id}/`,
            formData,
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    // No need to set Content-Type manually for FormData
                },
            }
        );
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Update error:", {
                data: error.response?.data,
                status: error.response?.status,
                headers: error.response?.headers,
                message: error.message,
                fullError: error
            });
            throw error.response?.data || new Error("Update failed");
        }
        throw error;
    }
};

// function to delete a parent
export const deleteParent = async (id: string) => {
    try {
        const response = await axiosInstance.delete(`${API_URL}/parent_info/${id}/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error deleting Parent.", error.response?.data || error.message)
            return error.response?.data || {error: "Something went wrong.Please retry..."}
        } else {
            console.error("Unknown error", error)
            return {error: "Unexpected error occurred!"}
        }
    }
}

// Student API Service

// Function to create a student
export const createStudent = async (
    payload: any,
    token: string
  ) => {
    try {
      const response = await axiosInstance.post(`${API_URL}/create_student/`, payload, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      return response.data;
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        console.error("Detailed error:", {
          status: error.response?.status,
          data: error.response?.data,
          config: error.config
        });
        throw error.response?.data || new Error("Failed to create student");
      }
      throw error;
    }
  };
  

// Function to fetch all students
export const fetchStudents = async () => {
    try {
        const response = await axiosInstance.get(`${API_URL}/fetch_all_students/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error fetching students:", error.response?.data || error.message);
            throw error.response?.data || new Error("Failed to fetch students");
        }
        throw error;
    }
};

// Function to fetch a single student
export const singleStudent = async (id: string) => {
    try {
        const response = await axiosInstance.get(`${API_URL}/student_info/${id}/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error fetching student:", error.response?.data || error.message);
            throw error.response?.data || new Error("Failed to fetch student");
        }
        throw error;
    }
};

// updateStudent using JSON
export const updateStudent = async (
    id: string,
    payload: any,
    token: string
) => {
    try {
        const response = await axiosInstance.patch(
            `${API_URL}/student_info/${id}/`,
            payload,
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            }
        );
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Update error:", error.response?.data);
            throw error.response?.data || new Error("Update failed");
        }
        throw error;
    }
};


// Function to delete a student
export const deleteStudent = async (id: string) => {
    try {
        const response = await axiosInstance.delete(`${API_URL}/student_info/${id}/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error deleting student:", error.response?.data || error.message);
            throw error.response?.data || new Error("Failed to delete student");
        }
        throw error;
    }
};

// Role API Service

// function to retreive all roles
export const fetchRoles = async () => {
    try {
        const response = await axiosInstance.get(`${API_URL}/create_role/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error retreiveng roles", error.response?.data || error.message);
            return error.response?.data || {error: "Error retreiveng Roles"}
        } else {
            console.error("Unknown error", error)
            return {error: "Unexpected error ocurred!"}
        }     
    }
}

// function to create a role
export const createRole = async (name: string) => {
    try {
        const response = await axiosInstance.post(`${API_URL}/create_role/`, {
            name: name,
        });
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error creating role", error.response?.data || error.message);
            return error.response?.data || {error: "Error creating Role"};
        } else {
            console.error("Unknown error", error);
            return {error: "Unexpected error occurred"};
        }
    }
};

// function to retreive a single role
export const singleRole = async (
    id: string,
) => {
    try {
        const response = await axiosInstance.get(`${API_URL}/role_info/${id}/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error retreiveng role", error.response?.data || error.message);
            return error.response?.data || {error: "Error retreiving role"}
        } else {
            console.error("Unknown error", error);
            return {error: "Unknown error"}
        }
    }
}

// function to update a role
export const updateRole = async (
    id: string,
    name: string,
) => {
    try {
        const response = await axiosInstance.patch(`${API_URL}/role_info/${id}/`, {
            name: name
        });
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error updating role", error.response?.data || error.message);
            return error.response?.data || {error: "Error updating role"}
        } else {
            console.error("Unknown error", error);
            return {error: "Unknown error"}
        }
    }
}

// function to delete a role
export const deleteRole = async (id: string) => {
    try {
        const response = await axiosInstance.delete(`${API_URL}/role_info/${id}/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error deleting role", error.response?.data || error.message);
            return error.response?.data || {error: "Error deleting role"}
        } else {
            console.error("Unknown error", error);
            return {error: "Unknown error"}
        }
    }
}

// function to fetch total students
export const totalStudents = async () => {
    try {
        const response = await axiosInstance.get(`${API_URL}/all_students/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error fetching Number of Students", error.response?.data || error.message);
            return error.response?.data || {error: "Error fetching number of students"}
        } else {
            console.error("Unknown error", error)
            return {error: "Unknown Error"}
        }
    }
}

// function to fetch total parents
export const totalParents = async () => {
    try {
        const response = await axiosInstance.get(`${API_URL}/all_parents/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error fetching Parents!", error.response?.data || error.message);
            return error.response?.data || {error: "Error fetching Parents!"};
        } else {
            console.error("Unknown Error", error);
            return {error: "Unknown Error"};
        }
    }
}

// function to etch the number of teachers
export const totalTeachers = async () => {
    try {
        const response = await axiosInstance.get(`${API_URL}/all_teachers/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error fetching teachers", error.response?.data || error.message);
            return error.response?.data || {error: "Error fetching teachers"};
        } else {
            console.error("Unknown Error", error);
            return {error: "Unknown Error"};
        }
    }
}

// Teacher Announcement API

// function to fetch teacher announcements
export const fetchTeacherAnnouncements = async () => {
    try {
        const response = await axiosInstance.get(`${API_URL}/teacher_targeted_announcements/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error fetching Teacher Announcements!", error.response?.data || error.message);
            return error.response?.data || {error: "Error fetching Teacher Announcements"};
        } else {
            console.error("Unknown Error", error);
            return {error: "Unknown Error"};
        }
    }
}

// Parent Announcement API

// function to fetch parent based announcements
export const fetchParentAnouncements = async () => {
    try {
        const response = await axiosInstance.get(`${API_URL}/parent_targeted_announcements/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error fetching Parent Announcements", error.response?.data || error.message);
            return error.response?.data || {error: "Error fetching Parent Announcements"};
        } else {
            console.error("Unknown Error", error);
            return {error: "Unknown Error"};
        }
    }
}

// Student Announcement API

// function to fetch student based Announcements
export const fetchStudentAnnouncements = async () => {
    try {
        const response = await axiosInstance.get(`${API_URL}/student_targeted_announcements/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error fetching Student Announcements", error.response?.data || error.message);
            return error.response?.data || {error: "Error fetching Student Announcements"};
        } else {
            console.error("Unknown Error", error);
            return {error: "Unknown Error"};
        }
    }
}

// Admin Announcement API

// function  to fetch admin targeted announcements
export const fetchAdminAnnouncements = async () => {
    try {
        const response = await axiosInstance.get(`${API_URL}/admin_targeted_announcements/`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            console.error("Error fetching Admin Announcements", error.response?.data || error.message);
            return error.response?.data || {error: "Error fetching Admin Announcements"};
        } else {
            console.error("Unknown Error", error);
            return {error: "Unknown Error"};
        }
    }
}
