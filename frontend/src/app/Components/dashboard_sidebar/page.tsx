'use client'
import Image from 'next/image'
import Link from 'next/link'
import React, { useEffect, useState } from 'react'

const DashboardSideBar = () => {
  const [role, setRole] = useState("")

  // Get role from localStorage
  useEffect(() => {
    const isAdmin = localStorage.getItem("is_admin") === "true";
    const isTeacher = localStorage.getItem("is_teacher") === "true";
    const isParent = localStorage.getItem("is_parent") === "true";
    const isStudent = localStorage.getItem("is_student") === "true";

    if (isAdmin) {
      setRole("admin")
    } else if (isTeacher) {
      setRole("teacher")
    } else if (isParent) {
      setRole("parent")
    } else if (isStudent) {
      setRole("student")
    }
  }, [])

  // Main component definition
  const mainComponents = [
    {
      title: 'MAIN MENU',
      items: [
        { text: 'Dashboard', logo: '/dashboard.png', link: 'Dashboard', roles: ['admin', 'teacher', 'parent', 'student'] },
        { text: 'Teacher Portal', logo: '/teacher.png', link: '/Components/AllTeachers', roles: ['admin', 'teacher'] },
        { text: 'Parent Portal', logo: '/parent.png', link: '/Components/AllParents', roles: ['admin', 'teacher', 'parent'] },
        { text: 'Student Portal', logo: '/student.png', link: '/Components/AllStudents', roles: ['admin', 'teacher', 'parent', 'student'] },
        { text: 'Admissions', logo: '/admission.png', link: '/Components/AllStudents', roles: ['admin', 'teacher', 'parent'] },
        { text: 'Reports', logo: '/report.png', link: '/Components/AllReports', roles: ['admin', 'teacher', 'parent', 'student'] },
        { text: 'Conferencing', logo: '/meet.png', link: '/Components/meetingForm', roles: ['admin', 'teacher'] },
        { text: 'About', logo: '/about.png', link: '/Components/About', roles: ['admin', 'teacher', 'parent', 'student'] },
      ]
    },
    {
      title: 'ACCOUNT',
      items: [
        { text: 'Logout', logo: '/logout.png', link: '/', roles: ['admin', 'teacher', 'parent', 'student'] }
      ]
    }
  ];

  return (
    <div>
      {/* Title Logo and main components */}
      <div>
        {/* Title Logo */}
        <div className="hover:bg-green-400 hover:text-white">
          <Link href='/' className=''>
            <div className="flex items-center gap-3 p-3">
              <Image src='/logo.png' alt='' width={20} height={20} className='w-10 h-10'/>
              <span className='font-semibold'>Bidii School</span>
            </div>
          </Link>
        </div>

        {/* Sidebar Navigation */}
        <div className="p-2">
          {mainComponents.map((section, sectionIndex) => (
            <div key={sectionIndex}>
              <h3 className='font-semibold text-[#808080] p-2 mt-2'>{section.title}</h3>
              {section.items
                .filter(item => item.roles.includes(role))
                .map((item, itemIndex) => (
                  <Link href={item.link} key={itemIndex}>
                    <div className="flex items-center gap-3 p-3 font-semibold hover:bg-[#708090] rounded-md hover:text-white">
                      <Image src={item.logo} alt='' width={20} height={20} className='w-8 h-8 p-1 bg-white rounded-md items-center'/>
                      <span className='hidden md:block'>{item.text}</span>
                    </div>
                  </Link>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default DashboardSideBar
