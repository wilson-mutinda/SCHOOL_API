'use client'
import React, { useEffect, useState } from 'react'
import DashboardSideBar from '../dashboard_sidebar/page'
import DashboardNavBar from '../dashboard_navbar/page'
import { fetchAdminAnnouncements, fetchParentAnouncements, fetchStudentAnnouncements, fetchTeacherAnnouncements, totalParents, totalStudents, totalTeachers } from '@/config/utils'
import Image from 'next/image'

const DashboardPage = () => {
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
  }, [])

  return (
    <div className='bg-yellow-100 min-h-screen'>
        {/* RIGTH AND LEFT SECTION */}
        <div className="flex flex-col sm:flex-row min-h-screen">
            {/* LEFT SECTION */}
            <div className="bg-[#dcdcdc] sm:w-[25%] md:w-[20%]">
                <DashboardSideBar/>
            </div>
            {/* RIGHT SECTION */}
            <div className="bg-[#e6e6fa] sm:w-[75%] md:w-[80%]">
                {/* NAVBAR AND PAGE DETAILS */}
                <div className="">
                  {/* NAVBAR */}
                  <div className="">
                    <DashboardNavBar/>
                  </div>
                  {/* PAGE DETAILS */}
                  <div className="">
                  {error && (
                    <p className='text-red-500 text-center p-2'>{error}</p>
                  )}
                    {/* LEFT AND RIGHT SECTION */}
                    <div className="flex items-center justify-between flex-col md:flex-row">
                      {/* LEFT */}
                      <div className="w-[65%]">
                        {/* USERS INFO AND REPORTS */}
                        <div className="">
                          {/* USERS */}
                          <div className="flex items-center justify-between gap-3 p-3">
                            {/* PARENT DIV */}
                            <div className="bg-blue-400 rounded-md p-4">
                              <h3 className='font-semibold text-gray-500'>Parents Info</h3>
                              <h4 className='font-semibold'>Total = {parents}</h4>
                            </div>
                            {/* STUDENT DIV */}
                            <div className="bg-blue-400 rounded-md p-4">
                              <h3 className='font-semibold text-gray-500'>Students Info</h3>
                              <h4 className='font-semibold'>Total = {students}</h4>
                            </div>
                            {/* TEACHER DIV */}
                            <div className="bg-blue-400 rounded-md p-4">
                              <h3 className='font-semibold text-gray-500'>Teachers Info</h3>
                              <h4 className='font-semibold'>Total = {teachers}</h4>
                            </div>
                          </div>
                          {/* REPORTS */}
                          <div className="">report</div>
                        </div>
                      </div>
                      {/* RIGHT */}
                      <div className="w-[35%]">
                        <h3 className='font-bold mt-3 mb-2 text-center text-rose-800 underline'>Announcements</h3>
                        {/* TEACHER BASED */}
                        <div className="bg-yellow-300 rounded-md p-2 mb-2">
                          <h3 className="text-lg font-bold mb-2">Teacher Announcements</h3>
                          {teacherAnnouncement.Announcements.map((announcement, index) => (
                            <div key={index} className="bg-white p-2 mb-2 rounded shadow">
                              <div className="flex items-center justify-between">
                                <div>
                                  <h4 className="font-semibold">{index + 1}. {announcement.title}</h4> {/* numbering */}
                                  <p className="text-sm text-gray-600">{announcement.description}</p> {/* description */}
                                  <p className="text-xs text-gray-400">{new Date(announcement.date_created).toLocaleString()}</p> {/* formatted date */}
                                </div>
                                <Image src='/option.png' alt='' width={20} height={20} />
                              </div>
                            </div>
                          ))}
                        </div>
                        {/* PARENT BASED */}
                        <div className="bg-blue-300 rounded-md p-2 mb-2">
                          <h3 className='text-lg font-bold mb-2'>Parent Announcements</h3>
                          {parentAnnouncements.Announcements.map((announcement, index) => (
                            <div key={index} className="bg-white p-2 mb-2 rounded shadow">
                              <div className="flex items-center justify-between">
                                <div className="">
                                  <h4 className='font-semibold'>{index + 1}. {announcement.title}</h4>
                                  <p className='text-sm text-gray-600'>{announcement.description}</p>
                                  <p className='text-xs text-gray-400'>{new Date(announcement.date_created).toLocaleString()}</p>
                                </div>
                                <Image src='/option.png' alt='' width={20} height={20} />
                              </div>
                            </div>
                          ))}
                        </div>
                        {/* STUDENT BASED */}
                        <div className="bg-green-400 rounded-md p-2 mb-2">
                          <h3 className='text-lg font-bold mb-2'>Student Announcements</h3>
                          {studentAnnouncements.Announcements.map((student_announcement, index) => (
                            <div key={index} className="bg-white p-2 mb-2 rounded shadow">
                              <div className="flex items-center justify-between">
                                <div className="">
                                  <h4 className='font-semibold'>{index + 1}. {student_announcement.title}</h4>
                                  <p className='text-sm text-gray-600'>{student_announcement.description}</p>
                                  <p className='text-xs text-gray-400'>{new Date(student_announcement.date_created).toLocaleString()}</p>
                                </div>
                                <Image src='/option.png' alt='' width={20} height={20} />
                              </div>
                            </div>
                          ))}
                        </div>
                        {/* ADMIN BASED */}
                        <div className="bg-gray-600 rounded-md p-2 mb-2">
                          <h3 className='text-lg font-bold mb-2'>Admin Announcements</h3>
                          {adminAnnouncements.Announcements.map((announcements, index) => (
                            <div key={index} className="bg-white p-2 mb-2 rounded shadow">
                              <div className="flex items-center justify-between">
                                <div className="">
                                  <h4 className='font-semibold'>{index + 1}. {announcements.title}</h4>
                                  <p className='text-sm text-gray-500'>{announcements.description}</p>
                                  <p className='text-xs text-gray-600'>{new Date(announcements.date_created).toLocaleString()}</p>
                                </div>
                                <Image src='/option.png' alt='' width={20} height={20} />
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
            </div>
        </div>
    </div>
  )
}

export default DashboardPage