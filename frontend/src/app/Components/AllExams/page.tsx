'use client'
import React, { useState } from 'react'
import DashboardSideBar from '../dashboard_sidebar/page'
import Link from 'next/link';
import Image from 'next/image';

interface Exam {
  id: string,
  exam_name: string,
  exam_teacher: string,
}

const AllExamsPage = () => {
  
  const [exams, setExams] = useState<Exam[]>([]);
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className='bg-yellow-100 min-h-screen'>
      {/* LEFT AND RIGHT SECTION */}
      <div className="flex flex-col sm:flex-row min-h-screen">
        {/* LEFT SECTION */}
        <div className="bg-[#dcdcdc] sm:w-[25%] md:w-[20%]">
          <DashboardSideBar/>
        </div>
        {/* RIGHT SECTION */}
        <div className="bg-[#e6e6fa] sm:w-[75%] md:w-[80%]">
          {/* SEARCH BAR AND TEACHER TABLE */}
          <div className="p-4">
            {/* SEARCH BAR */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center ring-2 ring-yellow-300 hover:ring-blue-300 rounded-md p-2 gap-3">
                <Image src='/search.png' alt='Search' width={20} height={20} className='w-6 h-6'/>
                <input 
                  type="text" 
                  placeholder="Search Exam..." 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className='outline-none bg-transparent w-full'
                />
              </div>
              <Link href='/Components/parentForm'>
                <button className='p-2'>
                  <Image src='/create.png' alt='Create' width={20} height={20} className='rounded-full bg-yellow-400 h-8 w-8'/>
                </button>
              </Link>
            </div>
            
            {/* TEACHER TABLE */}
            <div className="overflow-x-auto">
              <table className='w-full border-collapse'>
                <thead>
                  <tr className='bg-gray-200'>
                    <th className='border border-gray-500 p-2'>ID</th>
                    <th className='border border-gray-500 p-2'>First Name</th>
                    <th className='border border-gray-500 p-2'>Last Name</th>
                    <th className='border border-gray-500 p-2'>Username</th>
                    <th className='border border-gray-500 p-2'>Email</th>
                    <th className='border border-gray-500 p-2'>Phone</th>
                    <th className='border border-gray-500 p-2'>Profile</th>
                    <th className='border border-gray-500 p-2'>Address</th>
                    <th className='border border-gray-500 p-2'>Teacher Code</th>
                    <th className='border border-gray-500 p-2'>Actions</th>
                  </tr>
                </thead>
                <tbody>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AllExamsPage