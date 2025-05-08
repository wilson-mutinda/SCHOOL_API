'use client'
import React, { useEffect, useState } from 'react'
import DashboardSideBar from '../dashboard_sidebar/page'
import Image from 'next/image'
import Link from 'next/link'
import { deleteStudent, fetchStudents } from '@/config/utils'
import { FiArrowLeft } from 'react-icons/fi'

interface User {
  first_name: string
  last_name: string
  username: string
  email: string
}

interface Student {
  id: number
  user: User
  parent_email: string
  parent_code: string
}

const AllStudentsPage = () => {
  const [students, setStudents] = useState<Student[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  const fetchData = async () => {
    setLoading(true)
    setError(null)

    try {
      const data = await fetchStudents()
      setStudents(data)
    } catch (err) {
      console.error("Error fetching students:", err)
      setError("Failed to fetch students.")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const handleDelete = async (id: number) => {
    const confirmDelete = confirm("Are you sure you want to delete this student?")
    if (!confirmDelete) return

    try {
      await deleteStudent(String(id))
      fetchData()
    } catch (error) {
      console.error("Delete failed", error)
      setError("Failed to delete student.")
    }
  }

  const filteredStudents = students.filter((student) => {
    const fullName = `${student.user.first_name} ${student.user.last_name}`.toLowerCase()
    const username = student.user.username.toLowerCase()
    const email = student.user.email.toLowerCase()
    const query = searchQuery.toLowerCase()

    return fullName.includes(query) || username.includes(query) || email.includes(query)
  })

  if (loading) {
    return (
      <div className="bg-yellow-100 min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full border-blue-400 w-12 h-12 border-b-2"></div>
      </div>
    )
  }

  return (
    <div className='bg-yellow-100 min-h-screen'>
      <div className="flex flex-col sm:flex-row min-h-screen">
        <div className="bg-[#dcdcdc] sm:w-[25%] md:w-[20%]">
          <DashboardSideBar />
        </div>

        <div className="bg-[#e6e6fa] sm:w-[75%] md:w-[80%] p-4">
          <div className="flex items-center justify-between mb-4">
             {/* BACK BUTTON */}
             <Link 
              href="/Components/Dashboard" 
              className="inline-flex items-center space-x-2 mb-2 text-blue-500 hover:text-blue-700 bg-green-500 hover:bg-yellow-300 rounded-lg p-3 transition-all duration-300 shadow-lg transform hover:scale-105"
            >
              <FiArrowLeft className="text-xl" />
              <span className='text-white font-semibold'>Back</span>
            </Link>
            <div className="flex items-center ring-2 ring-yellow-300 hover:ring-blue-300 rounded-md p-2 gap-3">
              <Image src='/search.png' alt='Search' width={20} height={20} className='w-6 h-6' />
              <input
                type="text"
                placeholder="Search Student..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className='outline-none bg-transparent w-full'
              />
            </div>
            <Link href='/Components/studentForm'>
              <button className='p-2'>
                <Image src='/create.png' alt='Create' width={20} height={20} className='rounded-full bg-yellow-400 h-8 w-8' />
              </button>
            </Link>
          </div>

          <div className="overflow-x-auto">
            <table className='w-full border-collapse'>
              <thead>
                <tr className='bg-gray-200'>
                  <th className='border border-gray-500 p-2'>#</th>
                  <th className='border border-gray-500 p-2'>First Name</th>
                  <th className='border border-gray-500 p-2'>Last Name</th>
                  <th className='border border-gray-500 p-2'>Username</th>
                  <th className='border border-gray-500 p-2'>Email</th>
                  <th className='border border-gray-500 p-2'>Parent Email</th>
                  <th className='border border-gray-500 p-2'>Parent Code</th>
                  <th className='border border-gray-500 p-2'>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredStudents.map((student, index) => (
                  <tr key={student.id} className='hover:bg-gray-50'>
                    <td className='border border-gray-500 p-2 text-center'>{index + 1}</td>
                    <td className='border border-gray-500 p-2'>{student.user.first_name}</td>
                    <td className='border border-gray-500 p-2'>{student.user.last_name}</td>
                    <td className='border border-gray-500 p-2'>{student.user.username}</td>
                    <td className='border border-gray-500 p-2'>{student.user.email}</td>
                    <td className='border border-gray-500 p-2'>{student.parent_email}</td>
                    <td className='border border-gray-500 p-2'>{student.parent_code}</td>
                    <td className='border border-gray-500 p-2'>
                      <div className="flex items-center justify-center gap-3">
                        <Link href={`/Components/studentForm?id=${student.id}`}>
                          <Image src='/update.png' alt='Update' width={20} height={20} className='rounded-md bg-blue-400 w-8 h-8 p-2' />
                        </Link>
                        <button onClick={() => handleDelete(student.id)}>
                          <Image src='/delete.png' alt='Delete' width={20} height={20} className='rounded-md bg-red-400 w-8 h-8 p-2' />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {error && <p className='text-red-500 mt-4'>{error}</p>}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AllStudentsPage
