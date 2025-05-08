
'use client'
import React, { useEffect, useState } from 'react'
import DashboardSideBar from '../dashboard_sidebar/page'
import DashboardNavBar from '../dashboard_navbar/page'
import { createZoomMeeting, fetchAdminAnnouncements, fetchParentAnouncements, fetchStudentAnnouncements, fetchTeacherAnnouncements, totalParents, totalStudents, totalTeachers } from '@/config/utils'
import Image from 'next/image'
import Link from 'next/link'
import { FiMessageSquare, FiBell, FiCalendar, FiUsers, FiBook, FiHome, FiSettings, FiPhoneCall, FiCameraOff, FiCamera, FiUnderline, FiWatch, FiZap, FiZoomOut, FiX, FiCircle, FiGitCommit, FiFacebook } from 'react-icons/fi'
import MeetingForm from '../meetingForm/page'

const DashboardPage = () => {
  // ... (keep all existing state declarations)
  const [students, setStudents] = useState('');
  const [parents, setParents] = useState('');
  const [teachers, setTeachers] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [announcement, setAnnouncement] = useState('');
  const [teacherAnnouncement, setTeacherAnnouncement] = useState<{
    message: string,
    Total: number,
    Announcements: {
      id: number,
      title: string,
      description: string,
      date_created : string
    }[];
  }>({
    message: '',
    Total: 0,
    Announcements: [],
  });

  const [parentAnnouncements, setParentAnnouncements] = useState<{
    message: string,
    Total: number,
    Announcements: {
      id: string,
      title: string,
      description: string,
      date_created: string
    }[];
  }>({
    message: '',
    Total: 0,
    Announcements: [],
  });

  const [studentAnnouncements, setStudentAnnouncements] = useState<{
    message: string,
    Total: number,
    Announcements: {
      id: string,
      title: string,
      description: string,
      date_created: string,
    }[];
  }>({
    message: '',
    Total: 0,
    Announcements: [],
  });

  const [adminAnnouncements, setAdminAnnouncements] = useState<{
    message: string,
    Total: number,
    Announcements: {
      id: string,
      title: string,
      description: string,
      date_created: string,
    }[]
  }>({
    message: '',
    Total: 0,
    Announcements: [],
  })

  // function to fetch all teacher announcements
  useEffect(() => {
    const fetchTeacherAssignment = async () => {
      const data = await fetchTeacherAnnouncements();

      if (data.error) {
        setError(data.error);
        return;
      }
      setTeacherAnnouncement(data);
    }
    fetchTeacherAssignment();
  }, []);

  // function to fetch parent announcemetns
  useEffect(() => {
    const fetchParentAnnouncements = async () => {
      const data = await fetchParentAnouncements();

      if (data.error){
        setError(data.error);
        return;
      }
      setParentAnnouncements(data)
    }
    fetchParentAnnouncements()
  }, []);

  // function to fetch student Announcements
  useEffect(() => {
    const fetchStudentAnnouncement = async () => {
      const data = await fetchStudentAnnouncements();
      if (data.error){
        setError(data.error);
        return;
      }
      setStudentAnnouncements(data);
    }
    fetchStudentAnnouncement();
  }, []);

  // function to fetch admin announcements
  useEffect(() => {
    const fetchAdminAnnouncement = async () => {
      const data = await fetchAdminAnnouncements();
      if (data.error) {
        setError(data.error);
        return;
      }
      setAdminAnnouncements(data);
    };
    fetchAdminAnnouncement();
  }, [])

  // function to fetch the total students
  useEffect(() => {
    const fetchStudentTotal = async () => {
      const data = await totalStudents();
      if (data.error) {
        setError(data.error);
        return;
      }
      setStudents(data.Total)
    }
    fetchStudentTotal()
  }, []);

  // function to fetch all parents
  useEffect(() => {
    const fetchParentTotal = async () => {
      const data = await totalParents();

      if (data.error) {
        setError(data.error);
        return;
      }
      setParents(data.Total)
    }
    fetchParentTotal()
  }, []);

  // function to fetch all teachers
  useEffect(() => {
    const fetchTeacherTotal = async () => {
      const data = await totalTeachers();

      if (data.error) {
        setError(data.error);
        return;
      }
      setTeachers(data.Total);
    }
    fetchTeacherTotal();
  }, []);

  const [role, setRole] = useState("");

useEffect(() => {
  const fetchUserRole = () => {
    const isAdmin = localStorage.getItem("is_admin") === "true";
    const isTeacher = localStorage.getItem("is_teacher") === "true";
    const isParent = localStorage.getItem("is_parent") === "true";
    const isStudent = localStorage.getItem("is_student") === "true";

    if (isAdmin) {
      setRole("admin");
    } else if (isTeacher) {
      setRole("teacher");
    } else if (isParent) {
      setRole("parent");
    } else if (isStudent) {
      setRole("student");
    } else {
      setRole("unknown");
    }
  };

  fetchUserRole();
}, []);

  return (
    <div className='bg-gray-50 min-h-screen'>
      <div className="flex flex-col lg:flex-row min-h-screen">
        {/* Sidebar - keep as is */}
        <div className="bg-indigo-800 lg:w-64 p-4 text-white">
          <DashboardSideBar/>
        </div>
        
        {/* Main Content Area */}
        <div className="flex-1 overflow-hidden">
          {/* Navbar */}
          <div className="bg-white shadow-sm">
            <DashboardNavBar/>
          </div>
          
          {/* Dashboard Content */}
          <div className="p-6">
            {error && (
              <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded">
                <p>{error}</p>
              </div>
            )}
            
            {/* Header with Quick Actions */}
<div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
  <div>
    <h1 className="text-2xl font-bold text-gray-800">Dashboard Overview</h1>
    <p className="text-gray-600">Welcome back! Here's what's happening today.</p>
  </div>

  <div className="flex gap-3 mt-4 md:mt-0">

    {/* Show "New Meeting" to Admin and Teacher only */}
    {(role === "admin" || role === "teacher") && (
      <Link href="/Components/meetingForm">
        <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
          <span className="w-5 h-5 text-gray-200">
            <FiCalendar />
          </span>
          <span>New Meeting</span>
        </button>
      </Link>
    )}

    {/* Show "New Announcement" to Admin and Teacher only */}
    {(role === "admin" || role === "teacher") && (
      <Link href="/Components/announcementForm">
        <button className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors">
          <span className="w-5 h-5 text-gray-400">
            <FiBell />
          </span>
          <span>New Announcement</span>
        </button>
      </Link>
    )}
    
  </div>
</div>

            
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-500 uppercase tracking-wider">Total Students</p>
                    <h3 className="text-3xl font-bold mt-2 text-gray-800">{students}</h3>
                    <p className="text-sm text-gray-500 mt-1">Registered students</p>
                  </div>
                  <div className="p-3 rounded-full bg-blue-50 text-blue-600">
                    <span  className="w-6 h-6 text-gray-400">
                      <FiUsers />
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-500 uppercase tracking-wider">Total Parents</p>
                    <h3 className="text-3xl font-bold mt-2 text-gray-800">{parents}</h3>
                    <p className="text-sm text-gray-500 mt-1">Registered parents</p>
                  </div>
                  <div className="p-3 rounded-full bg-green-50 text-green-600">
                    <span  className="w-6 h-6 text-gray-400">
                      <FiUsers />
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-500 uppercase tracking-wider">Total Teachers</p>
                    <h3 className="text-3xl font-bold mt-2 text-gray-800">{teachers}</h3>
                    <p className="text-sm text-gray-500 mt-1">Registered teachers</p>
                  </div>
                  <div className="p-3 rounded-full bg-purple-50 text-purple-600">
                    <span  className="w-6 h-6 text-gray-400">
                      <FiUsers />
                    </span>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
  {/* Teacher Announcements */}
  {(role === 'admin' || role === 'teacher') && (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="bg-gradient-to-r from-yellow-500 to-yellow-400 p-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <span className="w-6 h-6 text-gray-400">
            <FiBook />
          </span>
          Teacher Announcements
        </h3>
      </div>
      <div className="p-4 space-y-4 max-h-96 overflow-y-auto">
        {teacherAnnouncement.Announcements.length > 0 ? (
          teacherAnnouncement.Announcements.map((announcement, index) => (
            <div key={index} className="border-b border-gray-100 pb-4 last:border-b-0">
              <div className="flex justify-between items-start">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-medium bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                      #{index + 1}
                    </span>
                    <h4 className="font-semibold text-gray-800">{announcement.title}</h4>
                  </div>
                  <p className="text-sm text-gray-600 mt-2">{announcement.description}</p>
                  <p className="text-xs text-gray-400 mt-2">
                    {new Date(announcement.date_created).toLocaleString()}
                  </p>
                </div>
                <button className="text-gray-400 hover:text-gray-600">
                  <Image src="/option.png" alt="Options" width={20} height={20} />
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-500">No teacher announcements found</p>
          </div>
        )}
      </div>
    </div>
  )}

  {/* Parent Announcements */}
  {(role === 'admin' || role === 'parent') && (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="bg-gradient-to-r from-blue-500 to-blue-400 p-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <span className="w-6 h-6 text-gray-400">
            <FiHome />
          </span>
          Parent Announcements
        </h3>
      </div>
      <div className="p-4 space-y-4 max-h-96 overflow-y-auto">
        {parentAnnouncements.Announcements.length > 0 ? (
          parentAnnouncements.Announcements.map((announcement, index) => (
            <div key={index} className="border-b border-gray-100 pb-4 last:border-b-0">
              <div className="flex justify-between items-start">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-medium bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                      #{index + 1}
                    </span>
                    <h4 className="font-semibold text-gray-800">{announcement.title}</h4>
                  </div>
                  <p className="text-sm text-gray-600 mt-2">{announcement.description}</p>
                  <p className="text-xs text-gray-400 mt-2">
                    {new Date(announcement.date_created).toLocaleString()}
                  </p>
                </div>
                <button className="text-gray-400 hover:text-gray-600">
                  <Image src="/option.png" alt="Options" width={20} height={20} />
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-500">No parent announcements found</p>
          </div>
        )}
      </div>
    </div>
  )}

  {/* Student Announcements */}
  {(role === 'admin' || role === 'student') && (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="bg-gradient-to-r from-green-500 to-green-400 p-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <span className="w-6 h-6 text-gray-400">
            <FiBook />
          </span>
          Student Announcements
        </h3>
      </div>
      <div className="p-4 space-y-4 max-h-96 overflow-y-auto">
        {studentAnnouncements.Announcements.length > 0 ? (
          studentAnnouncements.Announcements.map((announcement, index) => (
            <div key={index} className="border-b border-gray-100 pb-4 last:border-b-0">
              <div className="flex justify-between items-start">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-medium bg-green-100 text-green-800 px-2 py-1 rounded-full">
                      #{index + 1}
                    </span>
                    <h4 className="font-semibold text-gray-800">{announcement.title}</h4>
                  </div>
                  <p className="text-sm text-gray-600 mt-2">{announcement.description}</p>
                  <p className="text-xs text-gray-400 mt-2">
                    {new Date(announcement.date_created).toLocaleString()}
                  </p>
                </div>
                <button className="text-gray-400 hover:text-gray-600">
                  <Image src="/option.png" alt="Options" width={20} height={20} />
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-500">No student announcements found</p>
          </div>
        )}
      </div>
    </div>
  )}

  {/* Admin Announcements */}
  {role === 'admin' && (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="bg-gradient-to-r from-gray-700 to-gray-600 p-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <span className="w-6 h-6 text-gray-400">
            <FiSettings />
          </span>
          Admin Announcements
        </h3>
      </div>
      <div className="p-4 space-y-4 max-h-96 overflow-y-auto">
        {adminAnnouncements.Announcements.length > 0 ? (
          adminAnnouncements.Announcements.map((announcement, index) => (
            <div key={index} className="border-b border-gray-100 pb-4 last:border-b-0">
              <div className="flex justify-between items-start">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-medium bg-gray-100 text-gray-800 px-2 py-1 rounded-full">
                      #{index + 1}
                    </span>
                    <h4 className="font-semibold text-gray-800">{announcement.title}</h4>
                  </div>
                  <p className="text-sm text-gray-600 mt-2">{announcement.description}</p>
                  <p className="text-xs text-gray-400 mt-2">
                    {new Date(announcement.date_created).toLocaleString()}
                  </p>
                </div>
                <button className="text-gray-400 hover:text-gray-600">
                  <Image src="/option.png" alt="Options" width={20} height={20} />
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-500">No admin announcements found</p>
          </div>
        )}
      </div>
    </div>
  )}
</div>
          </div>
        </div>
      </div>
    </div>
  )  
}

export default DashboardPage