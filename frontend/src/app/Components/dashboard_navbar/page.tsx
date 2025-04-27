'use client'
import { fetchRoles, totalStudents } from '@/config/utils'
import Image from 'next/image'
import Link from 'next/link'
import React, { useEffect, useState } from 'react'

const DashboardNavBar = () => {

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
    <div>
      {/* SEARCH BAR, LINKS, PERSONAL DETAILS */}
      <div className="p-2 flex justify-between items-center w-full bg-[#ffffe0]">
        {/* SEARCH BAR */}
        <div className="flex items-center gap-3 p-2 ring-2 ring-blue-300 rounded-md hover:ring-yellow-300 w-full md:w-auto">
          <Image src='/search.png' alt='' width={20} height={20} className='w-6 h-6'/>
          <input type="text" name="search" placeholder="Search here..." className='bg-transparent outline-none' />
        </div>
        {/* LINKS */}
        <div className="hidden md:flex items-center justify-between gap-3">
          {/* ADMINS */}
          <div className="">
            <Link href='/Components/AllAdmins'>
              <span className='font-semibold'>Admins</span>
            </Link>
          </div>
          {/* TEACHERS */}
          <div className="">
            <Link href='/Components/AllTeachers'>
              <span className='font-semibold'>Teachers</span>
            </Link>
          </div>
          {/* PARENTS */}
          <div className="">
            <Link href='/Components/AllParents'>
              <span className='font-semibold'>Parents</span>
            </Link>
          </div>
          {/* STUDENTS */}
          <div className="">
            <Link href='/Components/AllStudents'>
              <span className='font-semibold'>Students</span>
            </Link>
          </div>
          {/* EXAMS */}
          <div className="">
            <Link href='/Components/Exams'>
              <span className='font-semibold'>Exams</span>
            </Link>
          </div>
          {/* RESULTS */}
          <div className="">
            <Link href='/'>
              <span className='font-semibold'>Results</span>
            </Link>
          </div>
          {/* ROLES */}
          <div className="">
            <Link href='/Components/AllRoles'>
              <span className='font-semibold'>Roles</span>
            </Link>
          </div>
        </div>
        {/* PERSONAL DETAILS */}
        <div className="hidden md:block">
          {/* AVATAR, USER, ICON */}
            <div className="flex items-center justify-between gap-4">
              {/* MESSAGE */}
            <div className="">
              <Image src='/message.png' alt='' width={20} height={20} className='w-8 h-8'/>
            </div>
            {/* ANNOUNCEMENT */}
            <div className="">
              <Image src='/announcement.png' alt='' width={20} height={20} className='w-8 h-8'/>
            </div>
            {/* AVATAR */}
            <div className="">
              <Image src={picture} alt='' width={20} height={20} className='w-10 h-10 rounded-full'/>
              <span className='text-sm font-semibold text-gray-600'>{role}</span>
            </div>
            {/* ICON */}
            <div className="">
              <div className="bg-green-400 h-9 w-9 rounded-full relative"/>
              <span className='absolute top-7 right-5 font-bold'>{letter}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DashboardNavBar