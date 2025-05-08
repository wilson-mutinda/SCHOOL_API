
'use client'
import { fetchRoles, totalStudents } from '@/config/utils'
import Image from 'next/image'
import Link from 'next/link'
import React, { useEffect, useState } from 'react'
import { FiSearch, FiMessageSquare, FiBell, FiChevronDown } from 'react-icons/fi'

const DashboardNavBar = () => {
  // ... (keep all existing state declarations)
  const [error, setError] = useState<string | null>(null);
  const [students, setStudents] = useState('');
  const [letter, setLetter] = useState<string | null>(null);
  const [role, setRole] = useState<string | null>(null);
  const [picture, setPicture] = useState<string>("/avatar.png");

  useEffect(() => {
    const isTeacher = localStorage.getItem("is_teacher") === "true";
    const isParent = localStorage.getItem("is_parent") === "true";

    const teacherPic = localStorage.getItem("teacher_profile_picture");
    const parentPic = localStorage.getItem("parent_profile_picture");

    if (isTeacher && teacherPic && teacherPic !== "null") {
      setPicture(teacherPic);
    } else if (isParent && parentPic && parentPic !== "null") {
      setPicture(parentPic);
    } else {
      setPicture("/avatar.png"); // default picture
    }
  }, []);

  // function to get the role
  useEffect (() => {
    const fetchUserRole = () => {
      const isAdmin = localStorage.getItem("is_admin") === "true";
      const isTeacher = localStorage.getItem("is_teacher") === "true";
      const isParent = localStorage.getItem("is_parent") === "true";
      const isStudent = localStorage.getItem("is_student") === "true";

      if (isAdmin) {
        setRole("admin")
      } else if (isTeacher) {
        setRole("Teacher")
      } else if (isParent) {
        setRole("Parent")
      } else if (isStudent) {
        setRole("Student")
      } else {
        setRole("?")
      }
    }
    fetchUserRole();
  }, [])

  // function to get the first letter from local storage
  useEffect(() => {
    const fetchFirstLetter = () => {
      const data = localStorage.getItem('first_letter');
      if (data) {
        setLetter(data);
      } else {
        setError("?")
      }
    };
    fetchFirstLetter();
  }, [])

  // get all students
  useEffect(() => {
    const fetchStudentCount = async () => {
      const data = await totalStudents();
      if (data.error) {
        setError(data.error);
        return;
      }
      setStudents(data.Total)
    };
    fetchStudentCount()
  }, []);

  return (
    <div className="bg-white border-b border-gray-200">
      <div className="px-6 py-3 flex items-center justify-between">
        {/* Search Bar */}
        <div className="flex-1 max-w-md">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <span className="h-5 w-5 text-gray-400">
              <FiSearch />
            </span>

            </div>
            <input
              type="text"
              placeholder="Search..."
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
        </div>
        
        {/* Navigation Links */}
        <div className="hidden lg:flex items-center space-x-8 ml-10">
          {(role === 'admin' || role === 'Teacher') && (
            <Link href='/Components/AllAdmins' className="text-sm font-medium text-gray-700 hover:text-indigo-600 transition-colors">
              Admins
            </Link>
          )}

          {(role === 'admin' || role === 'Teacher') && (
            <Link href='/Components/AllTeachers' className="text-sm font-medium text-gray-700 hover:text-indigo-600 transition-colors">
              Teachers
            </Link>
          )}

          {(role === 'admin' || role === 'Teacher' || role === 'Parent') && (
            <Link href='/Components/AllParents' className="text-sm font-medium text-gray-700 hover:text-indigo-600 transition-colors">
              Parents
            </Link>
          )}

          {(role === 'admin' || role === 'Teacher' || role === 'Student' || role === 'Parent') && (
            <Link href='/Components/AllStudents' className="text-sm font-medium text-gray-700 hover:text-indigo-600 transition-colors">
              Students
            </Link>
          )}

          {(role === 'admin' || role === 'Teacher' || role === 'Student') && (
            <Link href='/Components/AllCats' className="text-sm font-medium text-gray-700 hover:text-indigo-600 transition-colors">
              Cats
            </Link>
          )}

          {(role === 'admin' || role === 'Teacher' || role === 'Student') && (
            <Link href='/Components/AllExams' className="text-sm font-medium text-gray-700 hover:text-indigo-600 transition-colors">
              Exams
            </Link>
          )}

          {(role === 'admin' || role === 'Teacher' || role === 'Student') && (
            <Link href='/Components/AllSubjects' className="text-sm font-medium text-gray-700 hover:text-indigo-600 transition-colors">
              Subjects
            </Link>
          )}
        </div>
        
        {/* User Profile Section */}
        <div className="ml-4 flex items-center md:ml-6">
          <button className="p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            <span className="sr-only">View notifications</span>
            <span className='h-5 w-5 text-gray-400'>
              <FiBell />
            </span>
          </button>
          
          <button className="p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ml-4">
            <span className="sr-only">View messages</span>
            <span className='h5 w-5 text-gray-400'>
              <FiMessageSquare/>
            </span>
          </button>
          
          {/* Profile dropdown */}
          <div className="ml-4 relative">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Image 
                  src={picture} 
                  alt="User profile" 
                  width={32} 
                  height={32} 
                  className="rounded-full"
                />
              </div>
              <div className="ml-3">
                <div className="text-sm font-medium text-gray-700">{role}</div>
              </div>
              <button className="ml-2 text-gray-400 hover:text-gray-500 focus:outline-none">
                <span  className="h-5 w-5 text-gray-400">
                  <FiChevronDown />
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DashboardNavBar